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


class Sidebar(QtWidgets.QFrame):
    def __init__(self, parent, object_name, geometry, style):
        super(Sidebar, self).__init__(parent)
        
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
        label_style = ''
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


class ItemLabel(QtWidgets.QLabel):
    def __init__(self, parent, object_name, labels, geometry, style, language):
        super(ItemLabel, self).__init__(parent)

        self.object_name = object_name
        self.text_es, self.text_en = labels
        x, y, w = geometry

        self.setObjectName(self.object_name)
        self.setGeometry(x, y, w, 30)
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


class ValueLabel(QtWidgets.QLabel):
    def __init__(self, parent, object_name, geometry, style):
        super(ValueLabel, self).__init__(parent)

        self.object_name = object_name
        x, y, w = geometry

        self.setObjectName(self.object_name)
        self.setGeometry(x, y, w, 30)
        self.apply_styleSheet(style)
    
    def apply_styleSheet(self, style):
        if style:
            value_label_style = (f'QLabel#{self.object_name} {{ border-radius: 15px; padding: 0 15 0 15;'
                f'border: 2px solid {light["on_background"]};'
                f'background-color: {light["surface"]};'
                f'color: {light["on_surface"]} }}')
        else:
            value_label_style = (f'QLabel#{self.object_name} {{ border-radius: 15px; padding: 0 15 0 15;'
                f'border: 2px solid {light["background"]};'
                f'background-color: {dark["surface"]};'
                f'color: {dark["on_surface"]} }}')
        self.setStyleSheet(value_label_style)


class IconLabel(QtWidgets.QLabel):
    def __init__(self, parent, object_name, geometry, icon):
        super(IconLabel, self).__init__(parent)

        self.object_name = object_name
        x, y, w, h = geometry

        self.setObjectName(self.object_name)
        self.setGeometry(x, y, w, h)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setPixmap(QtGui.QIcon(f'{current_path}/images/{icon}').pixmap(16))

class ColorLabel(QtWidgets.QLabel):
    def __init__(self, parent, object_name, geometry, color, style, language):
        super(ColorLabel, self).__init__(parent)

        self.object_name = object_name
        x, y = geometry
        self.color = color

        self.setObjectName(self.object_name)
        self.setGeometry(x, y, 30, 30)
        self.apply_styleSheet(style)
    
    def apply_styleSheet(self, style):
        if style:
            label_style = (f'QLabel#{self.object_name} {{ border-radius:15px;'
                f'color: {light["surface"]};'
                f'background-color: rgb({self.color}) }}')
        else:
            label_style = (f'QLabel#{self.object_name} {{ border-radius:15px;'
                f'color: {light["surface"]};'
                f'background-color: rgb({self.color}) }}')
        self.setStyleSheet(label_style)
    

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
        self.setEnabled(True)
        self.apply_styleSheet(style)
        self.language_text(language)
        self.setIcon(QtGui.QIcon(f'{current_path}/images/{icon}'))

    def apply_styleSheet(self, style):
        if style:
            button_style = (f'QToolButton#{self.object_name} {{ border: 0px solid; border-radius: 15; padding: 0 15 0 15;'
                f'background-color: {light["primary"]};'
                f'color: {light["on_primary"]} }}'
                f'QToolButton#{self.object_name}:hover {{ border: 0px solid; border-radius: 15; padding: 0 15 0 15;'
                f'background-color: {light["secondary"]};'
                f'color: {light["on_secondary"]} }}')
        else:
            button_style = (f'QToolButton#{self.object_name} {{ border: 0px solid; border-radius: 15; padding: 0 15 0 15;'
                f'background-color: {dark["primary"]};'
                f'color: {dark["on_primary"]} }}'
                f'QToolButton#{self.object_name}:hover {{ border: 0px solid; border-radius: 15; padding: 0 15 0 15;'
                f'background-color: {dark["secondary"]};'
                f'color: {dark["on_secondary"]} }}')
        self.setStyleSheet(button_style)

    def language_text(self, language):
        if language == 0:
            self.setText(self.text_es)
        elif language == 1:
            self.setText(self.text_en)


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


class ColorButton(QtWidgets.QToolButton):
    def __init__(self, parent, object_name, labels, geometry, icon, color, style, language):
        super(ColorButton, self).__init__(parent)

        self.object_name = object_name
        self.text_es, self.text_en = labels
        x, y, w = geometry

        self.setObjectName(self.object_name)
        self.setGeometry(x, y, w, 30)
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.setAutoRaise(True)
        self.setEnabled(True)
        self.apply_styleSheet(style, color)
        self.language_text(language)
        self.setIcon(QtGui.QIcon(f'{current_path}/images/{icon}'))

    def apply_styleSheet(self, style, color):
        color_rgb = color.split(',')
        rojo = float(color_rgb[0]) / 255.0
        verde = float(color_rgb[1]) / 255.0
        azul = float(color_rgb[2]) / 255.0

        luminancia = 0.2156 * rojo + 0.7152 * verde + 0.0722 * azul

        contraste_blanco = 1.05 / (luminancia + 0.05)
        contraste_negro = (luminancia + 0.05) / 0.05

        text_color = ''
        if contraste_negro > contraste_blanco:
            text_color = '0, 0, 0'
        else:
            text_color = '255, 255, 255'

        if style:
            button_style = (f'QToolButton#{self.object_name} {{ border: 0px solid; padding: 0 15 0 15;'
                f'border-radius: 15; background-color: rgb({color});'
                f'color: rgb({text_color}) }}'
                f'QToolButton#{self.object_name}:hover {{ border: 3px solid; padding: 0 15 0 15;'
                f'border-radius: 15; border-color: {light["secondary"]} }}')
        else:
            button_style = (f'QToolButton#{self.object_name} {{ border: 0px solid; padding: 0 15 0 15;'
                f'border-radius: 15; background-color: rgb({color});'
                f'color: rgb({text_color}) }}'
                f'QToolButton#{self.object_name}:hover {{ border: 3px solid; padding: 0 15 0 15;'
                f'border-radius: 15; border-color: {dark["secondary"]} }}')
        self.setStyleSheet(button_style)

    # Example
    # def on_color_button_clicked(self):
    #     selected_color = QtWidgets.QColorDialog.getColor()
    #     color = f'{selected_color.red()}, {selected_color.green()}, {selected_color.blue()}'
    #     self.color_button.apply_styleSheet(theme_value, color)
    #     settings.setValue('color', color)

    def language_text(self, language):
        if language == 0:
            self.setText(self.text_es)
        elif language == 1:
            self.setText(self.text_en)


class CheckableButton(QtWidgets.QToolButton):
    def __init__(self, parent, object_name, labels, geometry, icons, style, language):
        super(CheckableButton, self).__init__(parent)

        self.object_name = object_name
        self.text_es, self.text_en = labels
        self.icon_on, self.icon_off = icons
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


class ListComboBox(QtWidgets.QComboBox):
    def __init__(self, parent, object_name, geometry, max_items, max_count, style):
        super(ListComboBox, self).__init__(parent)

        self.object_name = object_name
        x, y, w = geometry

        self.setObjectName(self.object_name)
        self.setGeometry(x, y, w, 30)
        self.setMaxVisibleItems(max_items)
        self.setMaxCount(max_count)
        self.setSizeAdjustPolicy(QtWidgets.QComboBox.SizeAdjustPolicy.AdjustToMinimumContentsLengthWithIcon)
        self.view().window().setWindowFlags(Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint | Qt.WindowType.NoDropShadowWindowHint)
        self.view().window().setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.apply_styleSheet(style)

    def apply_styleSheet(self, style):
        if style:
            list_combobox_style = (
                f'QComboBox#{self.object_name} {{ border: 0px solid; border-radius: 15; padding: 0 15 0 15;'
                f'color: {light["on_background"]};'
                f'background-color: {light["background"]} }}'
                f'QComboBox#{self.object_name}::drop-down {{ border-color: {light["background"]} }}'
                f'QComboBox#{self.object_name}::down-arrow {{ image: url({current_path}/images/down_triangle.png) }}'
                f'QComboBox#{self.object_name}:!Enabled {{ background-color: {light["disable"]} }}'
                f'QComboBox#{self.object_name} QListView {{ border: 1px solid; border-radius: 15; padding: 0 15 0 15;'
                f'background-color: {light["background"]}; color: {light["on_background"]} }}'
                )
        else:
            list_combobox_style = (
                f'QComboBox#{self.object_name} {{ border: 0px solid; border-radius: 15; padding: 0 15 0 15;'
                f'color: {light["on_background"]};'
                f'background-color: {light["background"]} }}'
                f'QComboBox#{self.object_name}::drop-down {{ border-color: {light["background"]} }}'
                f'QComboBox#{self.object_name}::down-arrow {{ image: url({current_path}/images/down_triangle.png) }}'
                f'QComboBox#{self.object_name}:!Enabled {{ background-color: {dark["disable"]} }}'
                f'QComboBox#{self.object_name} QListView {{ border: 1px solid; border-radius: 15; padding: 0 15 0 15;'
                f'background-color: {light["background"]}; color: {light["on_background"]} }}'
                )
        self.setStyleSheet(list_combobox_style)

    def add_item(self, item):
        self.addItem(item)


class StaticComboBox(QtWidgets.QComboBox):
    def __init__(self, parent, object_name, geometry, max_items, options_dict, style, language):
        super(StaticComboBox, self).__init__(parent)

        self.object_name = object_name
        x, y, w = geometry
        self.options_dict = options_dict

        self.setObjectName(self.object_name)
        self.setGeometry(x, y, w, 30)
        self.setMaxVisibleItems(max_items)
        self.setMaxCount(max_items)
        self.setSizeAdjustPolicy(QtWidgets.QComboBox.SizeAdjustPolicy.AdjustToMinimumContentsLengthWithIcon)
        self.language_text(language)
        self.setCurrentIndex(-1)
        self.view().window().setWindowFlags(Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint | Qt.WindowType.NoDropShadowWindowHint)
        self.view().window().setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.apply_styleSheet(style)
        
    def apply_styleSheet(self, style):
        if style:
            static_combobox_style = (
                f'QComboBox#{self.object_name} {{ border: 0px solid; border-radius: 15; padding: 0 15 0 15;'
                f'color: {light["on_background"]};'
                f'background-color: {light["background"]} }}'
                f'QComboBox#{self.object_name}::drop-down {{ border-color: {light["background"]} }}'
                f'QComboBox#{self.object_name}::down-arrow {{ image: url({current_path}/images/down_triangle.png) }}'
                f'QComboBox#{self.object_name}:!Enabled {{ background-color: {light["disable"]} }}'
                f'QComboBox#{self.object_name} QListView {{ border: 1px solid; border-radius: 15; padding: 0 15 0 15;'
                f'background-color: {light["background"]}; color: {light["on_background"]} }}'
                )
        else:
            static_combobox_style = (
                f'QComboBox#{self.object_name} {{ border: 0px solid; border-radius: 15; padding: 0 15 0 15;'
                f'color: {light["on_background"]};'
                f'background-color: {light["background"]} }}'
                f'QComboBox#{self.object_name}::drop-down {{ border-color: {light["background"]} }}'
                f'QComboBox#{self.object_name}::down-arrow {{ image: url({current_path}/images/down_triangle.png) }}'
                f'QComboBox#{self.object_name}:!Enabled {{ background-color: {dark["disable"]} }}'
                f'QComboBox#{self.object_name} QListView {{ border: 1px solid; border-radius: 15; padding: 0 15 0 15;'
                f'background-color: {light["background"]}; color: {light["on_background"]} }}'
                )
        self.setStyleSheet(static_combobox_style)

    def language_text(self, language):
        for key, value in self.options_dict.items():
            self.addItem('')
            if language == 0:
                self.setItemText(key, value[0])
            elif language == 1:
                self.setItemText(key, value[1])


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
        self.setEnabled(True)
        self.apply_styleSheet(style)

    def apply_styleSheet(self, style):
        if style:
            self.setStyleSheet(f'QSlider#{self.object_name} {{ background-color: {light["surface"]} }}')
        else:
            self.setStyleSheet(f'QSlider#{self.object_name} {{ background-color: {dark["surface"]} }}')


class ObjectLineEdit(QtWidgets.QLineEdit):
    def __init__(self, parent, object_name, geometry, style):
        super(ObjectLineEdit, self).__init__(parent)

        self.object_name = object_name
        x, y, w = geometry

        self.setObjectName(self.object_name)
        self.setGeometry(x, y, w, 30)
        self.setEnabled(True)
        self.setClearButtonEnabled(True)
        self.apply_styleSheet(style)

    def apply_styleSheet(self, style):
        if style:
            edit_style = (f'QLineEdit#{self.object_name} {{ border: 0px solid; border-radius: 15; padding: 0 15 0 15;'
                    f'color: {light["on_background"]};'
                    f'background-color: {light["background"]} }}'
                    f'QLineEdit#{self.object_name}:!Enabled {{ border: 0px solid; border-radius: 15; padding: 0 15 0 15;'
                    f'background-color: {light["disable"]} }}')
        else:
            edit_style = (f'QLineEdit#{self.object_name} {{ border: 0px solid; border-radius: 15; padding: 0 15 0 15;'
                    f'color: {light["on_background"]};'
                    f'background-color: {light["background"]} }}'
                    f'QLineEdit#{self.object_name}:!Enabled {{ border: 0px solid; border-radius: 15; padding: 0 15 0 15;'
                    f'background-color: {dark["disable"]} }}')
        self.setStyleSheet(edit_style)


class ObjectSpinBox(QtWidgets.QSpinBox):
    def __init__(self, parent, object_name, geometry, min_value, max_value, style):
        super(ObjectSpinBox, self).__init__(parent)

        self.object_name = object_name
        x, y, w = geometry

        self.setObjectName(self.object_name)
        self.setGeometry(x, y, w, 30)
        self.setMinimum(min_value)
        self.setMaximum(max_value)
        self.apply_styleSheet(style)

    def apply_styleSheet(self, style):
        if style:
            spin_style = (f'QSpinBox {{ border: 0px solid; border-radius: 15; padding: 0 15 0 15;'
                    f'color: {light["on_background"]};'
                    f'background-color: {light["background"]} }}'
                    f'QSpinBox::up-button {{ border-color: {light["background"]} }}'
                    f'QSpinBox::down-button {{ border-color: {light["background"]} }}'
                    f'QSpinBox::up-arrow {{ image: url({current_path}/images/up_triangle.png) }}'
                    f'QSpinBox::down-arrow {{ image: url({current_path}/images/down_triangle.png) }}'
                    f'QSpinBox:!Enabled {{ background-color: {light["disable"]} }}')
        else:
            spin_style = (f'QSpinBox {{ border: 0px solid; border-radius: 15; padding: 0 15 0 15;'
                    f'color: {light["on_background"]};'
                    f'background-color: {light["background"]} }}'
                    f'QSpinBox::up-button {{ border-color: {light["background"]} }}'
                    f'QSpinBox::down-button {{ border-color: {light["background"]} }}'
                    f'QSpinBox::up-arrow {{ image: url({current_path}/images/up_triangle.png) }}'
                    f'QSpinBox::down-arrow {{ image: url({current_path}/images/down_triangle.png) }}'
                    f'QSpinBox:!Enabled {{ background-color: {light["disable"]} }}')
        self.setStyleSheet(spin_style)


class ObjectDoubleSpinBox(QtWidgets.QDoubleSpinBox):
    def __init__(self, parent, object_name, geometry, min_value, max_value, style):
        super(ObjectDoubleSpinBox, self).__init__(parent)

        self.object_name = object_name
        x, y, w = geometry

        self.setObjectName(self.object_name)

        self.setGeometry(x, y, w, 30)
        self.setMinimum(min_value)
        self.setMaximum(max_value)
        self.apply_styleSheet(style)

    def apply_styleSheet(self, style):
        if style:
            spin_2_style = (f'QDoubleSpinBox {{ border: 0px solid; border-radius: 15; padding: 0 15 0 15;'
                    f'color: {light["on_background"]};'
                    f'background-color: {light["background"]} }}'
                    f'QDoubleSpinBox::up-button {{ border-color: {light["background"]} }}'
                    f'QDoubleSpinBox::down-button {{ border-color: {light["background"]} }}'
                    f'QDoubleSpinBox::up-arrow {{ image: url({current_path}/images/up_triangle.png) }}'
                    f'QDoubleSpinBox::down-arrow {{ image: url({current_path}/images/down_triangle.png) }}'
                    f'QDoubleSpinBox:!Enabled {{ background-color: {light["disable"]} }}')
        else:
            spin_2_style = (f'QDoubleSpinBox {{ border: 0px solid; border-radius: 15; padding: 0 15 0 15;'
                    f'color: {light["on_background"]};'
                    f'background-color: {light["background"]} }}'
                    f'QDoubleSpinBox::up-button {{ border-color: {light["background"]} }}'
                    f'QDoubleSpinBox::down-button {{ border-color: {light["background"]} }}'
                    f'QDoubleSpinBox::up-arrow {{ image: url({current_path}/images/up_triangle.png) }}'
                    f'QDoubleSpinBox::down-arrow {{ image: url({current_path}/images/down_triangle.png) }}'
                    f'QDoubleSpinBox:!Enabled {{ background-color: {dark["disable"]} }}')
        self.setStyleSheet(spin_2_style)


class ObjectDateEdit(QtWidgets.QDateEdit):
    def __init__(self, parent, object_name, geometry, style):
        super(ObjectDateEdit, self).__init__(parent)

        self.object_name = object_name
        x, y, w = geometry

        self.setObjectName(self.object_name)
        self.setGeometry(x, y, w, 30)
        self.setCalendarPopup(True)
        self.setFrame(False)
        self.setSpecialValueText('')
        self.setDate(QtCore.QDate.currentDate())
        self.apply_styleSheet(style)

    def apply_styleSheet(self, style):
        if style:
            date_edit_style = (f'QDateEdit#{self.object_name} {{ border: 0px solid; border-radius: 15; padding: 0 15 0 15;'
            f'color: {light["on_background"]};'
            f'background-color: {light["background"]} }}'
            f'QDateEdit#{self.object_name}::drop-down {{ border-color: {light["background"]} }}'
            f'QDateEdit#{self.object_name}::down-arrow {{ image: url({current_path}/images/down_triangle.png) }}'
            )
        else:
            date_edit_style = (f'QDateEdit#{self.object_name} {{ border: 0px solid; border-radius: 15; padding: 0 15 0 15;'
            f'color: {light["on_background"]};'
            f'background-color: {light["background"]} }}'
            f'QDateEdit#{self.object_name}::drop-down {{ border-color: {light["background"]} }}'
            f'QDateEdit#{self.object_name}::down-arrow {{ image: url({current_path}/images/down_triangle.png) }}'
            )
        self.setStyleSheet(date_edit_style)


class lineSeparator(QtWidgets.QFrame):
    def __init__(self, parent=None, x=0, y=0, w=0, style=True):
        super(lineSeparator, self).__init__(parent)
        
        self.setGeometry(x, y, w, 10)
        self.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.apply_styleSheet(style)

    def apply_styleSheet(self, style):
        if style:
            line_style = f'background-color: {light["surface"]}'
        else:
            line_style = f'background-color: {dark["surface"]}'
        self.setStyleSheet(line_style)