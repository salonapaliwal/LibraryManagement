from PyQt5.QtCore import *
from PyQt5.QtGui import *
from  PyQt5.QtWidgets import *
import sys
#import mysql-connector
import  pymysql
pymysql.install_as_MySQLdb()
from PyQt5.uic import loadUiType
import datetime
from xlrd import *
from xlsxwriter import *


ui,_=loadUiType('Library.ui')
login,_=loadUiType('Login.ui')


class Login(QWidget,login):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.Handel_Login)
        style = open('themes/qdarkorange.css', 'r')
        style = style.read()
        self.setStyleSheet(style)
    def Handel_Login(self):
        self.db = pymysql.connect(host='localhost', user='root', password='*****', db='library')
        self.cur = self.db.cursor()
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        sql = '''SELECT * FROM users'''
        self.cur.execute(sql)
        data = self.cur.fetchall()
        for row in data:
            if username == row[1] and password == row[3]:
                self.window2=MainApp()
                self.close()
                self.window2.show()
            else:
                self.label.setText('Make Sure You Enter your Username and Password Correctly')





class MainApp(QMainWindow,ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handel_UI_Changes()
        self.Handel_Buttons()
        self.Show_Author()
        self.Show_category()
        self.Show_Publisher()
        self.Show_Category_comboBox()
        self.Show_Author_comboBox()
        self.Show_Publisher_comboBox()
        self.Dark_Blue_Theme()
        self.show_all_clients()
        self.Show_All_Books()
        self.Show_all_operations()

    def Handel_UI_Changes(self):
        self.Hiding_Themes()
        self.tabWidget.tabBar().setVisible(False)
    def Handel_Buttons(self):
        self.pushButton_5.clicked.connect(self.Show_Themes)
        self.pushButton_23.clicked.connect(self.Hiding_Themes)
        self.pushButton.clicked.connect(self.Open_Day_To_Day_Tab)
        self.pushButton_2.clicked.connect(self.Open_Books_Tab)
        self.pushButton_3.clicked.connect(self.Open_Users_Tab)
        self.pushButton_4.clicked.connect(self.Open_Settings_Tab)
        self.pushButton_18.clicked.connect(self.Open_Clients_Tab)
        self.pushButton_7.clicked.connect(self.Add_new_Book)
        self.pushButton_55.clicked.connect(self.Search_Books)
        self.pushButton_53.clicked.connect(self.Edit_Books)
        self.pushButton_54.clicked.connect(self.Delete_Books)
        self.pushButton_15.clicked.connect(self.Add_Author)
        self.pushButton_16.clicked.connect(self.Add_Category)
        self.pushButton_17.clicked.connect(self.Add_Publisher)
        self.pushButton_11.clicked.connect(self.Add_New_User)
        self.pushButton_13.clicked.connect(self.Login)
        self.pushButton_12.clicked.connect(self.Edit_User)
        self.pushButton_8.clicked.connect(self.Dark_Orange_Theme)
        self.pushButton_9.clicked.connect(self.QDark_Style_Theme)
        self.pushButton_10.clicked.connect(self.Dark_Blue_Theme)
        self.pushButton_22.clicked.connect(self.Dark_Gray_Theme)
        self.pushButton_14.clicked.connect(self.Add_new_client)
        self.pushButton_58.clicked.connect(self.Search_client)
        self.pushButton_57.clicked.connect(self.Edit_client)
        self.pushButton_56.clicked.connect(self.Delete_client)
        self.pushButton_6.clicked.connect(self.Handel_Day_Operations)
        self.pushButton_21.clicked.connect(self.Export_Day_Operations)
        self.pushButton_19.clicked.connect(self.Export_Books)
        self.pushButton_20.clicked.connect(self.Export_Client)

    def Show_Themes(self):
        self.groupBox_3.show()
    def Hiding_Themes(self):
        self.groupBox_3.hide()
#########################################################
##################Opening Tabs###########################
    def Open_Day_To_Day_Tab(self):
        self.tabWidget.setCurrentIndex(0)
    def Open_Books_Tab(self):
        self.tabWidget.setCurrentIndex(1)
    def Open_Clients_Tab(self):
        self.tabWidget.setCurrentIndex(2)
    def Open_Users_Tab(self):
        self.tabWidget.setCurrentIndex(3)
    def Open_Settings_Tab(self):
        self.tabWidget.setCurrentIndex(4)

    #########################################################
    ##################Day To Day Operations###########################
    def Handel_Day_Operations(self):
        self.db = pymysql.connect(host='localhost', user='root', password='****', db='library')
        self.cur = self.db.cursor()
        book_title=self.lineEdit.text()
        client_name=self.lineEdit_8.text()
        type=self.comboBox.currentText()
        days_number=self.comboBox_2.currentIndex()+1
        today_date=datetime.date.today()
        to_date=today_date+datetime.timedelta(days=days_number)

        self.cur.execute('''
            INSERT INTO dayoperations(book_name,type,days,date,client,to_date) 
            VALUES (%s,%s,%s,%s,%s,%s)
            ''',(book_title,type,days_number,today_date,client_name,to_date))
        self.db.commit()
        self.statusBar().showMessage('New Operation Added')
        self.Show_all_operations()
    def Show_all_operations(self):
        self.db = pymysql.connect(host='localhost', user='root', password='****', db='library')
        self.cur = self.db.cursor()
        self.cur.execute('''
            SELECT book_name,client,type,date,to_date FROM dayoperations
            ''')
        data=self.cur.fetchall()
        self.tableWidget.setRowCount(0)
        self.tableWidget.insertRow(0)
        for row, form in enumerate(data):
            for col, item in enumerate(form):
                self.tableWidget.setItem(row, col, QTableWidgetItem(str(item)))
                col += 1
            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)
        self.db.close()




    #########################################################
    ##################Books###########################
    def Add_new_Book(self):
        self.db=pymysql.connect(host='localhost',user='root',password='****',db='library')
        self.cur=self.db.cursor()
        book_title=self.lineEdit_2.text()
        book_description=self.textEdit.toPlainText()
        book_code=self.lineEdit_3.text()
        book_category=self.comboBox_3.currentText()
        book_author = self.comboBox_4.currentText()
        book_publisher = self.comboBox_5.currentText()
        book_price= self.lineEdit_4.text()

        self.cur.execute('''
            INSERT INTO book(book_name,book_description,book_code,book_category,book_author,book_publisher,book_price)
            VALUES(%s,%s,%s,%s,%s,%s,%s)
            ''',(book_title,book_description,book_code,book_category,book_author,book_publisher,book_price))
        self.db.commit()
        self.statusBar().showMessage('New Book Added')
        ## These lines are to empty the lines for next input##
        self.lineEdit_2.setText('')
        self.textEdit.setPlainText('')
        self.lineEdit_3.setText('')
        self.comboBox_3.setCurrentIndex(0)
        self.comboBox_4.setCurrentIndex(0)
        self.comboBox_5.setCurrentIndex(0)
        self.lineEdit_4.setText('')
        self.Show_All_Books()




    def Search_Books(self):
        self.db = pymysql.connect(host='localhost', user='root', password='****', db='library')
        self.cur = self.db.cursor()
        book_title = self.lineEdit_28.text()
        sql = ''' SELECT * FROM book WHERE book_name = %s'''
        self.cur.execute(sql,[(book_title)])
        data=self.cur.fetchone()
        self.lineEdit_25.setText(data[1])
        self.textEdit_4.setPlainText(data[2])
        self.comboBox_12.setCurrentText(data[4])
        self.comboBox_13.setCurrentText(data[5])
        self.comboBox_14.setCurrentText(data[6])
        self.lineEdit_26.setText(data[3])
        self.lineEdit_27.setText(str(data[7]))

    def Edit_Books(self):
        self.db = pymysql.connect(host='localhost', user='root', password='****', db='library')
        self.cur = self.db.cursor()
        book_title = self.lineEdit_25.text()
        book_description = self.textEdit_4.toPlainText()
        book_code = self.lineEdit_26.text()
        book_category = self.comboBox_12.currentText()
        book_author = self.comboBox_13.currentText()
        book_publisher = self.comboBox_14.currentText()
        book_price = self.lineEdit_27.text()
        search_book_title=self.lineEdit_28.text()
        self.cur.execute('''
        UPDATE book SET book_name=%s ,book_description=%s ,book_code=%s ,book_category=%s ,book_author=%s ,book_publisher=%s ,book_price=%s WHERE book_name=%s
        ''',(book_title,book_description,book_code,book_category,book_author,book_publisher,book_price,search_book_title))
        self.db.commit()
        self.statusBar().showMessage('Updated')
        self.Show_All_Books()
    def Delete_Books(self):
        self.db = pymysql.connect(host='localhost', user='root', password='****', db='library')
        self.cur = self.db.cursor()
        book_title=self.lineEdit_28.text()
        warning=QMessageBox.warning(self,'Delete Book','Are you sure you want to delete this book?',QMessageBox.Yes | QMessageBox.No)
        if warning ==QMessageBox.Yes:
            sql='''DELETE FROM book where book_name=%s'''
            self.cur.execute(sql,[(book_title)])
            self.db.commit()
            self.statusBar().showMessage("Book Deleted")
            self.Show_All_Books()
    def Show_All_Books(self):
        self.db = pymysql.connect(host='localhost', user='root', password='****', db='library')
        self.cur = self.db.cursor()
        self.cur.execute('''SELECT book_code,book_name,book_description ,book_category,book_author,book_publisher,book_price FROM book''')
        data = self.cur.fetchall()
        self.tableWidget_5.setRowCount(0)
        self.tableWidget_5.insertRow(0)
        for row, form in enumerate(data):
            for col, item in enumerate(form):
                self.tableWidget_5.setItem(row, col, QTableWidgetItem(str(item)))
                col += 1
            row_position = self.tableWidget_5.rowCount()
            self.tableWidget_5.insertRow(row_position)
        self.db.close()

#########################################################
##################Users###########################
    def Add_New_User(self):
        self.db = pymysql.connect(host='localhost', user='root', password='****', db='library')
        self.cur = self.db.cursor()
        username=self.lineEdit_9.text()
        email=self.lineEdit_10.text()
        password=self.lineEdit_11.text()
        password2=self.lineEdit_12.text()
        if password==password2:
            self.cur.execute('''
                INSERT INTO users(user_name,user_email,user_password)
                VALUES (%s,%s,%s)
            ''',(username,email,password))
            self.db.commit()
            self.statusBar().showMessage("New User Added")
        else:
            self.label_36.setText("please add a valid password twice")
    def Login(self):
        self.db = pymysql.connect(host='localhost', user='root', password='****', db='library')
        self.cur = self.db.cursor()
        username=self.lineEdit_13.text()
        password=self.lineEdit_14.text()
        sql='''SELECT * FROM users'''
        self.cur.execute(sql)
        data=self.cur.fetchall()
        for row in data:
            if username==row[1] and password==row[3]:
                print("user match")
                self.statusBar().showMessage('Valid Username and password')
                self.groupBox_4.setEnabled(True)
                self.lineEdit_17.setText(row[1])
                self.lineEdit_18.setText(row[2])
                self.lineEdit_16.setText(row[3])
    def Edit_User(self):

        username=self.lineEdit_17.text()
        email=self.lineEdit_18.text()
        password=self.lineEdit_16.text()
        password2=self.lineEdit_15.text()
        original_name=self.lineEdit_13.text()
        if password==password2:
            self.db = pymysql.connect(host='localhost', user='root', password='****', db='library')
            self.cur = self.db.cursor()
            self.cur.execute('''
                UPDATE users SET user_name=%s,user_email=%s,user_password=%s WHERE user_name=%s
                ''',(username,email,password,original_name))
            self.db.commit()
            self.statusBar().showMessage('user data updated successfully')

        else:
            print("make sure you enter correct password")
#########################################################
##################settings###########################
    def Add_Category(self):
        self.db = pymysql.connect(host='localhost', user='root', password='****', db='library')
        self.cur = self.db.cursor()
        category_name=self.lineEdit_20.text()
        self.cur.execute('''
        INSERT INTO category (category_name) VALUES (%s)
        ''',(category_name))
        self.db.commit()
        self.statusBar().showMessage('New Category added')
        self.lineEdit_20.setText("")
        self.Show_category()
        self.Show_Category_comboBox()
    def Show_category(self):
        self.db = pymysql.connect(host='localhost', user='root', password='****', db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''SELECT category_name  FROM  category''')
        data=self.cur.fetchall()

        if data:
            self.tableWidget_3.setRowCount(0)
            self.tableWidget_3.insertRow(0)
            for row ,form in enumerate(data):
                for column,item in enumerate(form):
                    self.tableWidget_3.setItem(row,column,QTableWidgetItem(str(item)))
                    column+=1

                row_position=self.tableWidget_3.rowCount()
                self.tableWidget_3.insertRow(row_position)
    def Add_Author(self):
        self.db = pymysql.connect(host='localhost', user='root', password='****', db='library')
        self.cur = self.db.cursor()
        author_name = self.lineEdit_21.text()
        self.cur.execute('''
                INSERT INTO authors (author_name) VALUES (%s)
                ''', (author_name))
        self.db.commit()
        self.statusBar().showMessage('New author added')
        self.Show_Author()
        self.Show_Author_comboBox()
    def Show_Author(self):
        self.db = pymysql.connect(host='localhost', user='root', password='****', db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''SELECT author_name  FROM  authors''')
        data = self.cur.fetchall()

        if data:
            self.tableWidget_4.setRowCount(0)
            self.tableWidget_4.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.tableWidget_4.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1

                row_position = self.tableWidget_4.rowCount()
                self.tableWidget_4.insertRow(row_position)
    def Add_Publisher(self):
        self.db = pymysql.connect(host='localhost', user='root', password='****', db='library')
        self.cur = self.db.cursor()
        publisher_name = self.lineEdit_22.text()
        self.cur.execute('''
                INSERT INTO publisher (publisher_name) VALUES (%s)
                ''', (publisher_name))
        self.db.commit()
        self.statusBar().showMessage('New Publisher added')
        self.Show_Publisher()
        self.Show_Publisher_comboBox()
    def Show_Publisher(self):
        self.db = pymysql.connect(host='localhost', user='root', password='****', db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''SELECT publisher_name  FROM  publisher''')
        data = self.cur.fetchall()

        if data:
            self.tableWidget_2.setRowCount(0)
            self.tableWidget_2.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.tableWidget_2.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1

                row_position = self.tableWidget_2.rowCount()
                self.tableWidget_2.insertRow(row_position)

#########################################################
#######################Clients###########################
    def Add_new_client(self):
        self.db = pymysql.connect(host='localhost', user='root', password='****', db='library')
        self.cur = self.db.cursor()
        clients_name=self.lineEdit_5.text()
        clients_email=self.lineEdit_6.text()
        clients_nationalid=self.lineEdit_7.text()
        self.cur.execute('''
            INSERT INTO clients (clients_name,clients_email,clients_nationalid) VALUES (%s,%s,%s)'''
                         ,(clients_name,clients_email,clients_nationalid))
        self.db.commit()
        self.db.close()
        self.statusBar().showMessage('New Client Added')
        self.lineEdit_5.setText('')
        self.lineEdit_6.setText('')
        self.lineEdit_7.setText('')
        self.show_all_clients()
    def show_all_clients(self):
        self.db = pymysql.connect(host='localhost', user='root', password='****', db='library')
        self.cur = self.db.cursor()
        self.cur.execute('''SELECT clients_name,clients_email,clients_nationalid FROM clients''')
        data=self.cur.fetchall()
        self.tableWidget_6.setRowCount(0)
        self.tableWidget_6.insertRow(0)
        for row,form in enumerate(data):
            for col,item in enumerate(form):
                self.tableWidget_6.setItem(row,col,QTableWidgetItem(str(item)))
                col+=1
            row_position=self.tableWidget_6.rowCount()
            self.tableWidget_6.insertRow(row_position)
        self.db.close()

    def Search_client(self):
        self.db = pymysql.connect(host='localhost', user='root', password='****', db='library')
        self.cur = self.db.cursor()
        client_nationalid=self.lineEdit_31.text()
        sql=''' SELECT * FROM clients where clients_nationalid=%s'''
        self.cur.execute(sql, [(client_nationalid)])
        data = self.cur.fetchone()
        self.lineEdit_32.setText(data[1])
        self.lineEdit_33.setText(data[2])
        self.lineEdit_34.setText(data[3])


    def Edit_client(self):
        self.db = pymysql.connect(host='localhost', user='root', password='****', db='library')
        self.cur = self.db.cursor()
        client_name=self.lineEdit_32.text()
        client_email=self.lineEdit_33.text()
        client_nationalid=self.lineEdit_34.text()
        search_client_nationalid=self.lineEdit_31.text()
        self.cur.execute('''
            UPDATE clients SET clients_name=%s,clients_email=%s,clients_nationalid=%s WHERE clients_nationalid=%s
            ''',(client_name,client_email,client_nationalid,search_client_nationalid))
        self.db.commit()
        self.statusBar().showMessage('Updated')
        self.show_all_clients()



    def Delete_client(self):
        self.db = pymysql.connect(host='localhost', user='root', password='****', db='library')
        self.cur = self.db.cursor()
        clients_nationalid=self.lineEdit_31.text()
        warning = QMessageBox.warning(self, 'Delete Client', 'Are you sure you want to delete this client?',QMessageBox.Yes | QMessageBox.No)
        if warning == QMessageBox.Yes:
            sql = '''DELETE FROM clients where clients_nationalid=%s'''
            self.cur.execute(sql, [(clients_nationalid)])
            self.db.commit()
            self.statusBar().showMessage("Client Deleted")
            self.show_all_clients()

#########################################################
####################### show Settings data in UI###########################
    def Show_Category_comboBox(self):
        self.db = pymysql.connect(host='localhost', user='root', password='****', db='library')
        self.cur = self.db.cursor()
        self.cur.execute(''' SELECT category_name FROM category''')
        data=self.cur.fetchall()
        self.comboBox_3.clear()
        for category in data:
            self.comboBox_3.addItem(category[0])
            self.comboBox_12.addItem(category[0])



    def Show_Author_comboBox(self):
        self.db = pymysql.connect(host='localhost', user='root', password='****', db='library')
        self.cur = self.db.cursor()
        self.cur.execute(''' SELECT author_name FROM authors''')
        data = self.cur.fetchall()
        self.comboBox_4.clear()
        for author in data:
            self.comboBox_4.addItem(author[0])
            self.comboBox_13.addItem(author[0])
    def Show_Publisher_comboBox(self):
        self.db = pymysql.connect(host='localhost', user='root', password='****', db='library')
        self.cur = self.db.cursor()
        self.cur.execute(''' SELECT publisher_name FROM publisher''')
        data = self.cur.fetchall()
        self.comboBox_5.clear()
        for publisher in data:
            self.comboBox_5.addItem(publisher[0])
            self.comboBox_14.addItem(publisher[0])

    #########################################################
    ##################Export Data###########################
    def Export_Day_Operations(self):
        self.db = pymysql.connect(host='localhost', user='root', password='****', db='library')
        self.cur = self.db.cursor()
        self.cur.execute('''
                    SELECT book_name,client,type,date,to_date FROM dayoperations
                    ''')
        data = self.cur.fetchall()
        wb=Workbook('day_operations.xlsx')
        sheet1=wb.add_worksheet()
        sheet1.write(0,0,'book title')
        sheet1.write(0,1, 'client name')
        sheet1.write(0,2, 'type')
        sheet1.write(0,3, 'from-date')
        sheet1.write(0,4, 'to-date')
        row_number=1
        for row in data:
            column_number=0
            for item in row:
                sheet1.write(row_number,column_number,str(item))
                column_number+=1
            row_number+=1

        wb.close()
        self.statusBar().showMessage('Report Created Successfully')

    def Export_Books(self):
        self.db = pymysql.connect(host='localhost', user='root', password='****', db='library')
        self.cur = self.db.cursor()
        self.cur.execute(
            '''SELECT book_code,book_name,book_description ,book_category,book_author,book_publisher,book_price FROM book''')
        data = self.cur.fetchall()
        wb = Workbook('Books.xlsx')
        sheet1 = wb.add_worksheet()
        sheet1.write(0, 0, 'book code')
        sheet1.write(0, 1, 'book name')
        sheet1.write(0, 2, 'book description')
        sheet1.write(0, 3, 'book category')
        sheet1.write(0, 4, 'book author')
        sheet1.write(0, 5, 'book publisher')
        sheet1.write(0, 6, 'book price')
        row_number = 1
        for row in data:
            column_number = 0
            for item in row:
                sheet1.write(row_number, column_number, str(item))
                column_number += 1
            row_number += 1

        wb.close()
        self.statusBar().showMessage('Report Created Successfully')
    def Export_Client(self):
        self.db = pymysql.connect(host='localhost', user='root', password='****', db='library')
        self.cur = self.db.cursor()
        self.cur.execute('''SELECT clients_name,clients_email,clients_nationalid FROM clients''')
        data = self.cur.fetchall()
        wb = Workbook('Clients.xlsx')
        sheet1 = wb.add_worksheet()
        sheet1.write(0, 0, 'client name')
        sheet1.write(0, 1, 'client email')
        sheet1.write(0, 2, 'client nationalid')

        row_number = 1
        for row in data:
            column_number = 0
            for item in row:
                sheet1.write(row_number, column_number, str(item))
                column_number += 1
            row_number += 1

        wb.close()
        self.statusBar().showMessage('Report Created Successfully')





#########################################################
####################### UI Themes###########################
    def Dark_Blue_Theme(self):
        style=open('themes/qdarkblue.css','r')
        style=style.read()
        self.setStyleSheet(style)
    def Dark_Gray_Theme(self):
        style = open('themes/qdarkgray.css', 'r')
        style = style.read()
        self.setStyleSheet(style)
    def Dark_Orange_Theme(self):
        style = open('themes/qdarkorange.css', 'r')
        style = style.read()
        self.setStyleSheet(style)
    def QDark_Style_Theme(self):
        style = open('themes/qdarkstyle.css', 'r')
        style = style.read()
        self.setStyleSheet(style)


def main():
    opp=QApplication(sys.argv)
    window=Login()
    window.show()
    opp.exec_()
if __name__=='__main__':
    main()



