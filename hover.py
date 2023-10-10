import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

# 创建一个包含几种颜色的Colormap
original_cmap = plt.cm.get_cmap('RdYlGn_r')

# 添加您希望的颜色（这里以蓝色为例）
custom_colors = ['#FF0000', '#00FF00', '#0000FF']  # 添加红、绿、蓝三种颜色
new_colors = original_cmap.colors + custom_colors

# 创建一个新的Colormap，包含添加的颜色
custom_cmap = ListedColormap(new_colors, name='custom_cmap')

# 使用新的Colormap绘制图形
data = [0, 1, 2, 3, 4]
plt.scatter(data, data, c=data, cmap=custom_cmap, s=100)
plt.colorbar(label='Data')

plt.show()
