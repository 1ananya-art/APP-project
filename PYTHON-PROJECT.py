import mysql.connector as driver
import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext

class DatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Employee Database Management")
        
        # Create a menu
        self.menu_frame = tk.Frame(root)
        self.menu_frame.pack(pady=10)

        tk.Button(self.menu_frame, text="Create Database", command=self.create_database).grid(row=0, column=0, padx=10)
        tk.Button(self.menu_frame, text="Show Databases", command=self.show_databases).grid(row=0, column=1, padx=10)
        tk.Button(self.menu_frame, text="Create Table", command=self.create_table).grid(row=1, column=0, padx=10)
        tk.Button(self.menu_frame, text="Show Tables", command=self.show_tables).grid(row=1, column=1, padx=10)
        tk.Button(self.menu_frame, text="Insert Record", command=self.insert_record).grid(row=2, column=0, padx=10)
        tk.Button(self.menu_frame, text="Update Record", command=self.update_record).grid(row=2, column=1, padx=10)
        tk.Button(self.menu_frame, text="Delete Record", command=self.delete_record).grid(row=3, column=0, padx=10)
        tk.Button(self.menu_frame, text="Search Record", command=self.search_record).grid(row=3, column=1, padx=10)
        tk.Button(self.menu_frame, text="Display Records", command=self.display_record).grid(row=4, column=0, columnspan=2, pady=10)

        self.text_area = scrolledtext.ScrolledText(root, width=50, height=15)
        self.text_area.pack(pady=10)

    def clear_text_area(self):
        self.text_area.delete(1.0, tk.END)

    def show_message(self, message):
        messagebox.showinfo("Information", message)

    def create_database(self):
        con = driver.connect(host='localhost', user='root', passwd='musql#27_05#', charset='utf8')
        cur = con.cursor()
        cur.execute('create database if not exists employee')
        con.commit()
        con.close()
        self.show_message("Database Created")

    def show_databases(self):
        con = driver.connect(host='localhost', user='root', passwd='musql#27_05#', charset='utf8')
        cur = con.cursor()
        cur.execute('show databases')
        databases = cur.fetchall()
        con.close()
        self.clear_text_area()
        self.text_area.insert(tk.END, "Databases:\n" + "\n".join([db[0] for db in databases]))

    def create_table(self):
        con = driver.connect(host='localhost', user='root', passwd='musql#27_05#', charset='utf8', database='employee')
        cur = con.cursor()
        cur.execute('create table if not exists emp(id integer primary key, ename varchar(15), salary float)')
        con.commit()
        con.close()
        self.show_message("Table Created")

    def show_tables(self):
        con = driver.connect(host='localhost', user='root', passwd='musql#27_05#', charset='utf8', database='employee')
        cur = con.cursor()
        cur.execute('show tables')
        tables = cur.fetchall()
        con.close()
        self.clear_text_area()
        self.text_area.insert(tk.END, "Tables:\n" + "\n".join([table[0] for table in tables]))

    def insert_record(self):
        ID = simpledialog.askinteger("Input", "ENTER EMPLOYEE ID:")
        NAME = simpledialog.askstring("Input", "ENTER NAME OF EMPLOYEE:")
        SALARY = simpledialog.askfloat("Input", "ENTER EMPLOYEE SALARY:")
        
        if ID and NAME and SALARY is not None:
            con = driver.connect(host='localhost', user='root', passwd='musql#27_05#', charset='utf8', database='employee')
            cur = con.cursor()
            query = "INSERT INTO emp(id,ename,salary) VALUES(%s,%s,%s)"
            cur.execute(query, (ID, NAME, SALARY))
            con.commit()
            con.close()
            self.show_message('Record Inserted')

    def update_record(self):
        d = simpledialog.askinteger("Input", "Enter Employee ID for update record:")
        ID = simpledialog.askinteger("Input", "ENTER NEW EMPLOYEE ID:")
        NAME = simpledialog.askstring("Input", "ENTER NEW NAME OF EMPLOYEE:")
        SALARY = simpledialog.askfloat("Input", "ENTER NEW SALARY FOR EMPLOYEE:")
        
        if d and ID and NAME and SALARY is not None:
            con = driver.connect(host='localhost', user='root', passwd='musql#27_05#', charset='utf8', database='employee')
            cur = con.cursor()
            query = "UPDATE emp SET id=%s, ename=%s, salary=%s WHERE id=%s"
            cur.execute(query, (ID, NAME, SALARY, d))
            con.commit()
            con.close()
            self.show_message("Record Updated")

    def delete_record(self):
        d = simpledialog.askinteger("Input", "Enter Employee ID for deleting record:")
        if d is not None:
            con = driver.connect(host='localhost', user='root', passwd='musql#27_05#', charset='utf8', database='employee')
            cur = con.cursor()
            query = "DELETE FROM emp WHERE id=%s"
            cur.execute(query, (d,))
            con.commit()
            con.close()
            self.show_message("Record Deleted")

    def search_record(self):
        choice = simpledialog.askinteger("Input", "Search by:\n1. ID\n2. Name\n3. Salary\nEnter choice (1-3):")
        query = ""
        
        if choice == 1:
            d = simpledialog.askinteger("Input", "Enter Employee ID which you want to search:")
            query = "SELECT * FROM emp WHERE id=%s"
            param = (d,)
        elif choice == 2:
            name = simpledialog.askstring("Input", "Enter Employee Name which you want to search:")
            query = "SELECT * FROM emp WHERE ename=%s"
            param = (name,)
        elif choice == 3:
            sal = simpledialog.askfloat("Input", "Enter Employee Salary which you want to search:")
            query = "SELECT * FROM emp WHERE salary=%s"
            param = (sal,)
        
        if query:
            con = driver.connect(host='localhost', user='root', passwd='musql#27_05#', charset='utf8', database='employee')
            cur = con.cursor()
            cur.execute(query, param)
            records = cur.fetchall()
            con.close()
            self.clear_text_area()
            self.text_area.insert(tk.END, "Records Found:\n" + "\n".join(str(record) for record in records))

    def display_record(self):
        con = driver.connect(host='localhost', user='root', passwd='musql#27_05#', charset='utf8', database='employee')
        cur = con.cursor()
        cur.execute('SELECT * FROM emp')
        records = cur.fetchall()
        con.close()
        self.clear_text_area()
        self.text_area.insert(tk.END, "All Employee Records:\n" + "\n".join(str(record) for record in records))

if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseApp(root)
    root.mainloop()
