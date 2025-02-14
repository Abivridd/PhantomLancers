import sqlite3
import tkinter as tk
from tkinter import messagebox, scrolledtext


conn = sqlite3.connect('grocery_lists.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS GroceryLists (list_id INTEGER PRIMARY KEY, list_name TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS GroceryItems (item_id INTEGER PRIMARY KEY, list_id INTEGER, item_name TEXT)''')
conn.commit()

def add_list_and_items():
    if cursor.execute('SELECT COUNT(*) FROM GroceryLists').fetchone()[0] >= 6:
        messagebox.showwarning("Limit Reached", "You can only have 6 grocery lists!")
        return
    
    list_name = list_name_entry.get().strip()
    if not list_name:
        messagebox.showwarning("Input Error", "Please enter a list name!")
        return

    items = [entry.get().strip() for entry in item_entries if entry.get().strip()]
    if not items:
        messagebox.showwarning("Input Error", "Please add at least one item!")
        return

    cursor.execute('INSERT INTO GroceryLists (list_name) VALUES (?)', (list_name,))
    list_id = cursor.lastrowid
    cursor.executemany('INSERT INTO GroceryItems (list_id, item_name) VALUES (?, ?)', [(list_id, item) for item in items])
    conn.commit()
    
    messagebox.showinfo("Success", "Grocery list added successfully!")
    
    list_name_entry.delete(0, tk.END)
    for entry in item_entries:
        entry.destroy()
    item_entries.clear()
    add_item_entry()
    
    display_grocery_lists()

def display_grocery_lists():
    cursor.execute('SELECT * FROM GroceryLists')
    lists = cursor.fetchall()

    output_text.config(state=tk.NORMAL)
    output_text.delete(1.0, tk.END)
    
    for list_item in lists:
        output_text.insert(tk.END, f"\n📌 {list_item[1]}\n", 'list_style')
        cursor.execute('SELECT item_name FROM GroceryItems WHERE list_id = ?', (list_item[0],))
        items = cursor.fetchall()
        
        for item in items:
            output_text.insert(tk.END, f"   • {item[0]}\n", 'item_style')
    
    output_text.config(state=tk.DISABLED)

def add_item_entry():
    if len(item_entries) < 10: 
        entry = tk.Entry(frame, font=("Arial", 12), width=25)
        entry.pack(pady=2)
        item_entries.append(entry)
    else:
        messagebox.showwarning("Limit Reached", "Maximum of 10 items per list!")


root = tk.Tk()
root.title("Grocery List App")
root.geometry("450x600")
root.configure(bg="#f9f9f9")

frame = tk.Frame(root, bg="#f0f0f0", padx=10, pady=10)
frame.pack(pady=10, padx=10, fill=tk.BOTH)

tk.Label(frame, text="📝 List Name:", bg="#f0f0f0", font=("Arial", 14, "bold")).pack(anchor="w", pady=(0, 5))
list_name_entry = tk.Entry(frame, font=("Arial", 12), width=30)
list_name_entry.pack(pady=5)

tk.Label(frame, text="🛒 Add Items:", bg="#f0f0f0", font=("Arial", 14, "bold")).pack(anchor="w", pady=(10, 5))
item_entries = []
add_item_entry()


add_item_btn = tk.Button(frame, text="➕ Add More Items", command=add_item_entry, font=("Arial", 12), bg="#d1e8e2", fg="black")
add_item_btn.pack(pady=5)

add_button = tk.Button(frame, text="✅ Save List", command=add_list_and_items, font=("Arial", 14, "bold"), bg="#ffafcc", fg="black")
add_button.pack(pady=10)

output_text = scrolledtext.ScrolledText(root, height=12, width=50, font=("Arial", 12), bg="#ffffff")
output_text.pack(pady=10, padx=10)
output_text.tag_config('list_style', foreground="#0000ff", font=("Arial", 12, "bold"))
output_text.tag_config('item_style', foreground="#008000", font=("Arial", 11))

display_grocery_lists()
root.mainloop()
