# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\edit_event_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_EditEventDialog(object):
    def setupUi(self, EditEventDialog):
        EditEventDialog.setObjectName("EditEventDialog")
        EditEventDialog.resize(367, 255)
        self.gridLayout = QtWidgets.QGridLayout(EditEventDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.date_edit = QtWidgets.QDateEdit(EditEventDialog)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.date_edit.setFont(font)
        self.date_edit.setObjectName("date_edit")
        self.gridLayout.addWidget(self.date_edit, 1, 1, 1, 3)
        self.title_line_edit = QtWidgets.QLineEdit(EditEventDialog)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.title_line_edit.setFont(font)
        self.title_line_edit.setObjectName("title_line_edit")
        self.gridLayout.addWidget(self.title_line_edit, 0, 1, 1, 3)
        self.time_edit = QtWidgets.QTimeEdit(EditEventDialog)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.time_edit.setFont(font)
        self.time_edit.setObjectName("time_edit")
        self.gridLayout.addWidget(self.time_edit, 2, 1, 1, 3)
        self.important_label = QtWidgets.QLabel(EditEventDialog)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.important_label.setFont(font)
        self.important_label.setObjectName("important_label")
        self.gridLayout.addWidget(self.important_label, 5, 0, 1, 1)
        self.date_label = QtWidgets.QLabel(EditEventDialog)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.date_label.setFont(font)
        self.date_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.date_label.setObjectName("date_label")
        self.gridLayout.addWidget(self.date_label, 1, 0, 1, 1)
        self.importatn_check_box = QtWidgets.QCheckBox(EditEventDialog)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.importatn_check_box.setFont(font)
        self.importatn_check_box.setText("")
        self.importatn_check_box.setObjectName("importatn_check_box")
        self.gridLayout.addWidget(self.importatn_check_box, 5, 1, 1, 1)
        self.close_btn = QtWidgets.QPushButton(EditEventDialog)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.close_btn.setFont(font)
        self.close_btn.setObjectName("close_btn")
        self.buttonGroup = QtWidgets.QButtonGroup(EditEventDialog)
        self.buttonGroup.setObjectName("buttonGroup")
        self.buttonGroup.addButton(self.close_btn)
        self.gridLayout.addWidget(self.close_btn, 8, 0, 1, 4)
        self.edit_add_file_btn = QtWidgets.QPushButton(EditEventDialog)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.edit_add_file_btn.setFont(font)
        self.edit_add_file_btn.setObjectName("edit_add_file_btn")
        self.gridLayout.addWidget(self.edit_add_file_btn, 4, 1, 1, 2)
        self.time_label = QtWidgets.QLabel(EditEventDialog)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.time_label.setFont(font)
        self.time_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.time_label.setObjectName("time_label")
        self.gridLayout.addWidget(self.time_label, 2, 0, 1, 1)
        self.edit_details_btn = QtWidgets.QPushButton(EditEventDialog)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.edit_details_btn.setFont(font)
        self.edit_details_btn.setObjectName("edit_details_btn")
        self.gridLayout.addWidget(self.edit_details_btn, 3, 1, 1, 3)
        self.datails_label = QtWidgets.QLabel(EditEventDialog)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.datails_label.setFont(font)
        self.datails_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.datails_label.setObjectName("datails_label")
        self.gridLayout.addWidget(self.datails_label, 3, 0, 1, 1)
        self.delete_file_btn = QtWidgets.QPushButton(EditEventDialog)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.delete_file_btn.setFont(font)
        self.delete_file_btn.setObjectName("delete_file_btn")
        self.gridLayout.addWidget(self.delete_file_btn, 4, 3, 1, 1)
        self.title_label = QtWidgets.QLabel(EditEventDialog)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.title_label.setFont(font)
        self.title_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.title_label.setObjectName("title_label")
        self.gridLayout.addWidget(self.title_label, 0, 0, 1, 1)
        self.label = QtWidgets.QLabel(EditEventDialog)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 4, 0, 1, 1)
        self.enter_edit_btn = QtWidgets.QPushButton(EditEventDialog)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.enter_edit_btn.setFont(font)
        self.enter_edit_btn.setObjectName("enter_edit_btn")
        self.buttonGroup.addButton(self.enter_edit_btn)
        self.gridLayout.addWidget(self.enter_edit_btn, 9, 0, 1, 4)
        self.color_select_btn = QtWidgets.QToolButton(EditEventDialog)
        self.color_select_btn.setObjectName("color_select_btn")
        self.gridLayout.addWidget(self.color_select_btn, 5, 3, 1, 1)
        self.label_2 = QtWidgets.QLabel(EditEventDialog)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 5, 2, 1, 1)

        self.retranslateUi(EditEventDialog)
        QtCore.QMetaObject.connectSlotsByName(EditEventDialog)

    def retranslateUi(self, EditEventDialog):
        _translate = QtCore.QCoreApplication.translate
        EditEventDialog.setWindowTitle(_translate("EditEventDialog", "Form"))
        self.important_label.setText(_translate("EditEventDialog", "Важное:"))
        self.date_label.setText(_translate("EditEventDialog", "Дата:"))
        self.close_btn.setText(_translate("EditEventDialog", "Отмена"))
        self.edit_add_file_btn.setText(_translate("EditEventDialog", "Изменить..."))
        self.time_label.setText(_translate("EditEventDialog", "Время:"))
        self.edit_details_btn.setText(_translate("EditEventDialog", "Изменить..."))
        self.datails_label.setText(_translate("EditEventDialog", "Описание:"))
        self.delete_file_btn.setText(_translate("EditEventDialog", "Удалить"))
        self.title_label.setText(_translate("EditEventDialog", "Название:"))
        self.label.setText(_translate("EditEventDialog", "Файл:"))
        self.enter_edit_btn.setText(_translate("EditEventDialog", "ОК"))
        self.color_select_btn.setText(_translate("EditEventDialog", "..."))
        self.label_2.setText(_translate("EditEventDialog", "Цвет:"))
