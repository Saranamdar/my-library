import sys
import belle
import menu
import MySQLdb
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.uic import loadUi
from datetime import date
from datetime import timedelta
import datetime
import copy
import json
from xlrd import *
from xlsxwriter import *

class login (QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(600)
        self.setFixedWidth(800)
        loadUi('login.ui',self)
        self.pushButton.clicked.connect(self.login)

    def go_home_page (self):
        widget.setCurrentIndex(1)
        


    def login(self):
        username=self.lineEdit.text()
        password=self.lineEdit_2.text()

        self.db=MySQLdb.connect(host='localhost',user='root',password='saramt981',db='library')
        self.cur=self.db.cursor()
        
        self.cur.execute('''SELECT * FROM  managers WHERE manager_name= %s AND manager_password=%s ''',(username,password))
        manager=self.cur.fetchone()
        if manager:
            self.go_home_page()

        else:
            QMessageBox.warning(self,'warning','invalid manager *__*\n try again')


        
   

class menu (QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(600)
        self.setFixedWidth(800)
        loadUi('menu.ui',self)
        self.pushButton.clicked.connect(self.show_books_tab)
        self.pushButton_2.clicked.connect(self.show_users_tab)
        self.pushButton_3.clicked.connect(self.show_borrow_return_tab)
        self.pushButton_4.clicked.connect(self.show_managers_tab)

    
    def show_books_tab(self):
        widget.setCurrentIndex(2)
    
    def show_users_tab(self):
        widget.setCurrentIndex(3)

    def show_borrow_return_tab(self):
        widget.setCurrentIndex(4)
    def show_managers_tab(self):
        widget.setCurrentIndex(5)




class managers (QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(600)
        self.setFixedWidth(800)
        loadUi('managers.ui',self)
        self.pushButton_12.clicked.connect(self.search)
        self.pushButton.clicked.connect(self.add_new_manager)
        self.pushButton_13.clicked.connect(self.edit_manager)
        self.pushButton_15.clicked.connect(self.delete_manager)
        self.show_list_of_managers()
        self.pushButton_2.clicked.connect(self.go_home_page)
        self.pushButton_3.clicked.connect(self.go_home_page)
        self.pushButton_4.clicked.connect(self.go_home_page)


    def go_home_page (self):
        widget.setCurrentIndex(1)


    def add_new_manager(self):

        name=self.lineEdit_9.text()
        email=self.lineEdit_10.text()
        mobile_number=self.lineEdit_3.text()
        national_id=self.lineEdit_4.text()
        password_first_time=self.lineEdit_11.text()
        password_second_time=self.lineEdit_12.text()

        self.db=MySQLdb.connect(host='localhost',user='root',password='saramt981',db='library')
        self.cur=self.db.cursor()
        self.cur.execute('''SELECT * FROM  managers WHERE manager_name= %s AND manager_password=%s ''',(name,password_first_time))
        manager=self.cur.fetchone()
        if not manager:

            if password_first_time==password_second_time:
                self.label_7.setText('')
                self.cur.execute('''INSERT INTO managers (manager_name,manager_password,manager_email,manager_mobile,manager_national_id)  VALUES (%s,%s,%s,%s,%s)''',(name,password_first_time,email,mobile_number,national_id))
                self.db.commit()
                QMessageBox.information(self,'info','New manager Added Succesfully ^__^')
                self.show_list_of_managers()

            else:
                self.label_7.setText('Passwords do not match T__T\nTry again')

        else:
            QMessageBox.warning(self,'warning','manager with same name and password already exists T__T\ntry another name or password')



    def search (self):

        try:
            name=self.lineEdit_13.text()
            password=self.lineEdit_14.text()
            self.db=MySQLdb.connect(host='localhost',user='root',password='saramt981',db='library')
            self.cur=self.db.cursor()
            self.cur.execute('''SELECT * FROM  managers WHERE manager_name= %s AND manager_password=%s ''',(name,password))
            manager=self.cur.fetchone()

            print(manager)
        
        
            self.lineEdit_15.setText(manager[1])
            self.lineEdit_16.setText(manager[3])
            self.lineEdit_17.setText(manager[2])
            self.lineEdit_18.setText(manager[2])
            self.lineEdit_2.setText(manager[5])
            self.lineEdit.setText(manager[4])
            self.label_6.setText('')
            self.label.setText('now you can edit or delet this manager ^__^')
            self.show_list_of_managers()
        
        except:
            QMessageBox.warning(self,"warning","manager doesn't exist T__T")
        

    def edit_manager (self):

        name=self.lineEdit_13.text()
        self.db=MySQLdb.connect(host='localhost',user='root',password='saramt981',db='library')
        self.cur=self.db.cursor()

        new_name=self.lineEdit_15.text()
        email=self.lineEdit_16.text()
        mobile_number=self.lineEdit.text()
        id=self.lineEdit_2.text()
        new_pass=self.lineEdit_17.text()
        new_pass2=self.lineEdit_18.text()
        if new_pass==new_pass2:
            self.cur.execute('''UPDATE managers SET manager_name=%s ,manager_password=%s ,manager_email=%s ,manager_mobile=%s ,manager_national_id=%s WHERE manager_name=%s''',(new_name,new_pass,email,mobile_number,id,name))
            self.db.commit()
            self.lineEdit_15.setText('')
            self.lineEdit_16.setText('')
            self.lineEdit.setText('')
            self.lineEdit_2.setText('')
            self.lineEdit_17.setText('')
            self.lineEdit_18.setText('')
            self.lineEdit_13.setText('')
            self.lineEdit_14.setText('')
            self.label.setText('')
            QMessageBox.information(self,"info","changes applied succesfully ^__^")
            self.show_list_of_users()
        else:
            QMessageBox.warning(self,"warning","you entered a fifferent password for the second time T__T\ncheck the password matches")


    def delete_manager(self):
        

        self.db=MySQLdb.connect(host='localhost',user='root',password='saramt981',db='library')
        self.cur=self.db.cursor()
        name=self.lineEdit_13.text()
        password=self.lineEdit_14.text()

        message = QMessageBox.question(self, " ", 
                                       "Are you sure you want to delete this manager? *__*",
                                       QMessageBox.Yes | 
                                       QMessageBox.No)
 
 
        if message == QMessageBox.Yes:

            self.db=MySQLdb.connect(host='localhost',user='root',password='saramt981',db='library')
            self.cur=self.db.cursor()
            self.cur.execute('''DELETE FROM managers WHERE manager_name=%s AND manager_password=%s ''',(name,password))
            self.db.commit()
            QMessageBox.information(self,'info','The manager deleted succesfully *__*')
            self.show_list_of_managers()

        else:
            pass
    
    
    def show_list_of_managers(self):
        self.db=MySQLdb.connect(host='localhost',user='root',password='saramt981',db='library')
        self.cur=self.db.cursor()
        self.cur.execute('''SELECT manager_name,manager_password,manager_email,manager_mobile,manager_national_id from managers''')
        data=self.cur.fetchall()
        
        self.tableWidget_2.setRowCount(0)
        self.tableWidget_2.insertRow(0)
        for row,item in enumerate(data):
            for column,manager in enumerate(item):
                self.tableWidget_2.setItem(row,column,QTableWidgetItem(str(manager)))
                column+=1
            next_row=self.tableWidget_2.rowCount()
            self.tableWidget_2.insertRow(next_row)


class books (QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(600)
        self.setFixedWidth(800)
        loadUi('books.ui',self)

        # self.tabWidget.tabBar().setVisible(False)
        self.pushButton_5.clicked.connect(self.go_home_page)
        # self.pushButton_4.clicked.connect(self.go_home_page)
        # self.pushButton_12.clicked.connect(self.go_home_page)
        # self.pushButton_10.clicked.connect(self.go_home_page)
        self.pushButton_9.clicked.connect(self.add_category)
        self.pushButton_7.clicked.connect(self.add_author)
        self.pushButton_8.clicked.connect(self.add_publisher)
        self.pushButton_6.clicked.connect(self.add_book)
        self.pushButton.clicked.connect(self.search_book)
        self.pushButton_11.clicked.connect(self.search_book2)
        self.pushButton_3.clicked.connect(self.save_button_clicked)
        self.pushButton_2.clicked.connect(self.delet_button_clicked)
        # self.pushButton_13.clicked.connect(self.go_home_page)
        self.pushButton_14.clicked.connect(self.make_json_file)
        self.pushButton_15.clicked.connect(self.make_excel_file)
        self.show_category_in_list()
        self.show_author_in_list()
        self.show_publisher_in_list()
        self.insert_to_category_combo()
        self.insert_to_author_combo()
        self.insert_to_publisher_combo()
        self.show_list_of_books()


    def go_home_page (self):
        widget.setCurrentIndex(1)
    
    def add_book(self):

        name=self.lineEdit_12.text()
        description=self.textEdit.toPlainText()
        code=self.lineEdit_10.text()
        category=self.comboBox_10.currentText()
        author=self.comboBox_11.currentText()
        publisher=self.comboBox_12.currentText()

        self.db=MySQLdb.connect(host='localhost',user='root',password='saramt981',db='library')
        self.cur=self.db.cursor()
        
        self.cur.execute('''SELECT * FROM  books WHERE book_name= %s AND book_code=%s ''',(name,code))
        book=self.cur.fetchone()
        
        if not book:
            self.cur.execute('''INSERT INTO books
            (book_name,book_description,book_code,book_category,book_author,book_publisher,status) VALUES(%s,%s,%s,%s,%s,%s,%s)''',(name,description,code,category,author,publisher,'available'))
            self.db.commit()
            QMessageBox.information(self,'info','new book addes ^__^')
            self.lineEdit_12.setText('')
            self.textEdit.setPlainText('')
            self.lineEdit_10.setText('')
            self.comboBox_10.setCurrentIndex(0)
            self.comboBox_11.setCurrentIndex(0)
            self.comboBox_12.setCurrentIndex(0)
            self.show_list_of_books()
            self.db.close()
        else:
            QMessageBox.warning(self,'warning','book with the same code already exists *__*\nchoose another code for the new book')

    def show_list_of_books(self):
        self.db=MySQLdb.connect(host='localhost',user='root',password='saramt981',db='library')
        self.cur=self.db.cursor()
        self.cur.execute('''SELECT book_name,book_code,book_category,book_author,book_publisher from books''')
        data=self.cur.fetchall()
        
        self.tableWidget.setRowCount(0)
        self.tableWidget.insertRow(0)
        for row,item in enumerate(data):
            for column,book in enumerate(item):
                self.tableWidget.setItem(row,column,QTableWidgetItem(str(book)))
                column+=1
            next_row=self.tableWidget.rowCount()
            self.tableWidget.insertRow(next_row)
    

    def make_json_file (self):

        self.db=MySQLdb.connect(host='localhost',user='root',password='saramt981',db='library')
        self.cur=self.db.cursor()
        self.cur.execute('''SELECT book_name,book_code,book_category,book_author,book_publisher from books''')
        data=self.cur.fetchall()

        with open("books.json", "w") as f:
            for item in data:
                json.dump(item, f,indent=1)


    def make_excel_file (self):
        
        self.db=MySQLdb.connect(host='localhost',user='root',password='saramt981',db='library')
        self.cur=self.db.cursor()
        self.cur.execute('''SELECT book_name,book_code,book_category,book_author,book_publisher from books''')
        data=self.cur.fetchall()
        f=Workbook('books.xlsx')
        excel_page=f.add_worksheet()
        excel_page.write(0,0,'book')
        excel_page.write(0,1,'code')
        excel_page.write(0,2,'category')
        excel_page.write(0,3,'author')
        excel_page.write(0,4,'publisher')

        row_num=1
        for row in data:
            column=0
            for item in row:
                excel_page.write(row_num,column,str(item))
                column+=1
            row_num+=1
        f.close()


    def search_book(self):
        try:

            book_title=self.lineEdit_7.text()
            self.db=MySQLdb.connect(host='localhost',user='root',password='saramt981',db='library')
            self.cur=self.db.cursor()
            self.cur.execute('''SELECT * FROM  books WHERE book_name= %s''',(book_title,))
            data=self.cur.fetchone()
            self.label_8.setText('now you can apply changes ^__^')
            self.lineEdit.setText(data[1])
            self.textEdit_2.setPlainText(data[2])
            self.comboBox_7.setCurrentText(data[4])
            self.lineEdit_8.setText(data[3])
            self.comboBox_8.setCurrentText(data[5])
            self.comboBox_9.setCurrentText(data[6])

        except:
            
            self.lineEdit_7.setText('')
            QMessageBox.warning(self,'warning',"book with this title doesn't exist T__T\n")
            

    def search_book2(self):
        try:

            book_title=self.lineEdit_11.text()
            self.db=MySQLdb.connect(host='localhost',user='root',password='saramt981',db='library')
            self.cur=self.db.cursor()
            self.cur.execute('''SELECT * FROM  books WHERE book_name= %s''',(book_title,))
            data=self.cur.fetchone()

            self.label_13.setText(data[1])
            self.textEdit_3.setPlainText(data[2])
            self.label_9.setText(data[4])
            self.label_10.setText(data[5])
            self.label_11.setText(data[6])
            
        
        except:

            self.lineEdit_11.setText('')
            QMessageBox.warning(self,'warning',"book with this title doesn't exist T__T\n")


    def save_button_clicked (self):

        name=self.lineEdit_7.text()
        self.db=MySQLdb.connect(host='localhost',user='root',password='saramt981',db='library')
        self.cur=self.db.cursor()
        self.cur.execute('''SELECT * FROM  books WHERE book_name= %s''',(name,))
        data=self.cur.fetchone()
        

        
        self.db=MySQLdb.connect(
        host='localhost',
        user='root',
        password='saramt981',
        db='library')
        self.cur=self.db.cursor()

        name=self.lineEdit.text()
        description=self.textEdit_2.toPlainText()
        code=self.lineEdit_8.text()
        category=self.comboBox_7.currentText()
        author=self.comboBox_8.currentText()
        publisher=self.comboBox_9.currentText()
        statusofbook='available'
        search_book_title=self.lineEdit_7.text()
        self.cur.execute('''UPDATE books SET book_name=%s ,book_description=%s ,book_code=%s ,book_category=%s ,book_author=%s ,book_publisher=%s,status=%s WHERE book_name=%s''',(name,description,code,category,author,publisher,statusofbook,search_book_title))
        self.db.commit()
        self.show_list_of_books()
        self.label_8.setText('')

        self.lineEdit.setText('')
        self.textEdit_2.setPlainText('')
        self.lineEdit_8.setText('')
        self.comboBox_7.setCurrentIndex(0)
        self.comboBox_8.setCurrentIndex(0)
        self.comboBox_9.setCurrentIndex(0)
        self.lineEdit_7.setText('')
        QMessageBox.information(self,"info","changes applied succesfully ^__^")
    


    def delet_button_clicked(self):
        self.db=MySQLdb.connect(
                host='localhost',
                user='root',
                password='saramt981',
                db='library')
        self.cur=self.db.cursor()
        book_title=self.lineEdit_11.text()
        message = QMessageBox.question(self, " ", 
                                       "Are you sure you want to delete this book?",
                                       QMessageBox.Yes | 
                                       QMessageBox.No)
 
 
        if message == QMessageBox.Yes:
            self.cur.execute('''DELETE FROM books WHERE book_name=%s''',[(book_title)])
            self.db.commit()
            QMessageBox.information(self,'info','The book deleted succesfully *__*')
            
            self.lineEdit_11.setText('')

            self.label_13.setText('')
            self.textEdit_3.setPlainText('')
            self.label_9.setText(str(''))
            # self.label_10.setText(str(''))
            self.label_11.setText(str(''))
            self.label_12.setText(str(''))
            self.show_list_of_books()



            
        else:
            pass

 
 
        


    
    def add_category(self):
        try:
            name=self.lineEdit_5.text()

            self.db=MySQLdb.connect(
                host='localhost',
                user='root',
                password='saramt981',
                db='library')
            self.cur=self.db.cursor()
            self.cur.execute('''INSERT INTO categories (category_name) VALUES (%s)''',(name,))
            self.db.commit()
            self.lineEdit_5.setText('')
            self.show_category_in_list()
            QMessageBox.information(self,'info','new category added ^__^')
            # self.label_4.setText("new category added ^__^")
            self.insert_to_category_combo()

            
        except:
             self.label_4.setText("Error Inserting Data T__T")
    
    def show_category_in_list(self):
        try:

            self.db=MySQLdb.connect(
                host='localhost',
                user='root',
                password='saramt981',
                db='library')
            self.cur=self.db.cursor()
            self.cur.execute('''SELECT category_name FROM categories''')
            categories=self.cur.fetchall()

            if categories:

                self.tableWidget_5.setRowCount(0)
                self.tableWidget_5.insertRow(0)
 
                for row_number, row_data in enumerate(categories):
                    self.tableWidget_5.insertRow(row_number)
 
                    for column_number, data in enumerate(row_data):
                        self.tableWidget_5.setItem(row_number,
                            column_number, QTableWidgetItem(str(data)))
                    
                    current_row=self.tableWidget_5.rowCount()
                    self.tableWidget_5.insertRow(current_row)
        except:
             print("Error occured")

        
    def add_author(self):
        try:
            name=self.lineEdit_3.text()

            self.db=MySQLdb.connect(
                host='localhost',
                user='root',
                password='saramt981',
                db='library')
            self.cur=self.db.cursor()
            self.cur.execute('''INSERT INTO authors (author_name) VALUES (%s)''',(name,))
            self.db.commit()
            self.lineEdit_3.setText('')
            #self.label_5.setText("new author added ^__^")
            QMessageBox.information(self,'info','new author added ^__^')
            self.show_author_in_list()
            self.insert_to_author_combo()
            
        except:
            self.label_5.setText("Error Inserting Data T__T")
            
    def show_author_in_list(self):
        try:

            self.db=MySQLdb.connect(
                host='localhost',
                user='root',
                password='saramt981',
                db='library')
            self.cur=self.db.cursor()
            self.cur.execute('''SELECT author_name FROM authors''')
            authors=self.cur.fetchall()

            if authors:

                self.tableWidget_3.setRowCount(0)
                self.tableWidget_3.insertRow(0)
 
                for row_number, row_data in enumerate(authors):
                    self.tableWidget_3.insertRow(row_number)
 
                    for column_number, data in enumerate(row_data):
                        self.tableWidget_3.setItem(row_number,
                            column_number, QTableWidgetItem(str(data)))
                    
                    current_row=self.tableWidget_3.rowCount()
                    self.tableWidget_3.insertRow(current_row)
        except:
             print("Error occured")
        

    def add_publisher(self):
        try:
            name=self.lineEdit_4.text()

            self.db=MySQLdb.connect(
                host='localhost',
                user='root',
                password='saramt981',
                db='library')
            self.cur=self.db.cursor()
            self.cur.execute('''INSERT INTO publishers (publisher_name) VALUES (%s)''',(name,))
            self.db.commit()
            self.lineEdit_4.setText('')
            #self.label_6.setText("new publisher added ^__^")
            QMessageBox.information(self,'info','new publisher added ^__^')
            self.show_publisher_in_list()
            self.insert_to_publisher_combo()
            
        except:
            self.label_6.setText("Error Inserting Data T__T")
    
    def show_publisher_in_list(self):
        try:

            self.db=MySQLdb.connect(
                host='localhost',
                user='root',
                password='saramt981',
                db='library')
            self.cur=self.db.cursor()
            self.cur.execute('''SELECT publisher_name FROM publishers''')
            publishers=self.cur.fetchall()

            if publishers:

                self.tableWidget_4.setRowCount(0)
                self.tableWidget_4.insertRow(0)
 
                for row_number, row_data in enumerate(publishers):
                    self.tableWidget_4.insertRow(row_number)
 
                    for column_number, data in enumerate(row_data):
                        self.tableWidget_4.setItem(row_number,
                            column_number, QTableWidgetItem(str(data)))
                    
                    current_row=self.tableWidget_4.rowCount()
                    self.tableWidget_4.insertRow(current_row)
        except:
             print("Error occured")


    def fetchall_combobox_data(self,row,column):

        self.db=MySQLdb.connect(
                host='localhost',
                user='root',
                password='saramt981',
                db='library')
        self.cur=self.db.cursor()
        self.cur.execute('''SELECT {} FROM {}'''.format(row,column))
        data=self.cur.fetchall()
        return data

    def insert_to_category_combo (self):
        data=self.fetchall_combobox_data('category_name','categories')
        self.comboBox_10.clear()
        self.comboBox_7.clear()
        for item in data:
            self.comboBox_10.addItem(item[0])
            self.comboBox_7.addItem(item[0])
    def insert_to_author_combo (self):
        data=self.fetchall_combobox_data('author_name','authors')
        self.comboBox_11.clear()
        self.comboBox_8.clear()
        for item in data:
            self.comboBox_11.addItem(item[0])
            self.comboBox_8.addItem(item[0])
    def insert_to_publisher_combo (self):
        data=self.fetchall_combobox_data('publisher_name','publishers')
        self.comboBox_12.clear()
        self.comboBox_9.clear()
        for item in data:
            self.comboBox_12.addItem(item[0])
            self.comboBox_9.addItem(item[0])




        
class users (QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(600)
        self.setFixedWidth(800)
        loadUi('users.ui',self)

        # self.pushButton.clicked.connect(self.go_home_page)
        # self.pushButton_2.clicked.connect(self.go_home_page)
        self.pushButton_11.clicked.connect(self.add_new_user)
        self.pushButton_12.clicked.connect(self.search_for_editing)
        self.pushButton_13.clicked.connect(self.editing_user)
        self.pushButton_14.clicked.connect(self.search_for_deleting)
        self.pushButton_15.clicked.connect(self.delete_user)
        self.pushButton_3.clicked.connect(self.go_home_page)
        # self.pushButton_4.clicked.connect(self.go_home_page)
        self.show_list_of_users()
        self.pushButton_5.clicked.connect(self.make_json_file)
        self.pushButton_6.clicked.connect(self.make_excel_file)

        

    def show_list_of_users(self):
        self.db=MySQLdb.connect(host='localhost',user='root',password='saramt981',db='library')
        self.cur=self.db.cursor()
        self.cur.execute('''SELECT user_name,user_email,user_password,user_national_id,mobile_number from users''')
        data=self.cur.fetchall()
        
        self.tableWidget.setRowCount(0)
        self.tableWidget.insertRow(0)
        for row,item in enumerate(data):
            for column,user in enumerate(item):
                self.tableWidget.setItem(row,column,QTableWidgetItem(str(user)))
                column+=1
            next_row=self.tableWidget.rowCount()
            self.tableWidget.insertRow(next_row)

    
    def make_json_file (self):
        self.db=MySQLdb.connect(host='localhost',user='root',password='saramt981',db='library')
        self.cur=self.db.cursor()
        self.cur.execute('''SELECT user_name,user_email,user_password,user_national_id,mobile_number from users''')
        data=self.cur.fetchall()

        with open("users.json", "w") as f:
            for item in data:
                json.dump(item, f,indent=1)


    def make_excel_file (self):
        self.db=MySQLdb.connect(host='localhost',user='root',password='saramt981',db='library')
        self.cur=self.db.cursor()
        self.cur.execute('''SELECT user_name,user_email,user_password,user_national_id,mobile_number from users''')
        data=self.cur.fetchall()
        f=Workbook('users.xlsx')
        excel_page=f.add_worksheet()
        excel_page.write(0,0,'name')
        excel_page.write(0,1,'email')
        excel_page.write(0,2,'password')
        excel_page.write(0,3,'id')
        excel_page.write(0,4,'mobile')

        row_num=1
        for row in data:
            column=0
            for item in row:
                excel_page.write(row_num,column,str(item))
                column+=1
            row_num+=1
        f.close()


    def add_new_user(self):

        name=self.lineEdit_9.text()
        email=self.lineEdit_10.text()
        mobile_number=self.lineEdit_3.text()
        national_id=self.lineEdit_4.text()
        password_first_time=self.lineEdit_11.text()
        password_second_time=self.lineEdit_12.text()

        self.db=MySQLdb.connect(host='localhost',user='root',password='saramt981',db='library')
        self.cur=self.db.cursor()
        self.cur.execute('''SELECT * FROM  users WHERE user_name= %s AND user_password=%s ''',(name,password_first_time))
        user=self.cur.fetchone()
        if not user:
            if password_first_time==password_second_time:
                self.cur.execute('''INSERT INTO users (user_name,user_email,user_password,User_national_id,mobile_number)  VALUES (%s,%s,%s,%s,%s)''',(name,email,password_first_time,national_id,mobile_number))
                self.db.commit()
                QMessageBox.information(self,'info','New User Added Succesfully ^__^')
                self.show_list_of_users()


                self.lineEdit_9.setText('')
                self.lineEdit_10.setText('')
                self.lineEdit_11.setText('')
                self.lineEdit_12.setText('')
                self.label.setText('')
                self.lineEdit_3.setText('')
                self.lineEdit_4.setText('')
            else:
                self.label.setText('Passwords do not match T__T\nTry again')
        else:
            QMessageBox.warning(self,'warning','user with same name and password already exists *__*\ntry another name or password')

    def search_for_editing(self):

        try:
            username=self.lineEdit_13.text()
            password=self.lineEdit_14.text()
            self.db=MySQLdb.connect(host='localhost',user='root',password='saramt981',db='library')
            self.cur=self.db.cursor()
            self.cur.execute('''SELECT * FROM  users WHERE user_name= %s AND user_password=%s ''',(username,password))
            user=self.cur.fetchone()
        
        
            self.lineEdit_15.setText(user[1])
            self.lineEdit_16.setText(user[2])
            self.lineEdit_17.setText(user[3])
            self.lineEdit_18.setText(user[3])
            self.lineEdit_2.setText(user[4])
            self.lineEdit.setText(user[5])
            self.label_6.setText('')
            self.label_7.setText('now you can edit the information of user ^__^')
            self.show_list_of_users()
        
        except:
            QMessageBox.warning(self,"warning","user with this username and possword doesn't exist T__T")

            
    def editing_user(self):

        name=self.lineEdit_13.text()
        self.db=MySQLdb.connect(host='localhost',user='root',password='saramt981',db='library')
        self.cur=self.db.cursor()

        new_name=self.lineEdit_15.text()
        email=self.lineEdit_16.text()
        mobile_number=self.lineEdit.text()
        id=self.lineEdit_2.text()
        new_pass=self.lineEdit_17.text()
        new_pass2=self.lineEdit_18.text()
        if new_pass==new_pass2:
            self.cur.execute('''UPDATE users SET user_name=%s ,user_email=%s ,user_password=%s ,user_national_id=%s ,mobile_number=%s WHERE user_name=%s''',(new_name,email,new_pass,id,mobile_number,name))
            self.db.commit()
            self.lineEdit_15.setText('')
            self.lineEdit_16.setText('')
            self.lineEdit.setText('')
            self.lineEdit_2.setText('')
            self.lineEdit_17.setText('')
            self.lineEdit_18.setText('')
            self.lineEdit_13.setText('')
            self.lineEdit_14.setText('')
            self.label_7.setText('')
            QMessageBox.information(self,"info","changes applied succesfully ^__^")
            self.show_list_of_users()
        else:
            QMessageBox.warning(self,"warning","you entered a fifferent password for the second time *__*\ncheck the password matches")

    def search_for_deleting(self):

        try:

            username=self.lineEdit_19.text()
            password=self.lineEdit_20.text()
            self.db=MySQLdb.connect(host='localhost',user='root',password='saramt981',db='library')
            self.cur=self.db.cursor()
            self.cur.execute('''SELECT * FROM  users WHERE user_name= %s AND user_password=%s ''',(username,password))
            user=self.cur.fetchone()
        
    
            self.label_11.setText(user[1])
            self.label_12.setText(user[2])
            self.label_13.setText(user[5])
            self.label_14.setText(user[4])
            self.label_15.setText(user[3])
            self.label_8.setText('')
        except:
            QMessageBox.warning(self,"user with this name and password doesent exist in tour service*__*\n")


    def delete_user(self):

        self.db=MySQLdb.connect(
                host='localhost',
                user='root',
                password='saramt981',
                db='library')
        self.cur=self.db.cursor()
        name=self.lineEdit_19.text()
        password=self.lineEdit_20.text()

        message = QMessageBox.question(self, " ", 
                                       "Are you sure you want to delete this user?",
                                       QMessageBox.Yes | 
                                       QMessageBox.No)
 
        if message == QMessageBox.Yes:

            self.label.setText('')
            self.db=MySQLdb.connect(
                host='localhost',
                user='root',
                password='saramt981',
                db='library')
            self.cur=self.db.cursor()
            self.cur.execute('''DELETE FROM users WHERE user_name=%s AND user_password=%s ''',(name,password))
            self.db.commit()
            QMessageBox.information(self,'info','The user deleted succesfully *__*')
            self.show_list_of_users()
            
            self.lineEdit_19.setText('')
            self.lineEdit_20.setText('')

            self.label_11.setText('')
            self.label_12.setText('')
            self.label_13.setText('')
            self.label_14.setText('')
            self.label_15.setText('')
            self.label_8.setText('')

        else:
            pass


    def go_home_page (self):
        widget.setCurrentIndex(1)


class rent_or_return (QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(600)
        self.setFixedWidth(800)
        loadUi('rent_return.ui',self)
        self.pushButton.clicked.connect(self.rent_book)
        self.pushButton_2.clicked.connect(self.returning)
        # self.pushButton_3.clicked.connect(self.go_home_page)
        # self.pushButton_4.clicked.connect(self.go_home_page)
        self.pushButton_7.clicked.connect(self.go_home_page)
        self.show_list_of_renting_books()
        self.pushButton_5.clicked.connect(self.make_json_file)
        self.pushButton_6.clicked.connect(self.make_excel_file)


    def go_home_page (self):
        widget.setCurrentIndex(1)


    def show_list_of_renting_books(self):

        self.db=MySQLdb.connect(host='localhost',user='root',password='saramt981',db='library')
        self.cur=self.db.cursor()
        self.cur.execute('''SELECT nameofbook,renter_name,status,days,from_day,last_day from renting''')
        data=self.cur.fetchall()
        
        self.tableWidget.setRowCount(0)
        self.tableWidget.insertRow(0)
        for row,item in enumerate(data):
            for column,book in enumerate(item):
                self.tableWidget.setItem(row,column,QTableWidgetItem(str(book)))
                column+=1
            next_row=self.tableWidget.rowCount()
            self.tableWidget.insertRow(next_row)
    
    def make_json_file(self):

        self.db=MySQLdb.connect(host='localhost',user='root',password='saramt981',db='library')
        self.cur=self.db.cursor()
        self.cur.execute('''SELECT nameofbook,renter_name,status,days,from_day,last_day from renting''')
        data=self.cur.fetchall()

        with open("renting.json", "w") as f:
            for item in data:
                json.dump(item, f,indent=1)


    def make_excel_file (self):
        
        self.db=MySQLdb.connect(host='localhost',user='root',password='saramt981',db='library')
        self.cur=self.db.cursor()
        self.cur.execute('''SELECT nameofbook,renter_name,status,days,from_day,last_day from renting''')
        data=self.cur.fetchall()
        f=Workbook('renting.xlsx')
        excel_page=f.add_worksheet()
        excel_page.write(0,0,'book')
        excel_page.write(0,1,'renter')
        excel_page.write(0,2,'status')
        excel_page.write(0,3,'days')
        excel_page.write(0,4,'from')
        excel_page.write(0,5,'to')
        row_num=1
        for row in data:
            column=0
            for item in row:
                excel_page.write(row_num,column,str(item))
                column+=1
            row_num+=1
        f.close()



    def rent_book(self):

        name_of_book=self.lineEdit.text()
        name_of_user=self.lineEdit_3.text()
        my_days=self.lineEdit_2.text()
        
        self.db=MySQLdb.connect(host='localhost',user='root',password='saramt981',db='library')
        self.cur=self.db.cursor()
        self.cur.execute('''SELECT * FROM  books WHERE book_name= %s''',(name_of_book,))
        book=self.cur.fetchone()

        self.db=MySQLdb.connect(host='localhost',user='root',password='saramt981',db='library')
        self.cur=self.db.cursor()
        self.cur.execute('''SELECT * FROM  renting WHERE nameofbook= %s''',(name_of_book,))
        book_in_renting_list=self.cur.fetchone()

        self.db=MySQLdb.connect(host='localhost',user='root',password='saramt981',db='library')
        self.cur=self.db.cursor()
        self.cur.execute('''SELECT * FROM  users WHERE user_name= %s''',(name_of_user,))
        user=self.cur.fetchone()

        if book and not book_in_renting_list and user and (int(my_days)<=7):

            
            
            # day2=int(copy.copy(day))
            # day3=copy.copy(day)
            curDTObj = datetime.datetime.now()


            my_date = curDTObj.strftime("%d %b %Y")
            ending_date=curDTObj+timedelta(days=int(my_days))
            my_ending_date=ending_date.strftime("%d %b %Y")
            print(my_date)
            # date_to=from_date+timedelta(days=day2)
            # from_date2=from_date
            # date_to2=date_to
            
            new_status="already rented"
            self.db=MySQLdb.connect(
            host='localhost',
            user='root',
            password='saramt981',
            db='library')

            self.cur=self.db.cursor()
            sql='''INSERT INTO renting (nameofbook,renter_name,status,days,from_day,last_day) VALUES (%s,%s,%s,%s,%s,%s)'''
            self.cur.execute(sql,(name_of_book,name_of_user,new_status,my_days,my_date,my_ending_date))
            self.db.commit()
            self.show_list_of_renting_books()
            self.lineEdit.setText('')
            self.lineEdit_2.setText('')
            self.lineEdit_3.setText('')
            QMessageBox.information(self,'info',"you rented the book succesfully ^__^ ")
            self.lineEdit.setText('')

        elif book_in_renting_list:
            QMessageBox.warning(self,'info',"this book in alredy rented *__*\ntry again a few days latar")
            
        elif not user:
            QMessageBox.warning(self,'warning',"the usert doesn't exist in our library *__*")
        elif int(days)>7:
            QMessageBox.warning(self,'warning',"you can't rent a book more than 7 days *__*")

        else:
            QMessageBox.warning(self,'warning',"the book you want doesn't exist in our library *__*")
        
            
    def returning(self):
        name_of_book=self.lineEdit_4.text()
        self.db=MySQLdb.connect(host='localhost',user='root',password='saramt981',db='library')
        self.cur=self.db.cursor()
        self.cur.execute('''SELECT * FROM  renting WHERE nameofbook= %s''',(name_of_book,))
        book=self.cur.fetchone()

        self.db=MySQLdb.connect(host='localhost',user='root',password='saramt981',db='library')
        self.cur=self.db.cursor()
        self.cur.execute('''DELETE FROM renting WHERE nameofbook=%s ''',(name_of_book,))
        self.db.commit()
        self.show_list_of_renting_books()
        self.lineEdit_4.setText('')
        QMessageBox.information(self,'info',"the book is returned succesfully ^__^")

            
        

        

        


app=QApplication(sys.argv)
widget=QtWidgets.QStackedWidget()
my_login_page=login()
my_menu=menu()
my_books=books()
my_users=users()
may_managers=managers()
my_rent_or_return=rent_or_return()
widget.addWidget(my_login_page)
widget.addWidget(my_menu)
widget.addWidget(my_books)
widget.addWidget(my_users)
widget.addWidget(my_rent_or_return)
widget.addWidget(may_managers)
widget.setCurrentIndex(0)
widget.show()

app.exec_()







