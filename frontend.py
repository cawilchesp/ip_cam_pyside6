from turtle import back
from PyQt6 import QtGui, QtWidgets
from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import pyqtSignal, pyqtSlot, Qt, QThread, QSettings

import sys
import cv2
import numpy as np
import psycopg2

import material3_components as mt3
import widgets
import backend
import camera


# ---------
# Funciones
# ---------
class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self, username, password, ip_address):
        super().__init__()
        self._run_flag = True
        self.username = username
        self.password = password
        self.ip_address = ip_address
        # Video data
        self.frame = None
        self.width = 0
        self.height = 0
        self.output = None
        
    def run(self):
        # capture from web cam
        source = f'rtsp://{self.username}:{self.password}@{self.ip_address}/axis-media/media.amp?Transport=multicast'

        cap = cv2.VideoCapture(source)
        self.width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        while self._run_flag:
            ret, cv_img = cap.read()
            if ret:
                self.change_pixmap_signal.emit(cv_img)
        # shut down capture system
        cap.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()


class App(QWidget):
    def __init__(self):
        super().__init__()
        # --------
        # Settings
        # --------
        self.settings = QSettings(f'{sys.path[0]}/settings.ini', QSettings.Format.IniFormat)
        self.language_value = int(self.settings.value('language'))
        self.theme_value = eval(self.settings.value('theme'))

        self.idioma_dict = {0: ('ESP', 'SPA'), 1: ('ING', 'ENG')}

        # -------------
        # Base de Datos
        # -------------
        self.ip_cameras_value = backend.create_db('ip_cam', 'ecf406MetroidPrime')

        # ----------------
        # Generación de UI
        # ----------------
        width = 1720
        height = 860
        screen_x = int(self.screen().availableGeometry().width() / 2 - (width / 2))
        screen_y = int(self.screen().availableGeometry().height() / 2 - (height / 2))

        if self.language_value == 0:
            self.setWindowTitle('Video de Cámara en Vivo')
        elif self.language_value == 1:
            self.setWindowTitle('Camera Live Video')
        self.setGeometry(screen_x, screen_y, width, height)
        self.setMinimumSize(width, height)
        if self.theme_value:
            self.setStyleSheet(f'QWidget {{ background-color: #E5E9F0; color: #000000 }}'
                f'QComboBox QListView {{ border: 1px solid #000000; border-radius: 5; padding: 0 10 0 10;'
                f'background-color: #B2B2B2; color: #000000 }}')
        else:
            self.setStyleSheet(f'QWidget {{ background-color: #3B4253; color: #E5E9F0 }}'
                f'QComboBox QListView {{ border: 1px solid #E5E9F0; border-radius: 5; padding: 0 10 0 10;'
                f'background-color: #2E3441; color: #E5E9F0 }}')

        # -----------
        # Card Título
        # -----------
        self.titulo_card = mt3.Card(self, 'titulo_card',
            (10, 10, width - 20, 50), self.theme_value)

        x_1 = width - 280
        self.idioma_menu = mt3.Menu(self.titulo_card, 'idioma_menu',
            (x_1, 10, 70), 2, 2, self.idioma_dict, self.theme_value, self.language_value)
        self.idioma_menu.setCurrentIndex(self.language_value)
        self.idioma_menu.currentIndexChanged.connect(self.on_idioma_menu_currentIndexChanged)
        
        x_1 += 80
        self.tema_switch = mt3.Switch(self.titulo_card, 'tema_switch',
            ('', ''), (x_1, 10, 50), ('light_mode.png','dark_mode.png'), self.theme_value, self.language_value)
        self.tema_switch.set_state(self.theme_value)
        self.tema_switch.clicked.connect(self.on_tema_switch_clicked)

        x_1 += 60
        self.manual_button = mt3.IconButton(self.titulo_card, 'manual_button',
            (x_1, 10), 'help.png', self.theme_value)
        self.manual_button.clicked.connect(self.on_manual_button_clicked)

        x_1 += 40
        self.about_button = mt3.IconButton(self.titulo_card, 'about_button',
            (x_1, 10), 'mail_L.png', self.theme_value)
        self.about_button.clicked.connect(self.on_about_button_clicked)

        x_1 += 40
        self.aboutQt_button = mt3.IconButton(self.titulo_card, 'aboutQt_button',
            (x_1, 10), 'about_qt.png', self.theme_value)
        self.aboutQt_button.clicked.connect(self.on_aboutQt_button_clicked)

        # -----------
        # Card Cámara
        # -----------
        self.camara_card = mt3.Card(self, 'camara_card',
            (10, 70, 190, 230), self.theme_value)

        y_1 = 10
        self.camara_label = mt3.TitleLabel(self.camara_card, 'camara_label',
            ('Cámara', 'Camera'), (10, y_1, 170), self.theme_value, self.language_value)

        y_1 += 40
        self.agregar_button = mt3.TextButton(self.camara_card, 'agregar_button',
            ('Agregar Cámara', 'Add Camera'), (10, y_1, 170), 'camera.png', self.theme_value, self.language_value)
        self.agregar_button.clicked.connect(self.on_agregar_button_clicked)

        y_1 += 40
        self.editar_button = mt3.TextButton(self.camara_card, 'editar_button',
            ('Editar Cámara', 'Edit Camera'), (10, y_1, 170), 'edit_camera.png', self.theme_value, self.language_value)
        self.editar_button.clicked.connect(self.on_editar_button_clicked)

        y_1 += 40
        self.eliminar_button = mt3.TextButton(self.camara_card, 'eliminar_button',
            ('Eliminar Cámara', 'Delete Camera'), (10, y_1, 170), 'no_camera.png', self.theme_value, self.language_value)
        self.eliminar_button.clicked.connect(self.on_eliminar_button_clicked)

        y_1 += 40
        self.recientes_label = mt3.LabelField(self.camara_card, 'recientes_label',
            ('Cámaras Recientes', 'Recent Cameras'), (10, y_1), self.theme_value, self.language_value)

        y_1 += 20
        self.ipaddress_menu = mt3.Menu(self.camara_card, 'ipaddress_menu',
            (10, y_1, 170), 10, 10, {}, self.theme_value, self.language_value)
        for data in self.ip_cameras_value:
            self.ipaddress_menu.add_item(data[1])
        self.ipaddress_menu.setCurrentIndex(-1)
        self.ipaddress_menu.currentIndexChanged.connect(self.on_ipaddress_menu_currentIndexChanged)

        # ----------------
        # Card Información
        # ----------------
        self.info_card = mt3.Card(self, 'info_card',
            (10, 310, 190, 260), self.theme_value)

        y_2 = 10
        self.info_label = mt3.TitleLabel(self.info_card, 'info_label',
            ('Información de la Cámara','Camera Information'), (10, y_2, 170), self.theme_value, self.language_value)

        y_2 += 40
        self.ipaddress_label = widgets.ItemLabel(self.info_card, 'ipaddress_label',
            ('IP Cámara', 'Camera IP'), (10, y_2, 170), self.theme_value, self.language_value)

        y_2 += 30
        self.ipaddress_value = widgets.ValueLabel(self.info_card, 'ipaddress_value',
            (10, y_2, 170), self.theme_value)

        y_2 += 40
        self.user_label = widgets.ItemLabel(self.info_card, 'user_label',
            ('Usuario', 'User'), (10, y_2, 170), self.theme_value, self.language_value)

        y_2 += 30
        self.user_value = widgets.ValueLabel(self.info_card, 'user_value',
            (10, y_2, 170), self.theme_value)
        
        y_2 += 40
        self.password_label = widgets.ItemLabel(self.info_card, 'password_label',
            ('Contraseña', 'Password'), (10, y_2, 170), self.theme_value, self.language_value)

        y_2 += 30
        self.password_value = widgets.ValueLabel(self.info_card, 'password_value',
            (10, y_2, 170), self.theme_value)

        # -------------
        # Card Opciones
        # -------------
        self.opciones_card = mt3.Card(self, 'opciones_card',
            (10, 580, 190, 170), self.theme_value)

        y_3 = 10
        self.opciones_label = mt3.TitleLabel(self.opciones_card, 'opciones_label',
            ('Opciones', 'Options'), (10, y_3, 170), self.theme_value, self.language_value)

        y_3 += 40
        self.start_button = mt3.TextButton(self.opciones_card, 'start_button',
            ('Iniciar', 'Start'), (10, y_3, 170), 'play.png', self.theme_value, self.language_value)
        self.start_button.setEnabled(False)
        self.start_button.clicked.connect(self.on_start_button_clicked)

        y_3 += 40
        self.stop_button = mt3.TextButton(self.opciones_card, 'stop_button',
            ('Detener', 'Stop'), (10, y_3, 170), 'stop.png', self.theme_value, self.language_value)
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self.on_stop_button_clicked)

        y_3 += 40
        self.record_button = mt3.Switch(self.opciones_card, 'record_button',
            ('Grabar', 'Record'), (10, y_3, 170), ('record.png', 'record.png'), self.theme_value, self.language_value)
        self.record_button.set_state(False)
        self.record_button.setEnabled(False)
        self.record_button.clicked.connect(self.on_record_button_clicked)

        # -----------
        # Card Imagen
        # -----------
        self.imagen_card = mt3.Card(self, 'imagen_card',
            (210, 70, 1300, 740), self.theme_value)

        self.image_label = QtWidgets.QLabel(self.imagen_card)
        self.image_label.setGeometry(10, 10, 1280, 720)
        self.image_label.setFrameStyle(QtWidgets.QFrame.Shape.Box)

        # --------------
        # Card Controles
        # --------------
        self.controles_card = mt3.Card(self, 'controles_card',
            (1520, 70, 190, 150), self.theme_value)

        y_4 = 10
        self.controles_label = mt3.TitleLabel(self.controles_card, 'controles_label',
            ('Controles', 'Controls'), (10, y_4, 170), self.theme_value, self.language_value)

        y_4 += 40
        self.up_control_button = mt3.IconButton(self.controles_card, 'up_control_button',
            (85, y_4), '', self.theme_value)
        self.up_control_button.setArrowType(Qt.ArrowType.UpArrow)
        self.up_control_button.setEnabled(False)
        self.up_control_button.clicked.connect(self.on_up_control_button_clicked)

        y_4 += 30
        self.left_control_button = mt3.IconButton(self.controles_card, 'left_control_button',
            (55, y_4), '', self.theme_value)
        self.left_control_button.setArrowType(Qt.ArrowType.LeftArrow)
        self.left_control_button.setEnabled(False)
        self.left_control_button.clicked.connect(self.on_left_control_button_clicked)

        self.right_control_button = mt3.IconButton(self.controles_card, 'right_control_button',
            (115, y_4), '', self.theme_value)
        self.right_control_button.setArrowType(Qt.ArrowType.RightArrow)
        self.right_control_button.setEnabled(False)
        self.right_control_button.clicked.connect(self.on_right_control_button_clicked)

        y_4 += 30
        self.down_control_button = mt3.IconButton(self.controles_card, 'down_control_button',
            (85, y_4), '', self.theme_value)
        self.down_control_button.setArrowType(Qt.ArrowType.DownArrow)
        self.down_control_button.setEnabled(False)
        self.down_control_button.clicked.connect(self.on_down_control_button_clicked)

        # -------------
        # Card Posición
        # -------------
        self.posicion_card = mt3.Card(self, 'posicion_card',
            (1520, 230, 190, 380), self.theme_value)

        y_5 = 10
        self.position_label = mt3.TitleLabel(self.posicion_card, 'position_label',
            ('Posición de la Cámara', 'Camera Position'), (10, y_5, 170), self.theme_value, self.language_value)

        y_5 += 40
        self.pan_text = mt3.TextField(self.posicion_card, 'pan_text',
            (10, y_5+10, 170), self.theme_value)

        self.pan_label = mt3.LabelField(self.posicion_card, 'pan_label',
            ('Horizontal', 'Pan'), (20, y_5), self.theme_value, self.language_value)
        
        y_5 += 70
        self.tilt_text = mt3.TextField(self.posicion_card, 'tilt_text',
            (10, y_5+10, 170), self.theme_value)

        self.tilt_label = mt3.LabelField(self.posicion_card, 'tilt_label',
            ('Vertical', 'Tilt'), (20, y_5), self.theme_value, self.language_value)
        
        y_5 += 70
        self.zoom_text = mt3.TextField(self.posicion_card, 'zoom_text',
        (10, y_5+10, 170), self.theme_value)

        self.zoom_label = mt3.LabelField(self.posicion_card, 'zoom_label',
            ('Aumento', 'Zoom'), (20, y_5), self.theme_value, self.language_value)
        
        y_5 += 70
        self.zoom_slider = mt3.ObjectSlider(self.posicion_card, 'zoom_slider',
            (10, y_5, 170), self.theme_value)
        self.zoom_slider.setMinimum(1)
        self.zoom_slider.setEnabled(False)
        self.zoom_slider.sliderMoved.connect(self.on_zoom_slider_sliderMoved)
        self.zoom_slider.sliderReleased.connect(self.on_zoom_slider_sliderReleased)

        y_5 += 40
        self.getPTZ_button = mt3.TextButton(self.posicion_card, 'getPTZ_button',
            ('Obtener PTZ', 'Get PTZ'), (10, y_5, 170), '', self.theme_value, self.language_value)
        self.getPTZ_button.setEnabled(False)
        self.getPTZ_button.clicked.connect(self.on_getPTZ_button_clicked)

        y_5 += 40
        self.setPTZ_button = mt3.TextButton(self.posicion_card, 'setPTZ_button',
            ('Establecer PTZ', 'Set PTZ'), (10, y_5, 170), '', self.theme_value, self.language_value)
        self.setPTZ_button.setEnabled(False)
        self.setPTZ_button.clicked.connect(self.on_setPTZ_button_clicked)

        # ---------------
        # Card Parámetros
        # ---------------
        self.parametros_card = mt3.Card(self, 'parametros_card',
            (1520, 620, 190, 230), self.theme_value)

        y_6 = 10
        self.parameters_label = mt3.TitleLabel(self.parametros_card, 'parameters_label',
            ('Parámetros', 'Parameters'), (10, y_6, 170), self.theme_value, self.language_value)

        y_6 += 40
        self.fps_text = mt3.TextField(self.parametros_card, 'fps_text',
            (10, y_6+10, 170), self.theme_value)

        self.fps_label = mt3.LabelField(self.parametros_card, 'fps_label',
            ('Captura FPS', 'Capture FPS'), (20, y_6), self.theme_value, self.language_value)

        y_6 += 70
        self.compression_spin = mt3.TextField(self.parametros_card, 'compression_spin',
            (10, y_6+10, 170), self.theme_value)

        self.compression_label = mt3.LabelField(self.parametros_card, 'compression_label',
            ('Compresión de Imagen', 'Image Compression'), (20, y_6), self.theme_value, self.language_value)

        y_6 += 70
        self.setParameters_button = widgets.TextButton(self.parametros_card, 'setParameters_button',
            ('Establecer Parámetros', 'Set Parameters'), (10, y_6, 170), '', self.theme_value, self.language_value)
        self.setParameters_button.setEnabled(False)
        self.setParameters_button.clicked.connect(self.on_setParameters_button_clicked)

    # ----------------
    # Funciones Título
    # ----------------
    def on_idioma_menu_currentIndexChanged(self, index: int):
        self.idioma_menu.language_text(index)

        self.camara_label.language_text(index)
        self.agregar_button.language_text(index)
        self.editar_button.language_text(index)
        self.eliminar_button.language_text(index)
        self.recientes_label.language_text(index)

        self.info_label.language_text(index)
        self.ipaddress_label.language_text(index)
        self.user_label.language_text(index)
        self.password_label.language_text(index)
        
        self.opciones_label.language_text(index)
        self.start_button.language_text(index)
        self.stop_button.language_text(index)
        self.record_button.language_text(index)

        self.controles_label.language_text(index)

        self.position_label.language_text(index)
        self.pan_label.language_text(index)
        self.tilt_label.language_text(index)
        self.zoom_label.language_text(index)
        self.getPTZ_button.language_text(index)
        self.setPTZ_button.language_text(index)

        self.parameters_label.language_text(index)
        self.fps_label.language_text(index)
        self.compression_label.language_text(index)
        self.setParameters_button.language_text(index)

        self.settings.setValue('language', str(index))


    def on_tema_switch_clicked(self, index: int):
        if index:
            self.setStyleSheet('background-color: #E5E9F0; color: #000000')
        else:
            self.setStyleSheet('background-color: #3B4253; color: #E5E9F0')

        self.titulo_card.apply_styleSheet(index)
        self.idioma_menu.apply_styleSheet(index)
        self.tema_switch.set_state(index)
        self.tema_switch.apply_styleSheet(index)
        self.manual_button.apply_styleSheet(index)
        self.about_button.apply_styleSheet(index)
        self.aboutQt_button.apply_styleSheet(index)

        self.camara_card.apply_styleSheet(index)
        self.camara_label.apply_styleSheet(index)
        self.agregar_button.apply_styleSheet(index)
        self.editar_button.apply_styleSheet(index)
        self.eliminar_button.apply_styleSheet(index)
        self.recientes_label.apply_styleSheet(index)

        self.info_card.apply_styleSheet(index)
        self.info_label.apply_styleSheet(index)
        self.ipaddress_label.apply_styleSheet(index)
        self.ipaddress_menu.apply_styleSheet(index)
        self.ipaddress_value.apply_styleSheet(index)
        self.user_label.apply_styleSheet(index)
        self.user_value.apply_styleSheet(index)
        self.password_label.apply_styleSheet(index)
        self.password_value.apply_styleSheet(index)
        
        self.opciones_card.apply_styleSheet(index)
        self.opciones_label.apply_styleSheet(index)
        self.start_button.apply_styleSheet(index)
        self.stop_button.apply_styleSheet(index)
        self.record_button.apply_styleSheet(index)

        self.imagen_card.apply_styleSheet(index)

        self.controles_card.apply_styleSheet(index)
        self.controles_label.apply_styleSheet(index)
        self.up_control_button.apply_styleSheet(index)
        self.left_control_button.apply_styleSheet(index)
        self.right_control_button.apply_styleSheet(index)
        self.down_control_button.apply_styleSheet(index)
        
        self.posicion_card.apply_styleSheet(index)
        self.position_label.apply_styleSheet(index)
        self.pan_label.apply_styleSheet(index)
        self.pan_text.apply_styleSheet(index)
        self.tilt_label.apply_styleSheet(index)
        self.tilt_text.apply_styleSheet(index)
        self.zoom_label.apply_styleSheet(index)
        self.zoom_text.apply_styleSheet(index)
        self.zoom_slider.apply_styleSheet(index)
        self.getPTZ_button.apply_styleSheet(index)
        self.setPTZ_button.apply_styleSheet(index)

        self.parametros_card.apply_styleSheet(index)
        self.parameters_label.apply_styleSheet(index)
        self.fps_label.apply_styleSheet(index)
        self.fps_text.apply_styleSheet(index)
        self.compression_label.apply_styleSheet(index)
        self.compression_spin.apply_styleSheet(index)
        self.setParameters_button.apply_styleSheet(index)
        
        self.settings.setValue('theme', str(index))


    def on_manual_button_clicked(self):

        return 0


    def on_about_button_clicked(self):
        self.about = backend.AboutApp()
        self.about.exec()


    def on_aboutQt_button_clicked(self):
        backend.about_qt_dialog(self, self.language_value)

    # ----------------
    # Funciones Cámara
    # ----------------
    def on_agregar_button_clicked(self):
        self.camera_window = camera.Camera()
        self.camera_window.exec()

        if self.camera_window.camera_data:
            self.ip_cameras_value = backend.add_db(self.camera_window.camera_data, 'ip_cam', 'ecf406MetroidPrime')

            self.ipaddress_menu.clear()
            for data in self.ip_cameras_value:
                self.ipaddress_menu.add_item(data[1])
            self.ipaddress_menu.setCurrentIndex(-1)
            self.ipaddress_value.setText('')
            self.user_value.setText('')
            self.password_value.setText('')

            if self.language_value == 0:
                QtWidgets.QMessageBox.information(self, 'Datos Guardados', 'Cámara agregada a la base de datos')
            elif self.language_value == 1:
                QtWidgets.QMessageBox.information(self, 'Data Saved', 'Camera added to database')
        else:
            if self.language_value == 0:
                QtWidgets.QMessageBox.critical(self, 'Error de Datos', 'No se dio información de una cámara nueva')
            elif self.language_value == 1:
                QtWidgets.QMessageBox.critical(self, 'Data Error', 'No information on a new camera was given')


    def on_editar_button_clicked(self):
        camera_name = self.ipaddress_menu.currentText()
        
        if camera_name != '':
            data = backend.get_db(camera_name, 'ip_cam', 'ecf406MetroidPrime')

            camera_id = data[0][0]
            self.camera_window = camera.Camera()
            self.camera_window.nombre_text.setText(data[0][1])
            self.camera_window.ip_text.setText(data[0][2])
            self.camera_window.username_text.setText(data[0][3])
            self.camera_window.password_text.setText(data[0][4])

            self.camera_window.exec()

            if self.camera_window.camera_data:
                self.ip_cameras_value = backend.edit_db(camera_id, self.camera_window.camera_data, 'ip_cam', 'ecf406MetroidPrime')

                self.ipaddress_menu.clear()
                for data in self.ip_cameras_value:
                    self.ipaddress_menu.add_item(data[1])
                self.ipaddress_menu.setCurrentIndex(-1)
                self.ipaddress_value.setText('')
                self.user_value.setText('')
                self.password_value.setText('')

                if self.language_value == 0:
                    QtWidgets.QMessageBox.information(self, 'Datos Guardados', 'Cámara editada en la base de datos')
                elif self.language_value == 1:
                    QtWidgets.QMessageBox.information(self, 'Data Saved', 'Camera edited in database')
            else:
                if self.language_value == 0:
                    QtWidgets.QMessageBox.critical(self, 'Error de Datos', 'No se dio información de la cámara')
                elif self.language_value == 1:
                    QtWidgets.QMessageBox.critical(self, 'Data Error', 'No information on a camera was given')
        else:
            if self.language_value == 0:
                QtWidgets.QMessageBox.critical(self, 'Error de Cámara', 'No se seleccionó una cámara')
            elif self.language_value == 1:
                QtWidgets.QMessageBox.critical(self, 'Camera Error', 'No camera selected')


    def on_eliminar_button_clicked(self):
        camera_name = self.ipaddress_menu.currentText()

        if camera_name != '':
            self.ip_cameras_value = backend.delete_db(camera_name, 'ip_cam', 'ecf406MetroidPrime')

            self.ipaddress_menu.clear()
            for data in self.ip_cameras_value:
                self.ipaddress_menu.add_item(data[1])
            self.ipaddress_menu.setCurrentIndex(-1)
            self.ipaddress_value.setText('')
            self.user_value.setText('')
            self.password_value.setText('')

            if self.language_value == 0:
                QtWidgets.QMessageBox.information(self, 'Datos Guardados', 'Cámara eliminada de la base de datos')
            elif self.language_value == 1:
                QtWidgets.QMessageBox.information(self, 'Data Saved', 'Camera deleted from database')
        else:
            if self.language_value == 0:
                QtWidgets.QMessageBox.critical(self, 'Error de Cámara', 'No se seleccionó una cámara')
            elif self.language_value == 1:
                QtWidgets.QMessageBox.critical(self, 'Camera Error', 'No camera selected')


    def on_ipaddress_menu_currentIndexChanged(self, index: int):
        if index != -1:
            self.ipaddress_value.setText(self.ip_cameras_value[self.ipaddress_menu.currentIndex()][2])
            self.user_value.setText(self.ip_cameras_value[self.ipaddress_menu.currentIndex()][3])
            self.password_value.setText(self.ip_cameras_value[self.ipaddress_menu.currentIndex()][4])
            if not self.stop_button.isEnabled():
                self.start_button.setEnabled(True)
    
    # ------------------
    # Funciones Opciones
    # ------------------
    def on_start_button_clicked(self):
        username = self.user_value.text()
        password = self.password_value.text()
        ip_address = self.ipaddress_value.text()

        # Check connection
        current_ptz = backend.get_PTZ(ip_address, username, password)

        if current_ptz != 'error':
            ptz_limits = backend.get_PTZ_limits(ip_address, username, password)

            self.pan_text.setMinimum(int(ptz_limits['MinPan']))
            self.pan_text.setMaximum(int(ptz_limits['MaxPan']))
            self.tilt_text.setMinimum(int(ptz_limits['MinTilt']))
            self.tilt_text.setMaximum(int(ptz_limits['MaxTilt']))
            self.zoom_text.setMinimum(int(ptz_limits['MinZoom']))
            self.zoom_text.setMaximum(int(ptz_limits['MaxZoom']))

            self.thread = VideoThread(username, password, ip_address) # create the video capture thread        
            self.thread.change_pixmap_signal.connect(self.update_image) # connect its signal to the update_image slot
            self.thread.start()

            self.pan_text.setValue(int(current_ptz['pan']))
            self.tilt_text.setValue(int(current_ptz['tilt']))
            self.zoom_text.setValue(int(current_ptz['zoom']))
            self.zoom_slider.setValue(int(current_ptz['zoom']))

            parameters = backend.get_parameters(ip_address, username, password)
            self.fps_text.setValue(int(parameters['root.Image.I0.Stream.FPS']))
            self.compression_spin.setValue(int(parameters['root.Image.I0.Appearance.Compression']))

            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            self.record_button.setEnabled(True)
            self.up_control_button.setEnabled(True)
            self.left_control_button.setEnabled(True)
            self.right_control_button.setEnabled(True)
            self.down_control_button.setEnabled(True)
            self.zoom_slider.setEnabled(True)
            self.getPTZ_button.setEnabled(True)
            self.setPTZ_button.setEnabled(True)
            self.setParameters_button.setEnabled(True)
        else:
            if self.language_value == 0:
                error_message = QtWidgets.QMessageBox.critical(self, 'Error de Conexión', 'No hubo conexión con la cámara')
            elif self.language_value == 1:
                error_message = QtWidgets.QMessageBox.critical(self, 'Connection Error', 'There was no connection to the camera')


    def on_stop_button_clicked(self):
        self.thread.stop()

        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.record_button.setEnabled(False)
        self.up_control_button.setEnabled(False)
        self.left_control_button.setEnabled(False)
        self.right_control_button.setEnabled(False)
        self.down_control_button.setEnabled(False)
        self.zoom_slider.setEnabled(False)
        self.getPTZ_button.setEnabled(False)
        self.setPTZ_button.setEnabled(False)
        self.setParameters_button.setEnabled(False)


    def on_record_button_clicked(self):
        fps = self.fps_text.value()
        width = self.thread.width
        height = self.thread.height
        fourcc = 'mp4v'
        file_name = f'{sys.path[0]}/{self.ipaddress_menu.currentText()}.avi'
        
        if self.record_button.isChecked():
            self.thread.output = cv2.VideoWriter(file_name, cv2.VideoWriter_fourcc(*fourcc), fps, (width, height))
            self.record_button.text_es = 'Grabando...'
            self.record_button.text_en = 'Recording...'
            self.record_button.language_text(self.language_value)
            self.record_button.set_state(True)
        else:
            self.thread.output.release()
            self.record_button.text_es = 'Grabar'
            self.record_button.text_en = 'Record'
            self.record_button.language_text(self.language_value)
            self.record_button.set_state(False)
    
    # -------------------
    # Funciones Controles
    # -------------------
    def on_left_control_button_clicked(self):
        self.pan_text.setValue(self.pan_text.value() - 10)
        username = self.user_value.text()
        password = self.password_value.text()
        ip_address = self.ipaddress_value.text()
        current_ptz = backend.set_PTZ(self.pan_text.value(), self.tilt_text.value(), self.zoom_text.value(), 
                        ip_address, username, password)

        if current_ptz == 'error':
            if self.language_value == 0:
                QtWidgets.QMessageBox.critical(self, 'Error de Conexión', 'No hubo conexión con la cámara')
            elif self.language_value == 1:
                QtWidgets.QMessageBox.critical(self, 'Connection Error', 'There was no connection to the camera')


    def on_right_control_button_clicked(self):
        self.pan_text.setValue(self.pan_text.value() + 10)
        username = self.user_value.text()
        password = self.password_value.text()
        ip_address = self.ipaddress_value.text()
        current_ptz = backend.set_PTZ(self.pan_text.value(), self.tilt_text.value(), self.zoom_text.value(), 
                        ip_address, username, password)

        if current_ptz == 'error':
            if self.language_value == 0:
                QtWidgets.QMessageBox.critical(self, 'Error de Conexión', 'No hubo conexión con la cámara')
            elif self.language_value == 1:
                QtWidgets.QMessageBox.critical(self, 'Connection Error', 'There was no connection to the camera')


    def on_up_control_button_clicked(self):
        self.tilt_text.setValue(self.tilt_text.value() + 10)
        username = self.user_value.text()
        password = self.password_value.text()
        ip_address = self.ipaddress_value.text()
        current_ptz = backend.set_PTZ(self.pan_text.value(), self.tilt_text.value(), self.zoom_text.value(), 
                        ip_address, username, password)

        if current_ptz == 'error':
            if self.language_value == 0:
                QtWidgets.QMessageBox.critical(self, 'Error de Conexión', 'No hubo conexión con la cámara')
            elif self.language_value == 1:
                QtWidgets.QMessageBox.critical(self, 'Connection Error', 'There was no connection to the camera')


    def on_down_control_button_clicked(self):
        self.tilt_text.setValue(self.tilt_text.value() - 10)
        username = self.user_value.text()
        password = self.password_value.text()
        ip_address = self.ipaddress_value.text()
        current_ptz = backend.set_PTZ(self.pan_text.value(), self.tilt_text.value(), self.zoom_text.value(), 
                        ip_address, username, password)

        if current_ptz == 'error':
            if self.language_value == 0:
                QtWidgets.QMessageBox.critical(self, 'Error de Conexión', 'No hubo conexión con la cámara')
            elif self.language_value == 1:
                QtWidgets.QMessageBox.critical(self, 'Connection Error', 'There was no connection to the camera')

    # ------------------
    # Funciones Posición
    # ------------------
    def on_zoom_slider_sliderMoved(self):
        self.zoom_text.setValue(self.zoom_slider.value())


    def on_zoom_slider_sliderReleased(self):
        username = self.user_value.text()
        password = self.password_value.text()
        ip_address = self.ipaddress_value.text()
        current_ptz = backend.set_PTZ(self.pan_text.value(), self.tilt_text.value(), self.zoom_text.value(), 
                        ip_address, username, password)

        if current_ptz == 'error':
            if self.language_value == 0:
                QtWidgets.QMessageBox.critical(self, 'Error de Conexión', 'No hubo conexión con la cámara')
            elif self.language_value == 1:
                QtWidgets.QMessageBox.critical(self, 'Connection Error', 'There was no connection to the camera')


    def on_getPTZ_button_clicked(self):
        username = self.user_value.text()
        password = self.password_value.text()
        ip_address = self.ipaddress_value.text()
        current_ptz = backend.get_PTZ(ip_address, username, password)

        if current_ptz != 'error':
            self.pan_text.setValue(int(current_ptz['pan']))
            self.tilt_text.setValue(int(current_ptz['tilt']))
            self.zoom_text.setValue(int(current_ptz['zoom']))
            self.zoom_slider.setValue(int(current_ptz['zoom']))
        else:
            if self.language_value == 0:
                QtWidgets.QMessageBox.critical(self, 'Error de Conexión', 'No hubo conexión con la cámara')
            elif self.language_value == 1:
                QtWidgets.QMessageBox.critical(self, 'Connection Error', 'There was no connection to the camera')

    def on_setPTZ_button_clicked(self):
        username = self.user_value.text()
        password = self.password_value.text()
        ip_address = self.ipaddress_value.text()
        current_ptz = backend.set_PTZ(self.pan_text.value(), self.tilt_text.value(), self.zoom_text.value(), 
                        ip_address, username, password)

        if current_ptz == 'error':
            if self.language_value == 0:
                QtWidgets.QMessageBox.critical(self, 'Error de Conexión', 'No hubo conexión con la cámara')
            elif self.language_value == 1:
                QtWidgets.QMessageBox.critical(self, 'Connection Error', 'There was no connection to the camera')

    # --------------------
    # Funciones Parametros
    # --------------------
    def on_setParameters_button_clicked(self):
        username = self.user_value.text()
        password = self.password_value.text()
        ip_address = self.ipaddress_value.text()
        current_ptz = backend.set_parameters(self.fps_text.value(), self.compression_spin.value(), 
                               ip_address, username, password)

        if current_ptz == 'error':
            if self.language_value == 0:
                QtWidgets.QMessageBox.critical(self, 'Error de Conexión', 'No hubo conexión con la cámara')
            elif self.language_value == 1:
                QtWidgets.QMessageBox.critical(self, 'Connection Error', 'There was no connection to the camera')


    # --------------
    # Funciones Main
    # --------------
    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        width = self.geometry().width()

        self.titulo_card.setGeometry(10, 10, width - 20, 50)
        self.idioma_menu.setGeometry(width - 280, 10, 70, 30)
        self.tema_switch.setGeometry(width - 200, 10, 50, 30)
        self.manual_button.setGeometry(width - 140, 10, 30, 30)
        self.about_button.setGeometry(width - 100, 10, 30, 30)
        self.aboutQt_button.setGeometry(width - 60, 10, 30, 30)

        self.controles_card.setGeometry(width-200, 70, 190, 150)
        self.posicion_card.setGeometry(width-200, 230, 190, 380)
        self.parametros_card.setGeometry(width-200, 620, 190, 230)

        return super().resizeEvent(a0)


    def closeEvent(self, event):
        try:
            self.thread.stop()
        except:
            pass
        event.accept()

    # ----------------
    # Funciones Imagen
    # ----------------
    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)
        if self.record_button.isChecked():
            self.thread.output.write(cv_img)
    
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format.Format_RGB888)
        p = convert_to_Qt_format.scaled(1280, 720, Qt.AspectRatioMode.KeepAspectRatio)
        return QPixmap.fromImage(p)

    
if __name__=="__main__":
    app = QApplication(sys.argv)
    a = App()
    a.show()
    sys.exit(app.exec())
