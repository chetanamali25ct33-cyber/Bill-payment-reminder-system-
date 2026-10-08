import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import date


# ---------------- DATABASE CONNECTION ----------------

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="dikshu@18",
        database="bill_reminder"
    )


# ---------------- ADD BILL ----------------

def add_bill():
    name = bill_name.get()
    btype = bill_type.get()
    amount = amount_entry.get()
    due = due_date.get()
    reminder = reminder_date.get()

    if name == "" or btype == "" or amount == "" or due == "" or reminder == "":
        messagebox.showwarning("Warning", "Please fill all fields")
        return

    try:
        db = connect_db()
        cursor = db.cursor()

        query = """
        INSERT INTO bills
        (bill_name, bill_type, amount, due_date, reminder_date, status)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        values = (name, btype, amount, due, reminder, "Pending")

        cursor.execute(query, values)
        db.commit()

        cursor.close()
        db.close()

        messagebox.showinfo("Success", "Bill added successfully!")

        clear_fields()
        show_bills()

    except Exception as e:
        messagebox.showerror("Database Error", str(e))


# ---------------- SHOW BILLS ----------------

def show_bills():
    for item in table.get_children():
        table.delete(item)

    try:
        db = connect_db()
        cursor = db.cursor()

        cursor.execute("SELECT * FROM bills")
        records = cursor.fetchall()

        for row in records:
            table.insert("", tk.END, values=row)

        cursor.close()
        db.close()

    except Exception as e:
        messagebox.showerror("Database Error", str(e))


# ---------------- DELETE BILL ----------------

def delete_bill():
    selected = table.selection()

    if not selected:
        messagebox.showwarning("Warning", "Please select a bill")
        return

    item = table.item(selected[0])
    bill_id = item["values"][0]

    try:
        db = connect_db()
        cursor = db.cursor()

        cursor.execute(
            "DELETE FROM bills WHERE id=%s",
            (bill_id,)
        )

        db.commit()

        cursor.close()
        db.close()

        messagebox.showinfo("Success", "Bill deleted successfully!")

        show_bills()

    except Exception as e:
        messagebox.showerror("Database Error", str(e))


# ---------------- MARK AS PAID ----------------

def mark_paid():
    selected = table.selection()

    if not selected:
        messagebox.showwarning("Warning", "Please select a bill")
        return

    item = table.item(selected[0])
    bill_id = item["values"][0]

    try:
        db = connect_db()
        cursor = db.cursor()

        cursor.execute(
            "UPDATE bills SET status='Paid' WHERE id=%s",
            (bill_id,)
        )

        db.commit()

        cursor.close()
        db.close()

        messagebox.showinfo("Success", "Bill marked as Paid!")

        show_bills()

    except Exception as e:
        messagebox.showerror("Database Error", str(e))


# ---------------- CLEAR FIELDS ----------------

def clear_fields():
    bill_name.delete(0, tk.END)
    bill_type.set("")
    amount_entry.delete(0, tk.END)
    due_date.delete(0, tk.END)
    reminder_date.delete(0, tk.END)


# ---------------- CHECK REMINDERS ----------------

def check_reminders():
    today = date.today()

    try:
        db = connect_db()
        cursor = db.cursor()

        cursor.execute("""
        SELECT bill_name, due_date
        FROM bills
        WHERE status='Pending'
        """)

        records = cursor.fetchall()

        upcoming = []

        for name, due in records:
            if due <= today:
                upcoming.append(
                    name + " - Due: " + str(due)
                )

        cursor.close()
        db.close()

        if upcoming:
            messagebox.showwarning(
                "Bill Reminder",
                "Pending / Overdue Bills:\n\n" +
                "\n".join(upcoming)
            )
        else:
            messagebox.showinfo(
                "Reminder",
                "No pending bills today!"
            )

    except Exception as e:
        messagebox.showerror("Database Error", str(e))


# ================= MAIN WINDOW =================

root = tk.Tk()
root.title("Bill Payment Reminder System")
root.geometry("1000x650")
root.resizable(False, False)


# ---------------- TITLE ----------------

title = tk.Label(
    root,
    text="BILL PAYMENT REMINDER SYSTEM",
    font=("Arial", 22, "bold")
)

title.pack(pady=20)


# ---------------- INPUT FRAME ----------------

input_frame = tk.Frame(root)
input_frame.pack(pady=10)


tk.Label(
    input_frame,
    text="Bill Name:",
    font=("Arial", 12)
).grid(row=0, column=0, padx=10, pady=10)

bill_name = tk.Entry(
    input_frame,
    width=25
)
bill_name.grid(row=0, column=1)


tk.Label(
    input_frame,
    text="Bill Type:",
    font=("Arial", 12)
).grid(row=0, column=2, padx=10)

bill_type = ttk.Combobox(
    input_frame,
    values=[
        "Electricity",
        "Mobile",
        "Internet",
        "Rent",
        "DTH",
        "Credit Card",
        "Other"
    ],
    width=22
)

bill_type.grid(row=0, column=3)


tk.Label(
    input_frame,
    text="Amount:",
    font=("Arial", 12)
).grid(row=1, column=0, padx=10, pady=10)

amount_entry = tk.Entry(
    input_frame,
    width=25
)

amount_entry.grid(row=1, column=1)


tk.Label(
    input_frame,
    text="Due Date:",
    font=("Arial", 12)
).grid(row=1, column=2, padx=10)

due_date = tk.Entry(
    input_frame,
    width=25
)

due_date.insert(0, "YYYY-MM-DD")
due_date.grid(row=1, column=3)


tk.Label(
    input_frame,
    text="Reminder Date:",
    font=("Arial", 12)
).grid(row=2, column=0, padx=10, pady=10)

reminder_date = tk.Entry(
    input_frame,
    width=25
)

reminder_date.insert(0, "YYYY-MM-DD")
reminder_date.grid(row=2, column=1)


# ---------------- BUTTONS ----------------

button_frame = tk.Frame(root)
button_frame.pack(pady=15)


tk.Button(
    button_frame,
    text="ADD BILL",
    width=15,
    command=add_bill
).grid(row=0, column=0, padx=8)


tk.Button(
    button_frame,
    text="CLEAR",
    width=15,
    command=clear_fields
).grid(row=0, column=1, padx=8)


tk.Button(
    button_frame,
    text="DELETE",
    width=15,
    command=delete_bill
).grid(row=0, column=2, padx=8)


tk.Button(
    button_frame,
    text="MARK AS PAID",
    width=15,
    command=mark_paid
).grid(row=0, column=3, padx=8)


tk.Button(
    button_frame,
    text="CHECK REMINDER",
    width=18,
    command=check_reminders
).grid(row=0, column=4, padx=8)


# ---------------- TABLE ----------------

table_frame = tk.Frame(root)
table_frame.pack(pady=20)


columns = (
    "ID",
    "Bill Name",
    "Bill Type",
    "Amount",
    "Due Date",
    "Reminder Date",
    "Status"
)

table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    height=12
)

for col in columns:
    table.heading(col, text=col)
    table.column(col, width=125)

table.pack()


# ---------------- START ----------------

show_bills()

root.mainloop()
