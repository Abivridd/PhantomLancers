import sqlite3
import tkinter as tk
from tkinter import messagebox, scrolledtext

#conects to other db
conn = sqlite3.connect('grocery_lists.db')
cursor = conn.cursor()
#gabs things from the other db
cursor.execute('''CREATE TABLE IF NOT EXISTS GroceryLists (list_id INTEGER PRIMARY KEY, list_name TEXT)''')
#grabs things from the other db
cursor.execute('''CREATE TABLE IF NOT EXISTS GroceryItems (item_id INTEGER PRIMARY KEY, list_id INTEGER, item_name TEXT)''')

#coloses conection to other db
conn.commit()

#verefies only 6 lists
def list_and_stuff():
    if cursor.execute('SELECT COUNT(*) FROM GroceryLists').fetchone()[0] >= 6:
        messagebox.showwarning("Limit Reached", "You can only have 6 grocery lists!")
        return
    
#names the list
    list_n = list_name_entry.get()
    if not list_n:
        messagebox.showwarning("Input Error", "Please enter a list name!")
        return

#items entry stuff
    items = [item.get() for item in item_entries]
    if any(not item for item in items):
        messagebox.showwarning("Input Error", "Please fill all items!")
        return

#saves item to db
    cursor.execute('INSERT INTO GroceryLists (list_name) VALUES (?)', (list_n,))
#gets the new vakue of row
    list_id = cursor.lastrowid
#runs whatever is mentioned
    cursor.executemany('INSERT INTO GroceryItems (list_id, item_name) VALUES (?, ?)', [(list_id, item) for item in items])
#colses connection
    conn.commit()
#shows list ins added to db
    messagebox.showinfo("Success", "Grocery list added!")
    display_grocery_lists()
#shows gocery lists
def display_grocery_lists():
    cursor.execute('SELECT * FROM GroceryLists')
    lists = cursor.fetchall()

#configers to make it to normal state
    output_text.config(state=tk.NORMAL)
#dels the end state
    output_text.delete(1.0, tk.END)
 # first put it on tkinter screen then gets everything from the db
    for list_item in lists:
        output_text.insert(tk.END, f"\n[List] {list_item[1]}\n", 'list_style')
        cursor.execute('SELECT item_name FROM GroceryItems WHERE list_id = ?', (list_item[0],))
        items = cursor.fetchall()
#dislays on tkinter screen
        for item in items:
            output_text.insert(tk.END, f"  - {item[0]}\n", 'item_style')
#configers to disabled state
    output_text.config(state=tk.DISABLED)
#main sreen definition
root = tk.Tk()
#puts title
root.title("Grocery List db")
#maeks a frame then puts pale aqua as colour
frame = tk.Frame(root, bg="#d1e8e2")
frame.pack(pady=10, padx=10)
#labels everything and also take input then defs grid
tk.Label(frame, text="List Name:", bg="#d1e8e2", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
list_name_entry = tk.Entry(frame, font=("Arial", 12))
list_name_entry.grid(row=0, column=1, padx=5, pady=5)
#sets item entryes empty
item_entries = []
#runs oly 6 times
for i in range(6):
    #labels takes entry grides it and apendes to the emplty list
    tk.Label(frame, text=f"Item {i+1}:", bg="#d1e8e2", font=("Arial", 12)).grid(row=i+1, column=0, padx=5, pady=5)
    entry = tk.Entry(frame, font=("Arial", 12))
    entry.grid(row=i+1, column=1, padx=5, pady=5)
    item_entries.append(entry)
#clears database
def clear_database():
    cursor.execute('DELETE FROM GroceryLists')
    cursor.execute('DELETE FROM GroceryItems')
    conn.commit()
    messagebox.showinfo("Database Cleared", "All grocery lists and items have been deleted!")
    display_grocery_lists()
#makes buttons
add_button = tk.Button(frame, text="Add List", command=list_and_stuff, font=("Arial", 12), bg="#ffafcc", fg="black")
add_button.grid(row=7, column=0, columnspan=2, pady=10)
clear_button = tk.Button(frame, text="Clear lists", command=clear_database, font=("Arial", 12), bg="#ff6961", fg="white")
clear_button.grid(row=8, column=0, columnspan=2, pady=10)
#shows the scroll bar with the lsits
output_text = scrolledtext.ScrolledText(root, height=10, width=40, font=("Arial", 12), bg="#ffffff")
output_text.pack(pady=10, padx=10)
output_text.tag_config('list_style', foreground="blue", font=("Arial", 12, "bold"))
output_text.tag_config('item_style', foreground="green", font=("Arial", 11))
#desplayes the grocey list
display_grocery_lists()
#runs it infinitly
root.mainloop()
#end of the dowikey
