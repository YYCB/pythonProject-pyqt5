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
fileCheckedList = list()


# 将配置文件中内容以字典形式返回
def conf_dict_update(file_path):
    conf_dict_temp = dict()
    n_temp = ''
    with open(file_path, 'r') as f:
        # 将配置文件中数据存入字典
        for n in f.readlines():
            n = n.strip()
            # 查找Topic
            if n.startswith('[') and n.isupper():
                n_temp = n.strip('[').strip(']')
                conf_dict_temp.setdefault(n_temp, [])
            # 查找变量
            elif n.find('=') != -1 and n.count('title') == 0:
                v_temp = n.split('=', 1)[0]
                if not v_temp.isspace():
                    conf_dict_temp.setdefault(n_temp).append(v_temp.split())
    f.close()
    return conf_dict_temp


# TODO:检查重复变量
def check_duplicate_variable():
         print("TODO：检查重复变量")


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

    # 搜寻被选中的文件并将目录寻入列表中
    def file_checked_list_update(self):
        fileCheckedList.clear()
        item = QtWidgets.QTreeWidgetItemIterator(self.treeWidget)
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
                fileCheckedList.append(file_dir)
            item.__iadd__(1)

        if len(fileCheckedList) == 0:
            self.textBrowser.append("<font color=\"#FF0000\">" +
                                    'ERROR::左侧树形图中未选择工作文件</font>'
                                    )
            self.textBrowser_2.append("<font color=\"#FF0000\">" +
                                    'ERROR::左侧树形图中未选择工作文件</font>'
                                    )

    # 单独文件添加内容，显示所有被选中的文件并选择
    def radioButton_single(self):
        # 更新被选中的文件列表
        self.file_checked_list_update()
        for f in fileCheckedList:
            self.fontComboBox.addItem(f)
        # 提示未选取目标文件
        if len(fileCheckedList) == 0:
            self.textBrowser.append("<font color=\"#FF0000\">" +
                                    'ERROE::请在左侧目录树中选择所需的control.toml文件' + '</font>')

    # 向配置文件中添加内容
    def addIntoConf(self):
        topic = '[' + self.textEdit_3_Topic.toPlainText().upper().strip() + ']'
        variable = self.textEdit_Variable.toPlainText().lower().strip()
        temp = self.textEdit_2.toPlainText().strip()
        # 更新工作区文件目录
        self.file_checked_list_update()
        # 检查所需输入是否安全
        if not len(topic) or not len(variable) or not len(temp):
            self.textBrowser.append("<font color=\"#FF0000\">" +
                                    'ERROR::请将待添加的 参数列表填写完整</font>'
                                    )
            return
        elif self.radioButton_3.isChecked() and self.fontComboBox.currentText() == 'control.toml':
            self.textBrowser.append("<font color=\"#FF0000\">" +
                                    'ERROE::Single模式请选择下方所需单独修改的control.toml文件' +
                                    '</font>'
                                    )
            return

        self.textBrowser.append("<font color=\"#FF0000\">" +
                                '[' +
                                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +
                                ']::</font>' +
                                'topic:' + str(topic) + '\t'
                                                        'variable:' + str(variable) + '\t'
                                                                                      'temp:' + str(temp)
                                )
        # 单个文件新加参数
        if self.radioButton_3.isChecked():
            self.textBrowser.append("<font color=\"#FF0000\">" +
                                    '[' +
                                    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +
                                    ']::</font>'+'写入到文件:' + self.fontComboBox.currentText())
            self.add_conf_file(self.fontComboBox.currentText())
        else:
            #  全部工作区内文件写入数据
            for file_dir in fileCheckedList:
                self.textBrowser.append("<font color=\"#FF0000\">" +
                                        '[' +
                                        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +
                                        ']::</font>'+
                                        '写入到文件:' + file_dir)
                self.add_conf_file(file_dir)

        self.textBrowser.moveCursor(self.textBrowser.textCursor().End)

    # TODO:文件写入
    def add_conf_file(self, file_path):
        with open(file_path, 'r+') as f:
            self.textBrowser.append("FFFFFF")
        f.close()

    # check按钮触发对比检查
    def checkOnClicked(self):
        # 更新被选中的文件列表
        self.file_checked_list_update()
        # 校验配置文件
        for filepath in fileCheckedList:
            self.check_conf_file(filepath)
        # 文本框显示到底部
        self.textBrowser_2.moveCursor(self.textBrowser.textCursor().End)

    # 校验配置文件函数
    def check_conf_file(self, file_path):
        error_cnt = 0
        # 获取配置文件中的数据
        conf_dict_temp = conf_dict_update(file_path)

        # 检查配置文件中缺少的变量
        for topic in goalDict.keys():
            conf_key_status = conf_dict_temp.get(topic, -1)
            if conf_key_status == -1:
                error_cnt = error_cnt + 1
                self.textBrowser_2.append("<font color=\"#FF0000\">" +
                                          "ERROR:\t 此文件缺少Topic::" +
                                          topic +
                                          '</font>')
                self.textBrowser_2.append("<font color=\"#FF0000\">" +
                                          'ERROR:\t ' + topic + '中包括：：' +
                                          str(goalDict[topic]) +
                                          '</font>')
            else:
                for u in goalDict[topic]:
                    if u not in conf_dict_temp[topic]:
                        self.textBrowser_2.append("<font color=\"#FF0000\">" +
                                                  "ERROR:\tTopic  " + topic +
                                                  "缺少参数：" +
                                                  str(u))
                        error_cnt = error_cnt + 1

        if error_cnt == 0:
            self.textBrowser_2.append("<font color=\"#0000FF\">" +
                                      '[' +
                                      time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +
                                      ']::</font>' +
                                      '校验通过！')
        # TODO::添加检查配置文件同一个topic下重复的变量
        # self.check_duplicate_variable()

    # 弹出窗口选择文件夹目录
    def msg(self):
        # 默认打开/home/root/ccu/ccu_config目录
        # 避免关闭后异常退出
        goalDict.clear()
        goalList.clear()
        # 弹出窗口选择文件夹目录
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
        self.treeWidget.topLevelItem(0).setExpanded(1)

    # 循环读取该目录下所有文件
    # 找到control_agent.cpp文件 提取所有需要的配置参数
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