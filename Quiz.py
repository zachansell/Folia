from typing import List, Tuple, Optional
import time

from QuizItem import QuizItem
from LeaveSet import LeaveSet

class Quiz:
    def __init__(self, question_pairs: List[Tuple[str, float]]):
        self.questions = [QuizItem(leave, value) for leave, value in question_pairs]
        self.current_index = 0
        self.start_time = time.time()
        self.finished = False
        #todo: add settings
    
    @property
    def current_question(self) -> Optional[QuizItem]:
        if self.current_index < len(self.questions):
            return self.questions[self.current_index]
        return None

    def make_guess(self, guess: float) -> None:
        if self.finished:
            return
            
        current = self.current_question
        if current:
            current.set_guess(guess)

            elapsed_seconds = int(time.time() - self.start_time)
            current.set_time_elapsed(elapsed_seconds)

            self.current_index += 1
            self.start_time = time.time()

            if self.current_index >= len(self.questions):
                self.finished = True


    def results(self) -> List[dict]:
        return [q.to_dict() for q in self.questions]

    def genQuizItems(self, ls: LeaveSet, settings: Dict[str, float]) -> List[QuizItem]:
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
