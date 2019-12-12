# Import:
import os
import sys
import csv
import xlsxwriter
import sqlite3
import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QFileDialog, QMessageBox
from PyQt5.QtWidgets import QListWidgetItem, QColorDialog
from PyQt5.QtGui import QBrush, QColor, QIcon
from PyQt5.QtCore import QSettings, QDate
from PyQt5.Qt import Qt

# Import Interface:
from ui_files.ui_diary_main_window import Ui_DiaryMainWindow
from ui_files.ui_diary_detalies_dialog import Ui_DetailsEventDialog
from ui_files.ui_details_edit_dialog import Ui_DetailsEditDialog
from ui_files.ui_edit_event_dialog import Ui_EditEventDialog
from ui_files.ui_settings_dialog import Ui_SettingsDialog
from ui_files.ui_help_dialog import Ui_HelpDialog


class DiaryMainWindow(QMainWindow, Ui_DiaryMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(icon_name))
        self.user_settings = QSettings('user_settings.ini', QSettings.IniFormat)
        self.default_settings = QSettings('default_settings.ini', QSettings.IniFormat)
        self.name_data_base = 'diary.db'
        self.data_base_connect = sqlite3.connect(self.name_data_base)
        self.file = 'NONE'  # Путь до файла для текущего события
        self.filter = 'Все'  # Текущий фильтр по датам

        self.initUI()
        self.confirm_settings()  # Применение пользовательских настроек
        self.load_filter()  # Инициализация фильра по датам
        self.load_data_base_on_widget()  # Загрузка событий из базы данных в виджет

    def initUI(self):
        self.setWindowTitle('Diary')

        self.remove_btn.setDisabled(True)
        self.open_detalies_btn.setDisabled(True)
        self.remove_file_btn.setDisabled(True)
        self.choice_color_btn.setDisabled(True)

        self.add_btn.clicked.connect(self.add_event)
        self.add_file_btn.clicked.connect(self.add_file)
        self.open_detalies_btn.clicked.connect(self.open_event)
        self.remove_btn.clicked.connect(self.remove_event)
        self.remove_file_btn.clicked.connect(self.remove_file)
        self.choice_color_btn.clicked.connect(self.choice_color)
        self.today_date_btn.clicked.connect(self.today_date)

        self.actionExport.triggered.connect(self.export)
        self.actionSettings.triggered.connect(self.settings_dialog_open)
        self.actionHelp.triggered.connect(self.help_dialog_open)
        self.all_list_events.itemPressed.connect(self.change_event)
        self.all_list_events.itemDoubleClicked.connect(self.open_event)
        self.sorted_combo_box.currentTextChanged.connect(self.load_data_base_on_widget)
        self.filter_combo_box.currentTextChanged.connect(self.load_data_base_on_widget)
        self.important_check_box.toggled.connect(self.toggled_important)

    def load_filter(self):
        """Инициализация фильтра по датам. Обновление выпадающего списка дат."""
        old_filter = self.filter_combo_box.currentText()  # В случаи если при текущем фильтре
        # событие удалится, но при этом останутся события на данную дату, выбранный фильтр останется
        self.filter_combo_box.clear()
        self.filter_combo_box.addItem('Все')
        cursor = self.data_base_connect.cursor()
        date_filter = cursor.execute("""SELECT DISTINCT date FROM diarys""").fetchall()
        date_filter = list(map(lambda date: datetime.date.fromisoformat(date[0]), date_filter))
        date_filter = list(map(lambda date: date.isoformat(), sorted(date_filter)))
        self.filter_combo_box.addItems(date_filter)
        if old_filter in date_filter:
            self.filter_combo_box.setCurrentText(old_filter)
        cursor.close()

    def toggled_important(self):
        """Функция-обработчик установки и снятия флага важного события"""
        if self.important_check_box.isChecked():
            self.choice_color_btn.setDisabled(False)
        else:
            self.choice_color_btn.setDisabled(True)

    def today_date(self):
        self.calendar_edit.setSelectedDate(QDate.currentDate())

    def choice_color(self):
        """Функция-обработчик нажатия на кнопку выбора цвета для важного события"""
        if self.color:
            color = QColorDialog.getColor(self.color, self, 'Выбрать цвет')
        else:
            color = QColorDialog.getColor(self.default_color, self, 'Выбрать цвет')
        if color.isValid():
            self.color = color

    def change_event(self):
        """Функция-обработчик выбора собтия из списка событий"""
        self.open_detalies_btn.setDisabled(False)
        self.remove_btn.setDisabled(False)

    def check_date_event_and_delete(self):
        """Функция автоматического удаления прошедших по дате событий"""
        today_date = datetime.datetime.now().date()  # Текущяя дата

        cursor = self.data_base_connect.cursor()
        data = cursor.execute('SELECT title, date, time FROM diarys').fetchall()

        # Удаление событий у которых дата меньше текущей (время не учитывается):
        for event in data:
            date_event_datetime = datetime.date.fromisoformat(event[1])
            if date_event_datetime < today_date:
                title_event = event[0]
                date_event = event[1]
                time_event = event[2]
                cursor.execute("""
                 DELETE FROM diarys WHERE title = ? AND date = ? AND time = ?
                """, (title_event, date_event, time_event,))
        self.data_base_connect.commit()
        cursor.close()

    def load_data_base_on_widget(self):
        """Закгрузка событий из базы даных в главный виждет событий"""
        if self.auto_delete_event_setting == 'true' or self.auto_delete_event_setting is True:
            self.check_date_event_and_delete()
        self.filter = self.filter_combo_box.currentText()
        cursor = self.data_base_connect.cursor()
        self.all_list_events.clear()
        if self.sorted_combo_box.currentText() == 'Дата и время':
            data = cursor.execute("""
            SELECT title, date, date_string, time, important, color, details
            FROM diarys ORDER BY NOT important, date, time, title""").fetchall()
        elif self.sorted_combo_box.currentText() == 'Название':
            data = cursor.execute("""
            SELECT title, date, date_string, time, important, color, details
            FROM diarys ORDER BY NOT important, title, date, time""").fetchall()
        for select_event in data:
            title = select_event[0]
            date = select_event[1]
            if self.filter != date and self.filter != 'Все':
                continue
            date_string = select_event[2]
            time = ':'.join(select_event[3].split(':')[:2])
            important = select_event[4]
            details = select_event[6]
            if len(details) > 40:
                details = details[0:40] + '...'
            string_on_widget_list_event = '  |  '.join([date_string, time, title, details])

            item = QListWidgetItem()
            item.setText(string_on_widget_list_event)
            if important:
                color_value = tuple(map(lambda x: int(x), select_event[5].split(',')))
                color = QColor(*color_value)
                brush = QBrush()
                brush.setStyle(Qt.SolidPattern)
                brush.setColor(color)
                item.setBackground(brush)

            self.all_list_events.addItem(item)

        cursor.close()

        if not self.all_list_events.currentItem():
            self.remove_btn.setDisabled(True)
            self.open_detalies_btn.setDisabled(True)

    def export(self):
        """Экспорт базы данных в файл"""
        file_name = QFileDialog.getSaveFileName(self, 'Экспорт', '', """
                                                XLSX File (*.xlsx);;
                                                XLS File (*.xls);;
                                                CSV File (*.csv);;
                                                ALL Files (*)""")[0]
        if file_name:
            cursor = self.data_base_connect.cursor()
            format_file = file_name.split('.')[-1]  # Формат выходного файла

            head = list(map(lambda data: str(data[0]), cursor.execute("""
                                SELECT title, details, date, time FROM diarys""").description
                            ))  # Название колонок из базы данных
            if self.sorted_combo_box.currentText() == 'Дата и время':
                data = cursor.execute("""
                SELECT title, details, date, time
                FROM diarys ORDER BY NOT important, date, time, title""").fetchall()
            elif self.sorted_combo_box.currentText() == 'Название':
                data = cursor.execute("""
                SELECT title, details, date, time
                FROM diarys ORDER BY NOT important, title, date, time""").fetchall()
            if self.filter != 'Все':
                data = tuple(
                    filter(lambda data: data[2] == self.filter, data))  # Применение фильра по дате
            if format_file == 'csv':
                with open(file_name, mode='w', encoding='utf8', newline='') as csv_file:
                    writer = csv.writer(csv_file, delimiter=';', quotechar='"')
                    writer.writerow(head)
                    for row in data:
                        writer.writerow(row)
            elif format_file == 'xlsx' or format_file == 'xls':
                xls_file = xlsxwriter.Workbook(file_name)
                date_format = xls_file.add_format(
                    {'num_format': self.date_export_format})  # Формат колонок для даты
                time_format = xls_file.add_format(
                    {'num_format': self.time_export_format})  # Формат колонок для времени
                sheet = xls_file.add_worksheet()
                sheet.write_row(0, 0, head)
                for row in range(len(data)):
                    for col in range(len(data[0])):
                        if col == 2:  # Дата
                            date = datetime.date.fromisoformat(data[row][col])
                            sheet.write_datetime(row + 1, col, date, date_format)
                        elif col == 3:  # Время
                            time = datetime.time.fromisoformat(data[row][col])
                            sheet.write_datetime(row + 1, col, time, time_format)
                        else:
                            sheet.write(row + 1, col, data[row][col])
                xls_file.close()
            else:
                with open(file_name, mode='w', encoding='utf8') as file:
                    file.write(';'.join(head) + '\n')
                    for row in data:
                        row = list(map(lambda data: str(data), row))
                        file.write(';'.join(row) + '\n')
            cursor.close()

    def add_event(self):
        """Функция-обработчик нажатия на кноку добавления события"""
        title = self.name_edit.text().strip()
        details = self.details_edit.toPlainText().strip()
        date = self.calendar_edit.selectedDate().toPyDate().isoformat()
        date_string = self.calendar_edit.selectedDate().toString()
        time = self.time_edit.time().toPyTime().isoformat()
        important = self.important_check_box.isChecked()
        color = ','.join(list(map(lambda chanel: str(chanel), self.color.getRgb())))

        if not date or not time or not title or not details:
            QMessageBox.information(self, 'Ошибка', 'Заполнены не все поля')
        else:
            cursor = self.data_base_connect.cursor()
            if cursor.execute("""SELECT * FROM diarys 
                                            WHERE title = ? AND
                                            date = ? AND time = ?""",
                              (title, date,
                               time,)).fetchall():  # Проверка на существование такого события
                QMessageBox.information(self, 'Ошибка', 'Такая запись уже существует')
            else:
                cursor.execute("""INSERT INTO 
                diarys(title, details, date, date_string, time, file, important, color) 
                VALUES (?, ?, ? ,?, ?, ?, ?, ?) """,
                               (title, details, date, date_string, time, self.file,
                                important, color))

                self.data_base_connect.commit()
                self.load_filter()
                self.load_data_base_on_widget()

                self.name_edit.setText('')
                self.details_edit.setText('')

                self.file = 'NONE'
                self.file_name_line_edit.setText('')
                self.remove_file_btn.setDisabled(True)

                self.color = self.user_settings.value('color_important_event', None)
                if not self.color:
                    self.color = self.default_settings.value('color_important_event')

                self.important_check_box.setChecked(False)
            cursor.close()

    def add_file(self):
        """Функция-обработчик нажатия на кнопку прикрепления файла к событию"""
        file_name = QFileDialog.getOpenFileName(self, 'Выбрать файл' '')[0]
        if file_name:
            self.file = file_name
            self.file_name_line_edit.setText(file_name.split('/')[-1])
            self.remove_file_btn.setDisabled(False)

    def remove_file(self):
        """Функция-обработчик нажатия на кнопку удаления файла"""
        self.file = 'NONE'
        self.file_name_line_edit.setText('')
        self.remove_file_btn.setDisabled(True)

    def remove_event(self):
        """Функция-обработчик нажатия на кнопку удаления события"""
        cursor = self.data_base_connect.cursor()
        select_event = self.all_list_events.currentItem().text().split('  |  ')
        date_string = select_event[0]
        time = select_event[1] + ':00'
        title = select_event[2]
        cursor.execute("""
        DELETE FROM diarys WHERE title = ? AND date_string = ? AND time = ?""",
                       (title, date_string, time,))
        self.open_detalies_btn.setDisabled(True)
        self.remove_btn.setDisabled(True)
        self.data_base_connect.commit()
        self.load_filter()
        self.load_data_base_on_widget()
        cursor.close()

    def open_event(self):
        """Функция-обработчик нажатия на кнопку открытия подробностей о событии"""
        cursor = self.data_base_connect.cursor()
        select_event = self.all_list_events.currentItem().text().split('  |  ')
        date_string = select_event[0]
        time = select_event[1] + ':00'
        title = select_event[2]
        current_event = cursor.execute("""
        SELECT * FROM diarys WHERE title = ? AND date_string = ? AND time = ?""",
                                       (title, date_string, time,)).fetchall()
        self.details_event_dialog = DetailsEventDialog(current_event, self.user_settings,
                                                       self.data_base_connect)
        self.details_event_dialog.finished.connect(self.load_data_base_on_widget)
        self.details_event_dialog.exec()
        cursor.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:  # Удаление выбранного события
            if self.remove_btn.isEnabled():
                self.remove_event()
        elif event.key() == Qt.Key_Return:  # Открытие выбранного события
            if self.open_detalies_btn.isEnabled():
                self.open_event()
        elif event.key() == Qt.Key_F1:  # Открытие справки
            self.help_dialog_open()

    def settings_dialog_open(self):
        """Открытие окна настроек"""
        self.settings_dialog = SettingsDialog(self.user_settings, self.default_settings,
                                              self.confirm_settings)
        self.settings_dialog.exec()

    def help_dialog_open(self):
        """Открытие окна О Приложении"""
        self.help_dialog = HelpDialog()
        self.help_dialog.exec()

    def confirm_settings(self):
        """Применение настроек"""
        self.font_main_setting = self.user_settings.value('font_main', None)
        self.font_main_size_setting = self.user_settings.value('font_main_size', None)

        self.font_details_setting = self.user_settings.value('font_details', None)
        self.font_details_size_setting = self.user_settings.value('font_details_size', None)

        self.sorting_default_setting = self.user_settings.value('sorting_default', None)
        self.auto_delete_event_setting = self.user_settings.value('auto_delete_event', None)

        self.date_export_format = self.user_settings.value('date_export_format', None)
        self.time_export_format = self.user_settings.value('time_export_format', None)

        self.color_important_event_setting = self.user_settings.value('color_important_event', None)

        if self.font_main_setting:
            font_main = self.font_main_setting
            font_main.setPixelSize(int(self.font_main_size_setting))
            self.all_list_events.setFont(font_main)

        if self.sorting_default_setting:
            self.sorted_combo_box.setCurrentText(self.sorting_default_setting)

        if not self.date_export_format:
            self.date_export_format = self.default_settings.value('date_export_format')

        if not self.time_export_format:
            self.time_export_format = self.default_settings.value('time_export_format')

        if self.color_important_event_setting:
            self.color = self.color_important_event_setting
        else:
            self.color = self.default_settings.value('color_important_event')

        if self.auto_delete_event_setting == 'true' or self.auto_delete_event_setting is True:
            self.load_data_base_on_widget()


class SettingsDialog(QDialog, Ui_SettingsDialog):
    def __init__(self, user_settings, default_settings, confirm_settings_func):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(icon_name))
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowTitle('Настройки')

        self.user_settings = user_settings
        self.default_settings = default_settings
        self.confirm_settings_func = confirm_settings_func
        self.color_important_event_btn.clicked.connect(self.choice_color)
        self.settings_button_box.clicked.connect(self.enter_settings)
        self.default_settings_load_btn.clicked.connect(self.load_default_settings)
        self.color = self.user_settings.value('color_important_event', None)
        if not self.color:
            self.color = self.default_settings.value('color_important_event')
        self.load_settings()

    def choice_color(self):
        color = QColorDialog.getColor(self.color, self, 'Выбрать цвет')
        if color.isValid():
            self.color = color

    def enter_settings(self, button):
        """Применение настроек"""
        text_button = button.text()
        if text_button == 'Apply' or text_button == 'OK':
            font_main = self.font_main_combo_box.currentFont()
            font_main_size = self.font_size_main_combo_box.currentText()

            font_details = self.font_details_combo_box.currentFont()
            font_details_size = self.font_size_details_combo_box.currentText()

            date_export_format = self.date_format_combo_box.currentText()
            time_export_format = self.time_format_combo_box.currentText()

            sorting_default = self.sotring_default_combo_box.currentText()
            auto_delete_event = self.auto_delete_event_check_box.isChecked()

            self.user_settings.setValue('font_main', font_main)
            self.user_settings.setValue('font_main_size', font_main_size)

            self.user_settings.setValue('font_details', font_details)
            self.user_settings.setValue('font_details_size', font_details_size)

            self.user_settings.setValue('date_export_format', date_export_format)
            self.user_settings.setValue('time_export_format', time_export_format)

            self.user_settings.setValue('sorting_default', sorting_default)
            self.user_settings.setValue('auto_delete_event', auto_delete_event)

            self.user_settings.setValue('color_important_event', self.color)

            self.confirm_settings_func()

        if text_button == 'OK' or text_button == 'Cancel':
            self.close()

    def load_settings(self):
        """Загрузка текущих настроек"""
        font_main_setting = self.user_settings.value('font_main', None)
        font_main_size_setting = self.user_settings.value('font_main_size', None)

        font_details_setting = self.user_settings.value('font_details', None)
        font_details_size_setting = self.user_settings.value('font_details_size', None)

        sorting_default_setting = self.user_settings.value('sorting_default', None)
        auto_delete_event_setting = self.user_settings.value('auto_delete_event', None)

        date_export_format = self.user_settings.value('date_export_format', None)
        time_export_format = self.user_settings.value('time_export_format', None)

        if font_main_setting:
            self.font_main_combo_box.setCurrentFont(font_main_setting)
        if font_main_size_setting:
            self.font_size_main_combo_box.setCurrentText(font_main_size_setting)

        if font_details_setting:
            self.font_details_combo_box.setCurrentFont(font_details_setting)
        if font_details_size_setting:
            self.font_size_details_combo_box.setCurrentText(font_details_size_setting)

        if sorting_default_setting:
            self.sotring_default_combo_box.setCurrentText(sorting_default_setting)

        if auto_delete_event_setting == 'true' or auto_delete_event_setting is True:
            self.auto_delete_event_check_box.setChecked(True)
        elif auto_delete_event_setting == 'false' or auto_delete_event_setting is False:
            self.auto_delete_event_check_box.setChecked(False)

        if date_export_format:
            self.date_format_combo_box.setCurrentText(date_export_format)
        if time_export_format:
            self.time_format_combo_box.setCurrentText(time_export_format)

    def load_default_settings(self):
        """Загрузка стандартных настроек"""
        font_main_setting = self.default_settings.value('font_main')
        font_main_size_setting = self.default_settings.value('font_main_size')

        font_details_setting = self.default_settings.value('font_details')
        font_details_size_setting = self.default_settings.value('font_details_size')

        sorting_default_setting = self.default_settings.value('sorting_default')
        auto_delete_event_setting = self.default_settings.value('auto_delete_event')

        date_export_format = self.default_settings.value('date_export_format')
        time_export_format = self.default_settings.value('time_export_format')

        color_important_event = self.default_settings.value('color_important_event')

        self.font_main_combo_box.setCurrentFont(font_main_setting)
        self.font_size_main_combo_box.setCurrentText(font_main_size_setting)

        self.font_details_combo_box.setCurrentFont(font_details_setting)
        self.font_size_details_combo_box.setCurrentText(font_details_size_setting)

        self.sotring_default_combo_box.setCurrentText(sorting_default_setting)

        self.date_format_combo_box.setCurrentText(date_export_format)
        self.time_format_combo_box.setCurrentText(time_export_format)

        self.color = color_important_event

        if auto_delete_event_setting == 'true' or auto_delete_event_setting is True:
            self.auto_delete_event_check_box.setChecked(True)
        elif auto_delete_event_setting == 'false' or auto_delete_event_setting is False:
            self.auto_delete_event_check_box.setChecked(False)


class DetailsEventDialog(QDialog, Ui_DetailsEventDialog):
    def __init__(self, event, user_settings, data_base_connect):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(icon_name))
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.event = event[0]
        self.user_settings = user_settings
        self.data_base_connect = data_base_connect
        self.event_edit.clicked.connect(self.edit_event)
        self.open_file_btn.clicked.connect(self.open_file)
        self.close_btn.clicked.connect(self.close)
        self.initUI()

    def initUI(self):
        font_setting = self.user_settings.value('font_details', None)
        size_font_setting = self.user_settings.value('font_details_size', None)

        if font_setting:
            font = font_setting
            font.setPixelSize(int(size_font_setting))
            self.details_event_text.setFont(font)

        self.title = self.event[1]
        self.details = self.event[2]
        self.date = self.event[3]
        self.string_date = self.event[4]
        self.time = self.event[5]
        self.file = self.event[6]
        self.important = self.event[7]
        self.color = self.event[8]

        self.setWindowTitle(self.title)
        self.name_event_label.setText(self.title)
        self.details_event_text.setText(self.details)
        self.date_event_label.setText(self.string_date)
        self.time_event_label.setText(':'.join(self.time.split(':')[:2]))

        if os.path.exists(self.file):  # Проверка на существование файла данного события
            self.open_file_btn.setVisible(True)
            self.name_file_label.setText(self.file.split('/')[-1])
        else:
            self.file = 'NONE'
            self.open_file_btn.setVisible(False)
            self.name_file_label.setText('')

    def open_file(self):
        os.startfile(self.file)

    def edit_event(self):
        """Открытие окна редактирования события"""
        self.edit_event_window = EditEventDialog(self.title, self.date, self.time, self.details,
                                                 self.file, self.important, self.color,
                                                 self.data_base_connect, self.user_settings, self)
        self.edit_event_window.finished.connect(self.initUI)
        self.edit_event_window.exec()


class EditEventDialog(QDialog, Ui_EditEventDialog):
    def __init__(self, title, date, time, details, file, important, color, data_base_connect,
                 settings, details_window):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(icon_name))
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

        self.title = title
        self.date = date
        self.time = time
        self.details = details
        self.file = file
        self.important = important
        self.color = color
        self.details_window = details_window
        self.data_base_connect = data_base_connect
        self.settings = settings

        self.edit_details_btn.clicked.connect(self.details_edit)
        self.enter_edit_btn.clicked.connect(self.enter_edit)
        self.edit_add_file_btn.clicked.connect(self.edit_add_file)
        self.delete_file_btn.clicked.connect(self.delete_file)
        self.close_btn.clicked.connect(self.close)
        self.color_select_btn.clicked.connect(self.select_color)
        self.importatn_check_box.toggled.connect(self.important_toggled)

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        if self.file == 'NONE':
            self.edit_add_file_btn.setText('Добавить...')
            self.delete_file_btn.setDisabled(True)
        else:
            self.edit_add_file_btn.setText('Изменить...')
            self.delete_file_btn.setDisabled(False)

        if self.important:
            self.importatn_check_box.setChecked(True)
            self.color_select_btn.setDisabled(False)
        else:
            self.importatn_check_box.setChecked(False)
            self.color_select_btn.setDisabled(True)

        date_list = self.date.split("-")
        time_list = self.time.split(":")

        year = int(date_list[0])
        month = int(date_list[1])
        day = int(date_list[2])

        hours = int(time_list[0])
        minutes = int(time_list[1])

        self.title_line_edit.setText(self.title)
        self.date_edit.setDate(datetime.date(year, month, day))
        self.time_edit.setTime(datetime.time(hours, minutes))

        self.title_line_edit.setFocus()

    def important_toggled(self):
        """Функция-обработчик установки и снятия флага важного события"""
        if self.importatn_check_box.isChecked():
            self.color_select_btn.setDisabled(False)
        else:
            self.color_select_btn.setDisabled(True)

    def select_color(self):
        current_color = tuple(map(lambda chanel: int(chanel), self.color.split(',')))
        current_color = QColor(*current_color)
        new_color = QColorDialog.getColor(current_color, self, 'Выбрать цвет')
        if new_color.isValid():
            self.color = ','.join(list(map(lambda chanel: str(chanel), new_color.getRgb())))

    def enter_edit(self):
        """Apply event changes"""
        new_title = self.title_line_edit.text()
        new_date = self.date_edit.date().toPyDate().isoformat()
        new_date_string = self.date_edit.date().toString()
        new_time = self.time_edit.time().toPyTime().isoformat()
        new_important = self.importatn_check_box.isChecked()

        if not new_date or not new_time or not new_title or not self.details:
            QMessageBox.information(self, 'Ошибка', 'Заполнены не все поля')
        else:
            cursor = self.data_base_connect.cursor()
            cursor.execute("""
            UPDATE diarys SET title = ?, date = ?, date_string = ?, time = ?, 
            details = ?, file = ?, important = ?, color = ?
            WHERE title = ? AND date = ? AND time = ?""",
                           (new_title, new_date, new_date_string, new_time,
                            self.details, self.file, new_important, self.color,
                            self.title, self.date, self.time,))
            self.data_base_connect.commit()
            new_event = cursor.execute(
                """SELECT * FROM diarys WHERE title = ? AND date = ? AND time = ?""",
                (new_title, new_date, new_time)).fetchall()
            self.details_window.event = new_event[0]

            cursor.close()
            self.close()

    def details_edit(self):
        """Открытие окна изменения деталей события"""
        self.details_edit_window = DetailsEditDialog(self.settings, self)
        self.details_edit_window.exec()

    def edit_add_file(self):
        """Добавление и изменеие файла"""
        file = QFileDialog.getOpenFileName(self, 'Выбрать файл' '')[0]
        if file:
            if self.file == 'NONE':
                self.edit_add_file_btn.setText('Изменить...')
                self.delete_file_btn.setDisabled(False)
            self.file = file

    def delete_file(self):
        """Удаление файла с события"""
        self.file = 'NONE'
        self.edit_add_file_btn.setText('Добавить...')
        self.delete_file_btn.setDisabled(True)


class DetailsEditDialog(QDialog, Ui_DetailsEditDialog):
    def __init__(self, settings, edit_event_window):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(icon_name))
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowTitle(edit_event_window.title)
        self.settings = settings
        self.edit_event_window = edit_event_window
        self.details_text_edit.setText(edit_event_window.details)
        self.enter_details_edit_btn.clicked.connect(self.enter_edit_details)

        font_setting = self.settings.value('font_details', None)
        size_font_setting = self.settings.value('font_details_size', None)

        if font_setting:
            font = font_setting
            font.setPixelSize(int(size_font_setting))
            self.details_text_edit.setFont(font)

    def enter_edit_details(self):
        new_details = self.details_text_edit.toPlainText()
        self.edit_event_window.details = new_details
        self.close()


class HelpDialog(QDialog, Ui_HelpDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(icon_name))
        self.setWindowTitle('О Прилолжении')
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.close_btn.clicked.connect(self.close)


if __name__ == '__main__':
    icon_name = 'icon.ico'
    app = QApplication(sys.argv)
    Diary = DiaryMainWindow()
    Diary.show()
    sys.exit(app.exec())
