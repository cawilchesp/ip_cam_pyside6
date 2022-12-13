from PyQt6 import QtWidgets
from PyQt6.QtCore import QSettings

import sys
import time
import psycopg2
import requests
from requests.auth import HTTPDigestAuth

import material3_components as mt3

# -------------
# Base de Datos
# -------------
def create_db(db_name: str, db_password: str):
    connection = psycopg2.connect(user='postgres', 
                                password=db_password, 
                                host='localhost', 
                                port='5432', 
                                database=db_name)
    cursor = connection.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS cameras (
                    id serial PRIMARY KEY,
                    nombre VARCHAR(128) UNIQUE NOT NULL,
                    ip_camera VARCHAR(15) UNIQUE NOT NULL,
                    username VARCHAR(128) NOT NULL,
                    password VARCHAR(128) NOT NULL
                    )""")
    connection.commit()

    cursor.execute('SELECT * FROM cameras')
    ip_cameras_value = cursor.fetchall()
    connection.close()

    return ip_cameras_value


def add_db(camera_data, db_name: str, db_password: str):
    name_value = camera_data['name']
    ip_value = camera_data['ip']
    username_value = camera_data['username']
    password_value = camera_data['password']

    connection = psycopg2.connect(user='postgres', 
                                password=db_password, 
                                host='localhost', 
                                port='5432', 
                                database=db_name)
    cursor = connection.cursor()
    insert_query = f"""INSERT INTO cameras (NOMBRE, IP_CAMERA, USERNAME, PASSWORD) 
                    VALUES ('{name_value}', '{ip_value}', '{username_value}', '{password_value}')"""
    cursor.execute(insert_query)
    connection.commit()
    cursor.execute('SELECT * FROM cameras')
    ip_cameras_value = cursor.fetchall()
    connection.close()
    
    return ip_cameras_value


def get_db(camera_name, db_name: str, db_password: str):
    connection = psycopg2.connect(user='postgres', 
                                password=db_password, 
                                host='localhost', 
                                port='5432', 
                                database=db_name)
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM cameras WHERE nombre='{camera_name}'")
    data = cursor.fetchall()
    connection.close()
    
    return data


def edit_db(camera_id, camera_data, db_name: str, db_password: str):
    name_value = camera_data['name']
    ip_value = camera_data['ip']
    username_value = camera_data['username']
    password_value = camera_data['password']

    connection = psycopg2.connect(user='postgres', 
                                password=db_password, 
                                host='localhost', 
                                port='5432', 
                                database=db_name)
    cursor = connection.cursor()
    update_query = f"""UPDATE cameras 
                    SET (nombre, ip_camera, username, password)
                    = ('{name_value}', '{ip_value}', '{username_value}', '{password_value}') 
                    WHERE id = '{camera_id}' """
    cursor.execute(update_query)
    connection.commit()
    cursor.execute('SELECT * FROM cameras')
    ip_cameras_value = cursor.fetchall()
    connection.close()

    return ip_cameras_value


def delete_db(camera_name, db_name: str, db_password: str):
    connection = psycopg2.connect(user='postgres', 
                                password=db_password, 
                                host='localhost', 
                                port='5432', 
                                database=db_name)
    cursor = connection.cursor()
    delete_query = f"DELETE FROM cameras WHERE nombre='{camera_name}'"
    cursor.execute(delete_query)
    connection.commit()
    cursor.execute('SELECT * FROM cameras')
    ip_cameras_value = cursor.fetchall()
    connection.close()

    return ip_cameras_value


# ------
# Cámara
# ------
def get_PTZ(ipaddress: str, username: str, password: str):
    data = { 'query': 'position' }
    result = {}
    camera_url = f'http://{ipaddress}/axis-cgi/com/ptz.cgi'
    timeout = 3 # seconds

    try:
        camera_res = requests.post(camera_url, data = data, auth = HTTPDigestAuth(username, password))
    
        for line in camera_res.text.splitlines():
            (name, var) = line.split('=', 2)
            try:
                result[name.strip()] = float(var)
            except ValueError:
                result[name.strip()] = var
        
        return result
    except:
        return 'error'


def set_PTZ(pan_data: str, tilt_data: str, zoom_data: str, ipaddress: str, username: str, password: str):
        camera_url = f'http://{ipaddress}/axis-cgi/com/ptz.cgi'

        data = {
            'camera': 1,
            'imagerotation': 0,
            'pan': pan_data,
            'tilt': tilt_data,
            'zoom': zoom_data,
            'html': 'no',
            'timestamp': int(time.time())
        }

        try:
            camera_res = requests.post(camera_url, data = data, auth = HTTPDigestAuth(username, password))
            return 'ok'
        except:
            return 'error'


def get_parameters(ipaddress: str, username: str, password: str):
    camera_url = f'http://{ipaddress}/axis-cgi/param.cgi'

    # ImageSource.I0.DayNight.IrCutFilter

    data = {
        'action': 'list',
        'group': 'Image.I0'
    }
    result = {}

    camera_res = requests.post(
        camera_url,
        data = data,
        auth = HTTPDigestAuth(username, password)
        )

    for line in camera_res.text.splitlines():
        (name, var) = line.split('=', 2)
        if name == 'root.Image.I0.Stream.FPS' or name == 'root.Image.I0.Appearance.Compression':
            try:
                result[name.strip()] = float(var)
            except ValueError:
                result[name.strip()] = var

    return result


def set_parameters(fps_data: int, compression_data: int, ipaddress: str, username: str, password: str):
    camera_url = f'http://{ipaddress}/axis-cgi/param.cgi'

    data = {
        'action': 'update',
        'Image.I0.Stream.FPS': str(fps_data),
        'Image.I0.Appearance.Compression': str(compression_data),
        'html': 'no',
        'timestamp': int(time.time())
    }

    try:
        camera_res = requests.post(camera_url, data = data,  auth = HTTPDigestAuth(username, password))
        return 'ok'
    except:
        return 'error'


def get_PTZ_limits(ipaddress: str, username: str, password: str):
    data = { 'query': 'limits' }
    result = {}
    camera_url = f'http://{ipaddress}/axis-cgi/com/ptz.cgi'
    timeout = 3 # seconds

    try:
        camera_res = requests.post(camera_url, data = data, auth = HTTPDigestAuth(username, password))
    
        for line in camera_res.text.splitlines():
            (name, var) = line.split('=', 2)
            try:
                result[name.strip()] = float(var)
            except ValueError:
                result[name.strip()] = var
        
        return result
    except:
        return 'error'

# ----------------
# About App Dialog
# ----------------
class AboutApp(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        # --------
        # Settings
        # --------
        self.settings = QSettings(f'{sys.path[0]}/settings.ini', QSettings.Format.IniFormat)
        self.language_value = int(self.settings.value('language'))
        self.theme_value = eval(self.settings.value('theme'))

        # ----------------
        # Generación de UI
        # ----------------
        width = 400
        height = 400
        screen_x = int(self.screen().availableGeometry().width() / 2 - (width / 2))
        screen_y = int(self.screen().availableGeometry().height() / 2 - (height / 2))

        if self.language_value == 0:
            self.setWindowTitle('Acerca de...')
        elif self.language_value == 1:
            self.setWindowTitle('About...')
        self.setGeometry(screen_x, screen_y, width, height)
        self.setMinimumSize(width, height)
        self.setMaximumSize(width, height)
        self.setModal(True)
        self.setObjectName('object_about')
        if self.theme_value:
            self.setStyleSheet(f'QWidget#object_about {{ background-color: #E5E9F0;'
                f'color: #000000 }}')
        else:
            self.setStyleSheet(f'QWidget#object_about {{ background-color: #3B4253;'
                f'color: #E5E9F0 }}')


        self.about_card = mt3.Card(self, 'about_card',
            (10, 10, width-20, height-20), self.theme_value)

        y, w = 10, width - 40
        mt3.TitleLabel(self.about_card, 'about_label',
            ('Video de Cámara en Vivo', 'Camera Live Video'), (10, y, w), self.theme_value, self.language_value)

        y += 40
        mt3.TitleLabel(self.about_card, 'version_label',
            ('Versión: 1.0', 'Version: 1.0'), (10, y, w), self.theme_value, self.language_value)

        y += 60
        mt3.LabelField(self.about_card, 'desarrollado_label',
            ('Desarrollado por:', 'Developed by:'), (10, y), self.theme_value, self.language_value)

        y += 40
        mt3.IconLabel(self.about_card, 'nombre_icon',
            (10, y), 'person', self.theme_value)

        y += 10
        mt3.LabelField(self.about_card, 'nombre_label',
            ('Carlos Andrés Wilches Pérez', 'Carlos Andrés Wilches Pérez'), (40, y), self.theme_value, self.language_value)

        y += 20
        mt3.IconLabel(self.about_card, 'profesion_icon',
            (10, y), 'school', self.theme_value)
        
        y += 10
        mt3.LabelField(self.about_card, 'profesion_label',
            ('Ingeniero Electrónico, BSc. MSc. PhD.', 'Electronic Engineer, BSc. MSc. PhD.'), (40, y), self.theme_value, self.language_value)
        
        y += 20
        mt3.LabelField(self.about_card, 'profesion_label',
            ('Universidad Nacional de Colombia', 'Universidad Nacional de Colombia'), (40, y), self.theme_value, self.language_value)

        y += 30
        mt3.LabelField(self.about_card, 'profesion_label',
            ('Maestría en Ingeniería Electrónica', 'Master in Electronic Engineering'), (40, y), self.theme_value, self.language_value)

        y += 20
        mt3.LabelField(self.about_card, 'profesion_label',
            ('Doctor en Ingeniería', 'Doctor in Engineering'), (40, y), self.theme_value, self.language_value)

        y += 20
        mt3.LabelField(self.about_card, 'profesion_label',
            ('Pontificia Universidad Javeriana', 'Pontificia Universidad Javeriana'), (40, y), self.theme_value, self.language_value)

        y += 20
        mt3.IconLabel(self.about_card, 'email_icon',
            (10, y), 'mail', self.theme_value)

        y += 10
        mt3.LabelField(self.about_card, 'email_label',
            ('cawilchesp@outlook.com', 'cawilchesp@outlook.com'), (40, y), self.theme_value, self.language_value)

        y += 30
        self.aceptar_button = mt3.TextButton(self.about_card, 'aceptar_button',
            ('Aceptar', 'Ok'), (w-90, y, 100), 'done.png', self.theme_value, self.language_value)
        self.aceptar_button.clicked.connect(self.on_aceptar_button_clicked)

    def on_aceptar_button_clicked(self):
        self.close()

# ---------------
# About Qt Dialog
# ---------------
def about_qt_dialog(parent, language: int):
    title = ''
    if language == 0:
        title = 'Acerca de Qt...'
    elif language == 1:
        title = 'About Qt...'

    QtWidgets.QMessageBox.aboutQt(parent, title)

