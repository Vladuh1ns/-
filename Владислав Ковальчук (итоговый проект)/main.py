import tkinter as tk        
from tkinter import ttk     
import sqlite3              

# Класс главного окна
class Main(tk.Frame):
    def __init__(self, root):                              
        super().__init__(root)                              
        self.init_main()                                    
        self.db = db                                        
        self.view_records()                                 
    # Создание и работа с главным окном
    def init_main(self):                                    

        # Создаем панель инструментов
        toolbar = tk.Frame(bg="#d7d8e0", bd=2)
        # упаковка              
        toolbar.pack(side=tk.TOP, fill=tk.X)                

        # СОЗДАНИЕ КНОПОК
        self.add_img = tk.PhotoImage(file="./img/add.png")  
        btn_open_dialog = tk.Button(
            toolbar, bg="#d7d8e0", bd=0, image=self.add_img, command=self.open_dialog
        )
        btn_open_dialog.pack(side=tk.LEFT)                  

        # Добавляем столбцы
        self.tree = ttk.Treeview(
            self, columns=("ID", "name", "tel", "email","salary"), height=45, show="headings"
        )
        # Устанавливаем размеры столбцов и выравниваем по центру
        self.tree.column("ID", width=30, anchor=tk.CENTER)          
        self.tree.column("name", width=300, anchor=tk.CENTER)       
        self.tree.column("tel", width=150, anchor=tk.CENTER)        
        self.tree.column("email", width=150, anchor=tk.CENTER)      
        self.tree.column("salary", width=90, anchor=tk.CENTER)      
        # Задаем именна
        self.tree.heading("ID", text="ID")                          
        self.tree.heading("name", text="ФИО")                       
        self.tree.heading("tel", text="Телефон")                    
        self.tree.heading("email", text="E-mail")                   
        self.tree.heading("salary", text="Зарплата")                   
        # Размещение таблицы в окне
        self.tree.pack(side=tk.LEFT)                                

        # Загрузили изображение кнопки обновления в переменнную
        self.update_img = tk.PhotoImage(file="./img/update.png")    
        # Создали кнопку
        # 1- привязали к панели инструментов
        # 2- установили цвет фона
        # 3- установили размер рамки
        # 4- установили иконку
        # 5- вызываем функцию,которая сработает при нажатии этой кнопки
        btn_edit_dialog = tk.Button(
            toolbar,
            bg="#d7d8e0",
            bd=0,
            image=self.update_img,
            command=self.open_update_dialog,
        )
        btn_edit_dialog.pack(side=tk.LEFT)                          # Размещение кнопку в окне, указывавая гду она(кнопка) будет находиться


        self.delete_img = tk.PhotoImage(file="./img/delete.png")    # Загрузили изображение кнопки обновления в переменнную
        # Создали кнопку
        # 1 - привязали к панели инструментов
        # 2- установили цвет фона
        # 3- установили размер рамки
        # 4- установили иконку
        # 5- вызываем функцию,которая сработает при нажатии этой кнопки
        btn_delete = tk.Button(
            toolbar,
            bg="#d7d8e0",
            bd=0,
            image=self.delete_img,
            command=self.delete_records,
        )
        btn_delete.pack(side=tk.LEFT)                               # Размещение кнопку в окне, указывавая гду она(кнопка) будет находиться


        self.search_img = tk.PhotoImage(file="./img/search.png")    # Загрузили изображение кнопки обновления в переменнную
        # Создали кнопку
        # 1 - привязали к панели инструментов
        # 2- установили цвет фона
        # 3- установили размер рамки
        # 4- установили иконку
        # 5- вызываем функцию,которая сработает при нажатии этой кнопки
        btn_search = tk.Button(
            toolbar,
            bg="#d7d8e0",
            bd=0,
            image=self.search_img,
            command=self.open_search_dialog,
        )
        btn_search.pack(side=tk.LEFT)                                                   # Размещение кнопку в окне, указывавая где она(кнопка) будет находиться

    def open_dialog(self):                                                              # Метод open_dialog
        Child()                                                                         # Вызвали класс, отвечающий за добавление данных в ьазу данных

    def records(self, name, tel, email,salary ):
        self.db.insert_data(name, tel, email,salary )                                   #Вызвали функцию добавления данных в базу данных
        self.view_records()                                                             #Вызвали функцию обновления данных и вывода данных на окно

    def view_records(self):
        self.db.cursor.execute("SELECT * FROM Employees")                                      #Запрос: Выбираем все данные из таблицы
        [self.tree.delete(i) for i in self.tree.get_children()]                         #Старые данные удаляем
        [self.tree.insert("", "end", values=row) for row in self.db.cursor.fetchall()]  #Вписываем новые данные в бд

    def open_update_dialog(self):
        Update()                                                                        # Вызываем класс

    def update_records(self, name, tel, email, salary):
        self.db.cursor.execute(                                                         # Запрос на обновление
            """UPDATE Employees SET name=?, tel=?, email=?, salary=? WHERE id=?""",

            # Передаём аргуметы на места "?"(первую выделенную строку, берём значение первого столбца)
            (name, tel, email,salary, self.tree.set(self.tree.selection()[0], "#1")),
        )
        self.db.conn.commit()                                                           # Сохраняем запрос
        self.view_records()                                                             # Вызываем функцию класса

    def delete_records(self):
        for selection_items in self.tree.selection():
            self.db.cursor.execute(                                                     # Запрос на удаление строки с таким-то id
                "DELETE FROM Employees WHERE id=?", (self.tree.set(selection_items, "#1"))     # Передаём аргумет на место "?"
            )
        self.db.conn.commit()                                                           # Сохраняем запрос
        self.view_records()                                                             # Вызываем функцию класса

    def open_search_dialog(self):
        Search()                                                                        # Вызываем класс

    def search_records(self, name):
        name = "%" + name + "%"                                                         # Доюавляем к строчке знаки процента
        self.db.cursor.execute("SELECT * FROM Employees WHERE name LIKE ?", (name,))           # Сюда передаем кортеж (name), а не просто name

        [self.tree.delete(i) for i in self.tree.get_children()]                         # Старые данные удаляем
        [self.tree.insert("", "end", values=row) for row in self.db.cursor.fetchall()]  # Вписываем новые данные в бд

# Создание окна ДОБАВЛЕНИЯ
class Child(tk.Toplevel):                                   
    def __init__(self):                                     
        super().__init__(root)                              
        self.init_child()                                   
        self.view = app
    # инициализация виджетов дочернего окна
    def init_child(self):
        self.title("Добавить сотрудника")                   
        self.geometry("400x220")                            
        self.resizable(False, False)                        

        self.grab_set()                                     
        self.focus_set()                                    
        # Текст
        label_name = tk.Label(self, text="ФИО:")            
        label_name.place(x=50, y=50)                        
        label_select = tk.Label(self, text="Телефон:")      
        label_select.place(x=50, y=80)                      
        label_sum = tk.Label(self, text="E-mail:")          
        label_sum.place(x=50, y=110)                        

        label_salary = tk.Label(self, text="Зарплата:")          
        label_salary.place(x=50, y=140)                        

        # Виджеты ввода
        self.entry_name = ttk.Entry(self)                   
        self.entry_name.place(x=200, y=50)                  
        self.entry_email = ttk.Entry(self)                  
        self.entry_email.place(x=200, y=80)                 
        self.entry_tel = ttk.Entry(self)                    
        self.entry_tel.place(x=200, y=110)                  

        self.entry_salary = ttk.Entry(self)                    
        self.entry_salary.place(x=200, y=140)                  

        # кнопка закрытия дочернего окна
        self.btn_cancel = ttk.Button(self, text="Закрыть", command=self.destroy)
        self.btn_cancel.place(x=220, y=170)

        # кнопка добавления
        self.btn_ok = ttk.Button(self, text="Добавить")
        self.btn_ok.place(x=300, y=170)

        #Отслеживаем событие, при котором сработает кнопка ДОБАВИТЬ.
        #Нажимая левой кнопкой мыши по этой кнопке мы вызываем функцию records и передаём ей информацию из полей: name, email,tel
        self.btn_ok.bind(
            "<Button-1>",
            lambda event: self.view.records(
                self.entry_name.get(), self.entry_email.get(), self.entry_tel.get(), self.entry_salary.get()
            ),
        )

# РЕДАКТИРОВАНИЕ СОТРУДНИКОВ
class Update(Child):
    def __init__(self):                                             
        super().__init__()                                          
        self.init_edit()                                            
        self.view = app                                             
        self.db = db                                                
        self.default_data()                                         

    #Метод редактирования данных в бд
    def init_edit(self):
        self.title("Редактирование данных сотрудника")               #Указали название заголовка
        btn_edit = ttk.Button(self, text="Редактировать")            #Создали кнопку и укзали текст на ней
        btn_edit.place(x=205, y=170)                                 #Указали координаты кнопки

        #Отслеживаем событие, при котором сработает кнопка ИЗМЕНИТЬ.
        #Нажимая левой кнопкой мыши по этой кнопке мы вызываем функцию update_records
        #и передаём ей информацию из полей: name, email,tel
        btn_edit.bind(
            "<Button-1>",
            lambda event: self.view.update_records(
                self.entry_name.get(), self.entry_email.get(), self.entry_tel.get(), self.entry_salary.get()
            ),
        )

        #Отслеживаем событие, при котором сработает кнопка .
        #Нажимая левой кнопкой мыши по этой кнопке мы вызываем функцию destroy к самой кнопке
        # add='+'  - соединяем две функции bind этой кнопки
        btn_edit.bind(
            "<Button-1>",
            lambda event: self.destroy(), add="+"
        )

        self.btn_ok.destroy()                                               #Закрываем кнопку btn_ok

    def default_data(self):
        self.db.cursor.execute(                                             # Запрос на выбор всех полей с таким-то id
            "SELECT * FROM Employees WHERE id=?",
            self.view.tree.set(self.view.tree.selection()[0], "#1"),        #Выбираем id выделенной строки
        )
        row = self.db.cursor.fetchone()
        # Получем доступ к первой записи из выборки                         
        self.entry_name.insert(0, row[1])                       
        self.entry_email.insert(0, row[2])                      
        self.entry_tel.insert(0, row[3])                        
        self.entry_salary.insert(0,row[4])


# Конструктор класса
class Search(tk.Toplevel):
    def __init__(self):                                         
        super().__init__()                                      
        self.init_search()                                      
        self.view = app                                         

    def init_search(self):
        self.title("Поиск сотрудника")                          
        self.geometry("300x100")                                
        self.resizable(False, False)                            

        label_search = tk.Label(self, text="Имя:")              
        label_search.place(x=50, y=20)                          

        self.entry_search = ttk.Entry(self)                     
        self.entry_search.place(x=100, y=20, width=150)         

        # Кнопка закрытия
        btn_cancel = ttk.Button(self, text="Закрыть", command=self.destroy)
        btn_cancel.place(x=185, y=50)

        # Кнопка поиска
        search_btn = ttk.Button(self, text="Найти")
        search_btn.place(x=105, y=50)

        #Отслеживаем событие, при котором сработает кнопка ПОИСК.
        #Нажимая левой кнопкой мыши по этой кнопке мы вызываем функцию search_records
        # И передаём ей информацию из поля entry_search
        search_btn.bind(
            "<Button-1>",
            lambda event: self.view.search_records(self.entry_search.get()),
        )
        #Отслеживаем событие, при котором сработает кнопка .
        #Нажимая левой кнопкой мыши по этой кнопке мы вызываем функцию destroy к самой кнопке
        search_btn.bind("<Button-1>", lambda event: self.destroy(), add="+")


# Класс Базы Данных
class DB:
    def __init__(self):
        # Создаем соединение с Базой Данных                                                                 
        self.conn = sqlite3.connect("db.db")                                            
        self.cursor = self.conn.cursor()                                                
        self.cursor.execute(                                                            
            '''
            CREATE TABLE IF NOT EXISTS Employees (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            tel TEXT NOT NULL,
            email TEXT NOT NULL,
            salary INTEGER
            )
            '''
        )
        self.conn.commit()                                                                                  
        self.data()

    # Метод для добавленияя изначальных данных в бд (не работает)
    def data(self):
        insert_into = 'INSERT INTO Employees (name, tel, email, salary) VALUES (?, ?, ?, ?)'


 
        self.conn.commit()                                                                                          


    def insert_data(self, name, tel, email, salary):                                                                
        self.cursor.execute(                                                                                        
            """INSERT INTO Employees(name, tel, email, salary) VALUES(?, ?, ?, ?)""", (name, tel, email, salary)    
        )
        self.conn.commit()                                                                                          
    # При запуске программы
if __name__ == "__main__":
    root = tk.Tk()                                  
    db = DB()                                       
    app = Main(root)                                
    app.pack()                                      
    root.title("Список сотрудников компании")       
    root.geometry("765x450")                        
    root.resizable(False, False)                    
    root.mainloop()                                 
    # Конец