import tkinter as tk
from tkinter import messagebox
import datetime

import sqlite3

#to generate reference number 
import random
import string



def insert_booking(first_name, last_name, passport_number, seat_row, seat_column):
    """Insert a booking with a unique reference into the database."""
    booking_reference = generate_booking_reference()
    cursor.execute('''
        INSERT INTO customer_bookings (booking_reference, first_name, last_name, passport_number, seat_row, seat_column)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (booking_reference, first_name, last_name, passport_number, seat_row, seat_column))
    conn.commit()

def fetch_all_bookings():
    """Retrieve all booking records from the database."""
    conn = sqlite3.connect('booking_system.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customer_bookings")
    results = cursor.fetchall()
    conn.close()
    return results

def remove_booking(seat_row, seat_column):
    """Delete a booking based on seat row and column."""
    conn = sqlite3.connect('booking_system.db')
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM customer_bookings
        WHERE seat_row = ? AND seat_column = ?
    ''', (seat_row, seat_column))
    conn.commit()
    conn.close()

used_ref = set()
def generate_booking_reference():
    """Generate a unique 8-character alphanumeric booking reference."""
    while True:
        ref = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        if ref not in used_ref:
            used_ref.add(ref)
            return ref



# Initializing the seat layout with 'F' for free, 'R' for reserved, 'X' for aisles
seats = [
    ['F']*20,  # Row 1
    ['F']*20,  # Row 2
    ['F']*20,  # Row 3
    ['X']*20,  # Aisle row (non-interactive)
    ['F']*20,  # Row 4
    ['F']*20,  # Row 5
    ['F']*20,  # Row 6
]

#  Initializing the storage space for the airplane
for i in range (4,7):
    for j in range (15,19):
        seats[i][j] = 'S'


class SeatBookingSystem:
    def __init__(self, root):
        # Set up the main window
        self.root = root
        self.root.title("Seat Booking System")
        self.selected_seat = None 
        self.reservation_history = {}
        # Title label at the top of the window
        self.title_label = tk.Label(root, text="Airplane Seat Booking System", font=('Arial', 16))
        self.title_label.grid(row=0, column=0, columnspan=20, pady=10)

        # Create the seat grid (20 seats per row and 7 rows in total)
        self.labels = []
        self.create_seat_grid()

        # Action buttons for booking, freeing, and showing seat status
        self.book_button = tk.Button(root, text="Book Seat", command=self.book_seat, font=('Arial', 12), width=20)
        self.book_button.grid(row=8, column=0, columnspan=2, pady=10)

        self.free_button = tk.Button(root, text="Free Seat", command=self.free_seat, font=('Arial', 12), width=20)
        self.free_button.grid(row=8, column=2, columnspan=2, pady=10)

        self.status_button = tk.Button(root, text="Show Status", command=self.show_status, font=('Arial', 12), width=20)
        self.status_button.grid(row=8, column=4, columnspan=4, pady=10)

        self.show_bookings_button = tk.Button(root, text="Show All Bookings", command=self.show_all_bookings, font=('Arial', 12), width=20)
        self.show_bookings_button.grid(row=8, column=8, columnspan=4, pady=10)

        self.show_history_button = tk.Button(root, text="Show Booking History", command=self.show_history, font=('Arial', 12), width=20)
        self.show_history_button.grid(row=8, column=12, columnspan=4, pady=10)

        # Input field for entering seat selection
        self.seat_label = tk.Label(root, text="Enter seat (e.g., 1A, 2B):", font=('Arial', 12))
        self.seat_label.grid(row=9, column=0, columnspan=2, pady=5)

        self.seat_input = tk.Entry(root, font=('Arial', 12), width=10)
        self.seat_input.grid(row=9, column=2, columnspan=2, pady=5)

    def create_seat_grid(self):
        """Create the grid of labels to represent seats in the window."""
        seat_letters = ['A', 'B', 'C', 'D', 'E', 'F']
        for i in range(7):  # 7 rows of seats (including aisle row)
            row_labels = []
            seat_letter = "X" if i == 3 else chr(65 + i -1) if i > 3 else chr(65+i) 
            for j in range(20):  # 20 seats in each row
                if i == 3:  # Aisle row (X row)
                    seat_label = "X"
                    label = tk.Label(self.root, text=seat_label, width=5, height=2, font=('Arial', 12), bg='gray')
                else:  # Seating rows
                    seat_label = f"{j+1}{seat_letter}"  # Seat name (e.g., 1A, 2B)
                    label = tk.Label(self.root, text=seat_label, width=5, height=2, font=('Arial', 12), relief="solid")
                label.grid(row=i+1, column=j, padx=2, pady=2)
                row_labels.append(label)
            self.labels.append(row_labels)

        # Apply initial color coding to each seat label
        self.update_all_seats()

    def book_seat(self):
        """Book a seat by selecting a row and column."""
        seat_input = self.seat_input.get().upper()
        if len(seat_input) < 2 or len(seat_input) > 3:
            messagebox.showerror("Invalid Input", "Please enter a valid seat (e.g., 1A, 2B).")
            return

        row = ord(seat_input[-1]) - 65  # Convert column letter to index (A=0, B=1, etc.)
        col = int(seat_input[:-1]) - 1  # Convert row number to 0-based index
        lower = False
        if row >= 3:
            row += 1  # Adjust row for the aisle row
            lower = True

        if row < 0 or row >= len(seats) or col < 0 or col >= len(seats[0]):
            messagebox.showerror("Invalid Seat", "Please enter a valid seat number within the seating range.")
            return

        if seats[row][col] == 'X':
            messagebox.showerror("Aisle Seat", "This seat is an aisle seat and cannot be booked.")
            return

        if seats[row][col] == 'S':
            messagebox.showerror("Storage Seat", "This seat is a storage seat and cannot be booked.")
            return

        if seats[row][col] == 'F':
            # Open a form to collect passenger details
            self.open_passenger_form(row, col, seat_input,lower)
        else:
            messagebox.showerror("Seat Occupied", "This seat is already reserved!")

    def open_passenger_form(self, row, col, seat_input,lower):
        """Open a form to collect passenger details."""
        form = tk.Toplevel(self.root)
        form.title("Passenger Details")

        tk.Label(form, text="First Name:").grid(row=0, column=0, padx=5, pady=5)
        first_name_entry = tk.Entry(form)
        first_name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form, text="Last Name:").grid(row=1, column=0, padx=5, pady=5)
        last_name_entry = tk.Entry(form)
        last_name_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form, text="Passport Number:").grid(row=2, column=0, padx=5, pady=5)
        passport_entry = tk.Entry(form)
        passport_entry.grid(row=2, column=1, padx=5, pady=5)

        def submit_details():
            first_name = first_name_entry.get()
            last_name = last_name_entry.get()
            passport_number = passport_entry.get()

            if not first_name or not last_name or not passport_number:
                messagebox.showerror("Incomplete Details", "Please fill in all fields.")
                return

            booking_ref = generate_booking_reference()
            seats[row][col] = booking_ref  # Mark the seat as reserved
            self.add_to_history(seat_input, f"booked: {booking_ref}, Name: {first_name} {last_name}, Passport: {passport_number}")

            insert_booking(first_name, last_name, passport_number, seat_input[-1], col+1)
            messagebox.showinfo("Seat Booked", f"Seat {col+1}{chr(65+row-1) if lower else chr(65+row)} has been successfully booked. Booking Reference: {booking_ref}")
            self.update_seat_label(row, col)
            form.destroy()

        tk.Button(form, text="Submit", command=submit_details).grid(row=3, column=0, columnspan=2, pady=10)

    def free_seat(self):
        """Free a reserved seat."""
        seat_input = self.seat_input.get().upper()
        if len(seat_input) < 2 or len(seat_input) > 3:
            messagebox.showerror("Invalid Input", "Please enter a valid seat (e.g., 1A, 2B).")
            return

        row = ord(seat_input[-1]) - 65  # Convert column letter to index (A=0, B=1, etc.)
        col = int(seat_input[:-1]) - 1  # Convert row number to 0-based index
        lower = False
        if row >= 3:
            row += 1  # Adjust row for the aisle row
            lower = True

        if row < 0 or row >= len(seats) or col < 0 or col >= len(seats[0]):
            messagebox.showerror("Invalid Seat", "Please enter a valid seat number within the seating range.")
            return

        if seats[row][col] == 'X':
            messagebox.showerror("Aisle Seat", "This seat is an aisle seat and cannot be freed.")
            return

        if seats[row][col] == 'S':
            messagebox.showerror("Storage Seat", "This seat is a storage seat and cannot be freed.")
            return

        if seats[row][col] in used_ref:
            seats[row][col] = 'F'  # Mark the seat as free
            self.add_to_history(seat_input, 'Freed')
            remove_booking(seat_input[-1], col + 1)  # Remove booking from database
            messagebox.showinfo("Seat Freed", f"Seat {col+1}{chr(65+row-1) if lower else chr(65+row)} has been successfully freed.")
            self.update_seat_label(row, col)
        else:
            messagebox.showerror("Seat Not Reserved", "This seat is not reserved!")

    def add_to_history(self, seat_input, action):
        """Add an entry to the reservation history."""
        if seat_input not in self.reservation_history:
            self.reservation_history[seat_input] = []
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.reservation_history[seat_input].append({
            'action': action,
            'timestamp': timestamp,
        })


    def show_history(self):
        """Show reservation history for a seat."""
        history_window = tk.Toplevel(self.root)
        history_window.title("Booking History")

        history_text = tk.Text(history_window, wrap='word', font=('Arial', 12))
        history_text.pack(expand=True, fill='both')

        for seat, history in self.reservation_history.items():
            history_text.insert('end', f"Seat {seat}:\n")
            for entry in history:
                history_text.insert('end', f"  {entry['timestamp']} - {entry['action']}\n")
            history_text.insert('end', "\n")

        history_text.config(state='disabled')

    def show_status(self):
        """Show the status of a selected seat."""
        seat_input = self.seat_input.get().upper()
        if len(seat_input) < 2 or len(seat_input) > 3:
            messagebox.showerror("Invalid Input", "Please enter a valid seat (e.g., 1A, 2B).")
            return  

        row = ord(seat_input[-1]) - 65  # Convert column letter to index (A=0, B=1, etc.)
        col = int(seat_input[:-1]) - 1  # Convert row number to 0-based index
        lower = False
        if row >= 3:
            row += 1  # Adjust row for the aisle row
            lower = True

        if row < 0 or row >= len(seats) or col < 0 or col >= len(seats[0]):
            messagebox.showerror("Invalid Seat", "Please enter a valid seat number within the seating range.")
            return

        seat_status = seats[row][col]
        seat_label = f"Seat {col+1}{chr(65+row-1) if lower else chr(65+row)}"

        if seat_status == 'F':
              messagebox.showinfo("Seat Status", f"{seat_label} is available.")
        elif seat_status == 'R':
            messagebox.showinfo("Seat Status", f"{seat_label} is reserved.")
        elif seat_status == 'X':
            messagebox.showinfo("Seat Status", f"{seat_label} is an aisle seat.")
        elif seat_status == 'S':
            messagebox.showinfo("Seat Status", f"{seat_label} is a storage seat.")

    def update_seat_label(self, row, col):
        """Update the seat label color based on its status."""
        seat = seats[row][col]
        label = self.labels[row][col]
        if seat == 'F':
            label.config(bg='lightgreen')
        elif seat in used_ref:
            label.config(bg='lightcoral')
        elif seat == 'X':
            label.config(bg='gray')
        elif seat == 'S':
            label.config(bg = "yellow")

    def update_all_seats(self):
        """Update all seat labels with their current status."""
        for row in range(7):
            for col in range(20):
                self.update_seat_label(row, col)

    def show_all_bookings(self):
        """Show all bookings in a new window."""
        bookings = fetch_all_bookings()
        if not bookings:
            messagebox.showinfo("No Bookings", "There are no bookings to display.")
            return

        bookings_window = tk.Toplevel(self.root)
        bookings_window.title("All Bookings")

        headers = ["ID", "Booking Reference", "First Name", "Last Name", "Passport Number", "Seat Row", "Seat Column"]
        for col, header in enumerate(headers):
            tk.Label(bookings_window, text=header, font=('Arial', 12, 'bold')).grid(row=0, column=col, padx=5, pady=5)

        for row, booking in enumerate(bookings, start=1):
            for col, value in enumerate(booking):
                tk.Label(bookings_window, text=value, font=('Arial', 12)).grid(row=row, column=col, padx=5, pady=5)


# Connect to a database (it creates the file if it doesn't exist)
conn = sqlite3.connect('booking_system.db')
cursor = conn.cursor()
# Create a table to store customer bookings
cursor.execute('''
    CREATE TABLE IF NOT EXISTS customer_bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        booking_reference TEXT UNIQUE,
        first_name TEXT,
        last_name TEXT,
        passport_number TEXT,
        seat_row TEXT,
        seat_column INTEGER
    )
''')


# Create the Tkinter window
root = tk.Tk()
app = SeatBookingSystem(root)
root.mainloop()