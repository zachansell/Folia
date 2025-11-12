from typing import Dict, Any, Optional
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
        # time_limit: Time limit for quiz in seconds
        quizItems = []
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