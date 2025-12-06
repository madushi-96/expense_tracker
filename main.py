import pandas as pd
import os
import matplotlib.pyplot as plt
from datetime import datetime
from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from PIL import Image, ImageTk

# ---------------------------------------------------
# CREATE DATA FOLDER + CSV FILE IF NOT EXISTS
# ---------------------------------------------------

DATA_FILE = "data/expenses.csv"

if not os.path.exists("data"):
    os.makedirs("data")

if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])
    df.to_csv(DATA_FILE, index=False)

# ---------------------------------------------------
# EXPENSE FUNCTIONS
# ---------------------------------------------------

def add_expense():
    date = date_entry.get()
    category = category_box.get()
    amount = amount_entry.get()
    description = desc_entry.get()

    if date == "" or category == "" or amount == "":
        messagebox.showerror("Error", "Please fill all fields")
        return

    try:
        amount = float(amount)
    except:
        messagebox.showerror("Error", "Amount must be a number")
        return

    df = pd.read_csv(DATA_FILE)
    new_row = {
        "Date": date,
        "Category": category,
        "Amount": amount,
        "Description": description,
    }

    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

    messagebox.showinfo("Success", "Expense added!")

    date_entry.delete(0, END)
    amount_entry.delete(0, END)
    desc_entry.delete(0, END)


def view_expenses():
    df = pd.read_csv(DATA_FILE)
    messagebox.showinfo("All Expenses", df.to_string())


def show_total_by_category():
    df = pd.read_csv(DATA_FILE)
    totals = df.groupby("Category")["Amount"].sum()

    win = Tk()
    win.title("Category Totals")
    win.geometry("350x350")

    Label(win, text="Total by Category", font=("Arial", 12, "bold")).pack()

    for cat, val in totals.items():
        Label(win, text=f"{cat}: Rs {val}").pack()


def monthly_report():
    df = pd.read_csv(DATA_FILE)
    df["Date"] = pd.to_datetime(df["Date"])
    df["Month"] = df["Date"].dt.to_period("M")

    monthly_sum = df.groupby("Month")["Amount"].sum()

    win = Tk()
    win.title("Monthly Report")
    win.geometry("350x400")

    Label(win, text="Monthly Report", font=("Arial", 12, "bold")).pack()

    for month, amount in monthly_sum.items():
        Label(win, text=f"{month}: Rs {amount}").pack()


def show_bar_chart():
    df = pd.read_csv(DATA_FILE)
    totals = df.groupby("Category")["Amount"].sum()

    plt.figure(figsize=(8, 5))
    plt.bar(totals.index, totals.values)
    plt.xlabel("Category")
    plt.ylabel("Amount")
    plt.title("Spending by Category")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


# ---------------------------------------------------
# EDIT / DELETE SCREEN
# ---------------------------------------------------

def edit_delete_screen():
    df = pd.read_csv(DATA_FILE)
    df.index = df.index + 1  # start index at 1

    win = Tk()
    win.title("Edit / Delete Expense")
    win.geometry("550x550")

    Label(win, text="All Expenses (Row No. Starts From 1)", 
          font=("Arial", 12, "bold")).pack()

    text_box = Text(win, width=70, height=18)
    text_box.pack()
    text_box.insert(END, df.to_string())

    Label(win, text="Enter Row Number to Edit/Delete:").pack()
    row_entry = Entry(win)
    row_entry.pack()

    # DELETE FUNCTION
    def delete_row():
        try:
            row_id = int(row_entry.get())
            df2 = pd.read_csv(DATA_FILE)
            df2.index = df2.index + 1
            df2 = df2.drop(row_id)
            df2.index = range(1, len(df2)+1)
            df2.to_csv(DATA_FILE, index=False)
            messagebox.showinfo("Success", "Row deleted successfully!")
            win.destroy()
        except:
            messagebox.showerror("Error", "Invalid row number")

    # EDIT FUNCTION
    def edit_row():
        try:
            row_id = int(row_entry.get())
            df2 = pd.read_csv(DATA_FILE)
            df2.index = df2.index + 1
            row = df2.loc[row_id]

            edit_win = Tk()
            edit_win.title("Edit Expense")
            edit_win.geometry("350x300")

            Label(edit_win, text="Edit Selected Expense", font=("Arial", 12, "bold")).pack()

            Label(edit_win, text="Date:").pack()
            date_edit = Entry(edit_win)
            date_edit.insert(0, row["Date"])
            date_edit.pack()

            Label(edit_win, text="Category:").pack()
            cat_edit = Entry(edit_win)
            cat_edit.insert(0, row["Category"])
            cat_edit.pack()

            Label(edit_win, text="Amount:").pack()
            amount_edit = Entry(edit_win)
            amount_edit.insert(0, row["Amount"])
            amount_edit.pack()

            Label(edit_win, text="Description:").pack()
            desc_edit = Entry(edit_win)
            desc_edit.insert(0, row["Description"])
            desc_edit.pack()

            def save_changes():
                df2.loc[row_id] = [
                    date_edit.get(),
                    cat_edit.get(),
                    float(amount_edit.get()),
                    desc_edit.get()
                ]
                df2.index = range(1, len(df2)+1)
                df2.to_csv(DATA_FILE, index=False)
                messagebox.showinfo("Success", "Row updated!")
                edit_win.destroy()
                win.destroy()

            Button(edit_win, text="Save", bg="green", fg="white", command=save_changes).pack(pady=10)

        except:
            messagebox.showerror("Error", "Invalid row number")

    Button(win, text="Delete", command=delete_row, bg="red", fg="white", width=20).pack(pady=10)
    Button(win, text="Edit", command=edit_row, bg="orange", fg="white", width=20).pack(pady=5)


# ---------------------------------------------------
# MAIN APPLICATION WINDOW
# ---------------------------------------------------

def main_window():
    global window, date_entry, category_box, amount_entry, desc_entry  # FIXED GLOBAL

    window = Tk()
    window.title("Expense Tracker - Dashboard")
    window.geometry("475x650")

    # BACKGROUND IMAGE
    bg_image = Image.open("images/1.jpg")
    bg_image = bg_image.resize((900, 700))
    bg_photo = ImageTk.PhotoImage(bg_image)

    bg_label = Label(window, image=bg_photo)
    bg_label.image = bg_photo
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    window.config(padx=20, pady=20, bg="white")

    # TITLE
    Label(window, text="Expense Tracker", font=("Arial", 20, "bold"), bg="#ffffff").place(x=110, y=10)

    # INPUTS
    Label(window, text="Select Date:", font=("Arial", 11), bg="#ffffff").place(x=50, y=80)
    date_entry = DateEntry(window, width=27, date_pattern="yyyy-mm-dd")
    date_entry.place(x=200, y=80)

    Label(window, text="Category:", font=("Arial", 11), bg="#ffffff").place(x=50, y=130)

    categories = [
        "Food", "Groceries", "Transport", "Fuel", "Electricity", "Water", "Internet",
        "Mobile Reload", "Medicine", "Doctor", "Clothes", "Education",
        "Entertainment", "Gifts", "Savings", "Other"
    ]

    category_box = ttk.Combobox(window, values=categories, width=27)
    category_box.place(x=200, y=130)

    Label(window, text="Amount:", font=("Arial", 11), bg="#ffffff").place(x=50, y=180)
    amount_entry = Entry(window, width=30)
    amount_entry.place(x=200, y=180)

    Label(window, text="Description:", font=("Arial", 11), bg="#ffffff").place(x=50, y=230)
    desc_entry = Entry(window, width=30)
    desc_entry.place(x=200, y=230)

    # BUTTONS
    Button(window, text="Add Expense", command=add_expense, width=25, bg="#4CAF50", fg="white").place(x=130, y=290)
    Button(window, text="View All Expenses", command=view_expenses, width=25, bg="#2196F3", fg="white").place(x=130, y=330)
    Button(window, text="Category Totals", command=show_total_by_category, width=25, bg="#9C27B0", fg="white").place(x=130, y=370)
    Button(window, text="Monthly Report", command=monthly_report, width=25, bg="#FF5722", fg="white").place(x=130, y=410)
    Button(window, text="Show Bar Chart", command=show_bar_chart, width=25, bg="#3F51B5", fg="white").place(x=130, y=450)
    Button(window, text="Edit/Delete Expense", command=edit_delete_screen, width=25, bg="#E91E63", fg="white").place(x=130, y=490)
    Button(window, text="Logout", command=logout, width=25, bg="#000000", fg="white").place(x=130, y=530)

    window.mainloop()


# ---------------------------------------------------
# LOGOUT FUNCTION (FIXED)
# ---------------------------------------------------

def logout():
    window.destroy()
    login_screen()


# ---------------------------------------------------
# LOGIN SCREEN
# ---------------------------------------------------

def login_screen():

    def verify():
        username = user_entry.get()
        password = pass_entry.get()

        if username == "admin" and password == "1234":
            login.destroy()
            main_window()
        else:
            messagebox.showerror("Error", "Invalid login details!")

    login = Tk()
    login.title("Login")
    login.geometry("300x200")

    Label(login, text="Username:").pack()
    user_entry = Entry(login)
    user_entry.pack()

    Label(login, text="Password:").pack()
    pass_entry = Entry(login, show="*")
    pass_entry.pack()

    Button(login, text="Login", command=verify, width=15, bg="green", fg="white").pack(pady=10)

    login.mainloop()


# ---------------------------------------------------
# START APPLICATION
# ---------------------------------------------------

login_screen()
