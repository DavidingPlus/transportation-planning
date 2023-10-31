"""
`JsonParser 本项目的工具类，存放json解析的东西

"""


class JsonParser:
    def getName(superHeroSquad):
        gdict = {"nodes": {}, "links": {}}

    # 将节点数据复制到gdict的"nodes"键中
        for node_data in superHeroSquad["data"]["nodes"]:
            node_id = node_data["id"]
            location = node_data["location"]
            is_main = node_data["isMain"]
            in_degree = node_data["in"]
            out_degree = node_data["out"]
            gdict["nodes"][node_id] = {
                "id": node_id,
                "location": location,
                "isMain": is_main,
                "in_degree": in_degree,
                "out_degree": out_degree
            }

    # 将链接数据复制到gdict的"links"键中
        for link_data in superHeroSquad["data"]["llinks"]:
            # 您可以根据需求生成链接名
            link_name = f"Link_{link_data['start']}_{link_data['end']}"
            start_id = link_data["start"]
            end_id = link_data["end"]
            limit = link_data["limit"]
            gdict["links"][link_name] = {
                "start": start_id,
                "end": end_id,
                "limit": limit,
                "distance": 0  # 默认距离就是0
            }
        return gdict
