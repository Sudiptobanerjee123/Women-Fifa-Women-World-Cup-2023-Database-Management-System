import pymysql
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import Toplevel, Button
from tkinter import Tk, ttk, Frame, Button, Label, Canvas


def connection(database_name):
    # Establish a connection to the MySQL database
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db=database_name,
    )
    return conn


# Back to Home button
def back_to_home(root, home_page_function):
    # Destroy all widgets in the current window
    for widget in root.winfo_children():
        widget.destroy()

    # Recreate the Home Page
    home_page_function(root)

# Generate the advanced SQL queries

def display_query_result(queries, columns_list, database_name, home_page_function):
    root = tk.Tk()
    root.title("Women Fifa World Cup 2023 ⚽️")
    width, height = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry('%dx%d+0+0' % (width, height))

    navbar_frame = Frame(root, bd=2, relief="solid", bg="#3498db")
    navbar_frame.grid(row=0, column=0, columnspan=13, sticky="nsew")

    label = Label(navbar_frame, text="Women Fifa World Cup 2023 ⚽️",
                  font=('Georgia Bold', 32), bg="#3498db", fg="white")
    label.grid(padx=500, pady=20)
    navbar_frame.grid_rowconfigure(0, weight=1)
    navbar_frame.grid_columnconfigure(0, weight=1)

    for i, (query, columns) in enumerate(zip(queries, columns_list)):
        tree_frame = tk.Frame(root, bd=6, relief="solid", background="#A9DFBF")
        tree_frame.grid(row=i+1, column=0, padx=150, pady=2, columnspan=5)

        my_tree = ttk.Treeview(tree_frame)
        my_tree['columns'] = columns

        # Configure style
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Helvetica Bold', 15))

        # Grid configuration
        my_tree.column("#0", width=0, stretch=tk.NO)
        for col in my_tree['columns']:
            my_tree.column(col, anchor=tk.W, width=200)
            my_tree.heading(col, text=col, anchor=tk.W)

        my_tree.grid(row=0, column=0, sticky="nsew")

        # Add a scrollbar
        tree_scroll = ttk.Scrollbar(
            tree_frame, orient="vertical", command=my_tree.yview)
        tree_scroll.grid(row=0, column=1, sticky="nsew")
        my_tree.configure(yscrollcommand=tree_scroll.set)

        # Execute query and insert data into the tree
        conn = connection(database_name)
        cursor = conn.cursor()
        cursor.execute(queries[i])
        results = cursor.fetchall()
        conn.commit()
        conn.close()

        for index, row in enumerate(results):
            my_tree.insert(parent='', index='end', iid=index,
                           text="", values=row, tag="orow")

        my_tree.tag_configure('orow', background='#EEEEEE', font=('Arial', 10))

    # Back button to navigate to home
    backBtn = tk.Button(
        root, text="Back to Home", padx=17, pady=7, width=7,
        bd=5, font=('Georgia', 16, 'bold'), bg="#FF9999", command=lambda: back_to_home(root, home_page_function))
    backBtn.grid(row=2, column=2, rowspan=2, columnspan=15, pady=4)


def display_database_system(database_name, table_name, entry_columns, labels, home_page_function):
    # Function to set placeholder text for entry widgets
    def set_ph(word, num):
        ph_list[num - 1].set(word)

    # Function to read data from the database
    def read():
        conn = connection(database_name)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        results = cursor.fetchall()
        conn.commit()
        conn.close()
        return results

    # Function to add data to the database
    def add():
        entry_values = [entry.get() for entry in entries]

        if any(not data.strip() for data in entry_values):
            messagebox.showinfo("Error", "Please fill up all the fields.")
            return
        else:
            try:
                conn = connection(database_name)
                cursor = conn.cursor()
                cursor.execute(f"INSERT INTO {table_name} VALUES ({
                               ', '.join(['%s']*len(entry_values))})", tuple(entry_values))
                conn.commit()
                conn.close()
            except pymysql.IntegrityError:
                messagebox.showinfo(
                    "Error", f"{table_name.capitalize()} already exists.")
                return

        clear_entry_fields()
        refresh_table()

    # Function to clear entry fields
    def clear_entry_fields():
        for ph, entry in zip(ph_list, entries):
            ph.set("")
            entry.delete(0, 'end')

    # Function to reset data in the table
    def reset():
        decision = messagebox.askquestion("Warning!!", f"Delete all data from {
                                          table_name.capitalize()}?")
        if decision == "yes":
            try:
                conn = connection(database_name)
                cursor = conn.cursor()
                cursor.execute(f"DELETE FROM {table_name}")
                conn.commit()
                conn.close()
            except:
                messagebox.showinfo("Error", "Sorry, an error occurred.")
                return

            refresh_table()

    # Function to delete selected data
    def delete():
        decision = messagebox.askquestion(
            "Warning!!", f"Delete the selected data from {table_name.capitalize()}?")
        if decision == "yes":
            try:
                conn = connection(database_name)
                cursor = conn.cursor()
                selected_item = my_tree.selection()[0]
                delete_data = my_tree.item(selected_item)['values'][0]
                cursor.execute(f"DELETE FROM {table_name} WHERE {
                               table_name.lower()}ID = %s", (delete_data,))
                conn.commit()
                conn.close()
            except:
                messagebox.showinfo("Error", "Sorry, an error occurred.")
                return

            refresh_table()

    # Function to update selected data
    def update():
        decision = messagebox.askquestion(
            "Warning!!", f"Update the selected data from {table_name.capitalize()}?")
        if decision == "yes":
            try:
                selected_item = my_tree.selection()[0]
                selected_entry_id = my_tree.item(selected_item)['values'][0]
            except IndexError:
                messagebox.showinfo("Error", "Please select a data row.")
                return

            entry_values = [entry.get() for entry in entries]

            if any(not data.strip() for data in entry_values):
                messagebox.showinfo("Error", "Please fill up all the fields.")
                return
            else:
                try:
                    conn = connection(database_name)
                    cursor = conn.cursor()
                    cursor.execute(f"UPDATE {table_name} SET {table_name.lower()}ID = %s, "
                                   + ', '.join([f"{col} = %s" for col in entry_columns[1:]])
                                   + f" WHERE {table_name.lower()}ID = %s",
                                   tuple(entry_values + [selected_entry_id]))
                    conn.commit()
                    conn.close()
                except pymysql.IntegrityError:
                    messagebox.showinfo(
                        "Error", f"{table_name.capitalize()} already exists.")
                    return

        clear_entry_fields()
        refresh_table()

    # Function to refresh the table
    def refresh_table():
        for data in my_tree.get_children():
            my_tree.delete(data)

        for array in read():
            my_tree.insert(parent='', index='end', iid=array,
                           text="", values=(array), tag="orow")

        my_tree.tag_configure('orow', background='#EEEEEE', font=('Arial', 12))
        my_tree.grid(row=4, column=0, columnspan=5,
                     rowspan=5, padx=10, pady=10)

    # Initialize the root window
    root = tk.Tk()
    root.title("Women Fifa World Cup 2023 ⚽️")
    width, height = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry('%dx%d+0+0' % (width, height))

    # Placeholders for entry
    ph_list = [tk.StringVar() for _ in entry_columns]

    # Navbar Frame
    navbar_frame = tk.Frame(root, bd=2, relief="solid", bg="#3498db")
    navbar_frame.grid(row=0, column=0, columnspan=13, sticky="nsew")

    # Create a label inside the frame
    label = tk.Label(navbar_frame, text=f"Women Fifa World Cup 2023 ⚽️  ({table_name.capitalize()})",
                     font=('Georgia Bold', 30), bg="#3498db", fg="white")
    label.grid(padx=500, pady=20)

    # To center the label horizontally and vertically
    navbar_frame.grid_rowconfigure(0, weight=1)
    navbar_frame.grid_columnconfigure(0, weight=1)

    # Create a frame for labels and entry widgets
    input_frame = tk.Frame(root, bd=8, relief="solid", bg="#A9DFBF")
    input_frame.grid(row=3, column=0, padx=300,
                     pady=30, columnspan=5, sticky="w")

    # Entry widgets
    entries = [tk.Entry(input_frame, width=30, bd=5, font=('Arial', 15), textvariable=ph, bg="lightgrey")
               for ph in ph_list]

    for i, label_text in enumerate(labels):
        label = tk.Label(input_frame, text=label_text, font=(
            'Helvetica', 18, 'bold'), bg="#A9DFBF", fg="black")
        label.grid(row=i, column=0, columnspan=1, pady=5, sticky="ew")
        entries[i].grid(row=i, column=1, padx=5, pady=0)

    # Buttons
    addBtn = tk.Button(
        root, text="Create", padx=15, pady=15, width=3,
        bd=5, font=('Georgia', 22, 'bold'), bg="#3498db", command=add)
    addBtn.grid(row=2, column=1, rowspan=2, columnspan=20, pady=4, padx=20)

    updateBtn = tk.Button(
        root, text="Update", padx=15, pady=15, width=3,
        bd=5, font=('Georgia', 22, 'bold'), bg="#84E8F8", command=update)
    updateBtn.grid(row=2, column=2, rowspan=2, columnspan=20, pady=10)

    deleteBtn = tk.Button(
        root, text="Delete", padx=15, pady=15, width=3,
        bd=5, font=('Georgia', 22, 'bold'), bg="#FF9999", command=delete)
    deleteBtn.grid(row=2, column=3, rowspan=2, columnspan=20, pady=4)

    backBtn = tk.Button(
        root, text="Back to Home", padx=17, pady=7, width=7,
        bd=5, font=('Georgia', 16, 'bold'), bg="#FF9999", command=lambda: back_to_home(root, home_page_function))
    backBtn.grid(row=3, column=2, rowspan=2, columnspan=15, pady=4)

    # Tree View
    tree_frame = tk.Canvas(root, bd=6, relief="solid", background="#A9DFBF")
    tree_frame.grid(row=4, column=0, padx=150, pady=0,
                    columnspan=5, sticky="nsew")

    my_tree = ttk.Treeview(tree_frame)
    my_tree['columns'] = entry_columns

    # Configure style
    style = ttk.Style()
    style.configure("Treeview.Heading", font=('Helvetica Bold', 15))

    # Grid configuration
    my_tree.column("#0", width=0, stretch=tk.NO)
    for col in my_tree['columns']:
        my_tree.column(col, anchor=tk.W, width=120)
        my_tree.heading(col, text=col, anchor=tk.W)

    my_tree.grid(row=0, column=0, sticky="nsew")

    # Add a scrollbar
    tree_scroll = ttk.Scrollbar(
        tree_frame, orient="vertical", command=my_tree.yview)
    tree_scroll.grid(row=5, column=2, rowspan=1000, sticky="nsew")
    my_tree.configure(yscrollcommand=tree_scroll.set)

    # Update weights for resizing
    tree_frame.grid_rowconfigure(0, weight=1)
    tree_frame.grid_columnconfigure(0, weight=1)
    refresh_table()
    root.mainloop()
