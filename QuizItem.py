# QuizItem.py



class QuizItem:

    def __init__(self, leave: str, value: float) -> None:
        self.leave: str = leave
        self.value: float = float(value)
        self.guess: float = 0.0
        self.delta: float = 0.0
        self.rating: str = ""
        self.time_elapsed: int = 0  # in seconds

    def set_guess(self, guess: float) -> None:
        self.guess = float(guess)
        self.delta = abs(self.guess - self.value)
        self.set_rating()

    def set_rating(self) -> None:
        excellent_threshold = 1.0
        great_threshold = 3.0
        good_threshold = 5.0

        if self.delta == 0:
            self.rating = "correct"
        elif self.delta <= excellent_threshold:
            self.rating = "excellent"
        elif self.delta <= great_threshold:
            self.rating = "great"
        elif self.delta <= good_threshold:
            self.rating = "good"
        else:
            self.rating = "poor"

    def set_time_elapsed(self, seconds: int) -> None:
        self.time_elapsed = int(seconds)


    def to_dict(self) -> dict:
        return {
            "leave": self.leave,
            "value": self.value,
            "guess": self.guess,
            "delta": self.delta,
            "rating": self.rating,
            "time_elapsed": self.time_elapsed,
        }