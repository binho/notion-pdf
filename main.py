#!/usr/bin/python
# -*- coding: utf-8 -*-

import browser
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QColor, QFont, QFontDatabase, QFontInfo, QIcon
from PyQt5.QtWidgets import (QAction, QApplication, QFileDialog, QLabel,
                             QLineEdit, QMainWindow, QMessageBox, QPushButton,
                             QTextEdit, QVBoxLayout, QWidget, QErrorMessage)

test_urls = [
    'https://www.notion.so/metalab/Add-Habit-bdaa7ef09412437b8e19b4effd49a689',
    # 'https://www.notion.so/metalab/Dashboard-9ecef974b09e4bdd8ee87607a493d777',
    # 'https://www.notion.so/metalab/Agenda-b77043a94e4e4579ba7da5ebcae2da6d',
    # 'https://www.notion.so/metalab/Onboarding-0573b66355d24854b67561c2f6b7050e'
]

class Window(QWidget):

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.title = 'Notion to PDF'
        self.width = 840
        self.height = 600
        self.download_path = '~/Downloads'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)

        self.setAutoFillBackground(True)

        self.font = QFont('Arial')
        self.font.setPointSize(15)
        self.font.setStyleStrategy(QFont.PreferAntialias)

        self.layout = QVBoxLayout()

        self.label = QLabel('1. Make sure the document is set as "Public Access" and "Can Read" on Notion.\n2. Add one Notion page URL per line and tap "Convert All" button.\n3. Google Chrome will open, load each URL and then save to PDF (Keep this window open while converting)')
        self.label.setFont(self.font)
        self.layout.addWidget(self.label)

        self.text_edit = QTextEdit(self)
        self.text_edit.setPlainText('\n'.join(test_urls))
        self.text_edit.setMinimumWidth(600)
        self.text_edit.setFont(self.font)
        # self.text_edit.setFont(QFontDatabase.systemFont(QFontDatabase.GeneralFont))
        self.layout.addWidget(self.text_edit)

        self.directory_button = QPushButton('Select Destination Folder ({})'.format(self.download_path), self)
        self.directory_button.setMinimumHeight(42)
        self.directory_button.setStyleSheet('border: 0; border-radius: 6px; background-color: white;')
        self.directory_button.setFont(self.font)
        self.directory_button.clicked.connect(self.select_directory)
        self.layout.addWidget(self.directory_button)

        self.convert_button = QPushButton('Convert All', self)
        self.convert_button.setMinimumHeight(60)
        self.convert_button.setFont(self.font)
        self.convert_button.clicked.connect(self.convert_all)
        self.convert_button.setStyleSheet('border: 0; border-radius: 6px; background-color: #26D0B7;')
        self.layout.addWidget(self.convert_button)

        self.setLayout(self.layout)

    @pyqtSlot()
    def select_directory(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.DirectoryOnly)

        if dialog.exec_() == QFileDialog.Accepted:
            self.download_path = dialog.selectedFiles()[0]
            self.directory_button.setText('Select Destination Folder ({})'.format(self.download_path))

    @pyqtSlot()
    def convert_all(self):
        value = self.text_edit.toPlainText()
        if not value:
            QMessageBox.warning(self, 'Error', 'Please enter a valid URL')
        else:
            urls = value.split('\n')
            browser.convert_to_pdf(urls, self.download_path)

            QMessageBox.information(self, 'Success', 'All URLs converted and saved to:\n{}'.format(self.download_path))

            self.text_edit.setPlainText('')

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = Window()

    window.setAutoFillBackground(True)

    p = window.palette()
    p.setColor(window.backgroundRole(), QColor("#F5F5F5"))
    window.setPalette(p)

    window.show()
    sys.exit(app.exec_())
