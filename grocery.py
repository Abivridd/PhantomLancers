import sqlite3

import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
from fpdf import FPDF

from collections import Counter

root = tk.Tk()
root.title("Grocery List App")
root.geometry("1000x1150")
root.configure(bg="#f9f9f9")
main_frame = tk.Frame(root, bg="#f0f0f0", padx=10, pady=10)
main_frame.pack(fill=tk.BOTH, expand=True)

conn = sqlite3.connect('grocery_lists.db')
cursor = conn.cursor()



cursor.execute('''CREATE TABLE IF NOT EXISTS GroceryLists (list_id INTEGER PRIMARY KEY, list_name TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS GroceryItems (item_id INTEGER PRIMARY KEY, list_id INTEGER, item_name TEXT)''')
conn.commit()

def save_lists_to_pdf():
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)


    pdf.add_page()
    pdf.set_font("Arial", style="B", size=16)
    pdf.cell(200, 10, "Grocery Lists", ln=True, align="C")
    pdf.ln(10)



    cursor.execute('SELECT * FROM GroceryLists')
    lists = cursor.fetchall()

    for list_item in lists:
        pdf.set_font("Arial", style="B", size=14)
        pdf.cell(200, 10, f"{list_item[1]}", ln=True)



        cursor.execute('SELECT item_name FROM GroceryItems WHERE list_id = ?', (list_item[0],))
        items = cursor.fetchall()
        pdf.set_font("Arial", size=12)
        for item in items:
            pdf.cell(200, 10, f" - {item[0]}", ln=True)
        pdf.ln(5)


    pdf.output("Grocery_Lists.pdf")



    messagebox.showinfo("Success", "Grocery lists saved as PDF!")
    show_main_frame()




def clear_db():
    cursor.execute("DELETE FROM GroceryItems")
    cursor.execute("DELETE FROM GroceryLists")
    conn.commit()
    messagebox.showinfo("Database Cleared", "All grocery lists have been deleted!")
    display_grocery_lists()
    show_main_frame()

def remove_last_item_entry():
    if item_entries:
        entry = item_entries.pop()
        entry.destroy()
    else:
        messagebox.showwarning("Error", "No more items to remove!")

def remove_list():
    cursor.execute("DELETE FROM GroceryLists WHERE list_id = (SELECT MAX(list_id) FROM GroceryLists)")
    conn.commit()
    display_grocery_lists()

def confirm_clear_db():
    main_frame.pack_forget()
    confirm_frame.pack(fill=tk.BOTH, expand=True)

def show_main_frame():
    confirm_frame.pack_forget()
    main_frame.pack(fill=tk.BOTH, expand=True)



confirm_frame = tk.Frame(root, bg="#f0f0f0", padx=10, pady=10)


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
    output_text.config(state=tk.NORMAL)
    output_text.delete(1.0, tk.END)

    cursor.execute('SELECT * FROM GroceryLists')
    lists = cursor.fetchall()

    for list_item in lists:
        output_text.insert(tk.END, f"\n📌 {list_item[1]}\n", 'list_style')
        cursor.execute('SELECT item_name FROM GroceryItems WHERE list_id = ?', (list_item[0],))
        items = cursor.fetchall()
        
        for item in items:
            output_text.insert(tk.END, f"   • {item[0]}\n", 'item_style')

    output_text.config(state=tk.DISABLED)

def add_item_entry():
    if len(item_entries) < 6: 
        entry = tk.Entry(main_frame, font=("Arial", 12), width=25)
        entry.pack(pady=1)
        item_entries.append(entry)
    else:
        messagebox.showwarning("Limit Reached", "Maximum of 6 items per list!")

def final_list():
    
    cursor.execute("SELECT item_name FROM GroceryItems")
    items = [item[0] for item in cursor.fetchall()]

    if not items:
        messagebox.showinfo("no items", "No items found in the grocery lists")
        return
    
    items = Counter(items)
    sorted_items = sorted(items.items(), key=lambda x: x[1], reverse=True)[:6]
    final_list_text.config(state=tk.NORMAL)
    final_list_text.delete(1.0, tk.END)
    final_list_text.insert(tk.END, "🥇 grocery list:\n", 'common_style')

    for item, count in sorted_items:
        final_list_text.insert(tk.END, f"   • {item}\n", 'common_item_style')

    final_list_text.config(state=tk.DISABLED)

    messagebox.showinfo("not enough lists","least required 2 lists")

tk.Label(main_frame, text="📝 List Name:", bg="#f0f0f0", font=("Arial", 14, "bold")).pack(anchor="w", pady=(0, 5))
list_name_entry = tk.Entry(main_frame, font=("Arial", 12), width=25)
list_name_entry.pack(pady=2)

tk.Label(main_frame, text="🛒 Add Items:", bg="#f0f0f0", font=("Arial", 14, "bold")).pack(anchor="w", pady=(10, 5))
item_entries = []
add_item_entry()

tk.Button(main_frame, text="➕ Add More Items", command=add_item_entry, font=("Arial", 12), bg="#d1e8e2").pack(pady=3)
tk.Button(main_frame, text="➖ Remove Last Item", command=remove_last_item_entry, font=("Arial", 12), bg="#ffaaaa").pack(pady=4)
tk.Button(main_frame, text="✅ Save List", command=add_list_and_items, font=("Arial", 14, "bold"), bg="#ffafcc").pack(pady=3, padx=2)
tk.Button(main_frame, text="📊 make list", command=final_list, font=("Arial", 14, "bold"), bg="#87CEFA").pack(pady=5)

output_text = scrolledtext.ScrolledText(main_frame, height=12, width=50, font=("Arial", 12), bg="#ffffff")
output_text.pack(pady=3, padx=3)

final_list_text = scrolledtext.ScrolledText(main_frame, height=5, width=50, font=("Arial", 12), bg="#ffffff")
final_list_text.pack(pady=5, padx=5)

delete_frame = tk.Frame(main_frame, bg="#f0f0f0")
delete_frame.pack(pady=5)

tk.Button(delete_frame, text="🗑 Remove Last List", command=remove_list, font=("Arial", 12), bg="#ff5555").pack(side=tk.LEFT, padx=5)
tk.Button(delete_frame, text="🗑 Clear DB", command=confirm_clear_db, font=("Arial", 12), bg="#ff5555").pack(side=tk.LEFT, padx=5)

tk.Label(confirm_frame, text="Do you want to get a copy of the lists before you delete them?", bg="#f0f0f0", font=("Arial", 12, "bold")).pack(pady=20)
button_frame = tk.Frame(confirm_frame, bg="#f0f0f0")
button_frame.pack()
tk.Button(button_frame, text="Yes", command=save_lists_to_pdf, font=("Arial", 12), bg="#d1e8e2", width=10).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="No", command=clear_db, font=("Arial", 12), bg="#ffaaaa", width=10).pack(side=tk.LEFT, padx=5)

display_grocery_lists()
root.mainloop()
