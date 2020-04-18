#!/usr/bin/env python
# coding=utf-8

from tkinter.filedialog import askopenfilename
from model import analysis_image, plt

if __name__ == '__main__':
    print('        pyImageColorAnalysisTool\nPowerd By Dorad, cug.xia@gmail.com')
    # select filepath
    filename = askopenfilename()
    # color num
    color_num = int(input('将图片分为多少种颜色? '))
    color_show_num = int(input('直方图显示多少颜色? '))

    center, percentage = analysis_image(filename, color_num, color_show_num)
    print('主要颜色及占比:')
    for c, p in zip(center, percentage):
        print('RGB(%s,%s,%s):%0.2f%%' % (c[0], c[1], c[2], p * 100))

    plt.show()
