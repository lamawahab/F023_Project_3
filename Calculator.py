#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 12:26:11 2025

@author: lamaalabdulwahab
"""

import tkinter as tk

class NumberPadCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("My Calculator")
        self.root.geometry("300x400")
        
        self.display = tk.Entry(root, font=("Arial", 24), justify='left', bd=10)
        self.display.grid(row=0, column=0, columnspan=3, ipadx=8, ipady=8)
        
        self.create_number_buttons()
        
    def create_number_buttons(self):
        numbers = [
            (1, 1, 0), (2, 1, 1), (3, 1, 2),
            (4, 2, 0), (5, 2, 1), (6, 2, 2),
            (7, 3, 0), (8, 3, 1), (9, 3, 2),
            (0, 4, 1)
        ]
        
        for num, row, col in numbers:
            button = tk.Button(self.root, text=str(num), font=("Arial", 18), width=5, height=2, 
                               command=lambda n=num: self.append_number(n))
            button.grid(row=row, column=col, padx=5, pady=5)
        
    def append_number(self, num):
        current_text = self.display.get()
        self.display.delete(0, tk.END)
        self.display.insert(0, current_text + str(num))
        
        
   
        
if __name__ == "__main__":
    root = tk.Tk()
    app = NumberPadCalculator(root)
    root.mainloop()