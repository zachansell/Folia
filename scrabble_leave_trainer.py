#!/usr/bin/env python3

import tkinter as tk
from tkinter import messagebox
import random
import json
import os
from LeaveSet import LeaveSet
from Quiz import Quiz

class SimpleLeaveTrainer:
    def __init__(self, root):
        self.root = root
        self.root.title("Folia: Scrabble Leave Trainer Demo")
        self.root.geometry("600x500")
        
        self.leaves = LeaveSet()
        self.quiz = None
        
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
        
        self.rating_label = tk.Label(quiz_frame, text="", font=("Arial", 10, "italic"))
        self.rating_label.pack(pady=5)
        
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
    
    def start_quiz(self, num_questions=10):
        questions = self._generate_questions(num_questions)
        self.quiz = Quiz(questions)
        self.stats['quizzes'] = self.stats.get('quizzes', 0) + 1
        self.save_session()
        self._show_question()
    
    def _generate_questions(self, count):
        all_leaves = list(self.leaves.items())
        return random.sample(all_leaves, min(count, len(all_leaves)))
    
    def _show_question(self):
        if not self.quiz or self.quiz.finished:
            return
        
        current = self.quiz.current_question
        if current:
            self.leave_label.config(text=current.leave)
            self.quiz_label.config(text="Guess the value:")
            self.rating_label.config(text="")
            self.guess_entry.delete(0, tk.END)
            self.guess_entry.focus_set()
            self._update_score_display()
        
    def check_guess(self):
        if not self.quiz:
            messagebox.showinfo("Info", "Start a quiz first!")
            return
        
        if self.quiz.finished:
            self._show_results()
            return
            
        try:
            guess = float(self.guess_entry.get())
            self.quiz.make_guess(guess)
            
            current = self.quiz.questions[self.quiz.current_index - 1]
            
            msg = f"Your guess: {current.guess:.1f}\nActual: {current.value:.1f}\nDiff: {current.delta:.1f}"
            self.quiz_label.config(text=msg)
            self.rating_label.config(text=f"Rating: {current.rating.upper()}")
            
            self._update_lifetime_stats(current)
            self._update_score_display()
            
            if not self.quiz.finished:
                self.root.after(2000, self._show_question)
            else:
                self.root.after(2000, self._show_results)
            
        except ValueError:
            messagebox.showerror("Error", "Enter a number.")
    
    def _update_score_display(self):
        completed = self.quiz.current_index
        total = len(self.quiz.questions)
        good_count = sum(1 for q in self.quiz.questions[:completed] if q.delta < 3)
        self.score_label.config(text=f"Score: {good_count}/{completed} of {total}")
    
    def _update_lifetime_stats(self, item):
        self.stats['lifetime_total'] = self.stats.get('lifetime_total', 0) + 1
        if item.delta < 3:
            self.stats['lifetime_score'] = self.stats.get('lifetime_score', 0) + 1
        self.save_session()
    
    def _show_results(self):
        results = self.quiz.results()
        avg_delta = sum(r['delta'] for r in results) / len(results)
        good_count = sum(1 for r in results if r['delta'] < 3)
        
        msg = f"Quiz Complete!\n\n"
        msg += f"Score: {good_count}/{len(results)}\n"
        msg += f"Avg Error: {avg_delta:.2f}\n\n"
        msg += "Start a new quiz?"
        
        if messagebox.askyesno("Results", msg):
            self.start_quiz()
    
    def lookup_leave(self):
        leave = self.lookup_entry.get().upper()
        leave = self.leaves.normalize_leave(leave)
        
        if leave in self.leaves:
            value = self.leaves.get(leave)
            self.result_label.config(text=f"{leave} = {value:.1f}")
        else:
            self.result_label.config(text="Not found")
    
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