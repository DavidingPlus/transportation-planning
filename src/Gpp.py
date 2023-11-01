from src.Graphs import Graph
from src.JsonParser import JsonParser
import src.Curvaa as Curve

import matplotlib.pyplot as plt
import json
import requests
import numpy as np


def func_templet(right, left, funcx, funcy):
    def func():
        t = np.linspace(right, left, int(1000*(left-right)))
        x = funcx(t)
        y = funcy(t)
        return x, y
    return func


def circle_parametric():
    t = np.linspace(0, 0.25, 1000)
    x = 2 - np.cos(2 * np.pi * t)
    y = 1 + np.sin(2 * np.pi * t)
    return x, y


def create_function(expression):
    # 定义一个匿名函数，接受x作为参数，并将表达式求值
    def func(t): return eval(expression)
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

    # 读取文件
    with open(path, 'r') as file:
        superHeroSquad = json.load(file)

    # 打开交互式绘图模式
    plt.ion()

    circle_parametrics = func_templet(0, 0.25, create_function(
        "2 - np.cos(2 * np.pi * t)"), create_function("1 + np.sin(2 * np.pi * t)"))
    gdict = JsonParser.getName(superHeroSquad)
    # cee2 = Curve.Curve(1, 2, circle_parametrics)

    my_graph = Graph(gdict)
    my_graph.getOD()

    graph_new = my_graph.__copy__()
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
