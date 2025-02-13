#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 12:26:11 2025

@author: lamaalabdulwahab
"""

import re
import tkinter as tk
import math
class NumberPadCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("My Calculator")
        self.root.geometry("300x400")
        
        #create a frame for the display and scrollbar
        display_frame = tk.Frame(root, bg="black", padx=3,pady=3)
        display_frame.grid(row=0, column=0, columnspan=3, sticky="ew")
        
        #entry widget for numbers and calculations (display)
        self.display = tk.Entry(display_frame, font=("Arial", 24), justify='left', bd=10, width=25)
        self.display.pack(side="left", expand=True, fill="both")
    
        #add scrollbar to help showcase long calculations
        scrollbar = tk.Scrollbar(display_frame, bg="red",orient="horizontal", command=self.display.xview)
        scrollbar.pack(side="bottom", fill="x")
    
        #link scrollbar to display
        self.display.config(xscrollcommand=scrollbar.set)

        
        self.expression=""
        
        self.create_number_buttons()
        self.create_calculation_buttons_lama() 
    
    safe_dict = {
            "sqrt": math.sqrt,
            "log": math.log,
            "pow": math.pow,
            "π":math.pi,
        }
        
    def create_number_buttons(self):
        numbers = [
            (1, 1, 0), (2, 1, 1), (3, 1, 2),
            (4, 2, 0), (5, 2, 1), (6, 2, 2),
            (7, 3, 0), (8, 3, 1), (9, 3, 2),
            (0, 4, 1)
        ]
        
        for num, row, col in numbers:
            button = tk.Button(self.root, text=str(num), font=("Arial", 18), width=5, height=2, 
                               command=lambda n=num: self.click(n))
            button.grid(row=row, column=col, padx=5, pady=5)
        
        
    #create buttons and place then in thinker window
    def create_calculation_buttons_lama(self):
        #equal button 
        button_equal = tk.Button(self.root, text="=", font=("Arial", 20), width=5, height=2,
                         command= self.evaluate_expression)
        button_equal.grid(row=4, column=0, padx=5, pady=5)
        
        button_clear = tk.Button(self.root, text="Clear", font=("Arial", 20), width=5, height=2,
                         command= self.clear)
        button_clear.grid(row=4, column=2, padx=5, pady=5)
        
        button_plus = tk.Button(self.root, text="+", font=("Arial", 20), width=5, height=2,
                                command= lambda: self.click("+"))
        button_plus.grid(row=1, column=3, padx=5, pady=5)
        
        button_minus = tk.Button(self.root, text="-", font=("Arial", 20), width=5, height=2,
                                command=lambda: self.click("-"))
        button_minus.grid(row=2, column=3, padx=5, pady=5)
       
        button_exponent = tk.Button(self.root, text="Exponent", font=("Arial", 20), width=5, height=2,
                                command=lambda: self.click("**"))
        button_exponent.grid(row=3, column=3, padx=5, pady=5)
       
        button_square = tk.Button(self.root, text="X²", font=("Arial", 20), width=5, height=2,
                                command=lambda: self.click("**2"))
        button_square.grid(row=3, column=4, padx=5, pady=5)
       
        button_bracket1 = tk.Button(self.root, text="(√)", font=("Arial", 20), width=5, height=2,
                                command=lambda: self.click("sqrt("))
        button_bracket1.grid(row=4, column=3, padx=5, pady=5)
       
        button_bracket1 = tk.Button(self.root, text="(", font=("Arial", 20), width=5, height=2,
                                command=lambda: self.click("("))
        button_bracket1.grid(row=1, column=4, padx=5, pady=5)
       
        button_bracket2 = tk.Button(self.root, text=")", font=("Arial", 20), width=5, height=2,
                                command=lambda: self.click(")"))
        button_bracket2.grid(row=1, column=5, padx=5, pady=5)
       
        button_PI = tk.Button(self.root, text="π", font=("Arial", 20), width=5, height=2,
                                command=lambda: self.click("π"))
        button_PI.grid(row=2, column=4, padx=5, pady=5)
       
        button_log = tk.Button(self.root, text="log(x)", font=("Arial", 20), width=5, height=2,
                                command=lambda: self.click("log("))
        button_log.grid(row=3, column=4, padx=5, pady=5)
        
    

    def set_operation(self, operator):
        current_text = self.display.get().strip()  #get the current number
    
        if current_text and (not self.expression or self.expression[-1] not in "+-"):  
            self.expression.append(current_text)  # add only if it's a number (not an operator)
    
        self.expression.append(operator)  #add the new operator
        self.display.delete(0, tk.END)#delete existing label
        self.display.insert(0, " ".join(self.expression))#update display 
    
        self.new_number = False#makes next number start fresh
        
    def click(self, value):
        self.expression = self.expression + str(value)#add value to the existing expression
        self.display.delete(0, tk.END)#clear display
        self.display.insert(0,self.expression)#put new expression into display
    
    def evaluate_expression(self):
        try:
            
            #prevent taking sqrt of negative numbers because it causes imaginery numbers
            sqrt_pattern = re.findall(r"sqrt\((-?\d+)\)", self.expression)
            for num in sqrt_pattern:
                if int(num) < 0:
                    raise ValueError("Cannot take sqrt of a negative number")
            
            #prevent expressions that only contain operators (like "--", "++", etc.)
            if not any(char.isdigit() for char in self.expression):
                raise SyntaxError("Invalid expression: No numbers")
            
    
            total = eval(self.expression, {"__builtins__": None}, self.safe_dict) #evaluate the calculation in expression
            self.expression = str(total)#update the expression to the result of calculations
            self.display.delete(0, tk.END)#clear display
            self.display.insert(0,self.expression)#put new expression into display
    
        except (ValueError, SyntaxError, NameError, TypeError, ZeroDivisionError): #if calculations don't work
            self.display.delete(0, tk.END)  # Clear display
            self.display.insert(0, "Error.. clear and try again")  #print error message for user
            self.expression = ""  #reset expression
    
    def clear(self):
        self.expression = ""#clear expression
        self.display.delete(0, tk.END)#clear display
        

        
   
        
if __name__ == "__main__":
    root = tk.Tk()
    app = NumberPadCalculator(root)
    root.mainloop()