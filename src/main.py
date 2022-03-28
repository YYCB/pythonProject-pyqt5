import sys
import os
import time
from os.path import expanduser
from PyQt5.QtWidgets import *
from untitled import *
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

folder = expanduser("~/ccu")
ccu_conf_dir = folder + '/ccu_config'
control_agent = folder + '/control/controller_agent.cpp'
goalString = "toml::find(ctrl_config,"
goalList = []
goalDict = dict()


class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
        # 触发文件夹目录选择
        self.pushButton.clicked.connect(self.msg)
        # check按钮 触发对比检查
        self.pushButton_2.clicked.connect(self.checkOnClicked)
        # add按钮 触发添加功能
        self.pushButton_add.clicked.connect(self.addIntoConf)
        self.radioButton_3.clicked.connect(self.radioButton_single)
        self.fontComboBox.clear()
        self.fontComboBox.addItem('control.toml')
        self.fontComboBox.hide()

    def radioButton_single(self):
        item = QtWidgets.QTreeWidgetItemIterator(self.treeWidget)
        cnt = 0
        while item.value():
            file_dir = ccu_conf_dir
            if item.value().checkState(0) == Qt.Checked:
                check_file_parent = item.value().parent()
                # 读取选中的配置文件路径
                file_dir_back = ';/' + item.value().text(0)
                while check_file_parent != self.treeWidget.topLevelItem(0):
                    file_dir_back += ';/' + check_file_parent.text(0)
                    check_file_parent = check_file_parent.parent()
                file_dir_list = list(reversed(file_dir_back.split(';')))
                for f in file_dir_list:
                    file_dir += f
                self.fontComboBox.addItem(file_dir)
            item.__iadd__(1)
            cnt = cnt + 1

        # 提示未选取目标文件
        if cnt == 0:
            self.textBrowser.append("<font color=\"#FF0000\">" +
                                    'ERROE::请在左侧目录树中选择所需的control.toml文件' + '</font>')

    def addIntoConf(self):
        topic = '[' + self.textEdit_3_Topic.toPlainText().upper().strip() + ']'
        variable = self.textEdit_Variable.toPlainText().lower().strip()
        temp = self.textEdit_2.toPlainText().strip()

        if len(topic) and len(variable) and len(temp):
            if self.radioButton_3.isChecked():
                self.textBrowser.append(self.fontComboBox.currentText())
            else:
                self.textBrowser.append("<font color=\"#FF0000\">" +
                                        '[' +
                                        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +
                                        ']::</font>' +
                                        'topic:' + str(topic) + '\t'
                                                                'variable:' + str(variable) + '\t'
                                                                                              'temp:' + str(temp)
                                        )

                item = QtWidgets.QTreeWidgetItemIterator(self.treeWidget)
                cnt = 0
                # 遍历全部结点，找出选中的文件
                while item.value():
                    file_dir = ccu_conf_dir
                    if item.value().checkState(0) == Qt.Checked:
                        check_file_parent = item.value().parent()
                        # 读取选中的配置文件路径
                        file_dir_back = ';/' + item.value().text(0)
                        while check_file_parent != self.treeWidget.topLevelItem(0):
                            file_dir_back += ';/' + check_file_parent.text(0)
                            check_file_parent = check_file_parent.parent()
                        file_dir_list = list(reversed(file_dir_back.split(';')))
                        for f in file_dir_list:
                            file_dir += f
                        self.textBrowser.append("<font color=\"#0000FF\">" +
                                                '[' +
                                                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +
                                                ']::</font>' +
                                                file_dir)
                        self.add_conf_file(file_dir)
                        cnt = cnt + 1

                    item.__iadd__(1)
        else:
            self.textBrowser.append("<font color=\"#FF0000\">" +
                                    'ERROR::请将待添加的 参数列表填写完整</font>'
                                    )
        self.textBrowser.moveCursor(self.textBrowser.textCursor().End)

    # TODO:文件写入
    def add_conf_file(self, file_path):
        with open(file_path, 'r+') as f:
            print('')
            # self.textBrowser.append("<font color=\"#0000FF\">" +
            #                         '[' +
            #                         time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +
            #                         ']::</font>' +
            #                         "开始添加参数")
        f.close()

    # check按钮触发对比检查
    def checkOnClicked(self):
        item = QtWidgets.QTreeWidgetItemIterator(self.treeWidget)
        cnt = 0
        # 遍历全部结点，找出选中的文件
        while item.value():
            file_dir = ccu_conf_dir
            if item.value().checkState(0) == Qt.Checked:
                check_file_parent = item.value().parent()
                # 读取选中的配置文件路径
                file_dir_back = ';/' + item.value().text(0)
                while check_file_parent != self.treeWidget.topLevelItem(0):
                    file_dir_back += ';/' + check_file_parent.text(0)
                    check_file_parent = check_file_parent.parent()
                file_dir_list = list(reversed(file_dir_back.split(';')))
                for f in file_dir_list:
                    file_dir += f
                self.textBrowser_2.append("<font color=\"#0000FF\">" +
                                          '[' +
                                          time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +
                                          ']::</font>' +
                                          file_dir)
                # 读取选中的文件内容
                self.textBrowser_2.append("<font color=\"#0000FF\">" +
                                          '[' +
                                          time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +
                                          ']::</font>' +
                                          "开始校验")
                self.check_conf_file(file_dir)
                cnt = cnt + 1

            item.__iadd__(1)
        # 提示未选取目标文件
        if cnt == 0:
            self.textBrowser_2.append("<font color=\"#FF0000\">" +
                                      '[' +
                                      time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +
                                      ']::</font>' +
                                      '请选择需要处理的control.toml文件')

        # 文本框显示到底部
        self.textBrowser_2.moveCursor(self.textBrowser.textCursor().End)

    # 校验配置文件函数
    def check_conf_file(self, file_path):
        error_cnt = 0
        conf_dict = dict()
        n_temp = ''
        with open(file_path, 'r') as f:
            conf_f_list = f.readlines()

            # 将配置文件数据存入字典
            for n in conf_f_list:
                # self.textBrowser.append(str(n))
                n = n.strip()
                if n.startswith('[') and n.isupper():
                    n_temp = n.strip('[').strip(']')
                    conf_dict.setdefault(n_temp, [])
                elif n.find('=') != -1 and n.count('title') == 0:
                    v_temp = n.split('=', 1)[0]
                    if not v_temp.isspace():
                        conf_dict.setdefault(n_temp).append(v_temp.split())
            # 检查配置文件中缺少的量
            for n in goalDict.keys():
                conf_key_status = conf_dict.get(n, -1)
                if conf_key_status == -1:
                    self.textBrowser_2.append("<font color=\"#FF0000\">" +
                                              "ERROR:\t 此文件缺少Topic::" +
                                              n +
                                              '</font>')
                    self.textBrowser_2.append("<font color=\"#FF0000\">" +
                                              'ERROR:\t ' + n + '中包括：：' +
                                              str(goalDict[n]) +
                                              '</font>')
                    error_cnt += 1
                else:
                    for u in goalDict[n]:
                        if u not in conf_dict[n]:
                            self.textBrowser_2.append("<font color=\"#FF0000\">" +
                                                      "ERROR:\tTopic  " + n +
                                                      "缺少参数：" +
                                                      str(u))
                            error_cnt += 1

            if error_cnt:
                self.textBrowser_2.append("<font color=\"#FF0000\">" +
                                          "ERROR:\t error_cnt " + str(error_cnt) +
                                          '</font>')
            else:
                self.textBrowser_2.append("<font color=\"#0000FF\">" +
                                          '[' +
                                          time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +
                                          ']::</font>' +
                                          '校验通过！')

            f.close()

    # 弹出窗口选择文件夹目录
    def msg(self):
        # 默认打开/home/root/ccu/ccu_config目录
        # 避免关闭后异常退出
        goalDict.clear()
        goalList.clear()
        if os.path.isdir(ccu_conf_dir):
            self.pushButton.setText(ccu_conf_dir)
            self.make_tree(ccu_conf_dir)
        # 读取目录中的control_agent.cpp文件
        # TODO:develop分支中已优化为宏定义形式需要适配
        if os.path.isfile(control_agent):
            with open(control_agent, 'r') as f:
                f_list = f.readlines()
                for n in f_list:
                    if n.count(goalString) and not n.count("//"):
                        n = n.strip().rstrip("\");")
                        n = n.lstrip(goalString).lstrip().lstrip("\"")
                        goalList.append(n)
                        n_list = n.split("\",")
                        n_list[1] = n_list[1].lstrip().lstrip("\"")
                        # 将需要查找的变量及对应topic 存入到相应字典里
                        goalDict.setdefault(n_list[0], []).append(n_list[1].split())
                f.close()
                # 调试功能：输出本地control需要读取的配置文件名称
                # for i in goalDict.keys():
                #     self.textBrowser.append(str(goalDict[i]))
                # self.textBrowser.append(str(goalDict))
                self.textBrowser_2.append("<font color=\"#0000FF\">" +
                                          '[' +
                                          time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +
                                          ']::</font>' +
                                          'controller_agent.cpp中总计参数为' + str(len(goalList)))
        else:
            self.textBrowser_2.append("<font color=\"#FF0000\">" +
                                      '[' +
                                      time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +
                                      ']::</font>' +
                                      'ERROR：未寻找到controller_agent.cpp文件')

    # 创建顶级目录
    def make_tree(self, f):
        root = self.populate(f)
        self.treeWidget.insertTopLevelItem(0, root)

    # 循环读取该目录下所有文件
    # 并找到control_agent.cpp文件 提取所有需要的配置参数
    def populate(self, path):
        tree_item = QTreeWidgetItem()
        tree_item.setText(0, os.path.basename(path))
        for file in os.listdir(path):
            if os.path.isdir(os.path.join(path, file)) and \
                    file != '.git' and \
                    file != 'ccu_autostart_script':
                tree_item.addChild(self.populate(os.path.join(path, file)))
            else:

                if file == 'control.toml':
                    sub_item = QTreeWidgetItem()
                    sub_item.setText(0, file)

                    if self.checkBox.isChecked():
                        sub_item.setCheckState(0, Qt.Checked)
                    else:
                        sub_item.setCheckState(0, Qt.Unchecked)
                    tree_item.addChild(sub_item)

        return tree_item


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())
