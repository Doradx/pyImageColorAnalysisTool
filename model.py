from PIL import Image, ImageColor
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans

##########
# 参数修改区

# image_path = '中国画.jpg'
image_path = 'res/中国画.jpg'
color_num = 10
color_show_num = 10


# 参数修改区
##########


def load_image_data(path):
    image = Image.open(path)
    if image.width > 300:
        image = image.resize((300, int(image.width / 300 * image.height)), Image.ANTIALIAS)
    imageArrayOrigin = np.asarray(image)
    imageArray = imageArrayOrigin.reshape((imageArrayOrigin.shape[0] * imageArrayOrigin.shape[1], 3))
    row = imageArrayOrigin.shape[0]
    col = imageArrayOrigin.shape[1]
    return imageArray, row, col


def get_center_and_hist(data, label):
    center = []
    hist = []
    for i in range(np.max(label) + 1):
        center.append(tuple(np.average(data[label == i, :], 0).astype(np.int)))
        hist.append(np.count_nonzero(label == i))
    percentage = np.true_divide(hist, data.shape[0])
    return center, hist, percentage


def plot_color_hist(center, hist, show_num=5):
    idx = np.argsort(-np.array(hist))  # 降序
    hist = hist[idx]
    center = np.array(center)[idx]
    # plot the bar
    plt.bar(range(show_num), hist[0:show_num] * 100, color=np.true_divide(center[0:show_num, :], 255))

    plt.xticks([])
    plt.xlabel('Color')
    plt.ylabel('Percentage/%')

    return center, hist


def create_label_image(row, col, label, center):
    image = Image.new(mode='RGB', size=(row, col))
    for r in range(row):
        for c in range(col):
            image.putpixel((r, c), center[label[r, c]])
    return image


def hsv2rgb(hsv):
    s = 'hsv(' + str(hsv[0]) + ',' + str(hsv[1] / 255) + '%,' + str(hsv[2] / 255) + '%)'
    return tuple(ImageColor.getrgb(s))


def analysis_image(path, color_num, show_num):
    data, row, col = load_image_data(path)

    km = KMeans(n_clusters=color_num)
    # 聚类获得每个像素所属的类别
    label = km.fit_predict(data)
    center, hist, p = get_center_and_hist(data, label)

    return plot_color_hist(center, p, show_num)


# # show the image
# image_new = create_label_image(row, col, label, center)
# image_new.show()
# pass

if __name__ == '__main__':
    center, percentage = analysis_image(image_path, color_num, color_show_num)
    print('主要颜色及占比:')
    for c, p in zip(center, percentage):
        print('RGB(%s,%s,%s):%0.2f%%' % (c[0], c[1], c[2], p * 100))

    plt.show()
