"""
`Graphs` 是基于plt和netWorkX的简单的计算规划展示交通流的类

Graphs主要使用了Astar算法进行计算，并通过该算法得到所需的结果进一步获取。

"""

import src.Curvaa as Curve
from src.Astar import Astars

from matplotlib.cm import ScalarMappable
from matplotlib.colors import LinearSegmentedColormap, LogNorm
import matplotlib.pyplot as plt
import networkx as nx
import math
from matplotlib.backend_bases import PickEvent
import matplotlib.pyplot as plt


class Graph:
    """Extensible Graph traffic net slove class.
    """

    def __init__(self, gdict=None):
        if gdict is None:
            gdict = {"nodes": {}, "links": {}}
        self.gdict = gdict
        self.curves = {}
        self.ODMartix = {}
        self.node_positions = {}  # 用于存储节点位置的字典
        self.cmap = plt.cm.get_cmap('RdYlGn_r')
        self.cmap.set_under('darkgreen')
        self.cmap.set_over('darkred')
        nodes = gdict.get("nodes", {})
        self.cmap = plt.cm.get_cmap('RdYlGn_r')
        self.cmap.set_under('darkgreen')  # 设置下限颜色为深绿色
        self.cmap.set_over('darkred')  # 设置上限颜色为深红色
        for node_id, node_info in nodes.items():
            location = node_info.get("location")[1:-1]
            if location is not None:
                self.node_positions[node_id] = tuple(
                    map(float, location.split(",")))
        links = gdict.get("links", {})
        for link_name, link_info in links.items():
            start_id = link_info.get("start", 0)
            end_id = link_info.get("end", 0)
            distance = self.calculateDistance(start_id, end_id)
            link_info["distance"] = distance

    def getNodes(self):
        return self.gdict["nodes"]

    def getLinks(self):
        return self.gdict["links"]

    def addNode(self, node_id, location, isMain, in_degree, out_degree):
        if node_id not in self.gdict["nodes"]:
            node_info = {
                "id": node_id,
                "location": location,
                "isMain": isMain,
                "in_degree": in_degree,
                "out_degree": out_degree,

            }
            self.gdict["nodes"][node_id] = node_info

            self.node_positions[node_id] = tuple(
                map(float, location[1:-1].split(",")))

    def calculateCurve(self, node1_id, node2_id, curve):
        if curve is None:
            return self.calculateDistance(node1_id, node2_id)
        else:
            node1_info = self.gdict["nodes"].get(node1_id)
            node2_info = self.gdict["nodes"].get(node2_id)
            if node1_info and node2_info:
                location1 = node1_info.get("location")[1:-1]
                location2 = node2_info.get("location")[1:-1]
                # 通过location计算出来距离
                if location1 and location2:
                    curvenew = Curve.Curve(
                        left=curve.left, right=curve.right, func=curve.func)
                    x1, y1 = map(float, location1.split(","))
                    x2, y2 = map(float, location2.split(","))
                    length = curvenew.get_curve()
                    return length
        return None

    def calculateDistance(self, node1_id, node2_id):
        node1_info = self.gdict["nodes"].get(node1_id)
        node2_info = self.gdict["nodes"].get(node2_id)
        if node1_info and node2_info:
            location1 = node1_info.get("location")[1:-1]
            location2 = node2_info.get("location")[1:-1]
            # 通过location计算出来距离
            if location1 and location2:
                x1, y1 = map(float, location1.split(","))
                x2, y2 = map(float, location2.split(","))
                distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                return distance
        return None

    def __copy__(self):
        # 创建一个新的对象副本
        new_instance = Graph(self.gdict)
        return new_instance

    def addLink(self, link_name, start_id, end_id, limit, curve):
        if link_name not in self.gdict["links"]:
            distance = self.calculateCurve(start_id, end_id, curve)
            if distance is not None:
                link_info = {
                    "start": start_id,
                    "end": end_id,
                    "limit": limit,
                    "distance": distance,
                    "curve": curve,
                    "resistiance": 1
                }
                self.gdict["links"][link_name] = link_info

    def drawCombinedGraph(self, graph_type):
        plt.figure(dpi=400)
        plt.axis('equal')
        G = nx.DiGraph()

        for node, node_info in self.gdict["nodes"].items():
            G.add_node(node, **node_info)  # 将节点属性添加到图中

        pos = self.node_positions

        # 创建一个字典来存储每对节点组合的偏移值
        edge_offsets = {}

        for link, link_info in self.gdict["links"].items():
            start = link_info.get("start", 0)
            end = link_info.get("end", 0)
            resistiance = link_info.get("resistiance", 0)
            limit = link_info.get("limit", "string")
            distance = link_info.get("distance", 0)
            curve = link_info.get("curve", None)

            # 计算偏移值
            offset = 0  # 默认为0
            if G.has_edge(end, start):
                # 如果存在相反方向的边，为其分配0.1或-0.1的偏移值
                offset = 0.1

            # 存储偏移值
            edge_offsets[(start, end)] = offset
            edge_offsets[(end, start)] = -offset
            if curve is None:
                G.add_edge(start, end, limit=limit,
                           distance=distance, resistiance=resistiance)

        labels = {node: node for node in G.nodes()}
        edge_labels = {(u, v): f"{d['distance']:.2f}" for u,
                       v, d in G.edges(data=True)}  # 显示距离

        # 创建一个包含所有边的列表
        edges = G.edges()
        vmin = 0
        vmax = 0
        if graph_type == 'EasyGraph':
            nx.draw(
                G, pos, with_labels=True, node_size=10, node_color='skyblue',
                font_size=6, edgelist=[],  # 这里将 edgelist 置空，因为我们自行绘制边
                linewidths=2  # 根据需要设置线宽
            )
        elif graph_type == 'DownGraph':
            edge_weights = {(u, v): d['resistiance']
                            for u, v, d in G.edges(data=True)}  # 显示权重
            weights = [edge_weights.get(edge, 0) for edge in G.edges()]
            weights = [((w - 1) / 0.15) ** 0.25 * 100 for w in weights]
            norm = plt.Normalize(0, 100)  # 设置映射范围

            # 绘制边的颜色映射
            edge_colors = weights

            nx.draw(
                G, pos, with_labels=True, node_size=10, node_color='skyblue',
                font_size=6, edgelist=[],  # 这里将 edgelist 置空，因为我们自行绘制边
                edge_cmap=self.cmap, edge_vmin=0, edge_vmax=100, edge_color=edge_colors,
                linewidths=2  # 根据需要设置颜色和颜色映射
            )

            sm = plt.cm.ScalarMappable(cmap=self.cmap, norm=norm)
            sm.set_array([])

            visited = [(-2, -3)]
            alpha = []

            for i, edge in enumerate(G.edges()):
                u, v = edge
                # 控制绘制顺序和透明度
                if G.has_edge(v, u):
                    if visited.count((v, u)) == 0:
                        ans = 0.5
                    else:
                        ans = -0.5
                else:
                    ans = -0
                alpha.append(ans)
                visited.append((u, v))
            vmax = 100
            cbar = plt.colorbar(sm, orientation='vertical',
                                label='Percentange of Congestion')

            for i, edge in enumerate(G.edges()):
                x = (pos[edge[0]][0] + pos[edge[1]][0]) / 2 + alpha[i]
                y = (pos[edge[0]][1] + pos[edge[1]][1]) / 2 + alpha[i] / 2
                plt.text(
                    x, y, round(weights[i], 2), fontsize=6, color='black',
                    ha='center', va='center'
                )

        elif graph_type == 'Graph':
            edge_labels = {
                (u, v): f"{d['distance']:.2f}" for u, v, d in G.edges(data=True)}  # 显示距离
            edge_weights = {(u, v): d['resistiance']
                            for u, v, d in G.edges(data=True)}  # 显示权重
            weights = [edge_weights.get(edge, 0) for edge in G.edges()]
            weights = [((w - 1) / 0.15) ** 0.25 for w in weights]
            visited = [(-2, -3)]
            alpha = []

            for i, edge in enumerate(G.edges()):
                u, v = edge
                # 控制绘制顺序和透明度
                ans = 0
                if G.has_edge(v, u):
                    # 根据边的方向设置透明度
                    ans = -0.5 if visited.count((v, u)) == 0 else 0.5
                alpha.append(ans)
                visited.append((u, v))

            norm = LogNorm(min(weights), max(weights))  # 设置映射范围

            # 绘制边的颜色映射
            edge_colors = [math.log(x) for x in weights]

            nx.draw(
                G, pos, with_labels=True, node_size=10, node_color='skyblue',
                font_size=6, edgelist=[],  # 这里将 edgelist 置空，因为我们自行绘制边
                edge_cmap=self.cmap, edge_vmin=0, edge_vmax=math.log(max(weights)),
                edge_color=edge_colors, linewidths=2  # 根据需要设置颜色和颜色映射
            )

            vmax = max(weights)
            vmin = min(weights)

            sm = plt.cm.ScalarMappable(cmap=self.cmap, norm=norm)
            sm.set_array([])

            cbar = plt.colorbar(sm, orientation='vertical',
                                label='log(log(O Resistance))')

            for i, edge in enumerate(G.edges()):
                x = (pos[edge[0]][0] + pos[edge[1]][0]) / 2 + alpha[i]
                y = (pos[edge[0]][1] + pos[edge[1]][1]) / 2 + alpha[i] / 2
                plt.text(
                    x, y, {(u, v): round(d['resistiance'], 2) for u, v, d in G.edges(
                        data=True)}.get((edge[0], edge[1])),
                    fontsize=6, color='black', ha='center', va='center'
                )

        # 绘制边
        for edge in edges:
            start, end = edge
            offset = edge_offsets.get(edge, 0)  # 获取边的偏移值
            offset = -offset  # 反向偏移
            x_values = [pos[start][0], pos[end][0] + offset]
            y_values = [pos[start][1], pos[end][1] + offset]
            edge_color = 'red'
            if graph_type != 'EasyGraph':
                edge_weight = edge_weights.get(edge, 0)
            if graph_type == 'DownGraph':
                edge_color = self.cmap(norm(edge_weight))
            elif graph_type == 'Graph':
                edge_color = self.cmap(norm(math.log(edge_weight)))
            print(edge_color)
            plt.plot(x_values, y_values, color=edge_color,
                     linestyle='-', linewidth=1, zorder=0)
            arrow_params = dict(
                arrowstyle='-|>', mutation_scale=10, color=edge_color)
            plt.annotate('', xy=(x_values[1], y_values[1]), xytext=(
                x_values[0], y_values[0]), arrowprops=arrow_params, zorder=0)
        for node, nodes in G.nodes(data=True):
            plt.text(
                pos[node][0], pos[node][1] +
                0.1, f"In-Degree: {nodes.get('in_degree')}\nOut-Degree: {nodes.get('out_degree')}",
                ha='center', color='purple', fontsize=4, bbox=dict(facecolor='red', alpha=0.0)
            )
        for link, link_info in self.gdict["links"].items():
            curve = link_info.get("curve", None)
            if curve is not None:
                print(link_info.get("resistiance", 0), graph_type)
                a = ((link_info.get("resistiance", 0) - 1) / 0.15) ** 0.25 if graph_type == 'Graph' else (
                    (link_info.get("resistiance", 0) - 1) / 0.15) ** 0.25*100
                curve.draw_function(
                    self.cmap, a, type=graph_type, vmax=vmax, vmin=vmin)

        ax = plt.gca()
        fig = ax.get_figure()  # 获取与当前坐标轴关联的图
        fig.canvas.mpl_connect(
            'pick_event', lambda event: self.on_pick(event, labels))

        # 设置坐标轴标签
        ax.set_xlabel("X轴")
        ax.set_ylabel("Y轴")
        plt.axis('on')
        plt.grid()
        plt.pause(0.5)
        plt.show()

    def on_pick(event, labels):
        if isinstance(event, PickEvent) and isinstance(event.artist, plt.Line2D):
            edge = event.artist.get_data()  # 获取选中的边的数据
            weight = labels.get(edge, None)  # 获取边的长度
            if weight is not None:
                print(f'Edge {edge} has length {weight}')

    def brp(self, link, depoment=4, alaph=0.15):
        bools = False
        if "pre-resistiance" not in link:
            link["pre-resistiance"] = 0
        if abs(link["pre-resistiance"]-link["resistiance"]) > 0.01:
            bools = True
        if link["resistiance"] > 2:
            bools = False

        link["pre-resistiance"] = link["resistiance"]
        link["resistiance"] = 1 + alaph * \
            (link["link_strength"] / 1200) ** depoment
        # print(link,link["resistiance"])
        return bools

    def findShortestPathRecurser(self, i=200, axispos=0.8):
        shortest_paths = {}
        shortest_lengths = {}
        bools = False
        for epoch in range(i):
            if bools == False and epoch != 0:
                break
            bools = False
            if epoch == 0:
                shortest_paths, shortest_lengths = self.findShortestPath(0)
            else:
                shortest_paths, shortest_lengths = self.findShortestPath(1)
            # print(shortest_lengths.items())
            # shortest_lengthsbeg=shortest_lengths
            for _, n in shortest_paths.items():
                # print(n)
                for num in range(len(n)-1):
                    for linkname, link in self.gdict.get("links", {}).items():
                        start_node_id = link.get("start")
                        end_node_id = link.get("end")

                        if start_node_id == n[num] and end_node_id == n[num+1]:
                            nums = (n[0], n[len(n)-1])
                            # print("ans=",self.ODMartix.get(nums))
                            im = self.ODMartix.get(nums)
                            # print(im)
                            if epoch == 0:
                                link["resistiance"] = 0
                                link["pre-resistiance"] = -1
                                if "link_strength" in link:
                                    link["link_strength"] += im
                                else:
                                    link["link_strength"] = im
                                link["link_pre"] = 0
                                bools = True
                            else:
                                link["link_strength"] = link["link_strength"] + \
                                    im*(1-axispos)/axispos

            for linkname, link in self.gdict.get("links", {}).items():
                if "link_strength" not in link:
                    link["link_strength"] = 0
                link["link_strength"] *= axispos
                if self.brp(link):
                    print(link)
                    bools = True
            # print(shortest_lengths,shortest_paths)
        return shortest_paths, shortest_lengths

    def findShortestPath(self, doing=0):
        # 创建一个图实例
        G = Astars(self.getNodes())

        # 添加边
        for link, link_info in self.gdict["links"].items():
            start = link_info.get("start", 0)
            end = link_info.get("end", 0)
            distance = link_info.get("distance", 0)
            resistiance = link_info.get("resistiance", 0)
            G.add_edge(start, end, distance, resistiance)

        # 找到最短路径
        shortest_paths = {}
        shortest_lengths = {}

        main_nodes = [
            node for node, node_info in self.gdict["nodes"].items() if node_info["isMain"]]
        # 在最短路中遍历寻找，将每个路都进行最短路的查找。
        for source in main_nodes:
            for target in main_nodes:
                if source != target:
                    if doing == 0:
                        shortest_length = G.astarshortLength(
                            source, target, weight='distance')
                    else:
                        shortest_length = G.astarshortLength(
                            source, target, weight='weight')
                    shortest_lengths[(source, target)] = shortest_length

                    # 计算最短路径
                    path = G.astar(
                        source, target, weight='distance' if doing == 0 else 'weight')
                    shortest_paths[(source, target)] = path

        return shortest_paths, shortest_lengths

    def getOD(self):
        self.traffic_flow = {}
        _, shortest_lengths = self.findShortestPath()
        # 获取最短路，存入。
        for m, n in shortest_lengths.items():
            i = m[0]
            j = m[1]
            if i != j:
                # 排除自己到自己的情况
                # 提取节点 i 和节点 j 的 "in" 和 "out" 属性值
                Pi = self.gdict.get("nodes", {}).get(i)["in_degree"]
                Pj = self.gdict.get("nodes", {}).get(j)["out_degree"]
                distance = n
                # 使用重力模型公式计算交通流量
                traffic = (1.0 * (Pi * Pj)) / (distance ** 2.0)
                # print(traffic)
                # 将交通流量添加到链路信息中
                self.ODMartix[m] = traffic
