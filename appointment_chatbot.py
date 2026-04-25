#!/usr/bin/env python3
"""
Appointment Booking Chatbot
An option-based chatbot for booking appointments.
"""

import json
from datetime import datetime, timedelta

class AppointmentChatbot:
    def __init__(self):
        self.services = {
            "1": {"name": "General Consultation", "duration": 30, "price": 50},
            "2": {"name": "Specialist Consultation", "duration": 45, "price": 100},
            "3": {"name": "Follow-up Visit", "duration": 20, "price": 30},
            "4": {"name": "Health Checkup", "duration": 60, "price": 150},
        }
        self.appointments = []
        self.current_booking = {}
        
    def display_welcome(self):
        """Display welcome message."""
        print("\n" + "="*50)
        print("  Welcome to Appointment Booking Chatbot")
        print("="*50)
        print("I'll help you book an appointment. Let's get started!\n")
    
    def display_services(self):
        """Display available services."""
        print("\n--- Available Services ---")
        for key, service in self.services.items():
            print(f"{key}. {service['name']} - {service['duration']} mins - ${service['price']}")
        print("0. Exit")
    
    def display_time_slots(self, date_str):
        """Display available time slots for a given date."""
        print(f"\n--- Available Time Slots for {date_str} ---")
        time_slots = ["09:00 AM", "09:30 AM", "10:00 AM", "10:30 AM", 
                      "11:00 AM", "11:30 AM", "02:00 PM", "02:30 PM",
                      "03:00 PM", "03:30 PM", "04:00 PM", "04:30 PM"]
        
        for i, slot in enumerate(time_slots, 1):
            print(f"{i}. {slot}")
        print("0. Go Back")
        return time_slots
    
    def get_user_choice(self, options_count):
        """Get user's choice from available options."""
        while True:
            try:
                choice = input("\nEnter your choice: ").strip()
                if choice.isdigit() and 0 <= int(choice) <= options_count:
                    return choice
                else:
                    print(f"Invalid choice. Please enter a number between 0 and {options_count}.")
            except KeyboardInterrupt:
                print("\n\nBooking cancelled.")
                return "0"
    
    def select_service(self):
        """Let user select a service."""
        self.display_services()
        choice = self.get_user_choice(len(self.services))
        
        if choice == "0":
            return False
        
        self.current_booking['service'] = self.services[choice]
        self.current_booking['service_id'] = choice
        print(f"\n✓ Selected: {self.current_booking['service']['name']}")
        return True
    
    def select_date(self):
        """Let user select a date."""
        print("\n--- Select Date ---")
        today = datetime.now()
        
        for i in range(7):
            date = today + timedelta(days=i)
            date_str = date.strftime("%Y-%m-%d")
            day_name = date.strftime("%A")
            print(f"{i+1}. {date_str} ({day_name})")
        print("0. Go Back")
        
        choice = self.get_user_choice(7)
        
        if choice == "0":
            return False
        
        selected_date = today + timedelta(days=int(choice)-1)
        self.current_booking['date'] = selected_date.strftime("%Y-%m-%d")
        self.current_booking['day'] = selected_date.strftime("%A")
        print(f"\n✓ Selected Date: {self.current_booking['date']} ({self.current_booking['day']})")
        return True
    
    def select_time(self):
        """Let user select a time slot."""
        time_slots = self.display_time_slots(self.current_booking['date'])
        choice = self.get_user_choice(len(time_slots))
        
        if choice == "0":
            return False
        
        self.current_booking['time'] = time_slots[int(choice)-1]
        print(f"\n✓ Selected Time: {self.current_booking['time']}")
        return True
    
    def enter_patient_details(self):
        """Collect patient details."""
        print("\n--- Patient Details ---")
        
        while True:
            name = input("Enter your full name: ").strip()
            if name:
                break
            print("Name cannot be empty.")
        
        while True:
            phone = input("Enter your phone number: ").strip()
            if phone and len(phone) >= 10:
                break
            print("Please enter a valid phone number (at least 10 digits).")
        
        email = input("Enter your email (optional): ").strip()
        
        self.current_booking['patient'] = {
            'name': name,
            'phone': phone,
            'email': email if email else None
        }
        
        print(f"\n✓ Patient: {name}")
        return True
    
    def confirm_booking(self):
        """Display booking summary and confirm."""
        print("\n" + "="*50)
        print("  Booking Summary")
        print("="*50)
        print(f"Service: {self.current_booking['service']['name']}")
        print(f"Duration: {self.current_booking['service']['duration']} minutes")
        print(f"Price: ${self.current_booking['service']['price']}")
        print(f"Date: {self.current_booking['date']} ({self.current_booking['day']})")
        print(f"Time: {self.current_booking['time']}")
        print(f"Patient: {self.current_booking['patient']['name']}")
        print(f"Phone: {self.current_booking['patient']['phone']}")
        if self.current_booking['patient']['email']:
            print(f"Email: {self.current_booking['patient']['email']}")
        print("="*50)
        
        while True:
            confirm = input("\nConfirm booking? (yes/no): ").strip().lower()
            if confirm in ['yes', 'y']:
                return True
            elif confirm in ['no', 'n']:
                return False
            print("Please enter 'yes' or 'no'.")
    
    def save_booking(self):
        """Save the booking."""
        booking_id = f"APT{len(self.appointments) + 1:04d}"
        self.current_booking['booking_id'] = booking_id
        self.current_booking['status'] = 'Confirmed'
        self.current_booking['created_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        self.appointments.append(self.current_booking.copy())
        
        print("\n" + "="*50)
        print("  ✓ Booking Confirmed!")
        print("="*50)
        print(f"Booking ID: {booking_id}")
        print(f"A confirmation SMS will be sent to {self.current_booking['patient']['phone']}")
        if self.current_booking['patient']['email']:
            print(f"A confirmation email will be sent to {self.current_booking['patient']['email']}")
        print("="*50)
    
    def book_appointment(self):
        """Complete booking flow."""
        self.current_booking = {}
        
        steps = [
            ("service", self.select_service),
            ("date", self.select_date),
            ("time", self.select_time),
            ("details", self.enter_patient_details),
        ]
        
        for step_name, step_func in steps:
            if not step_func():
                print("\nBooking cancelled.")
                return
        
        if self.confirm_booking():
            self.save_booking()
        else:
            print("\nBooking cancelled.")
    
    def view_appointments(self):
        """View all appointments."""
        if not self.appointments:
            print("\nNo appointments booked yet.")
            return
        
        print("\n" + "="*50)
        print("  All Appointments")
        print("="*50)
        
        for apt in self.appointments:
            print(f"\nBooking ID: {apt['booking_id']}")
            print(f"Service: {apt['service']['name']}")
            print(f"Date: {apt['date']} ({apt['day']}) at {apt['time']}")
            print(f"Patient: {apt['patient']['name']}")
            print(f"Status: {apt['status']}")
            print("-"*30)
    
    def display_main_menu(self):
        """Display main menu."""
        print("\n--- Main Menu ---")
        print("1. Book New Appointment")
        print("2. View All Appointments")
        print("3. Exit")
    
    def run(self):
        """Run the chatbot."""
        self.display_welcome()
        
        while True:
            self.display_main_menu()
            choice = self.get_user_choice(3)
            
            if choice == "1":
                self.book_appointment()
            elif choice == "2":
                self.view_appointments()
            elif choice == "3":
                print("\nThank you for using Appointment Booking Chatbot!")
                print("Have a great day! 👋\n")
                break


if __name__ == "__main__":
    chatbot = AppointmentChatbot()
    try:
        chatbot.run()
    except KeyboardInterrupt:
        print("\n\nChatbot terminated. Goodbye!")
