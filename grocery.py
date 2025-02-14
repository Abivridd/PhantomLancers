import sqlite3
import tkinter as tk
from tkinter import messagebox

conn = sqlite3.connect('grocery_lists.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS GroceryLists (list_id INTEGER PRIMARY KEY, list_name TEXT)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS GroceryItems (item_id INTEGER PRIMARY KEY, list_id INTEGER, item_name TEXT)''')

conn.commit()
  
def add_list_and_items():
    list_name = list_name_entry.get()

    if not list_name:
        messagebox.showwarning("Input Error", "Please enter a list name!")
        return



    items = [item.get() for item in item_entries]
    if any(not item for item in items):
        messagebox.showwarning("Input Error", "Please fill all items!")
        return

    cursor.execute('INSERT INTO GroceryLists (list_name) VALUES (?)', (list_name,))
    list_id = cursor.lastrowid

    cursor.executemany('INSERT INTO GroceryItems (list_id, item_name) VALUES (?, ?)', [(list_id, item) for item in items])

    conn.commit()
 
    messagebox.showinfo("Success", "Grocery list added!")
    display_grocery_lists()

def display_grocery_lists():
    cursor.execute('SELECT * FROM GroceryLists')

    lists = cursor.fetchall()

    output_text.delete(1.0, tk.END)


    for list_item in lists:

        output_text.insert(tk.END, f"{list_item[1]}\n")
        cursor.execute('SELECT item_name FROM GroceryItems WHERE list_id = ?', (list_item[0],))
        items = cursor.fetchall()

        
        for item in items:
            output_text.insert(tk.END, f"  - {item[0]}\n")

root = tk.Tk()
root.title("Grocery List App")

frame = tk.Frame(root)
frame.pack(pady=10)

list_name_label = tk.Label(frame, text="List Name:")
list_name_label.grid(row=0, column=0)
list_name_entry = tk.Entry(frame)
list_name_entry.grid(row=0, column=1)

item_entries = [tk.Entry(frame) for _ in range(6)]
for i, entry in enumerate(item_entries):
    entry.grid(row=i+1, column=1)
    tk.Label(frame, text=f"Item {i+1}:").grid(row=i+1, column=0)

add_button = tk.Button(frame, text="Add List", command=add_list_and_items)

add_button.grid(row=7, column=0, columnspan=2, pady=10)

output_text = tk.Text(root, height=10, width=40)

output_text.pack(pady=10)

display_grocery_lists()

root.mainloop()
