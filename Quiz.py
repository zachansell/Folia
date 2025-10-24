from typing import List, Tuple, Optional
import time

from QuizItem import QuizItem

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
