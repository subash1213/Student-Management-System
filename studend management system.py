import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

conn = sqlite3.connect("students.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students ( id INTEGER PRIMARY KEY,name TEXT NOT NULL,department TEXT,year INTEGER, email TEXT)""")
conn.commit()

ADMIN_USERNAME = "subash"
ADMIN_PASSWORD = "1234"


root = tk.Tk()
root.title("Student Management System")
root.geometry("700x500")


login_frame = tk.Frame(root)
login_frame.pack(pady=50)

tk.Label(login_frame, text="Username:").grid(row=0, column=0)
tk.Label(login_frame, text="Password:").grid(row=1, column=0)

username_entry = tk.Entry(login_frame)
password_entry = tk.Entry(login_frame, show="*")
username_entry.grid(row=0, column=1)
password_entry.grid(row=1, column=1)

def login():
    username = username_entry.get()
    password = password_entry.get()
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        login_frame.pack_forget()
        main_frame.pack()
    else:
        messagebox.showerror("Login Failed", "Incorrect Username or Password")

tk.Button(login_frame, text="Login", command=login).grid(row=2, column=0, columnspan=2, pady=2)


main_frame = tk.Frame(root)


tk.Label(main_frame, text="ID:").grid(row=0, column=0)
tk.Label(main_frame, text="Name:").grid(row=1, column=0)
tk.Label(main_frame, text="Department:").grid(row=2, column=0)
tk.Label(main_frame, text="Year:").grid(row=3, column=0)
tk.Label(main_frame, text="Email:").grid(row=4, column=0)

id_entry = tk.Entry(main_frame)
name_entry = tk.Entry(main_frame)
dept_entry = tk.Entry(main_frame)
year_entry = tk.Entry(main_frame)
email_entry = tk.Entry(main_frame)

id_entry.grid(row=0, column=1)
name_entry.grid(row=1, column=1)
dept_entry.grid(row=2, column=1)
year_entry.grid(row=3, column=1)
email_entry.grid(row=4, column=1)


tree = ttk.Treeview(main_frame, columns=("ID", "Name", "Dept", "Year", "Email"), show="headings")
for col in ("ID", "Name", "Dept", "Year", "Email"):
    tree.heading(col, text=col)
tree.grid(row=6, column=0, columnspan=2, pady=20)


def add_student():
    try:
        cursor.execute(
            "INSERT INTO students VALUES (?, ?, ?, ?, ?)",
            (int(id_entry.get()), name_entry.get(), dept_entry.get(), int(year_entry.get()), email_entry.get())
        )
        conn.commit()
        messagebox.showinfo("Success", "Student added successfully")
        display_students()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def display_students():
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute("SELECT * FROM students")
    for student in cursor.fetchall():
        tree.insert("", tk.END, values=student)

def update_student():
    cursor.execute("""
    UPDATE students SET name=?, department=?, year=?, email=? WHERE id=?
    """, (name_entry.get(), dept_entry.get(), int(year_entry.get()), email_entry.get(), int(id_entry.get())))
    conn.commit()
    messagebox.showinfo("Success", "Student updated successfully")
    display_students()

def delete_student():
    cursor.execute("DELETE FROM students WHERE id=?", (int(id_entry.get()),))
    conn.commit()
    messagebox.showinfo("Deleted", "Student deleted successfully")
    display_students()

def search_student():
    cursor.execute("SELECT * FROM students WHERE id=?", (int(id_entry.get()),))
    result = cursor.fetchone()
    if result:
        tree.delete(*tree.get_children())
        tree.insert("", tk.END, values=result)
    else:
        messagebox.showinfo("Not Found", "Student ID not found")


tk.Button(main_frame, text="Add", command=add_student).grid(row=5, column=0)
tk.Button(main_frame, text="Update", command=update_student).grid(row=5, column=1)
tk.Button(main_frame, text="Delete", command=delete_student).grid(row=5, column=2)
tk.Button(main_frame, text="Search", command=search_student).grid(row=5, column=3)
tk.Button(main_frame, text="Display All", command=display_students).grid(row=7, column=0, columnspan=2, pady=10)

root.mainloop()
conn.close()
