from PyQt5.Qt import *
import sys
import re


# 自定义用户姓名验证器
class UserNameValidator(QValidator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fixup_bool = True
        self.fixup_success = False  # 最终的结果

    def validate(self, input_value: str, input_value_pos: int):
        """
        if 匹配的条件:
            :return Acceptable  # 正确为成功
        else:
            :return Intermediate  # 不正确为疑问
        这样就可以解决用户输入错误的东西不会出现的问题了
        """
        if re.search('[^\u4e00-\u9fa5]', input_value):
            return (QValidator.Intermediate, input_value, input_value_pos)
        return (QValidator.Acceptable, input_value, input_value_pos)

    def fixup(self, input_value):
        return input_value  # 这里可以直接返回接收到的内容


# 自定义用户验证器
class UserValidator(QValidator):
    def validate(self, input_value: str, input_value_pos: int):
        if re.search('[\u4e00-\u9fa5]', input_value) or not re.search('[a-zA-Z]',
                                                                      input_value[0] if input_value else 'a'):
            return (QValidator.Invalid, input_value, input_value_pos)
        return (QValidator.Acceptable, input_value, input_value_pos)  # 返回的两个数据会依次通过修正器然后返回给页面


def rigisterSuccess():
    for one in submit_data_list:
        if not one.hasAcceptableInput() or not one.isModified():
            print(f'注册失败{one.text()},{one.hasAcceptableInput()},{one.isModified()}')
            break
    else:
        print('注册成功')
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle('注册页面')
    # 设置一个标题文本框
    input_text_title = QLineEdit(window)
    input_text_title.setText('这个是注册页面')
    # 设置标题文本框为只读
    input_text_title.setReadOnly(True)
    window.resize(500, 500)
    # 创建用户名和密码文本输入框和用户姓名框
    input_text_user = QLineEdit(window)  # 用户名
    input_text_pwd = QLineEdit(window)  # 密码
    input_text_username = QLineEdit(window)  # 用户真实姓名
    input_text_invitation = QLineEdit(window)  # 邀请码
    # 提交对象列表
    submit_data_list = [input_text_username, input_text_user, input_text_pwd, input_text_invitation]
    # 设置提示
    input_text_username.setPlaceholderText('输入你的真实姓名')
    input_text_user.setPlaceholderText('输入用户名')
    input_text_pwd.setPlaceholderText('输入密码')
    input_text_invitation.setPlaceholderText('请输入邀请码')
    # 设置两个输入框的大小和标题框大脚
    input_text_user.resize(300, 20)
    input_text_pwd.resize(300, 20)
    input_text_username.resize(200, 20)
    input_text_title.resize(100, 20)
    input_text_invitation.resize(300, 20)
    # 将密码设置密文传输
    input_text_pwd.setEchoMode(QLineEdit.Password)
    # 设置一键清除文本功能
    input_text_user.setClearButtonEnabled(True)
    input_text_pwd.setClearButtonEnabled(True)
    input_text_invitation.setClearButtonEnabled(True)


    # 将密码在可见和不可见之前进行切换
    def openEye():
        if input_text_pwd.echoMode() == QLineEdit.Normal:
            input_text_pwd.setEchoMode(QLineEdit.Password)
            input_text_pwd_action.setIcon(QIcon('OpenEyes.png'))
        else:
            input_text_pwd.setEchoMode(QLineEdit.Normal)
            input_text_pwd_action.setIcon(QIcon('CloseEyes.png'))


    input_text_pwd_action = QAction(input_text_pwd)
    input_text_pwd_action.setIcon(QIcon('OpenEyes.png'))
    input_text_pwd_action.triggered.connect(openEye)
    input_text_pwd.addAction(input_text_pwd_action, QLineEdit.TrailingPosition)
    # 设置用户名补全功能
    completer = QCompleter(['mubai', 'wangza', 'huzhognqi'], input_text_user)
    """
    QCompleter(QAbstractItemModel, parent: QObject = None)
    QCompleter(Iterable[str], parent: QObject = None)  # 可迭代字符串对象
    QCompleter(parent: QObject = None)
    """
    input_text_user.setCompleter(completer)
    # 设置用户名框和密码框的位置和标题框位置
    input_text_title.move(200, 50)
    input_text_username.move(150, 100)
    input_text_user.move(100, 150)
    input_text_pwd.move(100, 200)
    input_text_invitation.move(100, 250)
    # 设置用户名和密码输入的最大长度
    input_text_username.setMaxLength(8)
    input_text_user.setMaxLength(16)
    input_text_pwd.setMaxLength(20)
    # 给用户名输入添加验证器，使用户名不能输入为中文，并且首字母必须为字母
    re_user_validator = UserValidator(input_text_user)
    input_text_user.setValidator(re_user_validator)
    re_username_validator = UserNameValidator(input_text_username)
    input_text_username.setValidator(re_username_validator)
    # 给邀请码设置掩码验证 8位验证码，4:4,大写字母+小写字母+数字+大写字母+0或1 + 小写字母+数字+0或1+0或1
    # eg: Mb1M0 b101  >A<A9>AB-<A9BB
    input_text_invitation.setInputMask('>A<A9>AB-<A9BB')
    # 给姓名和标题的字体设置为居中对齐
    input_text_title.setAlignment(Qt.AlignCenter)
    input_text_username.setAlignment(Qt.AlignCenter)
    input_text_invitation.setAlignment(Qt.AlignCenter)
    # 设置注册按钮
    btn_submit = QPushButton('注册', window)
    btn_submit.move(200, 300)
    btn_submit.clicked.connect(rigisterSuccess)
    window.show()
    sys.exit(app.exec())