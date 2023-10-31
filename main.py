# Python Qt 图形化的主程序
import src.Gpp as Gpp
import ui.draw as draw

from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

# json的数据文件路径
path = "./res/data.json"


# 自己封装的一个MainWindow类，我们工作逻辑的代码就放在Work中
class MainWindow:
    def __init__(self) -> None:
        # 主程序对象成员
        self.mainWindow = QMainWindow()

        # 创建ui，引用draw文件中的Ui_Form类
        self.ui = draw.Ui_Form()

        # 调用Ui_MainWindow类的setupUi，创建初始组件
        self.ui.setupUi(self.mainWindow)

        # 调用工作函数
        self.work()

    # 工作函数都在这里面
    def work(self) -> None:
        self.ui.DownGraphBtn.clicked.connect(self.DownGraph_Slot)
        self.ui.EasyGraphBtn.clicked.connect(self.EasyGraph_Slot)
        self.ui.GraphBtn.clicked.connect(self.Graph_Slot)

    # 我们需要传递一些参数给Gpp的work函数，所以我自己写一个槽函数来实现
    def DownGraph_Slot(self):
        Gpp.work(path, 0)

    def EasyGraph_Slot(self):
        Gpp.work(path, 1)

    def Graph_Slot(self):
        Gpp.work(path, 2)

    # show函数
    def show(self) -> None:
        self.mainWindow.show()


# PyQt主程序的框架
if __name__ == "__main__":
    # 实例化，传参
    app = QApplication(sys.argv)

    # 实例化主窗口
    m = MainWindow()

    # 展示主窗口
    m.show()

    # 进入程序的主循环，并通过exit函数确保主循环安全结束(该释放资源的一定要释放)
    sys.exit(app.exec_())
