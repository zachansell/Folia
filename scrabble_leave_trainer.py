#!/usr/bin/env python3

import tkinter as tk
from tkinter import messagebox
import random
import json
import os
from LeaveSet import LeaveSet
from Quiz import Quiz
from QuizItem import QuizItem

class SimpleLeaveTrainer:
    def __init__(self, root):
        self.root = root
        self.root.title("Folia: Scrabble Leave Trainer Demo")
        self.root.geometry("600x500")
        
        self.leaves = LeaveSet()
        self.quiz = None
        self.score = 0
        self.total = 0
        
        self.session_file = "session.json"
        self.load_session()
        
        self.setup_ui()
    
    def setup_ui(self):
        tk.Label(self.root, text="Scrabble Leave Value Training", 
                font=("Arial", 16, "bold")).pack(pady=10)
        
        tk.Label(self.root, text="Demo", 
                font=("Arial", 10)).pack()
        
        main_frame = tk.Frame(self.root)
        main_frame.pack(pady=20)
        
        quiz_frame = tk.LabelFrame(main_frame, text="Quizzing Mode", padx=20, pady=20)
        quiz_frame.pack(side=tk.LEFT, padx=20)
        
        self.quiz_label = tk.Label(quiz_frame, text="Press Start", 
                                   font=("Arial", 12))
        self.quiz_label.pack(pady=10)
        
        self.leave_label = tk.Label(quiz_frame, text="", 
                                    font=("Courier", 24, "bold"))
        self.leave_label.pack(pady=10)
        
        self.guess_entry = tk.Entry(quiz_frame, font=("Arial", 12))
        self.guess_entry.pack(pady=5)
        
        tk.Button(quiz_frame, text="Submit", 
                 command=self.check_guess).pack(pady=5)
        
        tk.Button(quiz_frame, text="Start Quiz", 
                 command=self.start_quiz).pack(pady=5)
        
        self.score_label = tk.Label(quiz_frame, text="Score: 0/0")
        self.score_label.pack(pady=5)
        
        lookup_frame = tk.LabelFrame(main_frame, text="Lookup Database", padx=20, pady=20)
        lookup_frame.pack(side=tk.LEFT, padx=20)
        
        tk.Label(lookup_frame, text="Enter leave:").pack(pady=5)
        
        self.lookup_entry = tk.Entry(lookup_frame, font=("Arial", 12))
        self.lookup_entry.pack(pady=5)
        
        tk.Button(lookup_frame, text="Lookup", 
                 command=self.lookup_leave).pack(pady=5)
        
        self.result_label = tk.Label(lookup_frame, text="", 
                                     font=("Arial", 12))
        self.result_label.pack(pady=10)
        
        stats_text = f"Total Sessions: {self.stats.get('sessions', 0)} | "
        stats_text += f"Total Quizzes: {self.stats.get('quizzes', 0)} | "
        stats_text += f"Lifetime Score: {self.stats.get('lifetime_score', 0)}/{self.stats.get('lifetime_total', 0)}"
        
        tk.Label(self.root, text=stats_text, font=("Arial", 9)).pack(side=tk.BOTTOM, pady=10)
    
    def start_quiz(self):
        all_leaves = list(self.leaves.items())
        selected_leaves = random.sample(all_leaves, min(10, len(all_leaves)))
        
        self.quiz = Quiz(selected_leaves)
        self.score = 0
        self.total = 0
        
        self.next_question()
        self.quiz_label.config(text="Guess the value:")
        self.stats['quizzes'] = self.stats.get('quizzes', 0) + 1
        
    def next_question(self):
        if self.quiz is None:
            return
            
        current = self.quiz.current_question
        if current:
            self.leave_label.config(text=current.leave)
            self.guess_entry.delete(0, tk.END)
        else:
            self.quiz_label.config(text="Quiz finished!")
            self.show_results()
        
    def check_guess(self):
        if self.quiz is None:
            messagebox.showinfo("Info", "Start a quiz first!")
            return
            
        current = self.quiz.current_question
        if current is None:
            messagebox.showinfo("Info", "Quiz is finished!")
            return
            
        try:
            guess = float(self.guess_entry.get())
            self.quiz.make_guess(guess)
            
            self.total += 1
            if current.rating in ("excellent", "great", "good"):
                self.score += 1
                result = f"Nice! ({current.rating.upper()})"
            elif current.rating == "correct":
                self.score += 1
                result = "Perfect! (CORRECT)"
            else:
                result = "Keep practicing (POOR)"
                
            msg = f"{result}\nYour guess: {guess:.1f}\nActual: {current.value:.1f}\nDiff: {current.delta:.1f}"
            self.quiz_label.config(text=msg)
            self.score_label.config(text=f"Score: {self.score}/{self.total}")
            
            self.stats['lifetime_total'] = self.stats.get('lifetime_total', 0) + 1
            if current.rating in ("excellent", "great", "good", "correct"):
                self.stats['lifetime_score'] = self.stats.get('lifetime_score', 0) + 1
            self.save_session()
            
            self.root.after(2000, self.advance_quiz)
            
        except ValueError:
            messagebox.showerror("Error", "Enter a number.")
    
    def advance_quiz(self):
        if self.quiz is None:
            return
        
        if self.quiz.finished:
            self.quiz_label.config(text="Quiz finished!")
            self.show_results()
        else:
            self.next_question()
    
    def lookup_leave(self):
        leave = self.lookup_entry.get().upper()
        leave = self.leaves.normalize_leave(leave)
        
        if leave in self.leaves:
            value = self.leaves.get(leave)
            self.result_label.config(text=f"{leave} = {value:.1f}")
        else:
            self.result_label.config(text="Not found")
    
    def show_results(self):
        """Display final quiz results"""
        if self.quiz is None:
            return
        
        results_text = f"Quiz Complete!\n\nFinal Score: {self.score}/{self.total}"
        percentage = (self.score / self.total * 100) if self.total > 0 else 0
        results_text += f"\nAccuracy: {percentage:.1f}%"
        
        messagebox.showinfo("Quiz Results", results_text)
    
    def load_session(self):
        if os.path.exists(self.session_file):
            try:
                with open(self.session_file, 'r') as f:
                    self.stats = json.load(f)
            except:
                self.stats = {'sessions': 0, 'quizzes': 0, 
                             'lifetime_score': 0, 'lifetime_total': 0}
        else:
            self.stats = {'sessions': 0, 'quizzes': 0, 
                         'lifetime_score': 0, 'lifetime_total': 0}
        self.stats['sessions'] = self.stats.get('sessions', 0) + 1
        
    def save_session(self):
        try:
            with open(self.session_file, 'w') as f:
                json.dump(self.stats, f)
        except:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleLeaveTrainer(root)
    root.mainloop()