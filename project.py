import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
from datetime import datetime

class SioplexParkingSystem:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sioplex Parking Service")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2c3e50')
        
        # Initialize
        self.admin_password = self.load_admin_password()
        self.parking_data = self.load_parking_data()
        self.exit_history = self.load_exit_history()
        self.total_revenue = self.load_revenue()
        self.blacklisted_vehicles = self.load_blacklisted_vehicles()
        
        # Parking lot
        self.parking_lot = {
            'car': {'total_slots': 50, 'price_per_hour': 30, 'emergency_slots': 5},
            'bike': {'total_slots': 100, 'price_per_hour': 15, 'emergency_slots': 10},
            'truck': {'total_slots': 20, 'price_per_hour': 60, 'emergency_slots': 2},
            'bus': {'total_slots': 15, 'price_per_hour': 80, 'emergency_slots': 2}
        }
        
        self.initialize_parking_slots()
        self.show_login_page()
        
    def initialize_parking_slots(self):
        for vehicle_type in self.parking_lot:
            if vehicle_type not in self.parking_data:
                self.parking_data[vehicle_type] = {
                    'occupied_slots': {},
                    'available_slots': list(range(1, self.parking_lot[vehicle_type]['total_slots'] + 1))
                }
    
    def show_login_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Company
        header_frame = tk.Frame(main_frame, bg='#34495e', relief='raised', bd=2)
        header_frame.pack(fill='x', pady=(0, 20))
        
        title_label = tk.Label(header_frame, text="SIOPLEX PARKING SERVICE", 
                              font=('Arial', 24, 'bold'), fg='#ecf0f1', bg='#34495e')
        title_label.pack(pady=20)
        
        subtitle_label = tk.Label(header_frame, text="Professional Vehicle Management Solutions", 
                                 font=('Arial', 12), fg='#bdc3c7', bg='#34495e')
        subtitle_label.pack(pady=(0, 20))
        
        # Company details and services
        details_frame = tk.Frame(main_frame, bg='#34495e', relief='sunken', bd=2)
        details_frame.pack(fill='x', pady=(0, 20))
        
        # columns
        left_frame = tk.Frame(details_frame, bg='#34495e')
        left_frame.pack(side='left', fill='both', expand=True, padx=30, pady=20)
        
        # Separator line
        separator = tk.Frame(details_frame, bg='#95a5a6', width=2)
        separator.pack(side='left', fill='y', padx=10)
        
        right_frame = tk.Frame(details_frame, bg='#34495e')
        right_frame.pack(side='right', fill='both', expand=True, padx=30, pady=20)
        
        # Company
        company_text = """🏢 Company Information:
• Established: 2024
• Location: Prime Business District
• Contact: +1-555-SIOPLEX
• Email: info@sioplex.com
• Website: www.sioplex.com"""
        
        company_label = tk.Label(left_frame, text=company_text, 
                                font=('Arial', 10), fg='#ecf0f1', bg='#34495e', 
                                justify='left', anchor='w')
        company_label.pack(anchor='w')
        
        # Services
        services_text = """🚗 Services Offered:
• Car Parking (₹30/hour)
• Bike Parking (₹15/hour) 
• Truck Parking (₹60/hour)
• Bus Parking (₹80/hour)
• 24/7 Security
• CCTV Surveillance
• Emergency Vehicle Priority
• Digital Receipt System"""
        
        services_label = tk.Label(right_frame, text=services_text, 
                                 font=('Arial', 10), fg='#ecf0f1', bg='#34495e', 
                                 justify='left', anchor='w')
        services_label.pack(anchor='w', padx=(20, 0))
        
        # Login 
        login_frame = tk.Frame(main_frame, bg='#34495e', relief='raised', bd=2)
        login_frame.pack(pady=20)
        
        login_label = tk.Label(login_frame, text="ADMIN LOGIN", 
                              font=('Arial', 16, 'bold'), fg='#ecf0f1', bg='#34495e')
        login_label.pack(pady=20)
        
        # Username
        username_frame = tk.Frame(login_frame, bg='#34495e')
        username_frame.pack(pady=10)
        
        username_label = tk.Label(username_frame, text="Username:", 
                                 font=('Arial', 12), fg='#ecf0f1', bg='#34495e')
        username_label.pack(side='left', padx=(0, 10))
        
        self.username_entry = tk.Entry(username_frame, font=('Arial', 12), width=20)
        self.username_entry.pack(side='left', padx=(0, 20))
        
        # Password
        password_frame = tk.Frame(login_frame, bg='#34495e')
        password_frame.pack(pady=10)
        
        password_label = tk.Label(password_frame, text="Password:", 
                                 font=('Arial', 12), fg='#ecf0f1', bg='#34495e')
        password_label.pack(side='left', padx=(0, 10))
        
        self.password_entry = tk.Entry(password_frame, font=('Arial', 12), width=20, show="*")
        self.password_entry.pack(side='left', padx=(0, 20))
        
        # Login 
        login_button = tk.Button(login_frame, text="LOGIN", 
                                font=('Arial', 12, 'bold'), bg='#27ae60', fg='white',
                                command=self.authenticate_login, width=15, height=2)
        login_button.pack(pady=20)
        
        footer_label = tk.Label(main_frame, text="© 2024 Sioplex Parking Service. All rights reserved.", 
                               font=('Arial', 8), fg='#95a5a6', bg='#2c3e50')
        footer_label.pack(side='bottom', pady=10)
    
    def authenticate_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if username == "admin" and password == self.admin_password:
            messagebox.showinfo("Success", "Login successful! Welcome to Sioplex Parking Service.")
            self.show_main_menu()
        else:
            messagebox.showerror("Error", "Invalid username or password!")
    
    def show_main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        header_frame = tk.Frame(main_frame, bg='#34495e', relief='raised', bd=2)
        header_frame.pack(fill='x', pady=(0, 20))
        
        title_label = tk.Label(header_frame, text="SIOPLEX PARKING SERVICE - ADMIN PANEL", 
                              font=('Arial', 20, 'bold'), fg='#ecf0f1', bg='#34495e')
        title_label.pack(pady=15)

        menu_frame = tk.Frame(main_frame, bg='#2c3e50')
        menu_frame.pack(expand=True, fill='both')
        
        # menu
        buttons = [
            ("🚗 PARK VEHICLE", self.park_vehicle, '#3498db'),
            ("🚪 REMOVE VEHICLE", self.remove_vehicle, '#e74c3c'),
            ("📊 SHOW PARKING STATUS", self.show_parking_status, '#f39c12'),
            ("🔍 SEARCH VEHICLE", self.search_vehicle, '#9b59b6'),
            ("💰 SHOW TOTAL REVENUE", self.show_total_revenue, '#27ae60'),
            ("📋 SHOW EXIT HISTORY", self.show_exit_history, '#1abc9c'),
            ("🚫 BLACKLIST VEHICLE", self.blacklist_vehicle, '#e74c3c'),
            ("📋 VIEW BLACKLIST", self.view_blacklist, '#8e44ad'),
            ("🔐 CHANGE ADMIN PASSWORD", self.change_admin_password, '#e67e22'),
            ("🔄 RESET SYSTEM", self.reset_system, '#95a5a6'),
            ("❌ EXIT", self.exit_system, '#c0392b')
        ]
        
        # grid of buttons
        for i, (text, command, color) in enumerate(buttons):
            row = i // 4
            col = i % 4
            
            button = tk.Button(menu_frame, text=text, font=('Arial', 11, 'bold'),
                              bg=color, fg='white', command=command,
                              width=18, height=3, relief='raised', bd=3)
            button.grid(row=row, column=col, padx=8, pady=8, sticky='nsew')
        
        for i in range(3):
            menu_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            menu_frame.grid_columnconfigure(i, weight=1)
    
    def park_vehicle(self):
        park_window = tk.Toplevel(self.root)
        park_window.title("Park Vehicle - Sioplex Parking Service")
        park_window.geometry("800x700")
        park_window.configure(bg='#2c3e50')

        main_frame = tk.Frame(park_window, bg='#2c3e50')
        main_frame.pack(expand=True, fill='both', padx=30, pady=30)
        
        title_label = tk.Label(main_frame, text="PARK VEHICLE", 
                              font=('Arial', 20, 'bold'), fg='#ecf0f1', bg='#2c3e50')
        title_label.pack(pady=(0, 30))
        
        # columns
        content_frame = tk.Frame(main_frame, bg='#2c3e50')
        content_frame.pack(expand=True, fill='both')
        
        # Left-Vehicle Details
        left_frame = tk.Frame(content_frame, bg='#2c3e50')
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 15))
        
        vehicle_frame = tk.Frame(left_frame, bg='#34495e', relief='raised', bd=2)
        vehicle_frame.pack(fill='x', pady=(0, 20))
        
        vehicle_title = tk.Label(vehicle_frame, text="VEHICLE DETAILS", 
                                font=('Arial', 14, 'bold'), fg='#ecf0f1', bg='#34495e')
        vehicle_title.pack(pady=15)
        
        type_frame = tk.Frame(vehicle_frame, bg='#34495e')
        type_frame.pack(pady=10)
        
        tk.Label(type_frame, text="Vehicle Type:", font=('Arial', 12), 
                fg='#ecf0f1', bg='#34495e').pack(side='left', padx=(0, 10))
        
        vehicle_type = tk.StringVar(value="car")
        type_combo = ttk.Combobox(type_frame, textvariable=vehicle_type, 
                                 values=["car", "bike", "truck", "bus"], 
                                 state="readonly", width=15)
        type_combo.pack(side='left')
        
        number_frame = tk.Frame(vehicle_frame, bg='#34495e')
        number_frame.pack(pady=10)
        
        tk.Label(number_frame, text="Vehicle Number:", font=('Arial', 12), 
                fg='#ecf0f1', bg='#34495e').pack(side='left', padx=(0, 10))
        
        vehicle_number = tk.Entry(number_frame, font=('Arial', 12), width=20)
        vehicle_number.pack(side='left')
        
        # Customer details
        customer_frame = tk.Frame(vehicle_frame, bg='#34495e')
        customer_frame.pack(pady=10)
        
        tk.Label(customer_frame, text="Customer Name:", font=('Arial', 12), 
                fg='#ecf0f1', bg='#34495e').pack(side='left', padx=(0, 10))
        
        customer_name = tk.Entry(customer_frame, font=('Arial', 12), width=20)
        customer_name.pack(side='left')
        
        # Phone number
        phone_frame = tk.Frame(vehicle_frame, bg='#34495e')
        phone_frame.pack(pady=10)
        
        tk.Label(phone_frame, text="Phone Number:", font=('Arial', 12), 
                fg='#ecf0f1', bg='#34495e').pack(side='left', padx=(0, 10))
        
        phone_number = tk.Entry(phone_frame, font=('Arial', 12), width=20)
        phone_number.pack(side='left')
        
        # Emergency vehicle checkbox
        emergency_frame = tk.Frame(vehicle_frame, bg='#34495e')
        emergency_frame.pack(pady=10)
        
        emergency_var = tk.BooleanVar()
        emergency_check = tk.Checkbutton(emergency_frame, text="Emergency Vehicle", 
                                        variable=emergency_var, font=('Arial', 12),
                                        fg='#ecf0f1', bg='#34495e', selectcolor='#e74c3c')
        emergency_check.pack()
        
        # Right - Services
        right_frame = tk.Frame(content_frame, bg='#2c3e50')
        right_frame.pack(side='right', fill='both', expand=True, padx=(15, 0))
        
        services_frame = tk.Frame(right_frame, bg='#34495e', relief='raised', bd=2)
        services_frame.pack(fill='both', expand=True)
        
        services_title = tk.Label(services_frame, text="SERVICES INCLUDED", 
                                 font=('Arial', 14, 'bold'), fg='#ecf0f1', bg='#34495e')
        services_title.pack(pady=15)
        
        services_list = [
            ("🚗 Car Parking", "₹30/hour"),
            ("🏍️ Bike Parking", "₹15/hour"),
            ("🚛 Truck Parking", "₹60/hour"),
            ("🚌 Bus Parking", "₹80/hour"),
            ("🛡️ 24/7 Security", "Included"),
            ("📹 CCTV Surveillance", "Included"),
            ("🚨 Emergency Vehicle Priority", "Included"),
            ("🧾 Digital Receipt System", "Included")
        ]
        
        for service, price in services_list:
            service_frame = tk.Frame(services_frame, bg='#34495e')
            service_frame.pack(fill='x', padx=20, pady=5)
            
            service_label = tk.Label(service_frame, text=service, 
                                    font=('Arial', 11), fg='#ecf0f1', bg='#34495e')
            service_label.pack(side='left')
            
            price_label = tk.Label(service_frame, text=price, 
                                  font=('Arial', 11, 'bold'), fg='#27ae60', bg='#34495e')
            price_label.pack(side='right')
        
        info_frame = tk.Frame(services_frame, bg='#34495e')
        info_frame.pack(fill='x', padx=20, pady=15)
        
        info_text = """ℹ️ All services are automatically included
   with your parking ticket. No additional
   charges for security and surveillance."""
        
        info_label = tk.Label(info_frame, text=info_text, 
                             font=('Arial', 10), fg='#bdc3c7', bg='#34495e',
                             justify='left', anchor='w')
        info_label.pack(anchor='w')
        
        def park_vehicle_action():
            v_type = vehicle_type.get()
            v_number = vehicle_number.get().strip().upper()
            c_name = customer_name.get().strip()
            c_phone = phone_number.get().strip()
            is_emergency = emergency_var.get()
            
            if not all([v_number, c_name, c_phone]):
                messagebox.showerror("Error", "Please fill all fields!")
                return
            
            # blacklisted check
            if self.check_blacklist(v_number):
                blacklist_info = self.get_blacklist_info(v_number)
                police_msg = " (POLICE REPORTED)" if blacklist_info['report_to_police'] else ""
                
                blacklist_warning = f"""🚫 VEHICLE BLACKLISTED!

Vehicle Number: {v_number}
Owner: {blacklist_info['owner_name']}
Address: {blacklist_info['address']}
Reason: {blacklist_info['reason']}{police_msg}
Date Added: {blacklist_info['date_added']}

This vehicle is not allowed to park in our facility.
Please contact security immediately."""
                
                messagebox.showerror("BLACKLISTED VEHICLE", blacklist_warning)
                return
            
            # already parked check
            for vt in self.parking_data:
                if v_number in self.parking_data[vt]['occupied_slots']:
                    messagebox.showerror("Error", f"Vehicle {v_number} is already parked!")
                    return
            
            available_slots = self.parking_data[v_type]['available_slots']
            if not available_slots:
                messagebox.showerror("Error", f"No available slots for {v_type}!")
                return
        
            if is_emergency:
                emergency_slots = list(range(
                    self.parking_lot[v_type]['total_slots'] - self.parking_lot[v_type]['emergency_slots'] + 1,
                    self.parking_lot[v_type]['total_slots'] + 1
                ))
                available_emergency = [s for s in emergency_slots if s in available_slots]
                if available_emergency:
                    slot = available_emergency[0]
                else:
                    slot = available_slots[0]
            else:
                regular_slots = [s for s in available_slots if s <= 
                               self.parking_lot[v_type]['total_slots'] - self.parking_lot[v_type]['emergency_slots']]
                if regular_slots:
                    slot = regular_slots[0]
                else:
                    slot = available_slots[0]
            
            entry_time = datetime.now()
            self.parking_data[v_type]['occupied_slots'][v_number] = {
                'slot': slot,
                'customer_name': c_name,
                'phone': c_phone,
                'entry_time': entry_time.strftime('%Y-%m-%d %H:%M:%S'),
                'is_emergency': is_emergency
            }
            
            self.parking_data[v_type]['available_slots'].remove(slot)
            
            self.save_parking_data()
            
            success_message = f"""Vehicle parked successfully!

Vehicle Details:
• Vehicle: {v_number}
• Type: {v_type.upper()}
• Slot: {slot}
• Entry Time: {entry_time.strftime('%Y-%m-%d %H:%M:%S')}

Services Included:
• 24/7 Security
• CCTV Surveillance
• Emergency Vehicle Priority
• Digital Receipt System

Rate: ₹{self.parking_lot[v_type]['price_per_hour']}/hour"""
            
            messagebox.showinfo("Success", success_message)
            
            # Show customer receipt
            self.show_customer_receipt(v_number, c_name, c_phone, v_type, slot, entry_time)
            
            park_window.destroy()
        
        park_button = tk.Button(main_frame, text="PARK VEHICLE", 
                               font=('Arial', 16, 'bold'), bg='#27ae60', fg='white',
                               command=park_vehicle_action, width=25, height=2)
        park_button.pack(pady=30)
    
    def remove_vehicle(self):
        remove_window = tk.Toplevel(self.root)
        remove_window.title("Remove Vehicle - Sioplex Parking Service")
        remove_window.geometry("500x300")
        remove_window.configure(bg='#2c3e50')
        
        main_frame = tk.Frame(remove_window, bg='#2c3e50')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        title_label = tk.Label(main_frame, text="REMOVE VEHICLE", 
                              font=('Arial', 18, 'bold'), fg='#ecf0f1', bg='#2c3e50')
        title_label.pack(pady=(0, 20))
        
        input_frame = tk.Frame(main_frame, bg='#34495e', relief='raised', bd=2)
        input_frame.pack(fill='x', pady=(0, 20))
    
        number_frame = tk.Frame(input_frame, bg='#34495e')
        number_frame.pack(pady=20)
        
        tk.Label(number_frame, text="Vehicle Number:", font=('Arial', 12), 
                fg='#ecf0f1', bg='#34495e').pack(side='left', padx=(0, 10))
        
        vehicle_number = tk.Entry(number_frame, font=('Arial', 12), width=20)
        vehicle_number.pack(side='left')
        
        def remove_vehicle_action():
            v_number = vehicle_number.get().strip().upper()
            
            if not v_number:
                messagebox.showerror("Error", "Please enter vehicle number!")
                return
            
            found_vehicle = None
            vehicle_type = None
            
            for vt in self.parking_data:
                if v_number in self.parking_data[vt]['occupied_slots']:
                    found_vehicle = self.parking_data[vt]['occupied_slots'][v_number]
                    vehicle_type = vt
                    break
            
            if not found_vehicle:
                messagebox.showerror("Error", f"Vehicle {v_number} not found in parking!")
                return
            
            entry_time = datetime.strptime(found_vehicle['entry_time'], '%Y-%m-%d %H:%M:%S')
            exit_time = datetime.now()
            duration = exit_time - entry_time
            hours = max(1, duration.total_seconds() / 3600)  # Minimum 1 hour
            
            price_per_hour = self.parking_lot[vehicle_type]['price_per_hour']
            total_fee = hours * price_per_hour
            
            receipt = self.generate_receipt(v_number, found_vehicle, vehicle_type, 
                                          entry_time, exit_time, hours, total_fee)
            
            slot = found_vehicle['slot']
            self.parking_data[vehicle_type]['occupied_slots'].pop(v_number)
            self.parking_data[vehicle_type]['available_slots'].append(slot)
            self.parking_data[vehicle_type]['available_slots'].sort()
 
            self.total_revenue += total_fee

            exit_record = {
                'vehicle_number': v_number,
                'vehicle_type': vehicle_type,
                'customer_name': found_vehicle['customer_name'],
                'phone': found_vehicle['phone'],
                'slot': slot,
                'entry_time': found_vehicle['entry_time'],
                'exit_time': exit_time.strftime('%Y-%m-%d %H:%M:%S'),
                'duration_hours': round(hours, 2),
                'total_fee': total_fee,
                'is_emergency': found_vehicle['is_emergency']
            }
            self.exit_history.append(exit_record)
         
            self.save_parking_data()
            self.save_exit_history()
            self.save_revenue()
          
            self.show_receipt(receipt)
            
            remove_window.destroy()
    
        remove_button = tk.Button(main_frame, text="REMOVE VEHICLE", 
                                 font=('Arial', 14, 'bold'), bg='#e74c3c', fg='white',
                                 command=remove_vehicle_action, width=20, height=2)
        remove_button.pack(pady=20)
    
    def generate_receipt(self, vehicle_number, vehicle_data, vehicle_type, 
                        entry_time, exit_time, hours, total_fee):
        receipt = f"""
╔══════════════════════════════════════════════════════════════╗
║                    SIOPLEX PARKING SERVICE                   ║
║                    Professional Vehicle Management           ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  RECEIPT NO: {datetime.now().strftime('%Y%m%d%H%M%S')}       ║
║  DATE: {exit_time.strftime('%d/%m/%Y')}                      ║
║  TIME: {exit_time.strftime('%H:%M:%S')}                      ║
║                                                              ║
╠══════════════════════════════════════════════════════════════╣
║  VEHICLE DETAILS:                                            ║
║    Vehicle Number: {vehicle_number:<40}                      ║
║    Vehicle Type: {vehicle_type.upper():<40}                  ║
║    Slot Number: {vehicle_data['slot']:<40}                   ║
║                                                              ║
╠══════════════════════════════════════════════════════════════╣
║  CUSTOMER DETAILS:                                           ║
║    Name: {vehicle_data['customer_name']:<40}                 ║
║    Phone: {vehicle_data['phone']:<40}                        ║
║                                                              ║
╠══════════════════════════════════════════════════════════════╣
║  PARKING DETAILS:                                            ║
║    Entry Time: {entry_time.strftime('%d/%m/%Y %H:%M:%S')}    ║
║    Exit Time: {exit_time.strftime('%d/%m/%Y %H:%M:%S')}      ║
║    Duration: {hours:.2f} hours                               ║
║    Rate: ₹{self.parking_lot[vehicle_type]['price_per_hour']}/hour║
║                                                              ║
╠══════════════════════════════════════════════════════════════╣
║  PAYMENT:                                                    ║
║    Total Amount: ₹{total_fee:.2f}                            ║
║                                                              ║
╠══════════════════════════════════════════════════════════════╣
║  COMPANY DETAILS:                                            ║
║    Sioplex Parking Service                                   ║
║    Prime Business District                                   ║
║    Contact: +1-555-SIOPLEX                                   ║
║    Email: info@sioplex.com                                   ║
║    Website: www.sioplex.com                                  ║
║                                                              ║
║  Thank you for choosing Sioplex Parking Service!             ║
║  Please visit again!                                         ║
╚══════════════════════════════════════════════════════════════╝
        """
        return receipt
    
    def show_receipt(self, receipt):
        """Display receipt in a new window"""
        receipt_window = tk.Toplevel(self.root)
        receipt_window.title("Parking Receipt - Sioplex Parking Service")
        receipt_window.geometry("700x800")
        receipt_window.configure(bg='#2c3e50')
   
        main_frame = tk.Frame(receipt_window, bg='#2c3e50')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
       
        receipt_text = tk.Text(main_frame, font=('Courier', 10), bg='#ecf0f1', 
                              fg='#2c3e50', wrap='word', height=35, width=80)
        receipt_text.pack(expand=True, fill='both')
        receipt_text.insert('1.0', receipt)
        receipt_text.config(state='disabled')
     
        print_button = tk.Button(main_frame, text="PRINT RECEIPT", 
                                font=('Arial', 12, 'bold'), bg='#3498db', fg='white',
                                command=lambda: self.print_receipt(receipt), width=20, height=2)
        print_button.pack(pady=20)
    
    def print_receipt(self, receipt):
        """Save receipt to file"""
        filename = f"receipt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, 'w') as f:
            f.write(receipt)
        messagebox.showinfo("Success", f"Receipt saved as {filename}")
    
    def show_customer_receipt(self, vehicle_number, customer_name, phone_number, vehicle_type, slot, entry_time):
        """Show customer receipt for parking entry"""
        receipt_window = tk.Toplevel(self.root)
        receipt_window.title("Customer Receipt - Sioplex Parking Service")
        receipt_window.geometry("500x700")
        receipt_window.configure(bg='#2c3e50')
        
        main_frame = tk.Frame(receipt_window, bg='#2c3e50')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Receipt content
        receipt_text = f"""
╔══════════════════════════════════════════════════════════════╗
║                    SIOPLEX PARKING SERVICE                   ║
║                    Customer Parking Receipt                  ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  RECEIPT NO: {datetime.now().strftime('%Y%m%d%H%M%S')}       ║
║  DATE: {entry_time.strftime('%d/%m/%Y')}                     ║
║  TIME: {entry_time.strftime('%H:%M:%S')}                     ║
║                                                              ║
╠══════════════════════════════════════════════════════════════╣
║  VEHICLE DETAILS:                                            ║
║    Vehicle Number: {vehicle_number:<40}                      ║
║    Vehicle Type: {vehicle_type.upper():<40}                  ║
║    Parking Slot: {slot:<40}                                  ║
║                                                              ║
╠══════════════════════════════════════════════════════════════╣
║  CUSTOMER DETAILS:                                           ║
║    Name: {customer_name:<40}                                 ║
║    Phone: {phone_number:<40}                                 ║
║                                                              ║
╠══════════════════════════════════════════════════════════════╣
║  PARKING DETAILS:                                            ║
║    Entry Time: {entry_time.strftime('%d/%m/%Y %H:%M:%S')}    ║
║    Rate: ₹{self.parking_lot[vehicle_type]['price_per_hour']}/hour║
║                                                              ║
╠══════════════════════════════════════════════════════════════╣
║  COMPANY DETAILS:                                            ║
║    Sioplex Parking Service                                   ║
║    Prime Business District                                   ║
║    Contact: +1-555-SIOPLEX                                   ║
║    Email: info@sioplex.com                                   ║
║    Website: www.sioplex.com                                  ║
║                                                              ║
╠══════════════════════════════════════════════════════════════╣
║  IMPORTANT:                                                  ║
║    • Keep this receipt safe                                  ║
║    • Present this receipt when removing vehicle              ║
║    • Receipt number required for exit                        ║
║    • 24/7 Security & CCTV Surveillance included              ║
║                                                              ║
║  Thank you for choosing Sioplex Parking Service!             ║
║  Please visit again!                                         ║
╚══════════════════════════════════════════════════════════════╝
        """
        
        # Receipt display
        receipt_display = tk.Text(main_frame, font=('Courier', 10), bg='#ecf0f1', 
                                 fg='#2c3e50', wrap='word', height=30, width=60)
        receipt_display.pack(expand=True, fill='both', padx=10, pady=10)
        receipt_display.insert('1.0', receipt_text)
        receipt_display.config(state='disabled')
        
        # Button frame
        button_frame = tk.Frame(main_frame, bg='#2c3e50')
        button_frame.pack(pady=20)
        
        # Print button
        def print_receipt_action():
            messagebox.showinfo("Print Service", "Print service is currently unavailable.\nPlease contact the administrator.")
        
        print_button = tk.Button(button_frame, text="PRINT RECEIPT", 
                                font=('Arial', 12, 'bold'), bg='#3498db', fg='white',
                                command=print_receipt_action, width=20, height=2)
        print_button.pack(side='left', padx=(0, 10))
        
        # Close button
        close_button = tk.Button(button_frame, text="CLOSE", 
                                font=('Arial', 12, 'bold'), bg='#95a5a6', fg='white',
                                command=receipt_window.destroy, width=15, height=2)
        close_button.pack(side='left', padx=(10, 0))
    
    def show_parking_status(self):

        status_window = tk.Toplevel(self.root)
        status_window.title("Parking Status - Sioplex Parking Service")
        status_window.geometry("1800x1000")
        status_window.configure(bg='#2c3e50')
       
        main_frame = tk.Frame(status_window, bg='#2c3e50')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        title_label = tk.Label(main_frame, text="PARKING STATUS", 
                              font=('Arial', 18, 'bold'), fg='#ecf0f1', bg='#2c3e50')
        title_label.pack(pady=(0, 20))
     
        notebook = ttk.Notebook(main_frame)
        notebook.pack(expand=True, fill='both')
        
        for vehicle_type in self.parking_lot:
          
            frame = tk.Frame(notebook, bg='#34495e')
            notebook.add(frame, text=vehicle_type.upper())
            
            type_header = tk.Label(frame, text=f"{vehicle_type.upper()} PARKING LOT", 
                                  font=('Arial', 16, 'bold'), fg='#ecf0f1', bg='#34495e')
            type_header.pack(pady=10)
            
            total_slots = self.parking_lot[vehicle_type]['total_slots']
            occupied_slots = len(self.parking_data[vehicle_type]['occupied_slots'])
            available_slots = len(self.parking_data[vehicle_type]['available_slots'])
            emergency_slots = self.parking_lot[vehicle_type]['emergency_slots']
            
            stats_text = f"Total Slots: {total_slots} | Occupied: {occupied_slots} | Available: {available_slots} | Emergency Slots: {emergency_slots}"
            stats_label = tk.Label(frame, text=stats_text, font=('Arial', 12), 
                                  fg='#ecf0f1', bg='#34495e')
            stats_label.pack(pady=5)
            
            canvas_frame = tk.Frame(frame, bg='#34495e')
            canvas_frame.pack(expand=True, fill='both', padx=2, pady=2)
            
            canvas = tk.Canvas(canvas_frame, bg='#34495e', highlightthickness=0, width=1700, height=700)
            v_scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview, 
                                      bg='#95a5a6', troughcolor='#34495e', width=16)
            h_scrollbar = tk.Scrollbar(canvas_frame, orient="horizontal", command=canvas.xview,
                                      bg='#95a5a6', troughcolor='#34495e', width=16)
          
            canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
            
            parking_frame = tk.Frame(canvas, bg='#34495e')
            window_id = canvas.create_window((0, 0), window=parking_frame, anchor="nw")
            
            def on_canvas_configure(event):
                canvas.configure(scrollregion=canvas.bbox("all"))
                canvas.itemconfig(window_id, width=event.width)
            
            canvas.bind('<Configure>', on_canvas_configure)
            
            cols = 30 
            rows = (total_slots + cols - 1) // cols
            
            for i in range(total_slots):
                row = i // cols
                col = i % cols
                
                slot_num = i + 1
                is_occupied = slot_num not in self.parking_data[vehicle_type]['available_slots']
                is_emergency = slot_num > (total_slots - emergency_slots)
                
                if is_occupied:
                    color = '#e74c3c'  # Red for occupied
                elif is_emergency:
                    color = '#f39c12'  # Orange for emergency
                else:
                    color = '#27ae60'  # Green for available
                
                # Create slot button
                slot_button = tk.Button(parking_frame, text=f"{slot_num}", 
                                       font=('Arial', 9, 'bold'), bg=color, fg='white',
                                       width=6, height=3, relief='raised', bd=2)
                slot_button.grid(row=row, column=col, padx=2, pady=2, sticky='nsew')
                
                # overwrite for occupied slots
                if is_occupied:
                    for v_num, v_data in self.parking_data[vehicle_type]['occupied_slots'].items():
                        if v_data['slot'] == slot_num:
                            tooltip_text = f"Vehicle: {v_num}\nCustomer: {v_data['customer_name']}\nEntry: {v_data['entry_time']}"
                            slot_button.config(text=f"{slot_num}\n{v_num[:8]}")
                            break
            
            v_scrollbar.pack(side="right", fill="y")
            h_scrollbar.pack(side="bottom", fill="x")
            canvas.pack(side="left", fill="both", expand=True)
            
    
            for i in range(rows):
                parking_frame.grid_rowconfigure(i, weight=1)
            for i in range(cols):
                parking_frame.grid_columnconfigure(i, weight=1)
            
            parking_frame.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))
          
            def _on_mousewheel(event):
                canvas.yview_scroll(int(-1*(event.delta/60)), "units")
            
            def _on_shift_mousewheel(event):
                canvas.xview_scroll(int(-1*(event.delta/60)), "units")
          
            canvas.bind("<MouseWheel>", _on_mousewheel)
            canvas.bind("<Shift-MouseWheel>", _on_shift_mousewheel)
            
            v_scrollbar.bind("<MouseWheel>", _on_mousewheel)
            h_scrollbar.bind("<Shift-MouseWheel>", _on_shift_mousewheel)
           
            legend_frame = tk.Frame(frame, bg='#34495e', relief='raised', bd=2)
            legend_frame.pack(pady=15, padx=20, fill='x')
            
            legend_title = tk.Label(legend_frame, text="COLOR LEGEND", 
                                   font=('Arial', 12, 'bold'), fg='#ecf0f1', bg='#34495e')
            legend_title.pack(pady=(10, 15))
           
            legend_items_frame = tk.Frame(legend_frame, bg='#34495e')
            legend_items_frame.pack(pady=(0, 10))
            
            legend_items = [
                ("🟢 Available Slots", '#27ae60', "Open for parking"),
                ("🔴 Occupied Slots", '#e74c3c', "Currently in use"),
                ("🟠 Emergency Slots", '#f39c12', "Reserved for emergency vehicles")
            ]
            
            for text, color, description in legend_items:
                legend_item = tk.Frame(legend_items_frame, bg='#34495e')
                legend_item.pack(side='left', padx=15)
             
                color_box = tk.Label(legend_item, text="  ", bg=color, width=4, height=2, 
                                   relief='raised', bd=1)
                color_box.pack(side='left')
                
                text_container = tk.Frame(legend_item, bg='#34495e')
                text_container.pack(side='left', padx=8)
                
                text_label = tk.Label(text_container, text=text, font=('Arial', 11, 'bold'), 
                                     fg='#ecf0f1', bg='#34495e')
                text_label.pack(anchor='w')
              
                desc_label = tk.Label(text_container, text=description, font=('Arial', 9), 
                                     fg='#bdc3c7', bg='#34495e')
                desc_label.pack(anchor='w')
    
    def search_vehicle(self):
     
        search_window = tk.Toplevel(self.root)
        search_window.title("Search Vehicle - Sioplex Parking Service")
        search_window.geometry("800x600")
        search_window.configure(bg='#2c3e50')
        
     
        main_frame = tk.Frame(search_window, bg='#2c3e50')
        main_frame.pack(expand=True, fill='both', padx=40, pady=40)
    
        center_frame = tk.Frame(main_frame, bg='#2c3e50')
        center_frame.pack(expand=True, fill='both')
        
      
        title_label = tk.Label(center_frame, text="SEARCH VEHICLE", 
                              font=('Arial', 20, 'bold'), fg='#ecf0f1', bg='#2c3e50')
        title_label.pack(pady=(0, 30))
 
        input_frame = tk.Frame(center_frame, bg='#34495e', relief='raised', bd=2)
        input_frame.pack(fill='x', pady=(0, 30))
        
      
        number_frame = tk.Frame(input_frame, bg='#34495e')
        number_frame.pack(pady=30)
    
        input_container = tk.Frame(number_frame, bg='#34495e')
        input_container.pack()
        
        tk.Label(input_container, text="Vehicle Number:", font=('Arial', 14), 
                fg='#ecf0f1', bg='#34495e').pack(pady=(0, 10))
        
        vehicle_number = tk.Entry(input_container, font=('Arial', 14), width=25)
        vehicle_number.pack(pady=(0, 20))
        
        button_frame = tk.Frame(input_container, bg='#34495e')
        button_frame.pack(pady=10)
       
        search_button = tk.Button(button_frame, text="SEARCH VEHICLE", 
                                 font=('Arial', 14, 'bold'), bg='#3498db', fg='white',
                                 command=lambda: search_vehicle_action(), width=18, height=2)
        search_button.pack(side='left', padx=(0, 15))
        
        show_all_button = tk.Button(button_frame, text="SHOW ALL VEHICLES", 
                                   font=('Arial', 14, 'bold'), bg='#27ae60', fg='white',
                                   command=lambda: show_all_vehicles(), width=18, height=2)
        show_all_button.pack(side='left', padx=(15, 0))
        
        result_frame = tk.Frame(center_frame, bg='#34495e', relief='sunken', bd=2)
        result_frame.pack(expand=True, fill='both', pady=(20, 0))
        
        result_label = tk.Label(result_frame, text="SEARCH RESULTS", 
                               font=('Arial', 14, 'bold'), fg='#ecf0f1', bg='#34495e')
        result_label.pack(pady=10)
        
        text_frame = tk.Frame(result_frame, bg='#34495e')
        text_frame.pack(expand=True, fill='both', padx=10, pady=(0, 10))
        
        result_text = tk.Text(text_frame, font=('Arial', 11), bg='#ecf0f1', 
                             fg='#2c3e50', wrap='word', height=12)
        scrollbar = tk.Scrollbar(text_frame, orient='vertical', command=result_text.yview)
        result_text.configure(yscrollcommand=scrollbar.set)
        
        result_text.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        def search_vehicle_action():
            v_number = vehicle_number.get().strip().upper()
            
            if not v_number:
                messagebox.showerror("Error", "Please enter vehicle number!")
                return
       
            result_text.delete('1.0', tk.END)
            
            found = False
            for vt in self.parking_data:
                if v_number in self.parking_data[vt]['occupied_slots']:
                    vehicle_data = self.parking_data[vt]['occupied_slots'][v_number]
                    found = True
                    
                    result = f"""
╔══════════════════════════════════════════════════════════════╗
║                    VEHICLE FOUND!                            ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Vehicle Details:                                            ║
║    • Vehicle Number: {v_number:<40}                          ║
║    • Vehicle Type: {vt.upper():<40}                          ║
║    • Slot Number: {vehicle_data['slot']:<40}                 ║
║                                                              ║
║  Customer Details:                                           ║
║    • Name: {vehicle_data['customer_name']:<40}               ║
║    • Phone: {vehicle_data['phone']:<40}                      ║
║                                                              ║
║  Parking Details:                                            ║
║    • Entry Time: {vehicle_data['entry_time']:<40}            ║
║    • Emergency Vehicle: {'Yes' if vehicle_data['is_emergency'] else 'No':<40} ║
║                                                              ║
║  Current Status: PARKED                                      ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
                    """
                    result_text.insert('1.0', result)
                    break
            
            if not found:
                all_vehicles = []
                for vt in self.parking_data:
                    for v_num in self.parking_data[vt]['occupied_slots']:
                        all_vehicles.append(f"• {v_num} ({vt.upper()})")
                
                if all_vehicles:
                    result = f"""╔══════════════════════════════════════════════════════════════╗
║                    VEHICLE NOT FOUND                         ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Vehicle {v_number} not found in parking lot.                ║
║                                                              ║
║  Currently Parked Vehicles:                                  ║
{chr(10).join([f"║    {vehicle:<50} ║" for vehicle in all_vehicles])}
║                                                              ║
║  Please try searching for one of the vehicles listed above.  ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝"""
                else:
                    result = f"""╔══════════════════════════════════════════════════════════════╗
║                    VEHICLE NOT FOUND                         ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Vehicle {v_number} not found in parking lot.                ║
║                                                              ║
║  No vehicles are currently parked in the system.             ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝"""
                
                result_text.insert('1.0', result)
        
        def show_all_vehicles():
            result_text.delete('1.0', tk.END)
            
            all_vehicles = []
            for vt in self.parking_data:
                for v_num in self.parking_data[vt]['occupied_slots']:
                    vehicle_data = self.parking_data[vt]['occupied_slots'][v_num]
                    all_vehicles.append(f"• {v_num} ({vt.upper()}) - Slot {vehicle_data['slot']} - {vehicle_data['customer_name']}")
            
            if all_vehicles:
                result = f"""╔══════════════════════════════════════════════════════════════╗
║                    ALL PARKED VEHICLES                       ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
{chr(10).join([f"║  {vehicle:<50} ║" for vehicle in all_vehicles])}
║                                                              ║
║  Total Vehicles: {len(all_vehicles):<40} ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝"""
            else:
                result = """╔══════════════════════════════════════════════════════════════╗
║                    NO VEHICLES FOUND                         ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  No vehicles are currently parked in the system.             ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝"""
            
            result_text.insert('1.0', result)
    
    def show_total_revenue(self):
        revenue_window = tk.Toplevel(self.root)
        revenue_window.title("Total Revenue - Sioplex Parking Service")
        revenue_window.geometry("600x500")
        revenue_window.configure(bg='#2c3e50')
    
        main_frame = tk.Frame(revenue_window, bg='#2c3e50')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        title_label = tk.Label(main_frame, text="TOTAL REVENUE", 
                              font=('Arial', 18, 'bold'), fg='#ecf0f1', bg='#2c3e50')
        title_label.pack(pady=(0, 20))
        
        revenue_frame = tk.Frame(main_frame, bg='#34495e', relief='raised', bd=2)
        revenue_frame.pack(expand=True, fill='both', pady=(0, 20))
        
        revenue_text = f"""
+------------------------------------------------------------------------------+
|                    SIOPLEX PARKING SERVICE                                   |
|                    Revenue Report                                            |
+------------------------------------------------------------------------------+
|                                                                              |
|  Total Revenue Earned: ₹{self.total_revenue:.2f}                             |
|                                                                              |
|  Date: {datetime.now().strftime('%d/%m/%Y')}                                 |
|  Time: {datetime.now().strftime('%H:%M:%S')}                                 |
|                                                                              |
+------------------------------------------------------------------------------+
|  Parking Rates:                                                              |
|    • Car: ₹{self.parking_lot['car']['price_per_hour']}/hour                  |
|    • Bike: ₹{self.parking_lot['bike']['price_per_hour']}/hour                |
|    • Truck: ₹{self.parking_lot['truck']['price_per_hour']}/hour              |
|    • Bus: ₹{self.parking_lot['bus']['price_per_hour']}/hour                  |
|                                                                              |
+------------------------------------------------------------------------------+
        """
        
        revenue_display = tk.Text(revenue_frame, font=('Courier', 11), bg='#ecf0f1', 
                                 fg='#2c3e50', wrap='none', height=20, width=70)
        revenue_display.pack(expand=True, fill='both', padx=10, pady=10)
        revenue_display.insert('1.0', revenue_text)
        revenue_display.config(state='disabled')
        
        h_scrollbar = tk.Scrollbar(revenue_frame, orient='horizontal', command=revenue_display.xview)
        revenue_display.configure(xscrollcommand=h_scrollbar.set)
        h_scrollbar.pack(side='bottom', fill='x')
    
    def show_exit_history(self):
        history_window = tk.Toplevel(self.root)
        history_window.title("Exit History - Sioplex Parking Service")
        history_window.geometry("1200x700")
        history_window.configure(bg='#2c3e50')
        
        main_frame = tk.Frame(history_window, bg='#2c3e50')
        main_frame.pack(expand=True, fill='both', padx=30, pady=30)
        
        title_label = tk.Label(main_frame, text="EXIT HISTORY", 
                              font=('Arial', 20, 'bold'), fg='#ecf0f1', bg='#2c3e50')
        title_label.pack(pady=(0, 30))
        
        tree_frame = tk.Frame(main_frame, bg='#34495e', relief='raised', bd=2)
        tree_frame.pack(expand=True, fill='both')
        
        columns = ('Vehicle', 'Type', 'Customer', 'Phone', 'Slot', 'Entry', 'Exit', 'Duration', 'Fee')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=20)
      
        column_widths = {
            'Vehicle': 120,
            'Type': 80,
            'Customer': 150,
            'Phone': 120,
            'Slot': 60,
            'Entry': 150,
            'Exit': 150,
            'Duration': 80,
            'Fee': 100
        }
        
        for col in columns:
            tree.heading(col, text=col, anchor='center')
            tree.column(col, width=column_widths[col], anchor='center')
      
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        scrollbar.pack(side='right', fill='y', pady=10)
   
        for record in self.exit_history:
            tree.insert('', 'end', values=(
                record['vehicle_number'],
                record['vehicle_type'].upper(),
                record['customer_name'],
                record['phone'],
                record['slot'],
                record['entry_time'],
                record['exit_time'],
                f"{record['duration_hours']}h",
                f"₹{record['total_fee']:.2f}"
            ))
    
    def change_admin_password(self):
        old_password = simpledialog.askstring("Change Password", "Enter current password:", show='*')
        
        if old_password == self.admin_password:
            new_password = simpledialog.askstring("Change Password", "Enter new password:", show='*')
            if new_password:
                confirm_password = simpledialog.askstring("Change Password", "Confirm new password:", show='*')
                
                if new_password == confirm_password:
                    self.admin_password = new_password
                    self.save_admin_password()
                    messagebox.showinfo("Success", "Password changed successfully!")
                else:
                    messagebox.showerror("Error", "Passwords do not match!")
        else:
            messagebox.showerror("Error", "Incorrect current password!")
    
    def reset_system(self):
        if messagebox.askyesno("Reset System", 
                              "Are you sure you want to reset the entire parking system?\n"
                              "This will clear all parking data, revenue, and blacklist!"):
            
            self.parking_data = {}
            self.initialize_parking_slots()
            
            self.exit_history = []
            
            self.total_revenue = 0.0
            
            self.blacklisted_vehicles = {}
         
            self.save_parking_data()
            self.save_exit_history()
            self.save_revenue()
            self.save_blacklisted_vehicles()
            
            messagebox.showinfo("Success", "System reset successfully!")
    
    def exit_system(self):
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.root.quit()
    
    def blacklist_vehicle(self):
        blacklist_window = tk.Toplevel(self.root)
        blacklist_window.title("Blacklist Vehicle - Sioplex Parking Service")
        blacklist_window.geometry("600x500")
        blacklist_window.configure(bg='#2c3e50')
        
        main_frame = tk.Frame(blacklist_window, bg='#2c3e50')
        main_frame.pack(expand=True, fill='both', padx=30, pady=30)
        
        title_label = tk.Label(main_frame, text="BLACKLIST VEHICLE", 
                              font=('Arial', 18, 'bold'), fg='#ecf0f1', bg='#2c3e50')
        title_label.pack(pady=(0, 20))
        
        # Input frame
        input_frame = tk.Frame(main_frame, bg='#34495e', relief='raised', bd=2)
        input_frame.pack(fill='x', pady=(0, 20))
        
        # Vehicle number
        number_frame = tk.Frame(input_frame, bg='#34495e')
        number_frame.pack(pady=15)
        
        tk.Label(number_frame, text="Vehicle Number:", font=('Arial', 12), 
                fg='#ecf0f1', bg='#34495e').pack(side='left', padx=(0, 10))
        
        vehicle_number = tk.Entry(number_frame, font=('Arial', 12), width=20)
        vehicle_number.pack(side='left')
        
        # Owner name
        owner_frame = tk.Frame(input_frame, bg='#34495e')
        owner_frame.pack(pady=15)
        
        tk.Label(owner_frame, text="Owner Name:", font=('Arial', 12), 
                fg='#ecf0f1', bg='#34495e').pack(side='left', padx=(0, 10))
        
        owner_name = tk.Entry(owner_frame, font=('Arial', 12), width=20)
        owner_name.pack(side='left')
        
        # Address
        address_frame = tk.Frame(input_frame, bg='#34495e')
        address_frame.pack(pady=15)
        
        tk.Label(address_frame, text="Address:", font=('Arial', 12), 
                fg='#ecf0f1', bg='#34495e').pack(side='left', padx=(0, 10))
        
        address = tk.Entry(address_frame, font=('Arial', 12), width=30)
        address.pack(side='left')
        
        # Reason for blacklisting
        reason_frame = tk.Frame(input_frame, bg='#34495e')
        reason_frame.pack(pady=15)
        
        tk.Label(reason_frame, text="Reason:", font=('Arial', 12), 
                fg='#ecf0f1', bg='#34495e').pack(side='left', padx=(0, 10))
        
        reason_var = tk.StringVar(value="Owner Report")
        reason_combo = ttk.Combobox(reason_frame, textvariable=reason_var, 
                                   values=["Owner Report", "Police Report", "Security Violation", "Other"], 
                                   state="readonly", width=20)
        reason_combo.pack(side='left')
        
        # Police report checkbox
        police_frame = tk.Frame(input_frame, bg='#34495e')
        police_frame.pack(pady=15)
        
        police_var = tk.BooleanVar()
        police_check = tk.Checkbutton(police_frame, text="Report to Police", 
                                     variable=police_var, font=('Arial', 12),
                                     fg='#ecf0f1', bg='#34495e', selectcolor='#e74c3c')
        police_check.pack()
        
        def blacklist_vehicle_action():
            v_number = vehicle_number.get().strip().upper()
            o_name = owner_name.get().strip()
            o_address = address.get().strip()
            o_reason = reason_var.get()
            report_to_police = police_var.get()
            
            if not all([v_number, o_name, o_address]):
                messagebox.showerror("Error", "Please fill all required fields!")
                return
            
            # Check if vehicle is already blacklisted
            if v_number in self.blacklisted_vehicles:
                messagebox.showerror("Error", f"Vehicle {v_number} is already blacklisted!")
                return
            
            # Add to blacklist
            blacklist_entry = {
                'vehicle_number': v_number,
                'owner_name': o_name,
                'address': o_address,
                'reason': o_reason,
                'report_to_police': report_to_police,
                'case_status': 'Open' if report_to_police else 'Reviewed',
                'date_added': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'reported_by': 'admin'
            }
            
            self.blacklisted_vehicles[v_number] = blacklist_entry
            self.save_blacklisted_vehicles()
            
            # Show confirmation message
            police_msg = " and reported to police" if report_to_police else ""
            messagebox.showinfo("Success", f"Vehicle {v_number} has been blacklisted{police_msg}!")
            
            blacklist_window.destroy()
        
        # Blacklist button
        blacklist_button = tk.Button(main_frame, text="ADD TO BLACKLIST", 
                                    font=('Arial', 14, 'bold'), bg='#e74c3c', fg='white',
                                    command=blacklist_vehicle_action, width=20, height=2)
        blacklist_button.pack(pady=20)
    
    def view_blacklist(self):
        blacklist_window = tk.Toplevel(self.root)
        blacklist_window.title("View Blacklist - Sioplex Parking Service")
        blacklist_window.geometry("1000x600")
        blacklist_window.configure(bg='#2c3e50')
        
        main_frame = tk.Frame(blacklist_window, bg='#2c3e50')
        main_frame.pack(expand=True, fill='both', padx=30, pady=30)
        
        title_label = tk.Label(main_frame, text="BLACKLISTED VEHICLES", 
                              font=('Arial', 18, 'bold'), fg='#ecf0f1', bg='#2c3e50')
        title_label.pack(pady=(0, 20))
        
        # Create treeview
        tree_frame = tk.Frame(main_frame, bg='#34495e', relief='raised', bd=2)
        tree_frame.pack(expand=True, fill='both')
        
        columns = ('Vehicle', 'Owner', 'Address', 'Reason', 'Police Report', 'Case Status', 'Date Added')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        column_widths = {
            'Vehicle': 120,
            'Owner': 150,
            'Address': 200,
            'Reason': 120,
            'Police Report': 100,
            'Case Status': 120,
            'Date Added': 150
        }
        
        for col in columns:
            tree.heading(col, text=col, anchor='center')
            tree.column(col, width=column_widths[col], anchor='center')
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        scrollbar.pack(side='right', fill='y', pady=10)
        
        # Populate treeview
        for vehicle_number, data in self.blacklisted_vehicles.items():
            tree.insert('', 'end', values=(
                vehicle_number,
                data['owner_name'],
                data['address'],
                data['reason'],
                "Yes" if data['report_to_police'] else "No",
                data.get('case_status', 'Reviewed'),  # Default to 'Reviewed' for existing entries
                data['date_added']
            ))
        

    
    def check_blacklist(self, vehicle_number):
        return vehicle_number.upper() in self.blacklisted_vehicles
    
    def get_blacklist_info(self, vehicle_number):
        return self.blacklisted_vehicles.get(vehicle_number.upper())
    
    def load_blacklisted_vehicles(self):
        try:
            with open('blacklisted_vehicles.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def save_blacklisted_vehicles(self):
        with open('blacklisted_vehicles.json', 'w') as f:
            json.dump(self.blacklisted_vehicles, f, indent=2)
    
    #file_management
    def load_parking_data(self):
        try:
            with open('parking_data.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def save_parking_data(self):
        with open('parking_data.json', 'w') as f:
            json.dump(self.parking_data, f, indent=2)
    
    def load_exit_history(self):
        try:
            with open('exit_history.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def save_exit_history(self):
        with open('exit_history.json', 'w') as f:
            json.dump(self.exit_history, f, indent=2)
    
    def load_revenue(self):
        try:
            with open('revenue.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return 0.0
    
    def save_revenue(self):
        with open('revenue.json', 'w') as f:
            json.dump(self.total_revenue, f)
    
    def load_admin_password(self):
        try:
            with open('admin_password.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return "admin123" 
    
    def save_admin_password(self):
        with open('admin_password.json', 'w') as f:
            json.dump(self.admin_password, f)
    
    def run(self):
        self.root.mainloop()

# Main execution
if __name__ == "__main__":
    app = SioplexParkingSystem()
    app.run()