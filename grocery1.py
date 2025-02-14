import sqlite3
import tkinter 
import tkinter as tk

root = tk.Tk()
list1 = tk.Frame()

conn = sqlite3.connect('grocery_lists.db')
cursor = conn.cursor()


cursor.execute('''
CREATE TABLE IF NOT EXISTS GroceryLists (
    list_id INTEGER PRIMARY KEY,
    list_name TEXT NOT NULL
);
''')
 







cursor.execute('''
CREATE TABLE IF NOT EXISTS GroceryItems (
    item_id INTEGER PRIMARY KEY,
    list_id INTEGER,
    item_name TEXT NOT NULL,
    FOREIGN KEY (list_id) REFERENCES GroceryLists (list_id)
);
''')


conn.commit()


import sqlite3


conn = sqlite3.connect('grocery_lists.db')
cursor = conn.cursor()


cursor.execute('''
CREATE TABLE IF NOT EXISTS GroceryLists (
    list_id INTEGER PRIMARY KEY,
    list_name TEXT NOT NULL
);
''')





cursor.execute('''
CREATE TABLE IF NOT EXISTS GroceryItems (
    item_id INTEGER PRIMARY KEY,
    list_id INTEGER,
    item_name TEXT NOT NULL,
    FOREIGN KEY (list_id) REFERENCES GroceryLists (list_id)
);
''')


conn.commit()



def add_grocery_list(list_name):
    cursor.execute('''
    INSERT INTO GroceryLists (list_name)
    VALUES (?);
     ''', (list_name,))
   
   
    conn.commit()
    return cursor.lastrowid 

def add_items_to_list(list_id, items):
    for item in items:
        
        cursor.execute('''
   
        INSERT INTO GroceryItems (list_id, item_name)
        VALUES (?, ?);
        ''', (list_id, item))
    conn.commit()


def display_grocery_lists():

    cursor.execute('SELECT * FROM GroceryLists')



    lists = cursor.fetchall()
    print("\nYour Grocery Lists and Items:")


    for list_item in lists:
        print(f"\nList: {list_item[1]} (ID: {list_item[0]})")
        cursor.execute('SELECT item_name FROM GroceryItems WHERE list_id = ?', (list_item[0],))
        items = cursor.fetchall()
        for idx, item in enumerate(items, 1):
            print(f"  {idx}. {item[0]}")


for i in range(6):
    list_name = input(f"\nEnter the name of grocery list #{i+1}: ")
    items = []
    print(f"Enter 6 items for the list '{list_name}':")
    for j in range(6):
        item = input(f"  Item #{j+1}: ")
        items.append(item)
    

    list_id = add_grocery_list(list_name)
    add_items_to_list(list_id, items)


display_grocery_lists()

conn.close()

def add_grocery_list(list_name):
    cursor.execute('''
    INSERT INTO GroceryLists (list_name)
    VALUES (?);
   
     ''', (list_name,))
   
   
    conn.commit()

    return cursor.lastrowid 

def add_items_to_list(list_id, items):
    
    for item in items:
        
        cursor.execute('''
   
        INSERT INTO GroceryItems (list_id, item_name)
        VALUES (?, ?);
        ''', (list_id, item))
    conn.commit()


def display_grocery_lists():

    cursor.execute('SELECT * FROM GroceryLists')



    lists = cursor.fetchall()
    print("\nYour Grocery Lists and Items:")


    for list_item in lists:
        print(f"\nList: {list_item[1]} (ID: {list_item[0]})")
        cursor.execute('SELECT item_name FROM GroceryItems WHERE list_id = ?', (list_item[0],))
        items = cursor.fetchall()
        for idx, item in enumerate(items, 1):
            print(f"  {idx}. {item[0]}")


for i in range(6):
    list_name = input(f"\nEnter the name of grocery list #{i+1}: ")
    items = []
    print(f"Enter 6 items for the list '{list_name}':")
    for j in range(6):
        item = input(f"  Item #{j+1}: ")
        items.append(item)
    

    list_id = add_grocery_list(list_name)
    add_items_to_list(list_id, items)


display_grocery_lists()

conn.close()


