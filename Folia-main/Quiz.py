from typing import List, Tuple, Optional
import time

from QuizItem import QuizItem

class Quiz:
    def __init__(self, question_pairs: List[Tuple[str, float]]):
        self.questions = [QuizItem(leave, value) for leave, value in question_pairs]
        self.current_index = 0
        self.start_time = time.time()
        self.finished = False
        self.total_time = 0
    
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
            self.total_time += elapsed_seconds

            self.current_index += 1
            self.start_time = time.time()

            if self.current_index >= len(self.questions):
                self.finished = True


    def results(self) -> List[dict]:
        return [q.to_dict() for q in self.questions]
    
    def statistics(self) -> dict:
        """Calculate quiz performance statistics"""
        if not self.questions:
            return {}
        
        # Include all questions that have been answered (guess has been set)
        answered = [q for q in self.questions if q.guess != 0 or q.delta != 0]
        deltas = [q.delta for q in answered]
        
        if not deltas:
            return {}
        
        correct = sum(1 for q in answered if q.rating == 'correct')
        excellent = sum(1 for q in answered if q.rating in ['correct', 'excellent'])
        accurate = sum(1 for q in answered if q.delta <= 3)
        
        return {
            'avg_delta': sum(deltas) / len(deltas),
            'min_delta': min(deltas),
            'max_delta': max(deltas),
            'total_time': self.total_time,
            'correct_count': correct,
            'excellent_count': excellent,
            'accuracy': accurate / len(deltas) if deltas else 0
        }
