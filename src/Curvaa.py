"""
Curvaa
========

Curvaa 是一个用于进行路径计算、绘制的库，在该算法中，我们可以进行
计算绘制，画出参数方程形式的路径。
"""

import math
from matplotlib import patches
from matplotlib.colors import LogNorm
import numpy as np
import matplotlib.pyplot as plt


class Curve:
    def __init__(self, left, right, func) -> None:
        self.func = func
        self.left = left
        self.right = right

    def get_curve(self):
        x, y = self.func()
        length = self.curve_length(x, y)
        # print("Curve Length:", length)
        return length

    def draw_function(self, cmaps, resistiance, type="Graph", vmax=100, vmin=0):
        x, y = self.func()
        print(resistiance)
        norm = LogNorm(
            vmin=vmin, vmax=vmax) if type == "Graph" else plt.Normalize(0, 100)
        print("resi",resistiance)
        plt.plot(x, y, label='Curve', linewidth=1.0, color=cmaps(
            norm(math.log(resistiance))) if type == "Graph" else cmaps(norm(resistiance)))
        # 计算箭头方向，可以根据需要调整箭头的位置和大小
        arrow = patches.FancyArrowPatch(
            (x[-2], y[-2]),  # 箭头的起始点
            (x[-1], y[-1]),  # 箭头的终止点
            mutation_scale=10,  # 控制箭头的大小
            color=cmaps(norm(math.log(resistiance))) if type == "Graph" else cmaps(
                norm(resistiance)),  # 填充颜色
            linewidth=1,  # 边框宽度
            zorder=2  # 控制绘制顺序，较大的值在上层
        )
        # 添加箭头到当前图中
        plt.gca().add_patch(arrow)
        # 计算曲线中间点的索引
        middle_index = len(x) // 2
        # 获取曲线中间点的坐标
        x_middle = x[middle_index]
        y_middle = y[middle_index]
        # 计算曲线在中间点的切线斜率
        slope = np.gradient(y, x)[middle_index]
        # 计算标注文本的角度（以度为单位）
        angle_degrees = np.degrees(np.arctan(slope))
        # 计算曲线长度
        curve_length = self.curve_length(x, y)
        if resistiance != 0:
            curve_length = resistiance
        a = curve_length
        # 创建标签文本
        label_text = f'{curve_length:.2f}'
        # 添加标注，并设置角度和位置
        plt.annotate(label_text, (x_middle, y_middle),
                     ha='center', fontsize=6,
                     bbox=dict(boxstyle='round,pad=0.5',
                               facecolor='white', alpha=0.0), rotation=angle_degrees*0.618)

    def curve_length(self, x, y):
        # 分段获取曲线的长度，微分
        segment_lengths = np.sqrt(np.diff(x)**2 + np.diff(y)**2)
        total_length = np.sum(segment_lengths)
        return total_length
