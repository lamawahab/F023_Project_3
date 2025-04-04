import tkinter as tk
from tkinter import messagebox
import datetime

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
        if len(seat_input) <2 or len(seat_input) > 3:
            messagebox.showerror("Invalid Input", "Please enter a valid seat (e.g., 1A, 2B).")
            return

        row = ord(seat_input[-1]) - 65  # Convert column letter to index (A=0, B=1, etc.)
        col = int(seat_input[:-1]) - 1  # Convert row number to 0-based index
        lower = False
        if (row >= 3):
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
            seats[row][col] = 'R'  # Mark the seat as reserved
            self.add_to_history(seat_input, 'Booked')
            messagebox.showinfo("Seat Booked", f"Seat {col+1}{chr(65+row- 1) if lower else chr(65+row)} has been successfully booked.")
            self.update_seat_label(row, col)
        else:
            messagebox.showerror("Seat Occupied", "This seat is already reserved!")

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

        if seats[row][col] == 'R':
            seats[row][col] = 'F'  # Mark the seat as free
            self.add_to_history(seat_input, 'Freed')
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
        seat_input = self.seat_input.get().upper()
        if seat_input in self.reservation_history:
            history = self.reservation_history[seat_input]
            history_str = "\n".join([f"{entry['timestamp']} - {entry['action']}" for entry in history])
            messagebox.showinfo(f"Reservation History for Seat {seat_input}", history_str)
        else:
            messagebox.showinfo("No History", f"No history available for Seat {seat_input}")
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
        elif seat == 'R':
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

# Create the Tkinter window
root = tk.Tk()
app = SeatBookingSystem(root)
root.mainloop()
