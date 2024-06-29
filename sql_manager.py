import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton,
    QTextEdit, QLineEdit, QLabel, QMessageBox, QTableWidget,
    QTableWidgetItem, QHBoxLayout
)
from PyQt5.QtCore import Qt
import pymysql

class MySQLManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.connection = None
        self.table_name = ""
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('MySQL Manager')
        self.setGeometry(100, 100, 800, 600)

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        
        self.layout = QVBoxLayout()
        self.centralWidget.setLayout(self.layout)
        
        self.connectionParamsLayout = QHBoxLayout()
        self.layout.addLayout(self.connectionParamsLayout)
        
        self.hostLabel = QLabel('Host:')
        self.connectionParamsLayout.addWidget(self.hostLabel)
        self.hostInput = QLineEdit(self)
        self.connectionParamsLayout.addWidget(self.hostInput)
        
        self.userLabel = QLabel('User:')
        self.connectionParamsLayout.addWidget(self.userLabel)
        self.userInput = QLineEdit(self)
        self.connectionParamsLayout.addWidget(self.userInput)
        
        self.passwordLabel = QLabel('Password:')
        self.connectionParamsLayout.addWidget(self.passwordLabel)
        self.passwordInput = QLineEdit(self)
        self.passwordInput.setEchoMode(QLineEdit.Password)
        self.connectionParamsLayout.addWidget(self.passwordInput)
        
        self.dbLabel = QLabel('Database:')
        self.connectionParamsLayout.addWidget(self.dbLabel)
        self.dbInput = QLineEdit(self)
        self.connectionParamsLayout.addWidget(self.dbInput)
        
        self.connectButton = QPushButton('Connect', self)
        self.connectButton.clicked.connect(self.connect_to_db)
        self.connectionParamsLayout.addWidget(self.connectButton)
        
        self.queryInput = QTextEdit(self)
        self.layout.addWidget(self.queryInput)
        
        self.executeButton = QPushButton('Execute', self)
        self.executeButton.clicked.connect(self.execute_query)
        self.layout.addWidget(self.executeButton)
        
        self.resultTable = QTableWidget(self)
        self.resultTable.setEditTriggers(QTableWidget.DoubleClicked)
        self.resultTable.cellChanged.connect(self.cell_changed)
        self.layout.addWidget(self.resultTable)
        
        self.logOutput = QTextEdit(self)
        self.logOutput.setReadOnly(True)
        self.layout.addWidget(self.logOutput)
        
    def log_message(self, message):
        self.logOutput.append(message)
        
    def connect_to_db(self):
        self.host = self.hostInput.text()
        self.user = self.userInput.text()
        self.password = self.passwordInput.text()
        self.db = self.dbInput.text()
        
        try:
            self.connection = pymysql.connect(host=self.host,
                                              user=self.user,
                                              password=self.password,
                                              db=self.db)
            self.log_message('Connected to database successfully')
            QMessageBox.information(self, 'Success', 'Connected to database successfully')
        except Exception as e:
            self.log_message(f'Error: {str(e)}')
            QMessageBox.critical(self, 'Error', str(e))
        
    def execute_query(self):
        query = self.queryInput.toPlainText()
        
        try:
            # Extract the table name from the query
            self.table_name = query.split()[3] if "from" in query.lower() else ""
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                
                self.resultTable.setColumnCount(len(cursor.description))
                self.resultTable.setRowCount(len(result))
                self.resultTable.setHorizontalHeaderLabels([desc[0] for desc in cursor.description])
                
                for row_idx, row_data in enumerate(result):
                    for col_idx, col_data in enumerate(row_data):
                        self.resultTable.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
                
                self.log_message('Query executed successfully')
        except Exception as e:
            self.log_message(f'Error: {str(e)}')
            QMessageBox.critical(self, 'Error', str(e))
    
    def cell_changed(self, row, column):
        if not self.connection or not self.table_name:
            return
        
        item = self.resultTable.item(row, column)
        if item:
            new_value = item.text()
            column_name = self.resultTable.horizontalHeaderItem(column).text()
            primary_key_column = self.resultTable.horizontalHeaderItem(0).text()
            primary_key_value = self.resultTable.item(row, 0).text()
            
            update_query = f"UPDATE {self.table_name} SET {column_name} = %s WHERE {primary_key_column} = %s"
            
            try:
                with self.connection.cursor() as cursor:
                    cursor.execute(update_query, (new_value, primary_key_value))
                self.connection.commit()
                self.log_message(f'Updated row {row + 1}, column "{column_name}" to "{new_value}"')
            except Exception as e:
                self.log_message(f'Error: {str(e)}')
                QMessageBox.critical(self, 'Error', str(e))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    manager = MySQLManager()
    manager.show()
    sys.exit(app.exec_())
