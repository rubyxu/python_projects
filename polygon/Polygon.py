#!/usr/bin/python
#encoding:utf-8
"""
-note:
1、此脚本功能：判断指定x，y坐标点是否在指定的多边形边界或内，精度经测试在0.0000000000000001；
2、此脚本在macbook开发之后适配windows；
3、码风较粗糙，或仅作为参考;
"""
import sys
#import termios
import io
import os
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

def pointOnBorder(x, y, poly):
    try:
        x, y = float(x), float(y)
    except:
        print("x, y is not float!")
        return False

    n = len(poly)
    for i in range(n):
        p1x, p1y = poly[i]
        p2x, p2y = poly[(i + 1) % n]
        v1x = p2x - p1x
        v1y = p2y - p1y #vector for the edge between p1 and p2
        v2x = x - p1x
        v2y = y - p1y #vector from p1 to the point in question
        if(v1x * v2y - v1y * v2x == 0): #if vectors are parallel
            #如果是0说明垂直x轴，只需要判断y轴范围即可
            if v1x == 0:
                if p1y >= p2y and p2y <= y <= p1y:
                    return True
                else:
                    return False
                if p1y <= p2y and p1y <= y <= p2y:
                    return True
                else:
                    return False
            if (v2x / v1x > 0): #if vectors are pointing in the same direction
                if(v1x * v1x + v1y * v1y >= v2x * v2x + v2y * v2y): #if v2 is shorter than v1
                    return True
    return False

def point_in_polygon(x, y, verts):
    """
    - PNPoly算法
    - xyverts  [(x1, y1), (x2, y2), (x3, y3), ...]
    """
    try:
        x, y = float(x), float(y)
    except:
        print("x, y is not float!")
        return False

    vertx = [xyvert[0] for xyvert in verts]
    verty = [xyvert[1] for xyvert in verts]

    # N个点中，横坐标和纵坐标的最大值和最小值，判断目标坐标点是否在这个四边形之内
    if not verts or not min(vertx) <= x <= max(vertx) or not min(verty) <= y <= max(verty):
        print("overflow")
        return False

    # 上一步通过后，核心算法部分
    nvert = len(verts)
    is_in = False
    for i in range(nvert):
        j = nvert - 1 if i == 0 else i - 1
        if ((verty[i] > y) != (verty[j] > y)) and (
                    x < (vertx[j] - vertx[i]) * (y - verty[i]) / (verty[j] - verty[i]) + vertx[i]):
            is_in = not is_in

    return is_in

###ress_key_to_continue###
def press_any_key_continue(msg):
    # 获取标准输入的描述符
    fd = sys.stdin.fileno()
    # 获取标准输入(终端)的设置
    old_ttyinfo = termios.tcgetattr(fd)
    # 配置终端
    new_ttyinfo = old_ttyinfo[:]
    # 使用非规范模式(索引3是c_lflag 也就是本地模式)
    new_ttyinfo[3] &= ~termios.ICANON
    # 关闭回显(输入不会被显示)
    new_ttyinfo[3] &= ~termios.ECHO
    # 输出信息
    sys.stdout.write(msg)
    sys.stdout.flush()
    # 使设置生效
    termios.tcsetattr(fd, termios.TCSANOW, new_ttyinfo)
    # 从终端读取
    os.read(fd, 7)
    # 还原终端设置
    termios.tcsetattr(fd, termios.TCSANOW, old_ttyinfo)

def graphics_version_1(location, result):
    # 新建画板
    fig1 = plt.figure(figsize=(9, 9), facecolor='lightgray',  edgecolor='black')
    #横轴纵轴命名
    box = dict(facecolor='red', pad=5, alpha=0.2)
    plt.xlabel(u'X轴',bbox=box)
    plt.ylabel(u'Y轴',bbox=box)
    #标题
    plt.suptitle(u'图1 标线表面色色品图', fontsize=20, fontweight='bold')
    plt.subplots_adjust(left=0.1, wspace=0.5, top=0.9)  #位置调整
    #设置坐标轴刻度
    my_x_ticks = np.arange(0, 1.0, 0.1)
    my_y_ticks = np.arange(0, 1.0, 0.1)
    plt.xticks(my_x_ticks)
    plt.yticks(my_y_ticks)
    # 添加子图
    ax3 = fig1.add_subplot(111, facecolor='gray')
    # 画多边形并添加到子图
    pgon_white = plt.Polygon([[], [], [], []], color='white', alpha=0.7)
    pgon_yellow = plt.Polygon([[], [], [], []], color='yellow', alpha=0.7)
    pgon_orange = plt.Polygon([[], [], [], []], color='orange', alpha=0.7)
    pgon_red = plt.Polygon([[], [], [], []], color='red', alpha=0.7)
    pgon_blue = plt.Polygon([[], [], [], []], color='blue', alpha=0.7)
    ax3.add_patch(pgon_white)
    ax3.add_patch(pgon_yellow)
    ax3.add_patch(pgon_orange)
    ax3.add_patch(pgon_red)
    ax3.add_patch(pgon_blue)
    
    #坐标系框线风格
    plt.grid(True, linestyle='-')

    #把指定的坐标点显示出来,plt.annotate()函数用于标注文字
    plt.annotate(s=str(location)+','+result,xy=location,xytext=(0.2,0.9),weight='bold',color='blue',
    arrowprops=dict(arrowstyle='->',connectionstyle='arc3',color='black',shrinkA=0,shrinkB=0),
    bbox=dict(boxstyle='round,pad=0.5', fc='lime', ec='k',lw=1 ,alpha=0.4))
    # 显示画板
    fig1.canvas.draw()
    plt.show()
    return

def graphics_version_2(location, result):
    # 新建画板
    fig2 = plt.figure(figsize=(9, 9), facecolor='lightgray',  edgecolor='black')
    #横轴纵轴命名
    box = dict(facecolor='red', pad=5, alpha=0.2)
    plt.xlabel(u'X轴',bbox=box)
    plt.ylabel(u'Y轴',bbox=box)
    #标题
    plt.suptitle(u'图2 标线涂料的室内检测图', fontsize=20, fontweight='bold')
    plt.subplots_adjust(left=0.1, wspace=0.5, top=0.9)  #位置调整
    #设置坐标轴刻度
    my_x_ticks = np.arange(0, 1.0, 0.1)
    my_y_ticks = np.arange(0, 1.0, 0.1)
    plt.xticks(my_x_ticks)
    plt.yticks(my_y_ticks)
    # 添加子图
    ax3 = fig2.add_subplot(111, facecolor='gray')
    # 画多边形并添加到子图
    pgon_normal_white = plt.Polygon([[], [], [], []], color='azure', alpha=0.7)
    pgon_normal_yellow = plt.Polygon([[], [], [], []], color='yellow', alpha=0.7)
    ax3.add_patch(pgon_normal_white)
    ax3.add_patch(pgon_normal_yellow)
    ax3.add_patch(pgon_reflex_white)
    ax3.add_patch(pgon_reflex_yellow)

    #坐标系框线风格
    plt.grid(True, linestyle='-')

    #把指定的坐标点显示出来
    plt.annotate(s=str(location)+','+result,xy=location,xytext=(0.2,0.9),weight='bold',color='blue',
    arrowprops=dict(arrowstyle='->',connectionstyle='arc3',color='black',shrinkA=0,shrinkB=0),
    bbox=dict(boxstyle='round,pad=0.5', fc='lime', ec='k',lw=1 ,alpha=0.4))
    # 显示画板
    fig2.canvas.draw()
    plt.show()
    return

def main():
    constMark = "--------------请输入---------------"
    infoMark_1 = "功能选择，请输入1或者2（1.xxx 2.xxx）"

    print(constMark.decode("utf-8").encode("gbk") + "\n" + infoMark_1.decode("utf-8").encode("gbk") + "\n" + constMark.decode("utf-8").encode("gbk"))
    entrance_number = raw_input("请根据提示选择功能:".decode("utf-8").encode("gbk"))
    try:
        entrance_number = int(entrance_number)
    except ValueError:
        print("未选择退出！".decode("utf-8").encode("gbk"))
        return
    if entrance_number != 1 and entrance_number != 2:
        print("选择有误，只能选择1或者2.".decode("utf-8").encode("gbk"))
        return

    entrance_x = raw_input("请输入x坐标(浮点型):".decode("utf-8").encode("gbk"))
    try:
        entrance_x = float(entrance_x)
    except ValueError:
        print("输入的x坐标轴类型错误".decode("utf-8").encode("gbk"))
        return

    if entrance_x > 1.0:
        print("输入的x轴值超出范围".decode("utf-8").encode("gbk"))
        return

    entrance_y = raw_input("请输入y坐标(浮点型):".decode("utf-8").encode("gbk"))
    try:
        entrance_y = float(entrance_y)
    except ValueError:
        print("输入的y坐标轴类型错误".decode("utf-8").encode("gbk"))
        return

    if entrance_y > 1.0:
        print("输入的y轴值超出范围".decode("utf-8").encode("gbk"))
        return

    print("输入的坐标为:".decode("utf-8").encode("gbk"))
    print(entrance_x, entrance_y)

    if entrance_number == 1:
        #以下多边形数据自定义
        xyverts_white = [(1, 1), (0, 0), (0.5, 0.5), (0.2, 0.2)]
        xyverts_yello = []
        xyverts_orange = []
        xyverts_red = []
        xyverts_blue = []

        #press_any_key_continue("已选择功能1, 确认选择按回车开始计算。。。\n")
        print("已选择功能1, 开始计算。。。\n".decode("utf-8").encode("gbk"))
        result_white_border = pointOnBorder(entrance_x, entrance_y, xyverts_white)
        result_white = point_in_polygon(entrance_x, entrance_y, xyverts_white)
        print("是否在白色边界[%s]".decode("utf-8").encode("gbk") % (result_white_border))
        print("是否在白色区域[%s]".decode("utf-8").encode("gbk") % (result_white))

        result_yello_border = pointOnBorder(entrance_x, entrance_y, xyverts_yello)
        result_yello = point_in_polygon(entrance_x, entrance_y, xyverts_yello)
        print("是否在黄色边界[%s]".decode("utf-8").encode("gbk") % (result_yello_border))
        print("是否在黄色区域[%s]".decode("utf-8").encode("gbk") % (result_yello))
        
        result_orange_border = pointOnBorder(entrance_x, entrance_y, xyverts_orange)
        result_orange = point_in_polygon(entrance_x, entrance_y, xyverts_orange)
        print("是否在橙色边界[%s]".decode("utf-8").encode("gbk") % (result_orange_border))
        print("是否在橙色区域[%s]".decode("utf-8").encode("gbk") % (result_orange))

        result_red_border = pointOnBorder(entrance_x, entrance_y, xyverts_red)
        result_red = point_in_polygon(entrance_x, entrance_y, xyverts_red)
        print("是否在红色边界[%s]".decode("utf-8").encode("gbk") % (result_red_border))
        print("是否在红色区域[%s]".decode("utf-8").encode("gbk") % (result_red))

        result_blue_border = pointOnBorder(entrance_x, entrance_y, xyverts_blue)
        result_blue = point_in_polygon(entrance_x, entrance_y, xyverts_blue)
        print("是否在蓝色边界[%s]".decode("utf-8").encode("gbk") % (result_blue_border))
        print("是否在蓝色区域[%s]".decode("utf-8").encode("gbk") % (result_blue))
       
        result = ""
        #转换中文
        if result_white_border == True:
            result = u"在白色边界"
        elif result_white == True:
            result = u"在白色内"
        elif result_yello_border == True:
            result = u"在黄色边界"
        elif result_yello == True:
            result = u"在黄色内"
        elif result_red_border == True:
            result = u"在红色边界"
        elif result_red ==  True:
            result = u"在红色内"
        elif result_blue_border ==  True:
            result = u"在蓝色边界"
        elif result_blue == True:
            result = u"在蓝色内"
        elif result_orange_border  ==  True:
            result = u"在橙色边界"
        elif result_orange == True:
            result = u"在橙色内"
        else:
            result = u"不在任何颜色内"
            
        #显示图形
        graphics_version_1((entrance_x, entrance_y), result)
        return 

    elif entrance_number == 2:
        #以下多边形数据自定义
        xyverts_normal_white = []
        xyverts_normal_yellow = []
        xyverts_reflex_white = []
        xyverts_reflex_yellow = []

        #press_any_key_continue("已选择功能2, 确认选择按回车开始计算。。。\n")
        print("已选择功能2, 开始计算。。。\n".decode("utf-8").encode("gbk"))
        result_normal_white_border = pointOnBorder(entrance_x, entrance_y, xyverts_normal_white)
        result_normal_white = point_in_polygon(entrance_x, entrance_y, xyverts_normal_white)
        print("是否在白色边界[%s]".decode("utf-8").encode("gbk") % (result_normal_white_border))
        print("是否在白色区域[%s]".decode("utf-8").encode("gbk") % (result_normal_white))

        result_normal_yellow_border = pointOnBorder(entrance_x, entrance_y, xyverts_normal_yellow)
        result_normal_yellow = point_in_polygon(entrance_x, entrance_y, xyverts_normal_yellow)
        print("是否在黄色边界[%s]".decode("utf-8").encode("gbk") % (result_normal_yellow_border))
        print("是否在黄色区域[%s]".decode("utf-8").encode("gbk") % (result_normal_yellow))

        result = ""
        #转换中文
        if result_normal_white_border == True:
            result = u"在普通材料白色区域边界"
        elif result_normal_yellow_border == True:
            result = u"在普通材料黄色区域边界"
        elif result_normal_white == True:
            result = u"在普通材料白色区域内"
        elif result_normal_yellow == True:
            result = u"在普通材料黄色区域内"
        else:
            result = u"不在任何颜色内"
        
        #显示图形
        graphics_version_2((entrance_x, entrance_y), result)
        return

    else:
        print("未确认退出！".decode("utf-8").encode("gbk"))
        return

if __name__ == "__main__":
    while True:
        main()
