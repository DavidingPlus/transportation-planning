"""
Astars
========

Astars 是一个用于进行路径计算的算法库，在该算法中，我们可以进行Astars作为算法的起始，我们选用
曼哈顿距离作为启发函数
"""
import collections
import heapq


class Astars:
    def __init__(self, nodes):
        self.graph = collections.defaultdict(list)
        self.nodes = nodes

    def add_edge(self, start, end, distance, resistiance):
        self.graph[start].append((end, distance, resistiance))

    def calculate_shortest_path(self, G, source, target, weight='distance'):
        visited = set()
        previous_nodes = {node: None for node in G.graph}
        min_distance = {node: float('inf') for node in G.graph}
        min_distance[source] = 0
        priority_queue = [(0, source)]

        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)

            if current_node in visited:
                continue

            visited.add(current_node)

            for neighbor, neighbor_distance, neighbor_resistance in G.graph[current_node]:
                if weight == 'distance':
                    weight_value = neighbor_distance
                elif weight == 'weight':
                    weight_value = neighbor_distance * neighbor_resistance
                else:
                    raise ValueError("Invalid weight parameter")

                distance = min_distance[current_node] + weight_value

                if distance < min_distance[neighbor]:
                    min_distance[neighbor] = distance
                    previous_nodes[neighbor] = current_node
                    heapq.heappush(priority_queue, (distance, neighbor))

        # 构建最短路径
        path = []
        current = target
        while current is not None:
            path.insert(0, current)
            current = previous_nodes[current]

        return path

    def astarshortLength(self, start, end, weight='distance'):
        """
        通过A*算法查找最短路，存入特定数组

        """
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {node: float('inf') for node in self.graph}
        g_score[start] = 0

        while open_set:
            current_score, current_node = heapq.heappop(open_set)

            if current_node == end:
                path_length = g_score[end]
                return path_length  # 返回最短路径长度

            for neighbor, neighbor_distance, neighbor_resistance in self.graph[current_node]:
                if weight == 'distance':
                    weight_value = neighbor_distance
                elif weight == 'weight':
                    weight_value = neighbor_distance * neighbor_resistance
                else:
                    raise ValueError("Invalid weight parameter")

                tentative_g_score = g_score[current_node] + weight_value

                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current_node
                    g_score[neighbor] = tentative_g_score
                    f_score = tentative_g_score + self.heuristic(neighbor, end)
                    heapq.heappush(open_set, (f_score, neighbor))

        return None  # 如果找不到路径，返回 None

    def astar(self, start, end, weight='distance'):
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {node: float('inf') for node in self.graph}
        g_score[start] = 0

        while open_set:
            _, current_node = heapq.heappop(open_set)

            if current_node == end:
                path = self.reconstruct_path(came_from, end)
                return path

            for neighbor, neighbor_distance, neighbor_resistance in self.graph[current_node]:
                if weight == 'distance':
                    weight_value = neighbor_distance
                elif weight == 'weight':
                    weight_value = neighbor_distance * neighbor_resistance
                else:
                    raise ValueError("Invalid weight parameter")

                tentative_g_score = g_score[current_node] + weight_value

                # 添加以下条件以确保不引入无穷大值
                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current_node
                    g_score[neighbor] = tentative_g_score
                    f_score = tentative_g_score + self.heuristic(neighbor, end)
                    heapq.heappush(open_set, (f_score, neighbor))

        return None

    def heuristic(self, node, end):
        # 曼哈顿距离作为启发式函数
        x1, y1 = self.get_coordinates(node)
        x2, y2 = self.get_coordinates(end)
        return abs(x1 - x2) + abs(y1 - y2)

    def get_coordinates(self, node):
        # 解析节点坐标
        node_info = self.nodes.get(node, {})
        location = node_info.get("location", "")
        if location:
            x, y = map(float, location.strip("()").split(","))
            return x, y
        return 0, 0

    def reconstruct_path(self, came_from, current_node):
        # 遍历返回数组，将结果返回
        path = []
        while current_node is not None:
            path.insert(0, current_node)
            current_node = came_from.get(current_node)
        # print(path)
        return path
