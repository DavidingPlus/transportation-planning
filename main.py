# Python Qt 图形化的主程序
import sys
from ui import draw
from PyQt5.QtWidgets import QApplication, QMainWindow

if __name__ == "__main__":
    # 实例化，传参
    app = QApplication(sys.argv)

    # 创建对象
    mainWindow = QMainWindow()

    # 创建ui，引用draw文件中的Ui_Form类
    ui = draw.Ui_Form()

    # 调用Ui_MainWindow类的setupUi，创建初始组件
    ui.setupUi(mainWindow)

    # 创建窗口
    mainWindow.show()

    # 进入程序的主循环，并通过exit函数确保主循环安全结束(该释放资源的一定要释放)
    sys.exit(app.exec_())
