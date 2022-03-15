# coding=utf-8
from PyQt5.Qt import *
import sys
from settings import *
import os
import json
import importlib


class UseQt(QWidget):
    def __init__(self):
        self.app = QApplication(sys.argv)
        super(UseQt, self).__init__()
        self.setWindowFlag(Qt.Window)
        self.staticParameter()
        self.setWindowTitle('qt工具')
        self.resize(1280, 720)
        self.setContentsMargins(0, 0, 0, 0)
        self.allLayout()
        self.createErrorDiag()
        self.createSuccessDiag()
        self.show()
        sys.exit(self.app.exec())

    def staticParameter(self):
        self.function_file_path = f'{os.getcwd()}/functionFolder'.replace('\\', '/')
        self.last_input_data_path = f'{os.getcwd()}/lastInputData'.replace('\\', '/')


    def allLayout(self):
        all_Vlayout = QVBoxLayout(self)
        all_Vlayout.setSpacing(0)

        all_Vlayout.setContentsMargins(0, 0, 0, 0)
        self.nav_tool = self.createNav(self)
        self.body_div = self.createBodyDiv(self)

        all_Vlayout.addWidget(self.nav_tool)
        all_Vlayout.addWidget(self.body_div)
        self.setLayout(all_Vlayout)

    def createNav(self, parent):
        nav_tool = QWidget(parent)
        nav_tool.setMinimumHeight(50)
        return nav_tool

    def createBodyDiv(self, parent):
        body_div = QSplitter(parent)
        body_div.setChildrenCollapsible(False)
        body_div.setOrientation(Qt.Vertical)
        import_leftRightDiv = self.leftRightDiv(body_div)
        body_div.addWidget(import_leftRightDiv)
        return body_div

    def leftRightDiv(self, parent):
        import_leftRightDiv = QSplitter(parent)
        import_leftRightDiv.setChildrenCollapsible(False)
        import_leftRightDiv.setOrientation(Qt.Horizontal)
        left_scroll_div = self.leftScrollDiv(import_leftRightDiv)
        right_div = self.rightDiv(import_leftRightDiv)

        import_leftRightDiv.addWidget(left_scroll_div)
        import_leftRightDiv.addWidget(right_div)
        import_leftRightDiv.setStretchFactor(1, 1)
        return import_leftRightDiv

    def leftScrollDiv(self, parent):
        left_scroll_div = QScrollArea(parent)
        self.leftScrollDivSonDiv(left_scroll_div)
        return left_scroll_div

    def itemsClicked(self, parent):
        def itemDoubleClickedFunction(item):
            if item.text(1) == 'file':
                if item.text(2):
                    with open(f'tips/{item.text(2)}.json', mode='rt', encoding='utf-8') as f1:
                        last_input_data_list = []
                        if os.path.exists(f'{self.last_input_data_path}/{item.text(2)}.txt'):
                            with open(f'{self.last_input_data_path}/{item.text(2)}.txt', mode='rt',
                                      encoding='utf-8') as f2:
                                while True:
                                    data = f2.readline().replace('\n', '')
                                    if not data:
                                        break

                                    last_input_data_list.append(data if data != 'None' else '')
                        function_data_json = json.loads(f1.read())
                        function_tips = function_data_json.get("FUNCTION_TIPS_AND_MODEL")
                        self.changeRightTopDivLabelText(function_tips.get('tip'), function_tips.get('model'))
                        # 设置函数
                        self.changeFlayoutInput(function_data_json.get("PARAMETERS_AND_MODEL"), last_input_data_list)
                        self.addFlayoursubmit(item.text(2), item.text(3), item.text(4))
                        self.right_bottom_div.setFixedWidth(self.right_bottom_div.sizeHint().width())
                        self.right_bottom_div.setFixedHeight(self.right_bottom_div.sizeHint().height())
                        self.right_div.setSizes([100000, self.right_bottom_div.sizeHint().height()])
                else:
                    self.changeRightTopDivLabelText('这个文件没有定义')
                    self.clearFlayoutInput()

        parent.itemDoubleClicked.connect(itemDoubleClickedFunction)

    def leftScrollDivSonDiv(self, parent):
        div_hlayout = QHBoxLayout(parent)
        tree = QTreeWidget(parent)
        self.itemsClicked(tree)
        tree.setContentsMargins(0, 0, 0, 0)
        tree.header().hide()
        self.addTreeItems(tree)
        div_hlayout.addWidget(tree)
        parent.setLayout(div_hlayout)

    def addTreeItems(self, parent):
        self.readFilePath(self.function_file_path, parent)

    def readFilePath(self, function_file_path, parent, parent_model='treeWidget', import_path=''):
        for file_name in os.listdir(function_file_path):
            file_path = f'{function_file_path}/{file_name}'
            if os.path.isdir(file_path):
                new_import_path = f'{import_path}/{file_name}'.lstrip('/')
                new_parent = self.addItemModel(parent, parent_model, file_name, 'dir')
                self.readFilePath(file_path, new_parent, 'treeItem', new_import_path)
            else:
                import_file_path = f'{import_path}/{file_name}'.lstrip('/').rsplit('.', 1)[0]
                self.addItemModel(parent, parent_model, file_name, 'file', import_file_path)

    def addItemModel(self, parent, parent_model, filename, file_model, import_path=''):
        item = QTreeWidgetItem()
        if file_model == 'dir':
            item.setIcon(0, self.app.style().standardIcon(QStyle.StandardPixmap(21)))
            # 设置文件类型
            item.setText(1, 'dir')
            # 设置文件绑定文件id
            item.setText(0, filename)
        elif file_model == 'file':
            item.setIcon(0, self.app.style().standardIcon(QStyle.StandardPixmap(25)))
            item.setText(1, 'file')
            # 绑定文件id
            if import_path in SCRIPT_PATH:
                # 绑定文件的运行函数id
                item.setText(2, str(SCRIPT_PATH[import_path]))
                # 绑定文件的导入地址
                item.setText(3, import_path)
                if RUN_FUNCTION.get(SCRIPT_PATH[import_path]):
                    # 设置运行函数的名字
                    item.setText(4, RUN_FUNCTION[SCRIPT_PATH[import_path]])
                else:
                    raise ValueError(f'from setting.py import RUN_FUNCTION no find{SCRIPT_PATH[import_path]} main')
                script_name = SCRIPT_NAME.get(SCRIPT_PATH[import_path])
                if script_name:
                    item.setText(0, script_name)
                else:
                    item.setText(0, filename)
            else:
                item.setText(0, filename)
        if parent_model == 'treeWidget':
            parent.addTopLevelItem(item)
        elif parent_model == 'treeItem':
            parent.addChild(item)
        return item

    def rightDiv(self, parent):
        self.right_div = QSplitter(parent)
        self.right_div.setChildrenCollapsible(False)
        self.right_div.setOrientation(Qt.Vertical)
        right_top_div = self.rightTopDiv(self.right_div)
        right_bottom_div = self.rightBottomDiv(self.right_div)

        self.right_div.addWidget(right_top_div)
        self.right_div.addWidget(right_bottom_div)
        self.right_div.setStretchFactor(0, 1)
        self.right_div.setStretchFactor(1, 0)
        return self.right_div

    def rightTopDiv(self, parent):
        right_top_div = QScrollArea(parent)
        right_top_div_Hlayout = QHBoxLayout(parent)
        self.text = QTextEdit(right_top_div)
        self.text.setReadOnly(True)
        self.text.setWordWrapMode(QTextOption.WordWrap)
        self.changeRightTopDivLabelText()
        right_top_div_Hlayout.addWidget(self.text, 1)
        right_top_div.setLayout(right_top_div_Hlayout)
        return right_top_div

    def changeRightTopDivLabelText(self, text='请选择函数', model='txt'):
        if model == 'txt':
            self.text.setText(text)
        elif model == 'HTML4':
            self.text.setHtml(text)
        else:
            raise TypeError(f'not have {model} Type, please select [txt, HTML4]')

    def rightBottomDiv(self, parent):
        self.right_bottom_scrolldiv = QScrollArea(parent)
        self.right_bottom_div = QWidget(self.right_bottom_scrolldiv)
        self.right_bottom_div_Flayout = QFormLayout()
        self.right_bottom_div_Flayout.setHorizontalSpacing(20)

        self.right_bottom_div.setLayout(self.right_bottom_div_Flayout)
        self.right_bottom_scrolldiv.setWidget(self.right_bottom_div)
        return self.right_bottom_scrolldiv

    def changeRightBottomDiv(self):
        self.right_bottom_div.hide()
        for row_number in range(self.right_bottom_div_Flayout.rowCount()):
            self.right_bottom_div_Flayout.removeRow(0)
        self.right_bottom_div.show()

    def clearFlayoutInput(self):
        self.right_bottom_div.hide()
        for row_num in range(self.right_bottom_div_Flayout.rowCount()):
            self.right_bottom_div_Flayout.removeRow(0)
        self.right_bottom_div.show()

    def changeFlayoutInput(self, parameters, last_input_data_list):
        self.right_bottom_div.hide()
        for row_num in range(self.right_bottom_div_Flayout.rowCount()):
            self.right_bottom_div_Flayout.removeRow(0)
        last_input_data_length = len(last_input_data_list)
        number = 0
        for label in parameters:
            self.addInputModel(self.right_bottom_div, self.right_bottom_div_Flayout, label, parameters[label],
                               last_input_data_list[number] if number < last_input_data_length else '')
            number += 1
        self.right_bottom_div.show()

    def addInputModel(self, parent, layout, label, model, last_input_data):
        addlabel = QLabel(f'{label}：', parent)
        if model[0] in ['file', 'dir']:
            addfild_widget = self.addFileDialogInput(parent, model, last_input_data)
            addfild_widget.setProperty('type', 'file')
        elif model[0] == 'radio':
            "类型,[第一个选项，第二个选项]"
            addfild_widget = self.addRadioInput(parent, model, last_input_data)
            addfild_widget.setProperty('type', 'radio')
        elif model[0] == 'txt':
            addfild_widget = self.addTxtInput(parent, model, last_input_data)
            addfild_widget.setProperty('type', 'txt')
        elif model[0] == 'json':
            addfild_widget = self.addTextDialogInput(parent, model, last_input_data)
            addfild_widget.setProperty('type', 'json')
        else:
            raise TypeError(f'no find {model[0]} input model, please select [file, dir, radio]')
        if addfild_widget.sizeHint().height() > addlabel.sizeHint().height():

            addfild_widget.setFixedHeight(addfild_widget.sizeHint().height())
            addlabel.setFixedHeight(addfild_widget.sizeHint().height())
        else:
            addfild_widget.setFixedHeight(addlabel.sizeHint().height())
            addlabel.setFixedHeight(addlabel.sizeHint().height())

        layout.addRow(addlabel, addfild_widget)


    def setTxtModel(self, addfild_widget, txt_type=None, length=None):
        if txt_type:
            if txt_type == 'int':
                addfild_widget_validator = QIntValidator(addfild_widget)
                addfild_widget.setValidator(addfild_widget_validator)
            elif txt_type == 'float':
                addfild_widget_validator = QDoubleValidator(addfild_widget)
                addfild_widget.setValidator(addfild_widget_validator)
        if length:
            addfild_widget.setFixedWidth(length)

    def addTxtInput(self, parent, model, last_input_data):

        addfild_widget = QLineEdit(parent)
        addfild_widget_lenght = QLabel(parent)
        addfild_widget_lenght.hide()
        addfild_widget_min_length = 200
        if len(model) > 1:
            self.setTxtModel(addfild_widget, *model[1:])
            addfild_widget.setProperty('data_type', model[1])
        else:
            addfild_widget.setProperty('data_type', 'str')

        def changeAddfild_widthLenght():
            addfild_widget_lenght.setText(addfild_widget.text())
            length = addfild_widget_lenght.sizeHint().width()
            if length > 200:
                addfild_widget.setFixedWidth(length)
            parent.setFixedWidth(parent.sizeHint().width())

        if last_input_data:
            addfild_widget.setText(last_input_data)
            addfild_widget_lenght.setText(last_input_data)
            length = addfild_widget_lenght.sizeHint().width()
            if length > 200:
                addfild_widget_min_length = length
        addfild_widget.textChanged.connect(changeAddfild_widthLenght)

        addfild_widget.setFixedWidth(addfild_widget_min_length)
        parent.setFixedWidth(parent.sizeHint().width())
        return addfild_widget

    def addRadioInput(self, parent, model, last_input_data):
        addfild_widget = QWidget(parent)
        addfild_layout = QHBoxLayout(addfild_widget)
        addfild_radioGroup = QButtonGroup(addfild_widget)

        for radio_txt in model[1:]:
            add_radio = QRadioButton(str(radio_txt), addfild_widget)
            if str(radio_txt) == last_input_data:
                add_radio.setChecked(True)
                addfild_widget.setProperty("data", last_input_data)
            addfild_layout.addWidget(add_radio)
            addfild_radioGroup.addButton(add_radio)

        addfild_widget.setLayout(addfild_layout)
        addfild_widget.setFixedWidth(addfild_widget.sizeHint().width())

        def btnSelected():
            btn = addfild_radioGroup.checkedButton()
            if btn:
                addfild_widget.setProperty("data", btn.text())

        addfild_radioGroup.buttonClicked.connect(btnSelected)

        return addfild_widget

    def addFileDialogInput(self, parent, model, last_input_data):

        addfild_widget = QWidget(parent)
        addfield_layout = QHBoxLayout(addfild_widget)
        field_label = QLabel(addfild_widget)

        if model[0] == 'file':
            field_button = QPushButton('选择文件', addfild_widget)
        else:
            field_button = QPushButton('选择文件夹', addfild_widget)
        if last_input_data:
            field_label.setText(last_input_data)
        addfield_layout.addWidget(field_label, 0)
        addfield_layout.addWidget(field_button, 0)
        field_button.setFixedWidth(field_button.sizeHint().width())
        addfild_widget.setLayout(addfield_layout)

        def addDia():
            if model[0] == 'file':
                result = QFileDialog.getOpenFileName(parent, *[i for i in model[1:]])
                if result[0]:
                    field_label.setText(result[0])
            else:
                result = QFileDialog.getExistingDirectory(parent, *[i for i in model[1:]])
                if result:
                    field_label.setText(result)
            addfild_widget.setFixedWidth(addfild_widget.sizeHint().width())
            parent.setFixedWidth(parent.sizeHint().width())

        field_button.clicked.connect(addDia)

        addfild_widget.setFixedWidth(addfild_widget.sizeHint().width())

        return addfild_widget

    def addTextDialogInput(self, parent, model, last_input_data):
        addfild_widget = QPushButton('添加一个数据', parent)
        json_dialog = QInputDialog(addfild_widget)
        json_dialog.setInputMode(QInputDialog.TextInput)
        json_dialog.setOptions(QInputDialog.UsePlainTextEditForTextInput)
        json_dialog.setWindowTitle('输入JSON数据')
        json_dialog.setLabelText('文本提示内容')
        if last_input_data:
            json_dialog.setTextValue(last_input_data)
        addfild_widget.setFixedWidth(150)
        addfild_widget.clicked.connect(lambda: json_dialog.open())
        return addfild_widget

    def addFlayoursubmit(self, id, file_path, runfunction_name):
        file_path = f'functionFolder.{file_path}'
        submit_btn = QPushButton('运行', self.right_bottom_div)
        submit_btn.setProperty('type', 'submit')

        def submit():
            parameter_list = []
            for row_number in range(1, self.right_bottom_div_Flayout.rowCount() * 2 - 1, 2):
                self.submitDataAdd(parameter_list, self.right_bottom_div_Flayout.itemAt(row_number).widget())
            self.runFunction(id, file_path, runfunction_name, parameter_list)

        submit_btn.clicked.connect(submit)
        submit_btn.setFixedWidth(50)
        self.right_bottom_div_Flayout.addRow(submit_btn)

    def submitDataAdd(self, parameter_list: list, widgets: QWidget):
        if widgets.property('type') == 'file':
            parameter_list.append(
                widgets.layout().itemAt(0).widget().text() if widgets.layout().itemAt(0).widget().text() else None)
        elif widgets.property('type') == 'radio':
            parameter_list.append(widgets.property('data'))
        elif widgets.property('type') == 'txt':
            if widgets.property('data_type') == 'int':
                data = int(widgets.text())
            elif widgets.property('data_type') == 'float':
                data = float(widgets.text())
            else:
                data = widgets.text()
            parameter_list.append(data if data else None)
        elif widgets.property('type') == 'json':
            data = f'{{"data":{widgets.children()[0].textValue() if widgets.children()[0].textValue() else "null"}}}'
            data = json.loads(data)
            parameter_list.append(data['data'])

    def runFunction(self, id, filePath, runFuntionClass, inputParameter):
        try:
            if runFuntionClass.find('.') != -1:
                className, functionName = runFuntionClass.rsplit('.')
                module = importlib.import_module(filePath)
                cls = getattr(module, className)
                obj = cls()
                getattr(obj, functionName)(*inputParameter)
            else:
                module = importlib.import_module(filePath)
                getattr(module, runFuntionClass)(*inputParameter)

            self.showSuccessMessage()
            with open(f'{self.last_input_data_path}/{id}.txt', mode='wt', encoding='utf-8') as f3:
                for one_data in inputParameter:
                    f3.write(f'{one_data}\n')
        except Exception as e:
            self.showErrorMessage(e)

    def createSuccessDiag(self):
        self.successMessage = QMessageBox(self)
        self.successMessage.setWindowTitle('运行成功')
        self.successMessage.setText('运行完成')

    def showSuccessMessage(self):
        self.successMessage.show()

    def createErrorDiag(self):
        self.errorMessage = QMessageBox(self)
        self.errorMessage.setWindowTitle('报错')
        self.errorMessage.setIcon(QMessageBox.Critical)

    def showErrorMessage(self, error_text):
        self.errorMessage.setText(str(error_text))
        self.errorMessage.show()
