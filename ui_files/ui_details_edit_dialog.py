# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\details_edit_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DetailsEditDialog(object):
    def setupUi(self, DetailsEditDialog):
        DetailsEditDialog.setObjectName("DetailsEditDialog")
        DetailsEditDialog.resize(540, 461)
        self.gridLayout = QtWidgets.QGridLayout(DetailsEditDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.details_text_edit = QtWidgets.QTextEdit(DetailsEditDialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.details_text_edit.setFont(font)
        self.details_text_edit.setObjectName("details_text_edit")
        self.gridLayout.addWidget(self.details_text_edit, 0, 0, 1, 1)
        self.enter_details_edit_btn = QtWidgets.QPushButton(DetailsEditDialog)
        self.enter_details_edit_btn.setObjectName("enter_details_edit_btn")
        self.gridLayout.addWidget(self.enter_details_edit_btn, 1, 0, 1, 1)

        self.retranslateUi(DetailsEditDialog)
        QtCore.QMetaObject.connectSlotsByName(DetailsEditDialog)

    def retranslateUi(self, DetailsEditDialog):
        _translate = QtCore.QCoreApplication.translate
        DetailsEditDialog.setWindowTitle(_translate("DetailsEditDialog", "Form"))
        self.enter_details_edit_btn.setText(_translate("DetailsEditDialog", "Изменить"))
