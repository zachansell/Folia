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
                 command=self.show_quiz_settings).pack(pady=5)
        
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
    
    def show_quiz_settings(self):
        """Open a configuration dialog for quiz settings"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Quiz Configuration")
        settings_window.geometry("480x650")
        
        canvas_frame = tk.Frame(settings_window)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(canvas_frame, highlightthickness=0)
        scrollbar = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        main_frame = scrollable_frame
        
        tk.Label(main_frame, text="Configure Your Quiz", 
                font=("Arial", 11, "bold")).pack(pady=8, anchor=tk.W, padx=10)
        
        tk.Label(main_frame, text="Number of Questions:", font=("Arial", 9)).pack(anchor=tk.W, padx=10)
        num_questions_var = tk.IntVar(value=10)
        num_q_inner = tk.Frame(main_frame)
        num_q_inner.pack(fill=tk.X, pady=3, padx=10)
        tk.Scale(num_q_inner, from_=1, to=50, orient=tk.HORIZONTAL, 
                variable=num_questions_var, length=220).pack(side=tk.LEFT)
        tk.Label(num_q_inner, textvariable=num_questions_var, width=3, font=("Arial", 9)).pack(side=tk.LEFT, padx=8)
        
        tk.Label(main_frame, text="Leave Length (letters):", font=("Arial", 9)).pack(anchor=tk.W, pady=(12, 3), padx=10)
        min_len_var = tk.IntVar(value=1)
        max_len_var = tk.IntVar(value=7)
        
        min_len_inner = tk.Frame(main_frame)
        min_len_inner.pack(fill=tk.X, pady=2, padx=10)
        tk.Label(min_len_inner, text="  Min:", width=6, font=("Arial", 9)).pack(side=tk.LEFT)
        tk.Scale(min_len_inner, from_=1, to=10, orient=tk.HORIZONTAL, 
                variable=min_len_var, length=200).pack(side=tk.LEFT)
        tk.Label(min_len_inner, textvariable=min_len_var, width=2, font=("Arial", 9)).pack(side=tk.LEFT, padx=5)
        
        max_len_inner = tk.Frame(main_frame)
        max_len_inner.pack(fill=tk.X, pady=2, padx=10)
        tk.Label(max_len_inner, text="  Max:", width=6, font=("Arial", 9)).pack(side=tk.LEFT)
        tk.Scale(max_len_inner, from_=1, to=10, orient=tk.HORIZONTAL, 
                variable=max_len_var, length=200).pack(side=tk.LEFT)
        tk.Label(max_len_inner, textvariable=max_len_var, width=2, font=("Arial", 9)).pack(side=tk.LEFT, padx=5)
        
        tk.Label(main_frame, text="Vowel Count:", font=("Arial", 9)).pack(anchor=tk.W, pady=(12, 3), padx=10)
        min_vowels_var = tk.IntVar(value=0)
        max_vowels_var = tk.IntVar(value=5)
        
        min_v_inner = tk.Frame(main_frame)
        min_v_inner.pack(fill=tk.X, pady=2, padx=10)
        tk.Label(min_v_inner, text="  Min:", width=6, font=("Arial", 9)).pack(side=tk.LEFT)
        tk.Scale(min_v_inner, from_=0, to=7, orient=tk.HORIZONTAL, 
                variable=min_vowels_var, length=200).pack(side=tk.LEFT)
        tk.Label(min_v_inner, textvariable=min_vowels_var, width=2, font=("Arial", 9)).pack(side=tk.LEFT, padx=5)
        
        max_v_inner = tk.Frame(main_frame)
        max_v_inner.pack(fill=tk.X, pady=2, padx=10)
        tk.Label(max_v_inner, text="  Max:", width=6, font=("Arial", 9)).pack(side=tk.LEFT)
        tk.Scale(max_v_inner, from_=0, to=7, orient=tk.HORIZONTAL, 
                variable=max_vowels_var, length=200).pack(side=tk.LEFT)
        tk.Label(max_v_inner, textvariable=max_vowels_var, width=2, font=("Arial", 9)).pack(side=tk.LEFT, padx=5)
        
        tk.Label(main_frame, text="Consonant Count:", font=("Arial", 9)).pack(anchor=tk.W, pady=(12, 3), padx=10)
        min_consonants_var = tk.IntVar(value=0)
        max_consonants_var = tk.IntVar(value=7)
        
        min_c_inner = tk.Frame(main_frame)
        min_c_inner.pack(fill=tk.X, pady=2, padx=10)
        tk.Label(min_c_inner, text="  Min:", width=6, font=("Arial", 9)).pack(side=tk.LEFT)
        tk.Scale(min_c_inner, from_=0, to=8, orient=tk.HORIZONTAL, 
                variable=min_consonants_var, length=200).pack(side=tk.LEFT)
        tk.Label(min_c_inner, textvariable=min_consonants_var, width=2, font=("Arial", 9)).pack(side=tk.LEFT, padx=5)
        
        max_c_inner = tk.Frame(main_frame)
        max_c_inner.pack(fill=tk.X, pady=2, padx=10)
        tk.Label(max_c_inner, text="  Max:", width=6, font=("Arial", 9)).pack(side=tk.LEFT)
        tk.Scale(max_c_inner, from_=0, to=8, orient=tk.HORIZONTAL, 
                variable=max_consonants_var, length=200).pack(side=tk.LEFT)
        tk.Label(max_c_inner, textvariable=max_consonants_var, width=2, font=("Arial", 9)).pack(side=tk.LEFT, padx=5)
        
        tk.Label(main_frame, text="Leave Value Range:", font=("Arial", 9)).pack(anchor=tk.W, pady=(12, 3), padx=10)
        min_value_var = tk.DoubleVar(value=-50.0)
        max_value_var = tk.DoubleVar(value=50.0)
        
        min_val_inner = tk.Frame(main_frame)
        min_val_inner.pack(fill=tk.X, pady=2, padx=10)
        tk.Label(min_val_inner, text="  Min:", width=6, font=("Arial", 9)).pack(side=tk.LEFT)
        tk.Scale(min_val_inner, from_=-50.0, to=50.0, orient=tk.HORIZONTAL, 
                variable=min_value_var, resolution=0.5, length=200).pack(side=tk.LEFT)
        tk.Label(min_val_inner, textvariable=min_value_var, width=6, font=("Arial", 9)).pack(side=tk.LEFT, padx=5)
        
        max_val_inner = tk.Frame(main_frame)
        max_val_inner.pack(fill=tk.X, pady=2, padx=10)
        tk.Label(max_val_inner, text="  Max:", width=6, font=("Arial", 9)).pack(side=tk.LEFT)
        tk.Scale(max_val_inner, from_=-50.0, to=50.0, orient=tk.HORIZONTAL, 
                variable=max_value_var, resolution=0.5, length=200).pack(side=tk.LEFT)
        tk.Label(max_val_inner, textvariable=max_value_var, width=6, font=("Arial", 9)).pack(side=tk.LEFT, padx=5)
        
        tk.Label(main_frame, text="Must Contain Letters:", font=("Arial", 9)).pack(anchor=tk.W, pady=(12, 3), padx=10)
        must_contain_entry = tk.Entry(main_frame, width=30, font=("Arial", 9))
        must_contain_entry.pack(pady=2, anchor=tk.W, padx=10)
        tk.Label(main_frame, text="(e.g., 'A' or 'QU')", font=("Arial", 7), fg="gray").pack(anchor=tk.W, padx=10)
        
        tk.Label(main_frame, text="Must NOT Contain:", font=("Arial", 9)).pack(anchor=tk.W, pady=(12, 3), padx=10)
        must_not_contain_entry = tk.Entry(main_frame, width=30, font=("Arial", 9))
        must_not_contain_entry.pack(pady=2, anchor=tk.W, padx=10)
        tk.Label(main_frame, text="(e.g., 'Z')", font=("Arial", 7), fg="gray").pack(anchor=tk.W, padx=10)
        
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=15, anchor=tk.W, padx=10)
        
        def start_with_settings():
            """Start quiz with the selected settings"""
            settings = {
                'num_questions': num_questions_var.get(),
                'min_len': min_len_var.get(),
                'max_len': max_len_var.get(),
                'min_vowels': min_vowels_var.get() if min_vowels_var.get() > 0 else None,
                'max_vowels': max_vowels_var.get() if max_vowels_var.get() < 7 else None,
                'min_consonants': min_consonants_var.get() if min_consonants_var.get() > 0 else None,
                'max_consonants': max_consonants_var.get() if max_consonants_var.get() < 8 else None,
                'min_value': min_value_var.get(),
                'max_value': max_value_var.get(),
                'must_contain': must_contain_entry.get().upper() if must_contain_entry.get().strip() else None,
                'must_not_contain': must_not_contain_entry.get().upper() if must_not_contain_entry.get().strip() else None,
            }
            
            settings_window.destroy()
            self.start_quiz_with_settings(settings)
        
        tk.Button(button_frame, text="Generate Quiz", command=start_with_settings, 
                 bg="#3498db", fg="white", width=20).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Cancel", command=settings_window.destroy, 
                 width=10).pack(side=tk.LEFT, padx=5)
    
    def start_quiz_with_settings(self, settings):
        """Start a quiz using the provided settings"""
        try:
            quiz_items = self.leaves.genQuizItems(settings)
            
            if not quiz_items:
                messagebox.showwarning("No Results", 
                    "No leaves match your filter criteria.\nTry adjusting the settings.")
                self.show_quiz_settings()
                return
            
            self.quiz = Quiz([(qi.leave, qi.value) for qi in quiz_items])
            self.score = 0
            self.total = 0
            
            self.next_question()
            self.quiz_label.config(text=f"Guess the value: ({len(quiz_items)} questions)")
            self.stats['quizzes'] = self.stats.get('quizzes', 0) + 1
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate quiz:\n{str(e)}")
            self.show_quiz_settings()
        
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