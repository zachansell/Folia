#!/usr/bin/env python3

import tkinter as tk
from tkinter import messagebox, ttk
import random
import json
import os
from LeaveSet import LeaveSet
from Quiz import Quiz

class SimpleLeaveTrainer:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Folia - Scrabble Leave Value Trainer")
        self.root.geometry("750x600")
        self.root.configure(bg='#f5f5f5')
        
        self._leaves = LeaveSet()
        self._quiz = None
        self._session_file = "session.json"
        
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
        btn_container.pack(pady=15)
        
        submit_btn = ttk.Button(btn_container, text="Submit Answer", 
                                command=self.check_guess)
        submit_btn.pack(side=tk.LEFT, padx=5)
        
        start_btn = ttk.Button(btn_container, text="Start Quiz", 
                               command=self.start_quiz)
        start_btn.pack(side=tk.LEFT, padx=5)
        
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
        """Start a new quiz"""
        questions = self._generate_questions(num_questions)
        self._quiz = Quiz(questions)
        self._stats['quizzes'] = self._stats.get('quizzes', 0) + 1
        self._save_session()
        self._show_question()
    
    def _generate_questions(self, count):
        """Generate quiz questions from the leave database"""
        all_leaves = list(self._leaves.items())
        return random.sample(all_leaves, min(count, len(all_leaves)))
    
    def _show_question(self):
        """Display current question"""
        if not self._quiz or self._quiz.finished:
            return
        
        current = self._quiz.current_question
        if current:
            self.leave_label.config(text=current.leave)
            self.quiz_label.config(text=f"What's the value of this leave?")
            self.rating_label.config(text="")
            self.guess_entry.delete(0, tk.END)
            self.guess_entry.focus_set()
            self._update_score_display()
        
    def check_guess(self):
        """Process user's guess"""
        if not self._quiz:
            messagebox.showinfo("Info", "Click 'Start Quiz' to begin!")
            return
        
        if self._quiz.finished:
            self._show_results()
            return
            
        try:
            guess = float(self.guess_entry.get())
            self._quiz.make_guess(guess)
            
            current = self._quiz.questions[self._quiz.current_index - 1]
            
            msg = f"You: {current.guess:.1f} | Actual: {current.value:.1f} | Diff: {current.delta:.1f}"
            self.quiz_label.config(text=msg)
            
            # Rating with colors
            rating_colors = {'correct': '#27ae60', 'excellent': '#2ecc71', 
                           'great': '#3498db', 'good': '#f39c12', 'poor': '#e74c3c'}
            self.rating_label.config(
                text=current.rating.upper(),
                fg=rating_colors.get(current.rating, '#7f8c8d')
            )
            
            self._update_lifetime_stats(current)
            self._update_score_display()
            
            if not self._quiz.finished:
                self.root.after(1800, self._show_question)
            else:
                self.root.after(1800, self._show_results)
            
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
    
    def _load_session(self):
        """Load persistent session data (Nov 9: Data encapsulation)"""
        default_stats = {
            'sessions': 0, 'quizzes': 0,
            'lifetime_score': 0, 'lifetime_total': 0,
            'total_delta': 0, 'perfect_count': 0
        }
        
        if os.path.exists(self._session_file):
            try:
                with open(self._session_file, 'r') as f:
                    self._stats = json.load(f)
            except:
                self._stats = default_stats
        else:
            self._stats = default_stats
            
        self._stats['sessions'] = self._stats.get('sessions', 0) + 1
        
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