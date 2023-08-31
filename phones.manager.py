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

        self.database = 'phons_manager.db'
        self.query_add_single_number = '''INSERT INTO Phons (Name,  Phone, Comment)VALUES (?,?,?)'''
        self.querry_selet_all_sort = '''SELECT  ID, Name, Phone, Comment FROM Phons ORDER BY Name'''
        self.querry_update_number = '''UPDATE Phons SET Phone = ? WHERE Phone LIKE ? '''
        self.querry_update_comment  ='''UPDATE Phons SET Comment = ? WHERE Comment LIKE ?'''
        self.querry_update_name = '''UPDATE Phons SET Name = ? WHERE Name LIKE ? '''
        self.querry_delet_row = '''DELETE FROM Phons WHERE Phone LIKE ? AND Name LIKE ?'''
        self.querry_found_row = '''SELECT  Name, Phone  FROM Phons WHERE Name LIKE ? AND Phone LIKE ?'''
        self.querry_found_number =  '''SELECT Phone, Comment FROM Phons  WHERE Name LiKE ?'''
        self.pushButton_Connect.clicked.connect(self.connect)
        self.pushButton_Show_All.clicked.connect(self.select_all)
        self.lineEdit_Added_name.text()
        self.lineEdit_Added_number.text()
        self.lineEdit_Added_comment.text()
        self.pushButton_Added.clicked.connect(self.uppend_table)
        self.lineEdit_found_name.text()
        self.lineEdit_found_number.text()
        self.lineEdit_update_name.text()
        self.lineEdit_update_number.text()
        self.lineEdit_update_comment.text()
        self.pushButton_Update.clicked.connect(self.update_number)
        self.lineEdit_del_nume.text()
        self.lineEdit_del_number.text()
        self.pushButton_dell.clicked.connect(self.delete_row)
        self.lineEdit_found_many_name.text()
        self.pushButton_Found.clicked.connect(self.found_number)
        self.pushButton_claer.clicked.connect(self.clear)
        self.listWidget.addItems([])

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
                add_new_name = self.lineEdit_Added_name.text()
                add_new_number =  self.lineEdit_Added_number.text()
                new_comment = self. lineEdit_Added_comment.text()
                if add_new_name.strip() and add_new_number.strip() and new_comment.strip():
                    conn.cursor().execute(self.query_add_single_number,(add_new_name,add_new_number,new_comment))
                    result = QMessageBox()
                    result.setText('Номер добавлен')
                    result.exec()
                if add_new_name =='' or add_new_number == '':
                    result = QMessageBox()
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
            try:
                del_name  = self.lineEdit_del_nume.text()
                del_number = self.lineEdit_del_number.text()
                if del_name.strip() and del_number.strip():
                    result = conn.cursor().execute(self.querry_found_row,(del_name,del_number))
                    result = conn.cursor().execute(self.querry_delet_row,(del_name,del_number))
                    result =  QMessageBox()
                    result.setText("Номер удален")
                    result.exec() 
                else:
                    res = 'Заполнены не все поля или номер никогда не сущестовал'
                    result =  QMessageBox()
                    result.setText(res)
                    result.exec()
            except sql.IntegrityError:
                result =  QMessageBox()
                result.setText("Ошибка удаления")
                result.exec()
               
                
            
  
    def update_number(self):
        with sql.connect(self.database) as conn:
            try:
                old_number = self.lineEdit_Old_name.text() 
                old_name = self.lineEdit_old_name.text()
                new_number = self.lineEdit_update_number.text()
                new_comment = self.lineEdit_update_comment_2.text()
                if old_number.strip() and old_name.strip() and new_number.strip() and new_comment == '' or old_number.strip() and old_name.strip() and new_number.strip() and new_comment.srip(): 
                    result = conn.cursor().execute(self.querry_found_row,(old_name,old_number))
                    print(result)
                    if result:
                        conn.cursor().execute(self.querry_update_number,(new_number,old_number))
                        #conn.cursor().execute(self.querry_update_comment,(new_comment,old_number))
                        res ='Запись обновлена'
                        result =  QMessageBox()
                        result.setText(res)
                        result.exec()
                else:
                    result =  QMessageBox()
                    result.setText('Запись не найдена')
                    result.exec()
            except sql.OperationalError:
                result =  QMessageBox()
                result.setText('Изменяемый номер не найден')
                result.exec()
            except sql.IntegrityError:
                result =  QMessageBox()
                result.setText('Номер уже существует')
                result.exec()
            except Exception:
                result =  QMessageBox()
                result.setText('Ошибка обновления')
                result.exec()



  
    def clear(self):
        pass   
 
    def found_number(self):
        with sql.connect(self.database) as conn:
            try:
                found_name = self.lineEdit_Found_name.text()
                if found_name.strip():
                    res = conn.cursor().execute(self.querry_found_number,(found_name)).fetchall()
                    print(res)
                    if res:
                        for row in res:
                            self.textEdit.setText(*row)
                    else:
                        result = QMessageBox()
                        result.setText('Имя не найдено')
                        result.exec()
                else:
                    result = QMessageBox()
                    result.setText('Введите имя')
                    result.exec()
            except sql.OperationalError:
                result = QMessageBox()
                result.setText('Ошибка выполнения')
                result.exec() 
            except Exception:
                result = QMessageBox()
                result.setText('Ошибка выполнения')
                result.exec()




    def clear_list(self):
        pass


        


app = QApplication(sys.argv)
window = Phone_Manager()
sys.exit(app.exec())