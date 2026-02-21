import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# ---------- DATABASE SETUP ----------
def setup_database():
    conn = sqlite3.connect("hospital.db")
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS Patient (
        patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        gender TEXT,
        phone TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS Doctor (
        doc_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        specialization TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS Appointment (
        appoint_id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        doc_id INTEGER,
        date TEXT,
        time TEXT,
        FOREIGN KEY(patient_id) REFERENCES Patient(patient_id),
        FOREIGN KEY(doc_id) REFERENCES Doctor(doc_id)
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS Bill (
        bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        amount REAL,
        FOREIGN KEY(patient_id) REFERENCES Patient(patient_id)
    )''')

    conn.commit()
    conn.close()

# ---------- FUNCTIONALITY ----------
def add_patient(name, age, gender, phone):
    conn = sqlite3.connect("hospital.db")
    c = conn.cursor()
    c.execute("INSERT INTO Patient (name, age, gender, phone) VALUES (?, ?, ?, ?)", (name, age, gender, phone))
    conn.commit()
    conn.close()

def add_doctor(name, specialization):
    conn = sqlite3.connect("hospital.db")
    c = conn.cursor()
    c.execute("INSERT INTO Doctor (name, specialization) VALUES (?, ?)", (name, specialization))
    conn.commit()
    conn.close()

def book_appointment(patient_id, doc_id, date, time):
    conn = sqlite3.connect("hospital.db")
    c = conn.cursor()
    c.execute("INSERT INTO Appointment (patient_id, doc_id, date, time) VALUES (?, ?, ?, ?)",
              (patient_id, doc_id, date, time))
    conn.commit()
    conn.close()

def generate_bill(patient_id, amount):
    conn = sqlite3.connect("hospital.db")
    c = conn.cursor()
    c.execute("INSERT INTO Bill (patient_id, amount) VALUES (?, ?)", (patient_id, amount))
    conn.commit()
    conn.close()

def view_patients():
    conn = sqlite3.connect("hospital.db")
    c = conn.cursor()
    c.execute("SELECT * FROM Patient")
    rows = c.fetchall()
    conn.close()
    return rows

# ---------- GUI ----------

def create_form(title, fields, submit_func):
    win = tk.Toplevel()
    win.title(title)
    win.geometry("300x300")
    win.resizable(False, False)

    form = {}
    for i, (label_text, var_type) in enumerate(fields):
        ttk.Label(win, text=label_text).grid(row=i, column=0, padx=10, pady=5, sticky="w")
        entry = ttk.Entry(win)
        entry.grid(row=i, column=1, padx=10, pady=5)
        form[label_text] = (entry, var_type)

    def submit():
        try:
            values = []
            for entry, var_type in form.values():
                val = entry.get()
                values.append(var_type(val))
            submit_func(*values)
            messagebox.showinfo("Success", f"{title} successful!")
            win.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input.\n{e}")

    ttk.Button(win, text="Submit", command=submit).grid(row=len(fields), columnspan=2, pady=10)

def add_patient_gui():
    fields = [("Name", str), ("Age", int), ("Gender", str), ("Phone", str)]
    create_form("Add Patient", fields, add_patient)

def add_doctor_gui():
    fields = [("Name", str), ("Specialization", str)]
    create_form("Add Doctor", fields, add_doctor)

def book_appointment_gui():
    fields = [("Patient ID", int), ("Doctor ID", int), ("Date (YYYY-MM-DD)", str), ("Time (HH:MM)", str)]
    create_form("Book Appointment", fields, book_appointment)

def generate_bill_gui():
    fields = [("Patient ID", int), ("Amount", float)]
    create_form("Generate Bill", fields, generate_bill)

def view_patients_gui():
    win = tk.Toplevel()
    win.title("All Patients")
    win.geometry("450x300")
    tree = ttk.Treeview(win, columns=("ID", "Name", "Age", "Gender", "Phone"), show='headings')
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Age", text="Age")
    tree.heading("Gender", text="Gender")
    tree.heading("Phone", text="Phone")

    rows = view_patients()
    for row in rows:
        tree.insert("", tk.END, values=row)

    tree.pack(expand=True, fill="both", padx=10, pady=10)

# ---------- MAIN WINDOW ----------
def main_gui():
    setup_database()
    root = tk.Tk()
    root.title("Hospital Management System")
    root.geometry("400x400")
    root.resizable(False, False)

    # Use modern theme
    style = ttk.Style()
    style.theme_use("clam")

    ttk.Label(root, text="🏥 Hospital Management System", font=("Helvetica", 16)).pack(pady=20)

    ttk.Button(root, text="Add Patient", width=25, command=add_patient_gui).pack(pady=5)
    ttk.Button(root, text="Add Doctor", width=25, command=add_doctor_gui).pack(pady=5)
    ttk.Button(root, text="Book Appointment", width=25, command=book_appointment_gui).pack(pady=5)
    ttk.Button(root, text="Generate Bill", width=25, command=generate_bill_gui).pack(pady=5)
    ttk.Button(root, text="View Patients", width=25, command=view_patients_gui).pack(pady=5)

    ttk.Button(root, text="Exit", width=25, command=root.destroy).pack(pady=20)

    root.mainloop()

main_gui()
