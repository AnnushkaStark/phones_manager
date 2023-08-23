from typing import Self, TextIO
from PyQt6 import QtCore
from PyQt6.QtWidgets import *
from PyQt6.QtWidgets import QWidget
import sys
from PyQt6 import *
import sqlite3 as sql
from user_interface import *

class Phone_Manager(Ui_MainWindow,QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()


        self.pushButton_Selec_all.clicked.connect(self.select_all)
        self.pushButton_Uppend.clicked.connect(self.uppend_table)
        self.lineEdit_add_new_name.text()
        self.lineEdit_add_new_number.text()
        self.pushButton_Update_number.clicked.connect(self.update_number)
        self.lineEdit_Old_name.text()
        self.lineEdit_Old_number_number.text()
        self.lineEdit_NeW_name.text()
        self.pushButton_Update_number_2.clicked.connect(self.update_name)
        self.lineEdit_Old_delet_number.text()
        self.lineEdit_delet_name.text()
        self.pushButton_Delete.clicked.connect(self.delete_row)
        self.lineEdit_Found_name.text()
        self.pushButton_Found.clicked.connect(self.delete_row)
        self.listWidget.addItems([])
        self.pushButton_Cjnnect.clicked.connect(self.connect)
        self.lineEdit_add_new_comment.text()
        self.database = 'phons_manager.db'
        self.query_add_single_number = '''INSERT INTO Phons (Name,  Phone, Comment)VALUES (?,?,?)'''
        self.query_add_single_number_no_comment = '''INSERT INTO Phons (Name,Phone)VALUES (?,?)'''
        self.querry_selet_all_sort = '''SELECT  ID, Name, Phone, Comment FROM Phons ORDER BY Name'''
        self.querry_update_number = '''UPDATE Phons SET Name = ? WHERE Name LIKE ? AND Phone LIKE ?'''
        self.querry_update_name = '''UPDATE Phons SET Phone = ? WHERE Name LIKE ? AND Phone LIKE ? '''
        self.querry_delet_row = '''DELETE FROM Phons WHERE Phone LIKE ? AND Name LIKE ?'''
        self.querry_found_row = '''SELECT  Name, Phone FROM Phons WHERE Name LIKE ? AND Phone LIKE ?'''
        self.querry_found_number =  '''SELECT FROM Phons Phone Comment WHERE Name LiKE ?'''

    def connect(self):
        try:
            conn = sql.connect(self.database)
            if conn:
                result = QMessageBox()
                result.setText('Подключение успешно')
                result.exec()
            else:
                result = QMessageBox()
                result.setText('Ошибка подключения')
                result.exec()
            
        except ConnectionError:
            print('Ошибка подкючения')


    def select_all(self):
        with sql.connect(self.database) as conn:
            try:
                result = conn.cursor().execute(self.querry_selet_all_sort).fetchall()
                self.tableWidget.setRowCount(len(result))
                self.tableWidget.setColumnCount(len(result[0]))
                
                for row in range(len(result)):
                    for column in range(len(result[row])):
                        item = QTableWidgetItem(str(result[row][column]))
                        self.tableWidget.setItem(row,column,item)
            except ConnectionError:
                result = result = QMessageBox()
                result.setText('Ошибка подключения')
                result.exec()
            except sql.OperationalError:
                result = result = QMessageBox()
                result.setText('Не удалось получить номера')
                result.exec()



    def uppend_table(self):
        with sql.connect(self.database) as conn:
            try:
                add_new_name = self.lineEdit_add_new_name.text()
                add_new_number = self.lineEdit_add_new_number.text()
                new_comment = self.lineEdit_add_new_comment.text()
                if add_new_name.strip() and add_new_number.strip() and new_comment.strip():
                    conn.cursor().execute(self.query_add_single_number,(add_new_name,add_new_number,new_comment))
                    result = result = QMessageBox()
                    result.setText('Номер добавлен')
                    result.exec()
                if add_new_name.strip() and add_new_number.strip() and new_comment == '':
                    conn.cursor().execute(self.query_add_single_number_no_comment,(add_new_name,add_new_number))
                    result = result = QMessageBox()
                    result.setText('Номер добавлен')
                    result.exec()
                if add_new_name =='' or add_new_number == '':
                    result = result = QMessageBox()
                    result.setText('Поле не может быть пустым')
                    result.exec()
            except sql.IntegrityError:
                result = result = QMessageBox()
                result.setText('Номер уже существует')
                result.exec()
            except sql.OperationalError:
                result = result = QMessageBox()
                result.setText('Ошибка добавления номера')
                result.exec()


    def delete_row(self): 
        with sql.connect(self.database)  as conn:
            del_number =  self.lineEdit_Old_delet_number.text()
            del_name =  self.lineEdit_delet_name.text()
            try:
                if del_name.strip() and del_number.strip():
                    result = conn.cursor().execute(self.querry_found_row,(del_name,del_number))
                if result:
                    conn.cursor().execute(self.querry_delet_row,(del_name,del_number))
                    res ='Запись удалена'
                    
                else:
                    res = 'Заполнены не все поля или запись не сущестовала'
                result =  QMessageBox()
                result.setText(res)
                result.exec()
            except Exception:
                result =  QMessageBox()
                result.setText('Ошибка удаления строки')
                result.exec()
  
    def update_number(self):
        pass

    def update_name(self):
        pass   
 
    def found_number(self):
        pass


        


app = QApplication(sys.argv)
window = Phone_Manager()
sys.exit(app.exec())