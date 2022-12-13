from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtCore import QSettings, QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator

import sys

import material3_components as mt3
import widgets

class Camera(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        # --------
        # Settings
        # --------
        self.settings = QSettings(f'{sys.path[0]}/settings.ini', QSettings.Format.IniFormat)
        self.language_value = int(self.settings.value('language'))
        self.theme_value = eval(self.settings.value('theme'))

        self.regExp1 = QRegularExpressionValidator(QRegularExpression('[0-9A-Za-zÁÉÍÓÚáéíóú\_]{1,30}'))
        self.regExp2 = QRegularExpressionValidator(QRegularExpression('[0-9]{1,10}'))
        self.regExp3 = QRegularExpressionValidator(QRegularExpression('^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'))

        self.camera_data = None

        # ----------------
        # Generación de UI
        # ----------------
        width = 290
        height = 390
        screen_x = int(self.screen().availableGeometry().width() / 2 - (width / 2))
        screen_y = int(self.screen().availableGeometry().height() / 2 - (height / 2))

        if self.language_value == 0:
            self.setWindowTitle('Nueva Cámara')
        elif self.language_value == 1:
            self.setWindowTitle('New Camera')
        self.setGeometry(screen_x, screen_y, width, height)
        self.setMinimumSize(width, height)
        self.setMaximumSize(width, height)
        self.setModal(True)
        if self.theme_value:
            self.setStyleSheet(f'QWidget {{ background-color: #E5E9F0;'
                f'color: #000000 }}')
        else:
            self.setStyleSheet(f'QWidget {{ background-color: #3B4253;'
                f'color: #E5E9F0 }}')


        self.camara_card = mt3.Card(self, 'camara_card',
            (10, 10, width - 20, height - 20), self.theme_value)
        
        y, w = 10, width - 40
        self.info_label = mt3.TitleLabel(self.camara_card, 'info_label',
            ('Información de la Cámara', 'Camera Information'), (10, y, w), self.theme_value, self.language_value)
        
        y += 40
        self.nombre_text = mt3.TextField(self.camara_card, 'nombre_text',
            (10, y+10, w), self.theme_value)
        self.nombre_text.setValidator(self.regExp1)

        self.nombre_label = mt3.LabelField(self.camara_card, 'nombre_label',
            ('Nombre de la Cámara', 'Camera Name'), (20, y), self.theme_value, self.language_value)
        
        y += 70
        self.ip_text = mt3.TextField(self.camara_card, 'ip_text',
            (10, y+10, w), self.theme_value)
        self.ip_text.setValidator(self.regExp3)

        self.ip_label = mt3.LabelField(self.camara_card, 'ip_label',
            ('IP de la Cámara', 'Camera IP'), (20, y), self.theme_value, self.language_value)

        y += 70
        self.username_text = mt3.TextField(self.camara_card, 'username_text',
            (10, y+10, w), self.theme_value)

        self.username_label = mt3.LabelField(self.camara_card, 'username_label',
            ('Usuario', 'Username'), (20, y), self.theme_value, self.language_value)

        y += 70
        self.password_text = mt3.TextField(self.camara_card, 'password_text',
            (10, y+10, w), self.theme_value)

        self.password_label = mt3.LabelField(self.camara_card, 'password_label',
            ('Contraseña', 'Password'), (20, y), self.theme_value, self.language_value)

        y += 70
        self.aceptar_button = mt3.TextButton(self.camara_card, 'aceptar_button',
            ('Aceptar', 'Ok'), (w-200, y, 100), 'done.png', self.theme_value, self.language_value)
        self.aceptar_button.clicked.connect(self.on_aceptar_button_clicked)

        self.cancelar_button = mt3.TextButton(self.camara_card, 'cancelar_button',
            ('Cancelar', 'Cancel'), (w-90, y, 100), 'close.png', self.theme_value, self.language_value)
        self.cancelar_button.clicked.connect(self.on_cancelar_button_clicked)

    # ---------
    # Funciones
    # ---------
    def on_aceptar_button_clicked(self):
        if (self.nombre_text.text() == '' or self.ip_text.text() == '' or 
            self.username_text.text() == '' or self.password_text.text() == ''):
            if self.language_value == 0:
                QtWidgets.QMessageBox.critical(self, 'Error en el Formulario', 'Faltan datos de la cámara')
            elif self.language_value == 1:
                QtWidgets.QMessageBox.critical(self, 'Form Error', 'Camera data missing')
        else:
            self.camera_data = {
                'name': self.nombre_text.text(),
                'ip': self.ip_text.text(),
                'username': self.username_text.text(),
                'password': self.password_text.text()
            }
            self.close()


    def on_cancelar_button_clicked(self):
        self.close()