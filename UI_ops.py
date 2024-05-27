# -*- coding: utf-8 -*-
"""
@Time ： 2023/12/10
@Auth ： Schwaze Katze
@File ：UI_ops.py
@IDE ：Pycharm(CE)
@Motto：ABC(Always Be Coding)
"""

from PyQt5.QtWidgets import *


class Dialog(QDialog):
    def __init__(self, parent=None):
        super(Dialog, self).__init__(parent)
        self.init_ui(parent)

    def init_ui(self, parent):
        self.setWindowTitle('新增课程信息')
        """水平布局"""
        hbox = QHBoxLayout()

        self.save_btn = QPushButton()
        self.save_btn.setText('保存')
        self.save_btn.clicked.connect(lambda: self.save_btn_click(parent))

        self.cancel_btn = QPushButton()
        self.cancel_btn.setText('取消')
        self.cancel_btn.clicked.connect(self.cancel_btn_click)

        hbox.addWidget(self.save_btn)
        hbox.addWidget(self.cancel_btn)

        '''表单布局'''
        fbox = QFormLayout()

        self.teacher_lab = QLabel()
        self.teacher_lab.setText('教师名：')
        self.teacher_text = QLineEdit()
        self.teacher_text.setPlaceholderText('请输入教师名')

        self.course_lab = QLabel()
        self.course_lab.setText('课程名：')
        self.course_text = QLineEdit()
        self.course_text.setPlaceholderText('请输入课程名')

        self.time_lab = QLabel()
        self.time_lab.setText('时间：')
        self.time_text = QLineEdit()
        self.time_text.setPlaceholderText('请输入课程时间')

        fbox.addRow(self.teacher_lab, self.teacher_text)
        fbox.addRow(self.course_lab, self.course_text)
        fbox.addRow(self.time_lab, self.time_text)


        vbox = QVBoxLayout()
        vbox.addLayout(fbox)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

    def save_btn_click(self, parent):
        if self.teacher_text.text().strip() != '' and self.course_text.text().strip() != '':
            print(parent.data_list)
            data = tuple([
                self.teacher_text.text(),
                self.course_text.text(),
                self.time_text.text()
                ])
            parent.data_list.append(data)
            print(parent.data_list)
            parent.query_data()
            self.close()

    def cancel_btn_click(self):
        self.close()

    def show_error(self, error=None):
        if error:
            if 'version' and 'Driver' in str(error):
                QMessageBox.critical(self, "错误", "Error: \n" + str(error)[:300] + "..." +
                                     "\n请尝试在管理器中更换浏览器内核!\n如果还未成功请根据提示下载匹配版本的浏览器内核!")
            else:
                QMessageBox.critical(self, "错误", "Error: \n" + str(error))
        else:
            QMessageBox.critical(self, "错误", "未知错误")

    def show_success(self):
        QMessageBox.information(self, "挂载结束", "后台挂载结束，请确认你是否已经选上目标课程。")

    def show_warning(self, warning: str):
        QMessageBox.warning(self, "警告", warning, QMessageBox.Cancel)

    @staticmethod
    def get_add_dialog(parent=None):
        dialog = Dialog(parent)
        return dialog.exec()
