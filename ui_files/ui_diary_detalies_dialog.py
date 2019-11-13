# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\diary_detalies_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DetailsEventDialog(object):
    def setupUi(self, DetailsEventDialog):
        DetailsEventDialog.setObjectName("DetailsEventDialog")
        DetailsEventDialog.resize(698, 701)
        self.gridLayout = QtWidgets.QGridLayout(DetailsEventDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.open_file_btn = QtWidgets.QPushButton(DetailsEventDialog)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.open_file_btn.setFont(font)
        self.open_file_btn.setObjectName("open_file_btn")
        self.gridLayout.addWidget(self.open_file_btn, 3, 1, 1, 1)
        self.name_file_label = QtWidgets.QLabel(DetailsEventDialog)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.name_file_label.setFont(font)
        self.name_file_label.setText("")
        self.name_file_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.name_file_label.setObjectName("name_file_label")
        self.gridLayout.addWidget(self.name_file_label, 3, 0, 1, 1)
        self.name_event_label = QtWidgets.QLabel(DetailsEventDialog)
        font = QtGui.QFont()
        font.setPointSize(17)
        self.name_event_label.setFont(font)
        self.name_event_label.setAlignment(QtCore.Qt.AlignCenter)
        self.name_event_label.setObjectName("name_event_label")
        self.gridLayout.addWidget(self.name_event_label, 0, 0, 1, 2)
        self.details_event_text = QtWidgets.QTextBrowser(DetailsEventDialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.details_event_text.setFont(font)
        self.details_event_text.setObjectName("details_event_text")
        self.gridLayout.addWidget(self.details_event_text, 2, 0, 1, 2)
        self.event_edit = QtWidgets.QPushButton(DetailsEventDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.event_edit.sizePolicy().hasHeightForWidth())
        self.event_edit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.event_edit.setFont(font)
        self.event_edit.setObjectName("event_edit")
        self.gridLayout.addWidget(self.event_edit, 4, 1, 1, 1)
        self.time_event_label = QtWidgets.QLabel(DetailsEventDialog)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.time_event_label.setFont(font)
        self.time_event_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.time_event_label.setObjectName("time_event_label")
        self.gridLayout.addWidget(self.time_event_label, 1, 1, 1, 1)
        self.date_event_label = QtWidgets.QLabel(DetailsEventDialog)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.date_event_label.setFont(font)
        self.date_event_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.date_event_label.setObjectName("date_event_label")
        self.gridLayout.addWidget(self.date_event_label, 1, 0, 1, 1)
        self.close_btn = QtWidgets.QPushButton(DetailsEventDialog)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.close_btn.setFont(font)
        self.close_btn.setObjectName("close_btn")
        self.gridLayout.addWidget(self.close_btn, 5, 1, 1, 1)

        self.retranslateUi(DetailsEventDialog)
        QtCore.QMetaObject.connectSlotsByName(DetailsEventDialog)

    def retranslateUi(self, DetailsEventDialog):
        _translate = QtCore.QCoreApplication.translate
        DetailsEventDialog.setWindowTitle(_translate("DetailsEventDialog", "Form"))
        self.open_file_btn.setText(_translate("DetailsEventDialog", "Открыть"))
        self.name_event_label.setText(_translate("DetailsEventDialog", "Name"))
        self.event_edit.setText(_translate("DetailsEventDialog", "Редактировать событие"))
        self.time_event_label.setText(_translate("DetailsEventDialog", "Time"))
        self.date_event_label.setText(_translate("DetailsEventDialog", "Data"))
        self.close_btn.setText(_translate("DetailsEventDialog", "Закрыть"))
