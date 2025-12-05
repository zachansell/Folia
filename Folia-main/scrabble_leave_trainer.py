#!/usr/bin/env python3

import tkinter as tk
from tkinter import messagebox, ttk
import random
import json
import os
from LeaveSet import LeaveSet
from Quiz import Quiz
from QuizItem import QuizItem

class SimpleLeaveTrainer:
    DEFAULT_SETTINGS = {
        'num_questions': 10,
        'min_len': 1,
        'max_len': 7,
        'min_vowels': 0,
        'max_vowels': 5,
        'min_consonants': 0,
        'max_consonants': 7,
        'min_value': -50.0,
        'max_value': 50.0,
        'must_contain': '',
        'must_not_contain': '',
    }
    
    def __init__(self, root):
        self.root = root
        self.root.title("Folia: Scrabble Leave Trainer Demo")
        self.root.geometry("600x500")
        
        self._leaves = LeaveSet()
        self.leaves = self._leaves  # Add alias for compatibility
        self.quiz = None
        self._quiz = None
        self.score = 0
        self.total = 0
        
        self.current_settings = self.DEFAULT_SETTINGS.copy()
        
        self._session_file = "session.json"
        self._stats = {}
        
        # Load session and setup
        self._load_session()
        self._setup_ui()
    
    def _setup_ui(self):
        """Build the application UI"""
        # Header
        header = tk.Frame(self.root, bg='#4a5568', height=50)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        tk.Label(header, text="Folia - Scrabble Leave Trainer", 
                font=("Helvetica", 16, "bold"), bg='#4a5568', fg='white').pack(pady=12)
        
        # Main content area
        main = tk.Frame(self.root, bg='#e2e8f0')
        main.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left: Quiz
        left = tk.Frame(main, bg='white', relief=tk.GROOVE, bd=2)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        tk.Label(left, text="Quiz Mode", font=("Helvetica", 12, "bold"), 
                bg='white', fg='black').pack(pady=(15, 10))
        
        # Start Quiz button - prominently at the top
        tk.Button(left, text="Start Quiz", 
                 command=self.show_quiz_settings, font=('Helvetica', 12, 'bold'),
                 bg='#3498db', fg='white', width=20, height=2).pack(pady=15)
        
        self.quiz_label = tk.Label(left, text="Click 'Start Quiz' to begin", 
                                   font=("Helvetica", 10), bg='white', fg='#4a5568')
        self.quiz_label.pack(pady=5)
        
        self.leave_label = tk.Label(left, text="", 
                                    font=("Courier", 40, "bold"), bg='white', fg='#2d3748')
        self.leave_label.pack(pady=20)
        
        tk.Label(left, text="Enter your guess:", font=("Helvetica", 10), 
                bg='white', fg='black').pack()
        
        self.guess_entry = tk.Entry(left, font=("Helvetica", 14), width=12, 
                                    justify='center', bg='white', fg='black',
                                    insertbackground='black')
        self.guess_entry.pack(pady=8)
        self.guess_entry.bind('<Return>', lambda e: self.check_guess())
        
        btn_container = tk.Frame(left, bg='white')
        btn_container.pack(pady=10)
        
        self.submit_btn = ttk.Button(btn_container, text="Submit Answer", 
                                command=self.check_guess)
        self.submit_btn.pack(side=tk.LEFT, padx=5)
        
        self.next_btn = ttk.Button(btn_container, text="Next Question", 
                                    command=self.advance_quiz, state='disabled')
        self.next_btn.pack(side=tk.LEFT, padx=5)
        
        self.score_label = tk.Label(left, text="Questions: 0/0 | Accurate: 0", 
                                    font=("Helvetica", 9), bg='white', fg='#718096')
        self.score_label.pack(pady=8)
        
        self.rating_label = tk.Label(left, text="", 
                                     font=("Helvetica", 11, "bold"), bg='white')
        self.rating_label.pack(pady=5)
        
        # Right: Lookup
        right = tk.Frame(main, bg='white', relief=tk.GROOVE, bd=2)
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        tk.Label(right, text="Leave Lookup", font=("Helvetica", 12, "bold"), 
                bg='white', fg='black').pack(pady=(15, 10))
        
        tk.Label(right, text="Enter tiles to look up:", font=("Helvetica", 10), 
                bg='white', fg='#4a5568').pack(pady=10)
        
        self.lookup_entry = tk.Entry(right, font=("Helvetica", 14), width=12, 
                                     justify='center', bg='white', fg='black',
                                     insertbackground='black')
        self.lookup_entry.pack(pady=10)
        self.lookup_entry.bind('<Return>', lambda e: self.lookup_leave())
        
        lookup_btn = ttk.Button(right, text="Search", command=self.lookup_leave)
        lookup_btn.pack(pady=15)
        
        self.result_label = tk.Label(right, text="", 
                                     font=("Courier", 16, "bold"), bg='white', fg='#2d3748')
        self.result_label.pack(pady=30)
        
        # Bottom stats bar
        stats = tk.Frame(self.root, bg='#cbd5e0')
        stats.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.stats_label = tk.Label(stats, text="", font=("Helvetica", 9), 
                                    bg='#cbd5e0', fg='#2d3748')
        self.stats_label.pack(pady=8)
        self._update_stats_display()
    
    def start_quiz(self, num_questions=10):
        """Start a new quiz - this redirects to settings dialog"""
        self.show_quiz_settings()
    
    def show_quiz_settings(self):
        """Open a configuration dialog for quiz settings"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Quiz Configuration")
        settings_window.geometry("500x700")
        
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
        num_questions_var = tk.IntVar(value=self.current_settings['num_questions'])
        num_q_inner = tk.Frame(main_frame)
        num_q_inner.pack(fill=tk.X, pady=3, padx=10)
        tk.Scale(num_q_inner, from_=1, to=50, orient=tk.HORIZONTAL, 
                variable=num_questions_var, length=220).pack(side=tk.LEFT)
        tk.Label(num_q_inner, textvariable=num_questions_var, width=3, font=("Arial", 9)).pack(side=tk.LEFT, padx=8)
        
        tk.Label(main_frame, text="Leave Length (letters):", font=("Arial", 9)).pack(anchor=tk.W, pady=(12, 3), padx=10)
        min_len_var = tk.IntVar(value=self.current_settings['min_len'])
        max_len_var = tk.IntVar(value=self.current_settings['max_len'])
        
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
        min_vowels_var = tk.IntVar(value=self.current_settings['min_vowels'])
        max_vowels_var = tk.IntVar(value=self.current_settings['max_vowels'])
        
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
        min_consonants_var = tk.IntVar(value=self.current_settings['min_consonants'])
        max_consonants_var = tk.IntVar(value=self.current_settings['max_consonants'])
        
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
        min_value_var = tk.DoubleVar(value=self.current_settings['min_value'])
        max_value_var = tk.DoubleVar(value=self.current_settings['max_value'])
        
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
        must_contain_entry.insert(0, self.current_settings['must_contain'])
        must_contain_entry.pack(pady=2, anchor=tk.W, padx=10)
        tk.Label(main_frame, text="(e.g., 'A' or 'QU')", font=("Arial", 7), fg="gray").pack(anchor=tk.W, padx=10)
        
        tk.Label(main_frame, text="Must NOT Contain:", font=("Arial", 9)).pack(anchor=tk.W, pady=(12, 3), padx=10)
        must_not_contain_entry = tk.Entry(main_frame, width=30, font=("Arial", 9))
        must_not_contain_entry.insert(0, self.current_settings['must_not_contain'])
        must_not_contain_entry.pack(pady=2, anchor=tk.W, padx=10)
        tk.Label(main_frame, text="(e.g., 'Z')", font=("Arial", 7), fg="gray").pack(anchor=tk.W, padx=10)
        
        # Separator
        tk.Frame(main_frame, height=2, bg='#e0e0e0').pack(fill=tk.X, pady=20, padx=10)
        
        # Ready to start label
        tk.Label(main_frame, text="Ready? Click below to start your quiz!", 
                font=("Arial", 10, "bold")).pack(pady=(5, 10), padx=10)
        
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
        
        button_frame = tk.Frame(main_frame, bg='white')
        button_frame.pack(pady=(5, 30))
        
        # Use ttk.Button for better cross-platform styling
        start_btn = ttk.Button(button_frame, text="Generate Quiz", command=start_with_settings)
        start_btn.pack(side=tk.LEFT, padx=10, ipadx=30, ipady=12)
        
        cancel_btn = ttk.Button(button_frame, text="Cancel", command=settings_window.destroy)
        cancel_btn.pack(side=tk.LEFT, padx=10, ipadx=20, ipady=12)
    
    def start_quiz_with_settings(self, settings):
        """Start a quiz using the provided settings"""
        try:
            quiz_items = self.leaves.genQuizItems(settings)
            
            if not quiz_items:
                messagebox.showwarning("No Results", 
                    "No leaves match your filter criteria.\nTry adjusting the settings.")
                self.show_quiz_settings()
                return
            
            #save settings for next time
            self.current_settings = {
                'num_questions': settings['num_questions'],
                'min_len': settings['min_len'],
                'max_len': settings['max_len'],
                'min_vowels': settings['min_vowels'] or 0,
                'max_vowels': settings['max_vowels'] or 7,
                'min_consonants': settings['min_consonants'] or 0,
                'max_consonants': settings['max_consonants'] or 8,
                'min_value': settings['min_value'],
                'max_value': settings['max_value'],
                'must_contain': settings['must_contain'] or '',
                'must_not_contain': settings['must_not_contain'] or '',
            }
            
            self.quiz = Quiz([(qi.leave, qi.value) for qi in quiz_items])
            self._quiz = self.quiz  # Keep both references for compatibility
            self.score = 0
            self.total = 0
            
            # Reset button states
            self.submit_btn.config(state='normal')
            self.next_btn.config(state='disabled')
            self.guess_entry.config(state='normal')
            
            self.next_question()
            self.quiz_label.config(text=f"Guess the value: ({len(quiz_items)} questions)")
            self._stats['quizzes'] = self._stats.get('quizzes', 0) + 1
            self._save_session()
            
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
            self.guess_entry.config(state='normal')
            self.submit_btn.config(state='normal')
            self.next_btn.config(state='disabled')
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
            
            # Disable submit, enable next, disable entry
            self.submit_btn.config(state='disabled')
            self.next_btn.config(state='normal')
            self.guess_entry.config(state='disabled')
            
            # Update score display
            self.score_label.config(text=f"Questions: {self.total}/{len(self.quiz.questions)} | Accurate: {self.score}")
            
            self._stats['lifetime_total'] = self._stats.get('lifetime_total', 0) + 1
            if current.rating in ("excellent", "great", "good", "correct"):
                self._stats['lifetime_score'] = self._stats.get('lifetime_score', 0) + 1
            self._save_session()
            
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a numeric value.")
    
    def _update_score_display(self):
        """Update current quiz score"""
        completed = self._quiz.current_index
        total = len(self._quiz.questions)
        good_count = sum(1 for q in self._quiz.questions[:completed] if q.delta < 3)
        self.score_label.config(text=f"Progress: {completed}/{total} | Accurate: {good_count}")
        self._update_stats_display()
    
    def _update_stats_display(self):
        """Update lifetime statistics display at the bottom bar"""
        sessions = self._stats.get('sessions', 0)
        quizzes = self._stats.get('quizzes', 0)
        score = self._stats.get('lifetime_score', 0)
        total = self._stats.get('lifetime_total', 0)
        accuracy = (score / total * 100) if total > 0 else 0
        
        stats_text = f"Sessions: {sessions} | Quizzes: {quizzes} | "
        stats_text += f"Lifetime Accuracy: {score}/{total} ({accuracy:.1f}%) | "
        stats_text += f"Avg Questions/Quiz: {total//quizzes if quizzes > 0 else 0}"
        
        self.stats_label.config(text=stats_text)
    
    def _update_lifetime_stats(self, item):
        """Update persistent statistics on disk"""
        self._stats['lifetime_total'] = self._stats.get('lifetime_total', 0) + 1
        if item.delta < 3:
            self._stats['lifetime_score'] = self._stats.get('lifetime_score', 0) + 1
        
        self._stats.setdefault('total_delta', 0)
        self._stats['total_delta'] += item.delta
        self._stats.setdefault('perfect_count', 0)
        if item.delta == 0:
            self._stats['perfect_count'] += 1
            
        self._save_session()
    
    def _show_results(self):
        """Display quiz results with statistics"""
        results = self._quiz.results()
        stats = self._quiz.statistics()
        
        msg = "Quiz Complete!\n\n"
        msg += f"Performance Summary:\n"
        msg += f"  Accurate Guesses: {int(stats['accuracy'] * len(results))}/{len(results)}\n"
        msg += f"  Perfect Answers: {stats['correct_count']}\n"
        msg += f"  Excellent or Better: {stats['excellent_count']}\n"
        msg += f"  Average Error: {stats['avg_delta']:.2f}\n"
        msg += f"  Best Guess: {stats['min_delta']:.2f} off\n"
        msg += f"  Worst Guess: {stats['max_delta']:.2f} off\n"
        msg += f"  Total Time: {stats['total_time']}s\n"
        msg += f"  Overall Accuracy: {stats['accuracy']*100:.1f}%\n\n"
        msg += "Start another quiz?"
        
        if messagebox.askyesno("Quiz Results", msg):
            self.start_quiz()
    
    def advance_quiz(self):
        if self.quiz is None:
            return
        
        if self.quiz.finished:
            self.quiz_label.config(text="Quiz finished!")
            self.show_results()
        else:
            self.next_question()
    
    def lookup_leave(self):
        """Look up a leave value in the database"""
        leave = self.lookup_entry.get().strip()
        if not leave:
            return
            
        leave = self._leaves.normalize_leave(leave)
        
        if leave in self._leaves:
            value = self._leaves.get(leave)
            self.result_label.config(
                text=f"{leave}\n= {value:.1f}",
                fg='#16a085'
            )
        else:
            self.result_label.config(
                text=f"{leave}\nNot found",
                fg='#e74c3c'
            )
    
    def show_results(self):
        """Display final quiz results"""
        if self.quiz is None:
            return
        
        results_text = f"Quiz Complete!\n\nFinal Score: {self.score}/{self.total}"
        percentage = (self.score / self.total * 100) if self.total > 0 else 0
        results_text += f"\nAccuracy: {percentage:.1f}%"
        
        # Try to show detailed statistics if available
        try:
            stats = self.quiz.statistics()
            results = self.quiz.results()
            if stats and results:
                results_text = "Quiz Complete!\n\n"
                results_text += f"Performance Summary:\n"
                results_text += f"  Accurate Guesses: {int(stats.get('accuracy', 0) * len(results))}/{len(results)}\n"
                results_text += f"  Average Error: {stats.get('avg_delta', 0):.2f}\n"
                results_text += f"  Best Guess: {stats.get('min_delta', 0):.2f} off\n"
                results_text += f"  Worst Guess: {stats.get('max_delta', 0):.2f} off\n"
        except:
            pass  # Use simple results if detailed stats not available
        
        if messagebox.askyesno("Quiz Results", results_text + "\n\nStart another quiz?"):
            self.start_quiz()
    
    def _load_session(self):
        """Load session statistics from disk"""
        default_stats = {
            'sessions': 0,
            'quizzes': 0,
            'lifetime_score': 0,
            'lifetime_total': 0,
            'total_delta': 0,
            'perfect_count': 0
        }
        
        if os.path.exists(self._session_file):
            try:
                with open(self._session_file, 'r') as f:
                    self._stats = json.load(f)
            except:
                self._stats = default_stats.copy()
        else:
            self._stats = default_stats.copy()
            
        self._stats['sessions'] = self._stats.get('sessions', 0) + 1
        self._save_session()
        
    def _save_session(self):
        """Persist session data to disk"""
        try:
            with open(self._session_file, 'w') as f:
                json.dump(self._stats, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save session data: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleLeaveTrainer(root)
    root.mainloop()