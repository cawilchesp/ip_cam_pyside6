from PyQt6 import QtGui, QtWidgets, QtCore
from PyQt6.QtWidgets import QWidget, QApplication, QStyle
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

import sys

light = {
    'background': '#E5E9F0',
    'surface': '#B2B2B2',
    'primary': '#42A4F5',
    'secondary': '#FF2D55',
    'on_background': '#000000',
    'on_surface': '#000000',
    'on_primary': '#000000',
    'on_secondary': '#000000',
    'disable': '#B2B2B2',
    'error': ''
}

dark = {
    'background': '#3B4253',
    'surface': '#2E3441',
    'primary': '#42A4F5',
    'secondary': '#FF2D55',
    'on_background': '#E5E9F0',
    'on_surface': '#E5E9F0',
    'on_primary': '#000000',
    'on_secondary': '#000000',
    'disable': '#B2B2B2',
    'error': ''
}

current_path = sys.path[0].replace('\\','/')

# ----
# Card
# ----
class Card(QtWidgets.QFrame):
    def __init__(self, parent, object_name, geometry, style):
        super(Card, self).__init__(parent)
        
        self.object_name = object_name
        x, y, w, h = geometry

        self.setObjectName(self.object_name)
        self.setGeometry(x, y, w, h)
        self.apply_styleSheet(style)
    
    def apply_styleSheet(self, style):
        if style:
            sidebar_style = f'QFrame#{self.object_name} {{ background-color: {light["surface"]}; border-radius: 15px }}'
        else:
            sidebar_style = f'QFrame#{self.object_name} {{ background-color: {dark["surface"]}; border-radius: 15px }}'
        self.setStyleSheet(sidebar_style)

# -----------
# Label Field
# -----------
class LabelField(QtWidgets.QLabel):
    def __init__(self, parent, object_name, labels, geometry, style, language):
        super(LabelField, self).__init__(parent)

        self.object_name = object_name
        self.text_es, self.text_en = labels
        x, y = geometry

        self.setObjectName(self.object_name)
        self.setGeometry(x, y, 20, 20)
        self.setFont(QtGui.QFont('Segoe UI', 9))
        self.apply_styleSheet(style)
        self.language_text(language)
    
    def apply_styleSheet(self, style):
        if style:
            label_style = (f'QLabel#{self.object_name} {{ border: 0px solid;'
                f'padding: 0 5 0 5;'
                f'background-color: {light["surface"]};'
                f'color: {light["on_surface"]} }}')
        else:
            label_style = (f'QLabel#{self.object_name} {{ border: 0px solid;'
                f'padding: 0 5 0 5;'
                f'background-color: {dark["surface"]};'
                f'color: {dark["on_surface"]} }}')
        self.setStyleSheet(label_style)

    def language_text(self, language):
        if language == 0:
            self.setText(self.text_es)
        elif language == 1:
            self.setText(self.text_en)
        self.adjustSize()

# -----------
# Text Button
# -----------
class TextButton(QtWidgets.QToolButton):
    def __init__(self, parent, object_name, labels, geometry, icon, style, language):
        super(TextButton, self).__init__(parent)

        self.object_name = object_name
        self.text_es, self.text_en = labels
        x, y, w = geometry

        self.setObjectName(self.object_name)
        self.setGeometry(x, y, w, 30)
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.setAutoRaise(True)
        self.apply_styleSheet(style)
        self.language_text(language)
        self.setIcon(QtGui.QIcon(f'{current_path}/images/{icon}'))

    def apply_styleSheet(self, style):
        if style:
            button_style = (f'QToolButton#{self.object_name} {{ border: 0px solid; border-radius: 15; padding: 0 10 0 10;'
                f'background-color: {light["primary"]};'
                f'color: {light["on_primary"]} }}'
                f'QToolButton#{self.object_name}:hover {{ '
                f'background-color: {light["secondary"]};'
                f'color: {light["on_secondary"]} }}')
        else:
            button_style = (f'QToolButton#{self.object_name} {{ border: 0px solid; border-radius: 15; padding: 0 10 0 10;'
                f'background-color: {dark["primary"]};'
                f'color: {dark["on_primary"]} }}'
                f'QToolButton#{self.object_name}:hover {{ '
                f'background-color: {dark["secondary"]};'
                f'color: {dark["on_secondary"]} }}')
        self.setStyleSheet(button_style)

    def language_text(self, language):
        if language == 0:
            self.setText(self.text_es)
        elif language == 1:
            self.setText(self.text_en)

# ----------------
# Segmented Button
# ----------------
class SegmentedButton(QtWidgets.QToolButton):
    def __init__(self, parent, object_name, geometry, labels, icons, position, style, language):
        super(SegmentedButton, self).__init__(parent)

        self.object_name = object_name
        self.text_es, self.text_en = labels
        self.icon_on, self.icon_off = icons
        self.position = position
        x, y, w = geometry

        self.setObjectName(self.object_name)
        self.setGeometry(x, y, w, 30)
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.setCheckable(True)
        self.setEnabled(True)
        self.apply_styleSheet(style)
        self.language_text(language)
        
    def set_state(self, state):
        if state:
            self.setIcon(QtGui.QIcon(f'{current_path}/images/{self.icon_on}'))
            self.setChecked(True)
        else:
            self.setIcon(QtGui.QIcon(f'{current_path}/images/{self.icon_off}'))
            self.setChecked(False)

    def apply_styleSheet(self, style):
        if self.position == 'left':
            border_position = 'border-top-left-radius: 15; border-bottom-left-radius: 15'
        elif self.position == 'center':
            border_position = 'border-radius: 0'
        elif self.position == 'right':
            border_position = 'border-top-right-radius: 15; border-bottom-right-radius: 15'
        if style:
            check_button_style = (f'QToolButton#{self.object_name} {{ '
                f'border: 1px solid {light["on_surface"]}; {border_position};'
                f'padding: 0 15 0 15;'
                f'background-color: {light["primary"]};'
                f'color: {light["on_primary"]} }}'
                f'QToolButton#{self.object_name}:checked {{'
                f'background-color: {light["secondary"]};'
                f'color: {light["on_secondary"]} }}')
        else:
            check_button_style = (f'QToolButton#{self.object_name} {{ '
                f'border: 1px solid {dark["on_surface"]}; {border_position};'
                f'padding: 0 15 0 15;'
                f'background-color: {dark["primary"]};'
                f'color: {dark["on_primary"]} }}'
                f'QToolButton#{self.object_name}:checked {{'
                f'background-color: {dark["secondary"]};'
                f'color: {dark["on_secondary"]} }}')
        self.setStyleSheet(check_button_style)

    def language_text(self, language):
        if language == 0:
            self.setText(self.text_es)
        elif language == 1:
            self.setText(self.text_en)

# -----------
# Icon Button
# -----------
class IconButton(QtWidgets.QToolButton):
    def __init__(self, parent, object_name, geometry, icon, style):
        super(IconButton, self).__init__(parent)

        self.object_name = object_name
        x, y = geometry

        self.setObjectName(self.object_name)
        self.setGeometry(x, y, 30, 30)
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.setAutoRaise(True)
        self.setEnabled(True)
        self.apply_styleSheet(style)
        self.setIcon(QtGui.QIcon(f'{current_path}/images/{icon}'))
    
    def apply_styleSheet(self, style):
        if style:
            onlyicon_button_style = (f'QToolButton#{self.object_name} {{ border: 0px solid; border-radius: 15;'
                f'background-color: {light["primary"]};'
                f'color: {light["on_primary"]} }}'
                f'QToolButton#{self.object_name}:hover {{ border: 0px solid; border-radius: 15;'
                f'background-color: {light["secondary"]};'
                f'color: {light["on_secondary"]} }}')
        else:
            onlyicon_button_style = (f'QToolButton#{self.object_name} {{ border: 0px solid; border-radius: 15;'
                f'background-color: {dark["primary"]};'
                f'color: {dark["on_primary"]} }}'
                f'QToolButton#{self.object_name}:hover {{ border: 0px solid; border-radius: 15;'
                f'background-color: {dark["secondary"]};'
                f'color: {dark["on_secondary"]} }}')
        self.setStyleSheet(onlyicon_button_style)

# ------------
# Color Button
# ------------
class ColorButton(QtWidgets.QToolButton):
    def __init__(self, parent, object_name, geometry, color, style):
        super(ColorButton, self).__init__(parent)

        self.object_name = object_name
        x, y = geometry

        self.setObjectName(self.object_name)
        self.setGeometry(x, y, 30, 30)
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.setAutoRaise(True)
        self.setEnabled(True)
        self.apply_styleSheet(style, color)

    def apply_styleSheet(self, style, color):
        if style:
            button_style = (f'QToolButton#{self.object_name} {{ border: 0px solid; padding: 0 15 0 15;'
                f'border-radius: 15; background-color: rgb({color}) }}'
                f'QToolButton#{self.object_name}:hover {{ border: 3px solid; padding: 0 15 0 15;'
                f'border-radius: 15; border-color: {light["secondary"]} }}')
        else:
            button_style = (f'QToolButton#{self.object_name} {{ border: 0px solid; padding: 0 15 0 15;'
                f'border-radius: 15; background-color: rgb({color}) }}'
                f'QToolButton#{self.object_name}:hover {{ border: 3px solid; padding: 0 15 0 15;'
                f'border-radius: 15; border-color: {dark["secondary"]} }}')
        self.setStyleSheet(button_style)

# ------
# Switch
# ------
class Switch(QtWidgets.QToolButton):
    def __init__(self, parent, object_name, labels, geometry, icons, style, language):
        super(Switch, self).__init__(parent)

        self.object_name = object_name
        self.text_es, self.text_en = labels
        self.icon_on, self.icon_off = icons
        x, y, w = geometry

        self.setObjectName(self.object_name)
        self.setGeometry(x, y, w, 30)
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.setCheckable(True)
        self.apply_styleSheet(style)
        self.language_text(language)
        
    def set_state(self, state):
        if state:
            self.setIcon(QtGui.QIcon(f'{current_path}/images/{self.icon_on}'))
            self.setChecked(True)
        else:
            self.setIcon(QtGui.QIcon(f'{current_path}/images/{self.icon_off}'))
            self.setChecked(False)

    def apply_styleSheet(self, style):
        if style:
            check_button_style = (f'QToolButton#{self.object_name} {{ border: 0px solid; padding: 0 15 0 15; border-radius: 15;'
                f'background-color: {light["primary"]};'
                f'color: {light["on_primary"]} }}'
                f'QToolButton#{self.object_name}:checked {{'
                f'background-color: {light["secondary"]};'
                f'color: {light["on_secondary"]} }}')
        else:
            check_button_style = (f'QToolButton#{self.object_name} {{ border: 0px solid; padding: 0 15 0 15; border-radius: 15;'
                f'background-color: {dark["primary"]};'
                f'color: {dark["on_primary"]} }}'
                f'QToolButton#{self.object_name}:checked {{'
                f'background-color: {dark["secondary"]};'
                f'color: {dark["on_secondary"]} }}')
        self.setStyleSheet(check_button_style)

    def language_text(self, language):
        if language == 0:
            self.setText(self.text_es)
        elif language == 1:
            self.setText(self.text_en)

# ----------
# Text Field
# ----------
class TextField(QtWidgets.QLineEdit):
    def __init__(self, parent, object_name, geometry, style):
        super(TextField, self).__init__(parent)

        self.object_name = object_name
        x, y, w = geometry

        self.setObjectName(self.object_name)
        self.setGeometry(x, y, w, 40)
        self.setEnabled(True)
        self.setClearButtonEnabled(True)
        self.apply_styleSheet(style)

    def apply_styleSheet(self, style):
        if style:
            edit_style = (f'QLineEdit#{self.object_name} {{ border: 1px solid {light["on_surface"]};'
                f'border-radius: 5; padding: 0 10 0 10;'
                f'color: {light["on_surface"]};'
                f'background-color: {light["surface"]} }}'
                f'QLineEdit#{self.object_name}:!Enabled {{ border: 1px solid {light["on_surface"]};'
                f'border-radius: 5; padding: 0 10 0 10;'
                f'background-color: {light["disable"]} }}')
        else:
            edit_style = (f'QLineEdit#{self.object_name} {{ border: 1px solid {dark["on_surface"]};'
                f'border-radius: 5; padding: 0 10 0 10;'
                f'color: {dark["on_surface"]};'
                f'background-color: {dark["surface"]} }}'
                f'QLineEdit#{self.object_name}:!Enabled {{ border: 1px solid {dark["on_surface"]};'
                f'border-radius: 5; padding: 0 10 0 10;'
                f'background-color: {dark["disable"]} }}')
        self.setStyleSheet(edit_style)

# ----------
# Date Field
# ----------
class DateField(QtWidgets.QDateEdit):
    def __init__(self, parent, object_name, geometry, style):
        super(DateField, self).__init__(parent)

        self.object_name = object_name
        x, y, w = geometry

        self.setObjectName(self.object_name)
        self.setGeometry(x, y, w, 40)
        self.setCalendarPopup(True)
        self.setFrame(False)
        self.setSpecialValueText('')
        self.setDate(QtCore.QDate.currentDate())
        self.apply_styleSheet(style)

    def apply_styleSheet(self, style):
        if style:
            date_edit_style = (f'QDateEdit#{self.object_name} {{ border: 1px solid {light["on_surface"]};'
                f'border-radius: 5; padding: 0 10 0 10;'
                f'color: {light["on_surface"]};'
                f'background-color: {light["surface"]} }}'
                f'QDateEdit#{self.object_name}::drop-down {{ background-color: {light["primary"]};'
                f'width: 30; height: 30; subcontrol-position: center right; left: -5; border-radius: 15 }}'
                f'QDateEdit#{self.object_name}::down-arrow {{ image: url({current_path}/images/calendar_L.png);'
                f'width: 16; height: 16 }}'
                )
        else:
            date_edit_style = (f'QDateEdit#{self.object_name} {{ border: 1px solid {dark["on_surface"]};'
                f'border-radius: 5; padding: 0 10 0 10;'
                f'color: {dark["on_surface"]};'
                f'background-color: {dark["surface"]} }}'
                f'QDateEdit#{self.object_name}::drop-down {{ background-color: {dark["primary"]};'
                f'width: 30; height: 30; subcontrol-position: center right; left: -5; border-radius: 15 }}'
                f'QDateEdit#{self.object_name}::down-arrow {{ image: url({current_path}/images/calendar_L.png);'
                f'width: 16; height: 16 }}'
                )
        self.setStyleSheet(date_edit_style)

# -----------
# Title Label
# -----------
class TitleLabel(QtWidgets.QLabel):
    def __init__(self, parent, object_name, labels, geometry, style, language):
        super(TitleLabel, self).__init__(parent)

        self.object_name = object_name
        self.text_es, self.text_en = labels
        x, y, w = geometry

        self.setObjectName(self.object_name)
        self.setGeometry(x, y, w, 30)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.apply_styleSheet(style)
        self.language_text(language)
    
    def apply_styleSheet(self, style):
        if style:
            label_style = (f'QLabel#{self.object_name} {{ border-radius: 15px; padding: 0 15 0 15;'
                f'background-color: {light["surface"]};'
                f'color: {light["on_surface"]} }}')
        else:
            label_style = (f'QLabel#{self.object_name} {{ border-radius: 15px; padding: 0 15 0 15;'
                f'background-color: {dark["surface"]};'
                f'color: {dark["on_surface"]} }}')
        self.setStyleSheet(label_style)

    def language_text(self, language):
        if language == 0:
            self.setText(self.text_es)
        elif language == 1:
            self.setText(self.text_en)

# ----------
# Item Label
# ----------
class ItemLabel(QtWidgets.QLabel):
    def __init__(self, parent, object_name, geometry, style):
        super(ItemLabel, self).__init__(parent)

        self.object_name = object_name
        x, y, w = geometry

        self.setObjectName(self.object_name)
        self.setGeometry(x, y, w, 30)
        self.apply_styleSheet(style)
    
    def apply_styleSheet(self, style):
        if style:
            label_style = (f'QLabel#{self.object_name} {{ padding: 0 10 0 10;'
                f'background-color: {light["surface"]};'
                f'color: {light["on_surface"]} }}')
        else:
            label_style = (f'QLabel#{self.object_name} {{ padding: 0 10 0 10;'
                f'background-color: {dark["surface"]};'
                f'color: {dark["on_surface"]} }}')
        self.setStyleSheet(label_style)

# -----------
# Value Label
# -----------
class ValueLabel(QtWidgets.QLabel):
    def __init__(self, parent, object_name, geometry, style):
        super(ValueLabel, self).__init__(parent)

        self.object_name = object_name
        x, y, w = geometry

        self.setObjectName(self.object_name)
        self.setGeometry(x, y, w, 40)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.apply_styleSheet(style)
    
    def apply_styleSheet(self, style):
        if style:
            value_label_style = (f'QLabel#{self.object_name} {{ border-radius: 20px; padding: 0 10 0 10;'
                f'border: 2px solid {light["on_background"]};'
                f'background-color: {light["surface"]};'
                f'color: {light["on_surface"]} }}')
        else:
            value_label_style = (f'QLabel#{self.object_name} {{ border-radius: 20px; padding: 0 10 0 10;'
                f'border: 2px solid {light["background"]};'
                f'background-color: {dark["surface"]};'
                f'color: {dark["on_surface"]} }}')
        self.setStyleSheet(value_label_style)

# ----------
# Icon Label
# ----------
class IconLabel(QtWidgets.QLabel):
    def __init__(self, parent, object_name, geometry, icon, style):
        super(IconLabel, self).__init__(parent)

        self.object_name = object_name
        x, y = geometry
        self.theme = style

        self.setObjectName(self.object_name)
        self.setGeometry(x, y, 30, 30)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.set_icon(icon, style)
        self.apply_styleSheet(style)

    def set_icon(self, icon, style):
        if style:
            self.setPixmap(QtGui.QIcon(f'{current_path}/images/{icon}_L.png').pixmap(24))
        else:
            self.setPixmap(QtGui.QIcon(f'{current_path}/images/{icon}_D.png').pixmap(24))

    def apply_styleSheet(self, style):
        if style:
            value_label_style = (f'QLabel#{self.object_name} {{ '
                f'background-color: {light["surface"]};'
                f'color: {light["on_surface"]} }}')
        else:
            value_label_style = (f'QLabel#{self.object_name} {{ '
                f'background-color: {dark["surface"]};'
                f'color: {dark["on_surface"]} }}')
        self.setStyleSheet(value_label_style)

# -----------
# Color Label
# -----------
class ColorLabel(QtWidgets.QLabel):
    def __init__(self, parent, object_name, geometry, color):
        super(ColorLabel, self).__init__(parent)

        self.object_name = object_name
        x, y = geometry

        self.setObjectName(self.object_name)
        self.setGeometry(x, y, 30, 30)
        self.set_color(color)

    def set_color(self, color):
        label_style = (f'QLabel#{self.object_name} {{ border: 2px solid {light["secondary"]};'
                f'border-radius:15px; background-color: rgb({color}) }}')
        self.setStyleSheet(label_style)

# ----
# Menú
# ----
class Menu(QtWidgets.QComboBox):
    def __init__(self, parent, object_name, geometry, max_items, max_count, options_dict, style, language):
        super(Menu, self).__init__(parent)

        self.object_name = object_name
        x, y, w = geometry
        self.options_dict = options_dict

        self.setObjectName(self.object_name)
        self.setGeometry(x, y, w, 30)
        self.setMaxVisibleItems(max_items)
        self.setMaxCount(max_count)
        self.setSizeAdjustPolicy(QtWidgets.QComboBox.SizeAdjustPolicy.AdjustToMinimumContentsLengthWithIcon)
        self.language_text(language)
        self.setCurrentIndex(-1)
        self.view().window().setWindowFlags(Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint | Qt.WindowType.NoDropShadowWindowHint)
        self.view().window().setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.apply_styleSheet(style)

    def apply_styleSheet(self, style):
        if style:
            list_combobox_style = (
                f'QComboBox#{self.object_name} {{ border: 1px solid {light["on_surface"]}; border-radius: 5; padding: 0 10 0 10;'
                f'color: {light["on_surface"]};'
                f'background-color: {light["surface"]} }}'
                f'QComboBox#{self.object_name}::drop-down {{ border-color: {light["background"]} }}'
                f'QComboBox#{self.object_name}::down-arrow {{ image: url({current_path}/images/triangle_down_L.png); width: 16; height: 16 }}'
                f'QComboBox#{self.object_name}:!Enabled {{ background-color: {light["disable"]} }}'
                f'QComboBox#{self.object_name} QListView {{ border: 1px solid {light["on_surface"]}; border-radius: 5; padding: 0 10 0 10;'
                f'background-color: {light["surface"]}; color: {light["on_surface"]} }}'
                )
        else:
            list_combobox_style = (
                f'QComboBox#{self.object_name} {{ border: 1px solid {dark["on_surface"]}; border-radius: 5; padding: 0 10 0 10;'
                f'color: {dark["on_surface"]};'
                f'background-color: {dark["surface"]} }}'
                f'QComboBox#{self.object_name}::drop-down {{ border-color: {light["background"]} }}'
                f'QComboBox#{self.object_name}::down-arrow {{ image: url({current_path}/images/triangle_down_D.png); width: 16; height: 16 }}'
                f'QComboBox#{self.object_name}:!Enabled {{ background-color: {dark["disable"]} }}'
                f'QComboBox#{self.object_name} QListView {{ border: 1px solid {dark["on_surface"]}; border-radius: 5; padding: 0 10 0 10;'
                f'background-color: {dark["surface"]}; color: {dark["on_surface"]} }}'
                )
        self.setStyleSheet(list_combobox_style)

    def language_text(self, language):
        for key, value in self.options_dict.items():
            self.addItem('')
            if language == 0:
                self.setItemText(key, value[0])
            elif language == 1:
                self.setItemText(key, value[1])

    def add_item(self, item):
        self.addItem(item)

# ------
# Slider
# ------
class ObjectSlider(QtWidgets.QSlider):
    def __init__(self, parent, object_name, geometry, style):
        super(ObjectSlider, self).__init__(parent)

        self.object_name = object_name
        x, y, w = geometry

        self.setObjectName(self.object_name)
        self.setGeometry(x, y, w, 30)
        self.setOrientation(Qt.Orientation.Horizontal)
        self.setMinimum(0)
        self.setSingleStep(1)
        self.apply_styleSheet(style)

    def apply_styleSheet(self, style):
        if style:
            self.setStyleSheet(f'QSlider#{self.object_name} {{ background-color: {light["surface"]} }}')
        else:
            self.setStyleSheet(f'QSlider#{self.object_name} {{ background-color: {dark["surface"]} }}')

