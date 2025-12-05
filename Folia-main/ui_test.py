#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox

def test_click():
    messagebox.showinfo("Success", "Button clicked successfully.")

root = tk.Tk()
root.title("Button Test")
root.geometry("400x300")
root.configure(bg='white')

tk.Label(root, text="Does this button work?", 
         font=('Helvetica', 16), bg='white').pack(pady=40)

btn = tk.Button(root, text="Click here.", command=test_click,
                font=('Helvetica', 18, 'bold'), width=15, height=3,
                bg='#2ecc71', fg='white')
btn.pack(pady=20)

tk.Label(root, text="If popup appears, buttons work.", 
         font=('Helvetica', 12), bg='white').pack(pady=20)

root.mainloop()

