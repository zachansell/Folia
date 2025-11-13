from typing import Dict, Any, Optional, List
import random
from QuizItem import QuizItem
import csv
import os

class LeaveSet:

    def __init__(self, csv_path: Optional[str] = None):
        self.values: Dict[str, Any] = {}
        self.csv_path = csv_path or os.path.join(os.path.dirname(__file__), "nwl-leave-values.csv")
        if os.path.exists(self.csv_path):
            self.load(self.csv_path)

    def load(self, path: str) -> None:
        values: Dict[str, Any] = {}
        dec_places = 1
        
        with open(path, newline='', encoding='utf-8') as fh:
            reader = csv.reader(fh)
            for i, row in enumerate(reader):
                if not row:
                    continue
                if len(row) < 2:
                    continue
                key = row[0].strip()
                raw_val = row[1].strip()
                if i == 0 and key.lower() in ("leave", "leaves", "name") and raw_val.lower() in ("value", "values", "val"):
                    continue
                val: Any = raw_val
                if raw_val != "":
                    try:
                        val = int(raw_val)
                    except ValueError:
                        try:
                            val = float(raw_val)
                        except ValueError:
                            val = raw_val
                else:
                    val = None
                values[key] = round(val,dec_places)
        self.values = values
        self.csv_path = path

    def get(self, leave: str, default: Any = None) -> Any:
        return self.values.get(leave, default)

    def __getitem__(self, leave: str) -> Any:
        return self.values[leave]

    def __contains__(self, leave: str) -> bool:
        return leave in self.values

    def items(self):
        return self.values.items()

    def keys(self):
        return self.values.keys()

    def values_list(self):
        return list(self.values.values())

    def normalize_leave(self, leave: str) -> str:
        leave = leave.upper()
        blanks = '?' * leave.count('?')
        other_chars = ''.join(sorted(c for c in leave if c != '?'))
        return blanks + other_chars

    def genQuizItems(self, settings: Dict[str, float]) -> List[QuizItem]:
        # Settings dictionary meanings (may not be all used):
        # num_questions: Number of questions in the quiz
        # min_len: Minimum length of the leave to be considered
        # max_len: Maximum length of the leave to be considered
        # max_vowels: Maximum number of vowels in the leave
        # min_vowels: Minimum number of vowels in the leave
        # max_consonants: Maximum number of consonants in the leave
        # min_consonants: Minimum number of consonants in the leave
        # must_contain: letters that must be in the leave
        # must_not_contain: letters that must not be in the leave
        # NOTE: for the containment settings, the input will be interpreted as a sequence of two-digit numbers 0-26 representing ? and A-Z
        # min_value: Minimum value of the leave
        # max_value: Maximum value of the leave
        # time_limit: Time limit for quiz in seconds - not necessary here
        # Read settings with sensible defaults
        num_questions = int(settings.get('num_questions', 0))
        min_len = settings.get('min_len', None)
        max_len = settings.get('max_len', None)
        min_vowels = settings.get('min_vowels', None)
        max_vowels = settings.get('max_vowels', None)
        min_consonants = settings.get('min_consonants', None)
        max_consonants = settings.get('max_consonants', None)
        must_contain = settings.get('must_contain', None)
        must_not_contain = settings.get('must_not_contain', None)
        min_value = settings.get('min_value', None)
        max_value = settings.get('max_value', None)

        def decode_letters(seq) -> Optional[set]:
            # string of digits representing two-digit codes (e.g. '010203') -> [00->'?', 01->'A', ...]
            if seq is None:
                return None
            if isinstance(seq, set):
                return {s.upper() for s in seq}
            if isinstance(seq, (list, tuple)):
                out = set()
                for item in seq:
                    if isinstance(item, int):
                        out.add('?' if item == 0 else chr(ord('A') + item - 1))
                    else:
                        s = str(item).strip()
                        if s.isdigit() and len(s) == 2:
                            n = int(s)
                            out.add('?' if n == 0 else chr(ord('A') + n - 1))
                        else:
                            out.update(ch.upper() for ch in s if ch.strip())
                return out
            if isinstance(seq, str):
                s = seq.strip()
                if s.isdigit() and len(s) % 2 == 0:
                    out = set()
                    for i in range(0, len(s), 2):
                        n = int(s[i:i+2])
                        out.add('?' if n == 0 else chr(ord('A') + n - 1))
                    return out
                return {ch.upper() for ch in s if ch.strip()}
            try:
                return {ch.upper() for ch in str(seq)}
            except Exception:
                return None

        must_contain_set = decode_letters(must_contain)
        must_not_contain_set = decode_letters(must_not_contain)

        VOWELS = set('AEIOUY')

        candidates = []

        for leave, val in self.items():
            if val is None:
                continue

            lname = str(leave).upper()
            letters_only = [c for c in lname if c != '?']
            length = len(letters_only)

            if min_len is not None and length < int(min_len):
                continue
            if max_len is not None and length > int(max_len):
                continue

            vowel_count = sum(1 for c in letters_only if c in VOWELS)
            cons_count = sum(1 for c in letters_only if c.isalpha() and c not in VOWELS)

            if min_vowels is not None and vowel_count < int(min_vowels):
                continue
            if max_vowels is not None and vowel_count > int(max_vowels):
                continue

            if min_consonants is not None and cons_count < int(min_consonants):
                continue
            if max_consonants is not None and cons_count > int(max_consonants):
                continue

            if must_contain_set:
                if not must_contain_set.issubset(set(lname)):
                    continue

            if must_not_contain_set:
                if must_not_contain_set & set(lname):
                    continue

            if min_value is not None:
                try:
                    if float(val) < float(min_value):
                        continue
                except Exception:
                    continue

            if max_value is not None:
                try:
                    if float(val) > float(max_value):
                        continue
                except Exception:
                    continue

            candidates.append((leave, val))

        if not candidates:
            return []

        if num_questions <= 0:
            num_questions = len(candidates)

        if num_questions >= len(candidates):
            selected = list(candidates)
        else:
            selected = random.sample(candidates, num_questions)

        quizItems = [QuizItem(leave, value) for leave, value in selected]
        return quizItems


def main() -> None:
    ls = LeaveSet()
    while True:
        try:
            leave = ls.normalize_leave(input("Enter leave (or '0' to exit): ").strip())
        except EOFError:
            print()
            break
        if leave == '0':
            break
        if not leave:
            continue
        if leave in ls:
            print(f"{leave} = {ls.get(leave)}")
        else:
            print(f"leave '{leave}' not found")


if __name__ == "__main__":
    main()