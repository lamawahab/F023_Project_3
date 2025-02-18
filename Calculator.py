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
        
        #create a frame for the display 
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
        
                
        # Label to indicate trig functions take radians
        trig_label = tk.Label(self.root, text="Trig functions use Rad\nMUST CONVERT BEFORE USING", font=("Arial", 12), fg="red")
        trig_label.grid(row=0, column=4, columnspan=3)
        
        self.expression=""
        #call functions to set the buttons in my calculator
        self.create_number_buttons()
        self.create_calculation_buttons() 
    
    #define fnctions since they don't exist in math class
    def csc(x):
        return 1 / math.sin(x) if math.sin(x) != 0 else float('inf')
    
    def sec(x):
        return 1 / math.cos(x) if math.cos(x) != 0 else float('inf')
    
    def cot(x):
        return 1 / math.tan(x) if math.tan(x) != 0 else float('inf')

    #create a dictionary with all the needed functions imported from math class
    safe_dict = {
            "sqrt": math.sqrt,
            "log": math.log,
            "pow": math.pow,
            "π":math.pi,
            "sin":math.sin,
           "cos":math.cos,
           "tan":math.tan,
           "arcsin":math.asin,
           "arccos":math.acos,
           "arctan":math.atan,
           "degrees": math.degrees,
           "radians": math.radians,
           "csc":csc,
           "sec":sec,
           "cot":cot
        }
    
    #function to create numbers on the calculator
    def create_number_buttons(self):
        numbers = [
            (1, 1, 0), (2, 1, 1), (3, 1, 2),
            (4, 2, 0), (5, 2, 1), (6, 2, 2),
            (7, 3, 0), (8, 3, 1), (9, 3, 2),
            (0, 4, 1)
        ]
        
        #for loop to go through all numbers and place them correctly using grid
        for num, row, col in numbers:
            button = tk.Button(self.root, text=str(num), font=("Arial", 18), width=5, height=2, 
                               command=lambda n=num: self.click(n))
            button.grid(row=row, column=col, padx=5, pady=5)
        
        
    #create buttons and place then in thinker window using grid
    def create_calculation_buttons(self):
        #equal button 
        button_equal = tk.Button(self.root, text="=", font=("Arial", 20), width=5, height=2,
                         command= self.evaluate_expression)
        button_equal.grid(row=4, column=0, padx=5, pady=5)
        #clear button
        button_clear = tk.Button(self.root, text="Clear", font=("Arial", 20), width=5, height=2,
                         command= self.clear)
        button_clear.grid(row=4, column=2, padx=5, pady=5)
        
        #point button
        button_plus = tk.Button(self.root, text=".", font=("Arial", 20), width=5, height=2,
                                command= lambda: self.click("."))
        button_plus.grid(row=1, column=7, padx=5, pady=5)
        
        #plus button
        button_plus = tk.Button(self.root, text="+", font=("Arial", 20), width=5, height=2,
                                command= lambda: self.click("+"))
        button_plus.grid(row=1, column=3, padx=5, pady=5)
        #minus button
        button_minus = tk.Button(self.root, text="-", font=("Arial", 20), width=5, height=2,
                                command=lambda: self.click("-"))
        button_minus.grid(row=2, column=3, padx=5, pady=5)
       #exponent button
        button_exponent = tk.Button(self.root, text="X^n", font=("Arial", 20), width=5, height=2,
                                command=lambda: self.click("**"))
        button_exponent.grid(row=4, column=4, padx=5, pady=5)
       #square button
        button_square = tk.Button(self.root, text="X²", font=("Arial", 20), width=5, height=2,
                                command=lambda: self.click("**2"))
        button_square.grid(row=3, column=4, padx=5, pady=5)
       #square root button
        button_sqrtroot = tk.Button(self.root, text="(√)", font=("Arial", 20), width=5, height=2,
                                command=lambda: self.click("sqrt("))
        button_sqrtroot.grid(row=4, column=3, padx=5, pady=5)
       #left bracaket
        button_bracket1 = tk.Button(self.root, text="(", font=("Arial", 20), width=5, height=2,
                                command=lambda: self.click("("))
        button_bracket1.grid(row=1, column=4, padx=5, pady=5)
        #right bracket
        button_bracket2 = tk.Button(self.root, text=")", font=("Arial", 20), width=5, height=2,
                                command=lambda: self.click(")"))
        button_bracket2.grid(row=1, column=5, padx=5, pady=5)
       #pi button
        button_PI = tk.Button(self.root, text="π", font=("Arial", 20), width=5, height=2,
                                command=lambda: self.click("π"))
        button_PI.grid(row=2, column=4, padx=5, pady=5)
       #log button
        button_log = tk.Button(self.root, text="log(x)", font=("Arial", 20), width=5, height=2,
                                command=lambda: self.click("log("))
        button_log.grid(row=1, column=6, padx=5, pady=5)
        #multiplication button
        button_multi = tk.Button(self.root, text="×", font=("Arial", 20), width=5, height=2,
                                command=lambda: self.click("*"))
        button_multi.grid(row=3, column=3, padx=5, pady=5)
        #division button
        button_div = tk.Button(self.root, text="÷", font=("Arial", 20), width=5, height=2,
                                command=lambda: self.click("/"))
        button_div.grid(row=4, column=3, padx=5, pady=5)
        #sin button
        button_sin = tk.Button(self.root, text="sin", font=("Arial", 20), width=5, height=2,
                                command=lambda: self.click("sin("))
        button_sin.grid(row=3, column=5, padx=5, pady=5)
        #cos button
        button_cos = tk.Button(self.root, text="cos", font=("Arial", 20), width=5, height=2,
                                command=lambda: self.click("cos("))
        button_cos.grid(row=4, column=5, padx=5, pady=5)
        #tan button
        button_tan = tk.Button(self.root, text="tan", font=("Arial", 20), width=5, height=2,
                                command=lambda: self.click("tan("))
        button_tan.grid(row=2, column=5, padx=5, pady=5)
        #arc sin button
        button_arcsin = tk.Button(self.root, text="arcsin", font=("Arial", 20), width=5, height=2,
                                command=lambda: self.click("arcsin("))
        button_arcsin.grid(row=2, column=6, padx=5, pady=5)
        #arc cos button
        button_arccos = tk.Button(self.root, text="arccos", font=("Arial", 20), width=5, height=2,
                                command=lambda: self.click("arccos("))
        button_arccos.grid(row=3, column=6, padx=5, pady=5)
        #arc tan button
        button_arctan = tk.Button(self.root, text="arctan", font=("Arial", 20), width=5, height=2,
                                command=lambda: self.click("arctan("))
        button_arctan.grid(row=4, column=6, padx=5, pady=5)
        
        #radian to degree btton
        button_rad_to_deg = tk.Button(self.root, text="rad → deg", font=("Arial", 14), width=7, height=2,
                                      command=self.convert_to_degrees)
        button_rad_to_deg.grid(row=5, column=4, padx=5, pady=5)
        
        #degree to radian button
        button_deg_to_rad = tk.Button(self.root, text="deg → rad", font=("Arial", 14), width=7, height=2,
                                      command=self.convert_to_radians)
        button_deg_to_rad.grid(row=5, column=5, padx=5, pady=5)
        #csc button
        button_csc = tk.Button(self.root, text="csc", font=("Arial", 20), width=5, height=2,
                                command=lambda: self.click("csc("))
        button_csc.grid(row=2, column=7, padx=5, pady=5)
        #sec button
        button_sec = tk.Button(self.root, text="sec", font=("Arial", 20), width=5, height=2,
                                command=lambda: self.click("sec("))
        button_sec.grid(row=3, column=7, padx=5, pady=5)
        #cot button
        button_cot = tk.Button(self.root, text="cot", font=("Arial", 20), width=5, height=2,
                                command=lambda: self.click("cot("))
        button_cot.grid(row=4, column=7, padx=5, pady=5)
        
    

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
        #clear expression
        self.expression = ""
        self.display.delete(0, tk.END)#clear display
        
    def convert_to_degrees(self):
        match = re.search(r"(\d+(\.\d+)?)$", self.expression)#find last number in the expression
        if match:
            value = float(match.group(1))#convert to float
            result = math.degrees(value)  #convert radians to degrees
            self.expression = self.expression[:match.start()] + str(result)#replace only the number
            self.display.delete(0, tk.END)
            self.display.insert(0, self.expression)

    def convert_to_radians(self):
        match = re.search(r"(\d+(\.\d+)?)$", self.expression)  #find last number in the expression
        if match:
            value = float(match.group(1))#convert to float
            result = math.radians(value) #convert degrees to radians
            self.expression = self.expression[:match.start()] + str(result)#replace only the number
            self.display.delete(0, tk.END)
            self.display.insert(0, self.expression)
                
        
   
        
if __name__ == "__main__":
    root = tk.Tk()
    app = NumberPadCalculator(root)
    root.mainloop()