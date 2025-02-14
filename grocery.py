import sqlite3
import tkinter as tk
from tkinter import messagebox, scrolledtext

# Database setup
conn = sqlite3.connect('grocery_lists.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS GroceryLists (list_id INTEGER PRIMARY KEY, list_name TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS GroceryItems (item_id INTEGER PRIMARY KEY, list_id INTEGER, item_name TEXT)''')
conn.commit()

def add_list_and_items():
    if cursor.execute('SELECT COUNT(*) FROM GroceryLists').fetchone()[0] >= 6:
        messagebox.showwarning("Limit Reached", "You can only have 6 grocery lists!")
        return
    
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

    output_text.config(state=tk.NORMAL)
    output_text.delete(1.0, tk.END)
    
    for list_item in lists:
        output_text.insert(tk.END, f"\n[List] {list_item[1]}\n", 'list_style')
        cursor.execute('SELECT item_name FROM GroceryItems WHERE list_id = ?', (list_item[0],))
        items = cursor.fetchall()
        
        for item in items:
            output_text.insert(tk.END, f"  - {item[0]}\n", 'item_style')
    
    output_text.config(state=tk.DISABLED)

# UI setup
root = tk.Tk()
root.title("Grocery List App")
root.configure(bg="#f8f1f1")

frame = tk.Frame(root, bg="#d1e8e2")
frame.pack(pady=10, padx=10)

tk.Label(frame, text="List Name:", bg="#d1e8e2", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
list_name_entry = tk.Entry(frame, font=("Arial", 12))
list_name_entry.grid(row=0, column=1, padx=5, pady=5)

item_entries = []
for i in range(6):
    tk.Label(frame, text=f"Item {i+1}:", bg="#d1e8e2", font=("Arial", 12)).grid(row=i+1, column=0, padx=5, pady=5)
    entry = tk.Entry(frame, font=("Arial", 12))
    entry.grid(row=i+1, column=1, padx=5, pady=5)
    item_entries.append(entry)

add_button = tk.Button(frame, text="Add List", command=add_list_and_items, font=("Arial", 12), bg="#ffafcc", fg="black")
add_button.grid(row=7, column=0, columnspan=2, pady=10)

output_text = scrolledtext.ScrolledText(root, height=10, width=40, font=("Arial", 12), bg="#ffffff")
output_text.pack(pady=10, padx=10)
output_text.tag_config('list_style', foreground="blue", font=("Arial", 12, "bold"))
output_text.tag_config('item_style', foreground="green", font=("Arial", 11))

display_grocery_lists()

root.mainloop()
