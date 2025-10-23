#!/usr/bin/env python3

import tkinter as tk
from tkinter import messagebox
import random
import json
import os
from LeaveSet import LeaveSet

class SimpleLeaveTrainer:
    def __init__(self, root):
        self.root = root
        self.root.title("Folia: Scrabble Leave Trainer Demo")
        self.root.geometry("600x500")
        
        self.leaves = LeaveSet()
        self.quiz_active = False
        self.current_leave = None
        self.current_value = None
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
        self.quiz_active = True
        self.score = 0
        self.total = 0
        self.next_question()
        self.quiz_label.config(text="Guess the value:")
        self.stats['quizzes'] = self.stats.get('quizzes', 0) + 1
        
    def next_question(self):
        all_leaves = list(self.leaves.items())
        leave, value = random.choice(all_leaves)
        self.current_leave = leave
        self.current_value = value
        self.leave_label.config(text=leave)
        self.guess_entry.delete(0, tk.END)
        
    def check_guess(self):
        if not self.quiz_active:
            messagebox.showinfo("Info", "Start a quiz first!")
            return
            
        try:
            guess = float(self.guess_entry.get())
            diff = abs(guess - self.current_value)
            
            self.total += 1
            if diff < 3:
                self.score += 1
                result = "Good!"
            else:
                result = "Keep practicing"
                
            msg = f"{result}\nYour guess: {guess:.1f}\nActual: {self.current_value:.1f}"
            self.quiz_label.config(text=msg)
            self.score_label.config(text=f"Score: {self.score}/{self.total}")
            
            self.stats['lifetime_total'] = self.stats.get('lifetime_total', 0) + 1
            if diff < 3:
                self.stats['lifetime_score'] = self.stats.get('lifetime_score', 0) + 1
            self.save_session()
            
            self.root.after(2000, self.next_question)
            
        except ValueError:
            messagebox.showerror("Error", "Enter a number.")
    
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