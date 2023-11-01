from src.Graphs import Graph
from src.JsonParser import JsonParser
import src.Curvaa as Curve

import matplotlib.pyplot as plt
import json
import requests
import numpy as np


def func_templet(right, left, funcx, funcy):
    # 定义一个函数模板，接受右边界，左边界，x函数，y函数作为参数
    def func():
        # 创建一个等差数列，从右边界到左边界，数量为1000
        t = np.linspace(right, left, int(1000*(left-right)))
        # 计算x函数的值
        x = funcx(t)
        # 计算y函数的值
        y = funcy(t)
        # 返回x和y的值
        return x, y
    # 返回函数模板
    return func


def circle_parametric():
    # 定义一个圆的参数函数，接受t作为参数
    t = np.linspace(0, 0.25, 1000)
    # 计算x的值
    x = 2 - np.cos(2 * np.pi * t)
    # 计算y的值
    y = 1 + np.sin(2 * np.pi * t)
    # 返回x和y的值
    return x, y


def create_function(expression):
    # 定义一个函数，接受表达式作为参数
    # 定义一个匿名函数，接受x作为参数，并将表达式求值
    def func(t): return eval(expression)
    # 返回函数
    return func


def request_get(path):
    # 通过get请求请求服务器上的数据
    response = requests.get("http://139.155.152.242:8080/getMap")
    # 存入文件
    with open(path, 'w') as file:
        file.write(response.text)


def work(path, num):
    # 发送get请求请求数据
    # request_get(path)

    # 打开交互式绘图模式
    plt.ion()

    # circle_parametrics = func_templet(0, 0.25, create_function(
    #     "2 - np.cos(2 * np.pi * t)"), create_function("1 + np.sin(2 * np.pi * t)"))
    # cee2 = Curve.Curve(1, 2, circle_parametrics)

    # 读取文件
    with open(path, 'r') as file:
        superHeroSquad = json.load(file)

    # 解析文件
    gdict = JsonParser.getName(superHeroSquad)
    # 创建图
    my_graph = Graph(gdict)
    # 获取有向图
    my_graph.getOD()

    # 创建图的副本
    graph_new = my_graph.__copy__()
    # 获取有向图
    graph_new.getOD()

    # 查找最短路径
    shortest_paths, shortest_lengths = my_graph.findShortestPath()
    print("Shortest Paths Answers:")
    for a, b in zip(shortest_paths.items(), shortest_lengths.items()):
        print(
            f"From Node {a[0][0]} to Node {a[0][1]}: {a[1]} min Length {b[1]}")

    shortest_paths, shortest_lengths = graph_new.findShortestPathRecurser(
        axispos=0.6)
    print("Shortest Time Answers:")
    for a, b in zip(shortest_paths.items(), shortest_lengths.items()):
        print(
            f"From Node {a[0][0]} to Node {a[0][1]}: {a[1]} min Time {b[1]}")

    # 画图操作，做按钮三选一这个东西
    if 0 == num:
        graph_new.drawCombinedGraph("DownGraph")
    elif 1 == num:
        graph_new.drawCombinedGraph("EasyGraph")
    elif 2 == num:
        graph_new.drawCombinedGraph("Graph")

    # 关闭交互式绘图
    plt.ioff()
    # 展示图形
    plt.show()
