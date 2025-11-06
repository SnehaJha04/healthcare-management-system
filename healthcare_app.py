import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3, re
DB_FILE = "healthcare.db"
def connect_db():
    return sqlite3.connect(DB_FILE)
def init_db():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        gender TEXT,
        dob TEXT,
        disorder TEXT,
        address TEXT,
        phone TEXT)
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS doctors (
        doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        specialization TEXT,
        phone TEXT,
        email TEXT)
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS appointments (
        appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        doctor_id INTEGER,
        date TEXT,
        time TEXT,
        FOREIGN KEY(patient_id) REFERENCES patients(patient_id),
        FOREIGN KEY(doctor_id) REFERENCES doctors(doctor_id))
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS payments (
        payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        appointment_id INTEGER,
        amount REAL,
        method TEXT,
        date TEXT,
        FOREIGN KEY(appointment_id) REFERENCES appointments(appointment_id))
    """)
    conn.commit()
    conn.close()
def focus_next(event):
    event.widget.tk_focusNext().focus()
    return "break"
def show_table_window(title, columns, records):
    view_window = tk.Toplevel(root)
    view_window.title(title)
    view_window.geometry("700x350")
    view_window.config(bg="#E6F0F7")
    ttk.Label(view_window, text=title, font=("Arial", 14, "bold"),background="#E6F0F7", foreground="#004080").pack(pady=10)
    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
    style.configure("Treeview", rowheight=25)
    tree = ttk.Treeview(view_window, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)
    for row in records:
        tree.insert("", tk.END, values=row)
    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
def add_patient():
    name = entry_patient_name.get().strip()
    gender = entry_patient_gender.get()
    dob = entry_patient_dob.get()
    disorder = entry_patient_disorder.get()
    address = entry_patient_address.get()
    phone = entry_patient_phone.get()
    if not name:
        messagebox.showerror("Invalid Input", "Name is required!")
        return
    if not re.match(r'^[A-Za-z ]+$', name):
        messagebox.showerror("Invalid Input", "Name must contain alphabets only!")
        return
    if not phone.isdigit():
        messagebox.showerror("Invalid Input", "Phone number must contain only digits!")
        return
    if len(phone) < 10:
        messagebox.showerror("Invalid Input", "Phone number must be at least 10 digits!")
        return
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO patients (name, gender, dob, disorder, address, phone) VALUES (?, ?, ?, ?, ?, ?)",
                (name, gender, dob, disorder, address, phone))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Patient added successfully!")
    clear_patient_fields()
def clear_patient_fields():
    entry_patient_name.delete(0, tk.END)
    entry_patient_gender.delete(0, tk.END)
    entry_patient_dob.delete(0, tk.END)
    entry_patient_disorder.delete(0, tk.END)
    entry_patient_address.delete(0, tk.END)
    entry_patient_phone.delete(0, tk.END)
def view_patients():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM patients")
    records = cur.fetchall()
    conn.close()
    if not records:
        messagebox.showinfo("Patients", "No records found!")
    else:
        show_table_window("Patient Details", ["ID", "Name", "Gender", "DOB", "Disorder", "Address", "Phone"], records)
def add_doctor():
    name = entry_doctor_name.get().strip()
    specialization = entry_doctor_specialization.get()
    phone = entry_doctor_phone.get()
    email = entry_doctor_email.get()
    if not name:
        messagebox.showerror("Invalid Input", "Name is required!")
        return
    if not re.match(r'^[A-Za-z ]+$', name):
        messagebox.showerror("Invalid Input", "Name must contain alphabets only!")
        return
    if not phone.isdigit():
        messagebox.showerror("Invalid Input", "Phone number must contain only digits!")
        return
    if len(phone) < 10:
        messagebox.showerror("Invalid Input", "Phone number must be at least 10 digits!")
        return
    if email and not re.match(r"^[a-zA-Z0-9._%+-]+@gmail\.com$", email):
        messagebox.showerror("Invalid Email", "Email must be a valid Gmail address (e.g. user@gmail.com).")
        return
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO doctors (name, specialization, phone, email) VALUES (?, ?, ?, ?)",
                (name, specialization, phone, email))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Doctor added successfully!")
    clear_doctor_fields()
def clear_doctor_fields():
    entry_doctor_name.delete(0, tk.END)
    entry_doctor_specialization.delete(0, tk.END)
    entry_doctor_phone.delete(0, tk.END)
    entry_doctor_email.delete(0, tk.END)
def view_doctors():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM doctors")
    records = cur.fetchall()
    conn.close()
    if not records:
        messagebox.showinfo("Doctors", "No records found!")
    else:
        show_table_window("Doctor Details", ["ID", "Name", "Specialization", "Phone", "Email"], records)
def add_appointment():
    patient_id = entry_app_patient.get()
    doctor_id = entry_app_doctor.get()
    date = entry_app_date.get()
    time = entry_app_time.get()
    if not patient_id or not doctor_id:
        messagebox.showerror("Error", "Patient ID and Doctor ID are required!")
        return
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO appointments (patient_id, doctor_id, date, time) VALUES (?, ?, ?, ?)",
                (patient_id, doctor_id, date, time))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Appointment added successfully!")
    clear_appointment_fields()
def clear_appointment_fields():
    entry_app_patient.delete(0, tk.END)
    entry_app_doctor.delete(0, tk.END)
    entry_app_date.delete(0, tk.END)
    entry_app_time.delete(0, tk.END)
def view_appointments():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM appointments")
    records = cur.fetchall()
    conn.close()
    if not records:
        messagebox.showinfo("Appointments", "No records found!")
    else:
        show_table_window("Appointment Details", ["ID", "Patient ID", "Doctor ID", "Date", "Time"], records)
def add_payment():
    appointment_id = entry_pay_appointment.get()
    amount = entry_pay_amount.get()
    method = entry_pay_method.get()
    date = entry_pay_date.get()
    if not appointment_id or not amount:
        messagebox.showerror("Error", "Appointment ID and Amount are required!")
        return
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO payments (appointment_id, amount, method, date) VALUES (?, ?, ?, ?)",
                (appointment_id, amount, method, date))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Payment added successfully!")
    clear_payment_fields()
def clear_payment_fields():
    entry_pay_appointment.delete(0, tk.END)
    entry_pay_amount.delete(0, tk.END)
    entry_pay_method.delete(0, tk.END)
    entry_pay_date.delete(0, tk.END)
def view_payments():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM payments")
    records = cur.fetchall()
    conn.close()
    if not records:
        messagebox.showinfo("Payments", "No records found!")
    else:
        show_table_window("Payment Details", ["ID", "Appointment ID", "Amount", "Method", "Date"], records)
root = tk.Tk()
root.title("Healthcare Management System")
root.geometry("750x550")
root.config(bg="#E6F0F7")
style = ttk.Style()
style.configure("TButton", font=("Arial", 10, "bold"), padding=6)
style.configure("TLabel", background="#E6F0F7", font=("Arial", 10))
title_label = tk.Label(root, text="🏥 Healthcare Management System",
                       font=("Arial", 18, "bold"), fg="#004080", bg="#E6F0F7")
title_label.pack(pady=10)
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both", padx=10, pady=10)
def make_tab(tab, fields, funcs):
    for i, label in enumerate(fields):
        ttk.Label(tab, text=label).grid(row=i, column=0, padx=10, pady=5, sticky="e")
        entry = ttk.Entry(tab, width=30)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entry.bind("<Return>", focus_next)
        funcs.append(entry)
    return funcs
def only_alphabets(P):
    return bool(re.match(r'^[A-Za-z ]*$', P))
vcmd = (root.register(only_alphabets), "%P")
tab_patient = ttk.Frame(notebook)
notebook.add(tab_patient, text="Patient")
fields = ["Name", "Gender", "DOB", "Disorder", "Address", "Phone"]
entries = []
entries = make_tab(tab_patient, fields, entries)
(entry_patient_name, entry_patient_gender, entry_patient_dob,
 entry_patient_disorder, entry_patient_address, entry_patient_phone) = entries
entry_patient_name.config(validate="key", validatecommand=vcmd)
ttk.Button(tab_patient, text="Add Patient", command=add_patient).grid(row=6, column=0, pady=10)
ttk.Button(tab_patient, text="View Patients", command=view_patients).grid(row=6, column=1, pady=10)
tab_doctor = ttk.Frame(notebook)
notebook.add(tab_doctor, text="Doctor")
fields = ["Name", "Specialization", "Phone", "Email"]
entries = []
entries = make_tab(tab_doctor, fields, entries)
(entry_doctor_name, entry_doctor_specialization, entry_doctor_phone, entry_doctor_email) = entries
entry_doctor_name.config(validate="key", validatecommand=vcmd)
ttk.Button(tab_doctor, text="Add Doctor", command=add_doctor).grid(row=4, column=0, pady=10)
ttk.Button(tab_doctor, text="View Doctors", command=view_doctors).grid(row=4, column=1, pady=10)
tab_appointment = ttk.Frame(notebook)
notebook.add(tab_appointment, text="Appointment")
fields = ["Patient ID", "Doctor ID", "Date", "Time"]
entries = []
entries = make_tab(tab_appointment, fields, entries)
(entry_app_patient, entry_app_doctor, entry_app_date, entry_app_time) = entries
ttk.Button(tab_appointment, text="Add Appointment", command=add_appointment).grid(row=4, column=0, pady=10)
ttk.Button(tab_appointment, text="View Appointments", command=view_appointments).grid(row=4, column=1, pady=10)
tab_payment = ttk.Frame(notebook)
notebook.add(tab_payment, text="Payment")
fields = ["Appointment ID", "Amount", "Method", "Date"]
entries = []
entries = make_tab(tab_payment, fields, entries)
(entry_pay_appointment, entry_pay_amount, entry_pay_method, entry_pay_date) = entries
ttk.Button(tab_payment, text="Add Payment", command=add_payment).grid(row=4, column=0, pady=10)
ttk.Button(tab_payment, text="View Payments", command=view_payments).grid(row=4, column=1, pady=10)
init_db()
root.mainloop()