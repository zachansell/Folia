#!/usr/bin/env python3
import tkinter as tk
from tkinter import simpledialog, messagebox
import random, time
from LeaveSet import LeaveSet

class App(tk.Tk):
    def __init__(self):
        super().__init__(); self.title("Folia - Scrabble Leave Value Study Tool"); self.geometry("800x600")
        self.content = tk.Frame(self, bg='#f0f0f0'); self.content.pack(fill=tk.BOTH, expand=True)
        self.ls = LeaveSet(); self.pool = []; 
        for k,v in self.ls.items():
            if 2<=len(k)<=5 and -20<=v<=30: self.pool.append((k,v)); 
            if len(self.pool)>=3000: break
        random.shuffle(self.pool); self.show_menu()
    def clear(self):
        try:
            self.content.destroy()
        except Exception:
            pass
        self.content = tk.Frame(self, bg='#f0f0f0')
        self.content.pack(fill=tk.BOTH, expand=True)
    def show_menu(self):
        self.clear(); tk.Label(self.content, text="FOLIA", font=('Helvetica',48,'bold'), bg='#f0f0f0').pack(pady=30)
        tk.Button(self.content, text="Start Quiz", command=self.start_quiz, font=('Helvetica',14), width=20, height=2, bg='#3498db', fg='white').pack(pady=10)
        tk.Button(self.content, text="Lookup Leave", command=self.lookup, font=('Helvetica',14), width=20, height=2, bg='#3498db', fg='white').pack(pady=10)
        tk.Button(self.content, text="Exit", command=self.destroy, font=('Helvetica',14), width=20, height=2, bg='#3498db', fg='white').pack(pady=10)
    def start_quiz(self):
        if len(self.pool)<10: messagebox.showerror("Error","Not enough leaves"); return
        self.items = random.sample(self.pool,10); self.i=0; self.guesses=[]; self.t0=time.time(); self.show_q()
    def show_q(self):
        print("[Folia] show_q start", self.i)
        self.clear(); leave,val=self.items[self.i]
        f = tk.Frame(self.content, bg='#f0f0f0'); f.pack(fill=tk.BOTH, expand=True)
        q = tk.Label(f, text=f"Question {self.i+1}/10", font=('Helvetica',16), bg='#f0f0f0', fg='#2c3e50'); q.pack(pady=10)
        L = tk.Label(f, text=leave, font=('Helvetica',72,'bold'), bg='#f0f0f0', fg='#2c3e50'); L.pack(pady=30)
        e=tk.Entry(f, font=('Helvetica',16), width=10); e.pack(pady=10); e.focus_set()
        out=tk.Label(f, text="Type a number and press Submit", font=('Helvetica',14), bg='#f0f0f0', fg='#2c3e50'); out.pack(pady=10)
        def submit():
            try:
                g=float(e.get()); d=abs(g-val); self.guesses.append(d)
                out.config(text=f"Your: {g:.1f}  |  Actual: {val:.1f}  |  Diff: {d:.1f}")
            except: messagebox.showerror("Error","Enter a number")
        tk.Button(f, text="Submit", command=submit, font=('Helvetica',14), bg='#2ecc71', fg='white').pack(pady=10)
        tk.Button(f, text=("Next" if self.i<9 else "Finish"), command=(lambda: self.next_q()), font=('Helvetica',14), bg='#9b59b6', fg='white').pack(pady=5)
        tk.Button(f, text="Back", command=self.show_menu, font=('Helvetica',12)).pack(pady=5)
        self.update_idletasks(); print("[Folia] show_q rendered")
    def next_q(self):
        self.i+=1
        if self.i<10: self.show_q()
        else:
            self.clear(); m=sum(self.guesses)/len(self.guesses) if self.guesses else 0
            tk.Label(self.content, text="Quiz Complete!", font=('Helvetica',28,'bold'), bg='#f0f0f0').pack(pady=20)
            tk.Label(self.content, text=f"Average Difference: {m:.2f}\nTime: {time.time()-self.t0:.1f}s", font=('Helvetica',14), bg='#f0f0f0').pack(pady=10)
            tk.Button(self.content, text="Back to Menu", command=self.show_menu, font=('Helvetica',14), bg='#3498db', fg='white').pack(pady=20)
    def lookup(self):
        s=simpledialog.askstring("Lookup","Enter a leave (1-6 tiles):", parent=self)
        if not s: return
        n=self.ls.normalize_leave(s); v=self.ls.get(n)
        messagebox.showinfo("Result", f"{n} = {v if v is not None else 'NOT FOUND'}")

if __name__=="__main__": App().mainloop()

