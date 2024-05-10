# 交通规划原理期末项目

# 项目组人员

- 小组人员：**王森，刘治学，田景颢，刘杰**
- 指导老师：**熊耀华**

# 具体分工

- 王森
  - 完成工具算法库`Astar`，`Curvaa`，`Graphs`的编写
  - 完成图形绘制和数据请求整合文件`Gpp.py`的编写
- 刘治学
  - 完成`PyQt5`的界面编写，包括`draw.py`和`draw.ui`
  - 完成主程序入口`main.py`的编写
  - 完成项目整体架构的设计和代码的汇总，以及文档的编写
- 田景颢
  - 完成`data.json`数据格式的设计和数据的生成
  - 完成`get`请求服务端的配置，能通过浏览器获取到数据的页面以及通过代码发送`get`请求获得数据
- 刘杰
  - 完成颜色工具库`hover`和`Json`数据处理工具库`JsonParser`的编写
  - 完成演示视频的录制和剪辑

# 注意事项

- 项目在`Github`上开源，地址：[https://github.com/DavidingPlus/Transportation-Planning](https://github.com/DavidingPlus/Transportation-Planning)

- 项目依赖`python3`环境，依赖`PyQt5`包，`windows`系统和`Linux`系统均兼容，本测试在`windows`上运行

  - 安装`PyQT5`：在终端使用如下命令

    ```bash
    pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pyqt5 pyqt5-tools
    ```

    

- 项目根目录中的`项目文档`是本`README.md`的`pdf`版本

- 项目根目录中的`演示视频`是该项目的测试视频

# 代码分析

## 整体框架

- 代码的框架如下：

  <img src="https://img-blog.csdnimg.cn/direct/2168b73844f14021b625db6f03b545c5.png" alt="image-20231229204237018" style="zoom:75%;" />

## res目录

- `res`目录：存放交通网络结点和边的数据，是一个`json`文件

  <img src="https://img-blog.csdnimg.cn/direct/e563b0417a4849fbad7d923528b5864a.png" alt="image-20231229204758402" style="zoom:60%;" />

## src目录

- `src`目录：存放代码执行需要的依赖文件，类似于库或者包

  - `Astar.py`

    - `Astars`是一个用于进行路径计算的算法库，在该算法中，我们可以进行`Astars`作为算法的起始，我们选用曼哈顿距离作为启发函数

    <img src="https://img-blog.csdnimg.cn/direct/758fdb90f31b47be9571ccf80c8e389c.png" alt="image-20231229204443744" style="zoom:60%;" />

  - `Curvva.py`

    - `Curvaa`是一个用于进行路径计算、绘制的库，在该算法中，我们可以进行计算绘制，画出参数方程形式的路径

    <img src="https://img-blog.csdnimg.cn/direct/d381b8d5e6df4aba8e3ae6dc3fd3a328.png" alt="image-20231229204817590" style="zoom:67%;" />

  - `Gpp.py`

    - `Gpp.py`是用来进行图形的基础绘制的文件，里面通过拿取`data.json`的数据，将数据转化为图展示出来，在其中还包括了发送`get`请求从远端服务器获得数据的操作

    <img src="https://img-blog.csdnimg.cn/direct/1251c2bc44294ff98709db46cfa36950.png" alt="image-20231229205120224" style="zoom:65%;" />

  - `Graphs.py`

    - `Graphs`是基于`plt`和`netWorkX`的简单的计算规划展示交通流的类
    - `Graphs`主要使用了`Astar`算法进行计算，并通过该算法得到所需的结果进一步获取

    <img src="https://img-blog.csdnimg.cn/direct/0f6fe237336e46f998f33f88ddba49ce.png" alt="image-20231229204853443" style="zoom:67%;" />

  - `hover.py`

    - 是一个颜色的工具库，最后的成品有三种不同的颜色主题进行展示，相关在这里进行定义

    <img src="https://img-blog.csdnimg.cn/direct/3e2bda1bc80444e7835787c442d89ed7.png" alt="image-20231229205228796" style="zoom:65%;" />

  - `JsonPraser.py`

    - `JsonParser`本项目的工具类，存放`json`解析的东西

    <img src="https://img-blog.csdnimg.cn/direct/c543f0c4ca94425ca896d584dfa51d09.png" alt="image-20231229204909300" style="zoom:65%;" />

## ui目录

- `ui`目录：存放成品展示的界面的`python`文件和`ui`文件

  - `draw.py`

    - 运用`pythonQt`库，在画出一个主界面加上三个按钮并且对应不同的事件

    <img src="https://img-blog.csdnimg.cn/direct/94db79bb40c543b4a725cff4b77f4801.png" alt="image-20231229205538583" style="zoom:60%;" />

  - `draw.ui`

    - 界面的`ui`文件

    <img src="https://img-blog.csdnimg.cn/direct/1cfe32d1556448f99a084c4d94558d58.png" alt="image-20231229205604683" style="zoom:65%;" />

## 主程序

- `main.py`：程序的主入口，创建`MainWindow`对象，并且运行之后展示出来，然后进行后续发送`get`请求，并处理数据画图的逻辑

  <img src="https://img-blog.csdnimg.cn/direct/f55c54a807304919b7a1e65d1a237bf2.png" alt="image-20231229205752120" style="zoom:65%;" />

