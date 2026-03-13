import os.path
import tkinter as tk
import tkinter.filedialog
import numpy as np
from PIL import Image, ImageTk
import tkinter.messagebox
import cv2


class App:
    def __init__(self, master):
        self.master = master
        self.master.title("机读卡答题区域定位系统")  # 设定标题
        self.master.geometry("1200x1000")  # 设定长宽

        # 创建菜单栏
        menu_bar = tk.Menu(self.master)
        # 第一列
        # add_command为加入行，内部参数分别是：名字，执行的函数，是否可用（第二列才出现这个）
        file_menu = tk.Menu(menu_bar, tearoff=0)  # 创建新列
        menu_bar.add_cascade(label="文件", menu=file_menu)  # 加入新列到菜单栏
        file_menu.add_command(label="打开图像", command=self.open_image)
        file_menu.add_command(label="保存图像", command=self.save_image)
        file_menu.add_separator()  # 分界线
        file_menu.add_command(label="退出", command=self.master.destroy)
        # 第二列 后续需用到所以用self创建
        self.edit_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="编辑", menu=self.edit_menu)
        self.edit_menu.add_command(label="矫正图像", command=self.test1)
        self.edit_menu.add_command(label="缩小区域", command=self.test5, state="disabled")
        self.edit_menu.add_command(label="水平定位", command=self.test2, state="disabled")
        self.edit_menu.add_command(label="垂直定位", command=self.test3, state="disabled")
        self.edit_menu.add_command(label="锁定答题区域", command=self.test4, state="disabled")
        self.edit_menu.add_command(label="输出答案", command=self.Show_Answer, state="disabled")
        self.edit_menu.add_separator()  # 分界线
        self.edit_menu.add_command(label="返回", command=self.back)
        # 第三列，使用说明
        mine_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="使用说明", menu=mine_menu)
        mine_menu.add_command(label="开发者", command=self.developer)
        mine_menu.add_command(label="特色", command=self.character)
        mine_menu.add_command(label="功能及使用", command=self.use)
        # 添加菜单，即将上面一大堆设定添加到界面上
        self.master.config(menu=menu_bar)

        # 创建画布，长宽自己设定
        self.canvas = tk.Canvas(self.master, width=1000, height=800)
        self.canvas.pack()

        # 添加文本框
        self.text = tk.Text(self.master, borderwidth = 3, height=20, width = 160, relief="sunken")
        self.text.place(x=0, y=650)
        # 添加按钮
        tk.Button(master, text="图像校正", width=10, command=self.test1).place(x=1000, y=100)
        tk.Button(master, text="缩小区域", width=10, command=self.test5).place(x=1000, y=150)
        tk.Button(master, text="水平定位", width=10, command=self.test2).place(x=1000, y=200)
        tk.Button(master, text="垂直定位", width=10,command=self.test3).place(x=1000, y=250)
        tk.Button(master, text="锁定答案区域", width=10, command=self.test4).place(x=1000, y=300)
        tk.Button(master, text="输出答案", width=10, command=self.Show_Answer).place(x=1000, y=350)
        tk.Button(master, text="返回", width=10, command=self.back).place(x=1000, y=400)

        # 初始化变量
        # 存储显示的图片
        self.image = None
        # 存储临时图像
        self.image_exmple = None
        # 存储已经显示过的所有图片，用于返回图片
        self.image_test = []
        # 存储垂直水平定位块的坐标
        self.Vertical_Answer = []
        self.Horizontal_Answer = []
        self.Horizontal_Tmp = []
        self.Answer = []
        self.Real_Answer = []
        self.Horizontal_Example = 0

    def open_image(self):
        # 打开图像文件，即获取图像在电脑中的绝对路径
        default_dir = r"文件路径"
        file_path = tkinter.filedialog.askopenfilename(title=u"选择文件",
                                                       initialdir=(os.path.expanduser((default_dir))))
        self.image = cv2.imread(file_path)  # 读取图像文件
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)  # 将图像转换为RGB格式
        self.show_image()  # 显示图像
        self.image_test = []  # 清空原本存储的图像
        self.image_test.append(self.image.copy())  # 存储图像
        self.text.delete("1.0", "end")

        # 以下方法具有检测功能，但是不知道为什么选不上文件
        # filename = filedialog.askopenfilename(filetypes=[("图像文件", "*.jpg;*.png;*.bmp")])
        # if filename:
        #     self.image = cv2.imread(filename) # 读取图像文件
        #     self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)  # 将图像转换为RGB格式
        #     self.show_image() # 显示图像

    def show_image(self):
        # 将图像转换为Tkinter PhotoImage格式
        image = cv2.resize(self.image, (800, 600))  # 调整图像的大小，使其能完整展现在画布上
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # 将图像转化成BGR格式
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # 再将图像转化成RGB格式
        image = Image.fromarray(image)  # 由上所得为数组，该函数是将数组转化图像
        self.photo = ImageTk.PhotoImage(image)  # 将图像转化成PhotoImage格式
        # 显示图像在画布上
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

    def save_image(self):
        if self.image is not None:
            cv2.imwrite('test.jpg', self.image)  # 保存图像在当前文件夹下

    def back(self):
        # 恢复图像
        if len(self.image_test) > 1:
            self.image_test.pop()  # 删除当前的图像
            self.image = self.image_test[-1]  # 返回到上一张图像
            self.show_image()  # 在画布上显示图像
        else:
            # 出现提示框，提示已经没有图片可以返回了
            tk.messagebox.showinfo("消息", "已经是第一张图片了！")

    def test1(self):
        # 校正图像 若图像相对正视角度有所偏移
        img = self.image  # 读取图像
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 将原图像灰度化
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)  # Canny边缘检测
        lines = cv2.HoughLines(edges, 1, np.pi / 180, 400)  # 霍夫直线检测
        # 获取倾斜角度 方法一
        angle = 0
        for line in lines:
            # 获取所得直线的角度，rho没啥用，theta为相对水平角度
            rho, theta = line[0]

            if theta < np.pi / 4:
                angle += theta
            elif theta > 3 * np.pi / 4:
                # 若小于45度或大于135度则加上角度并减去90度
                angle += (theta - np.pi)
            else:
                # 若大于45度或下于135度则直接加上角度
                angle += (theta - np.pi / 2)

        # 平均倾斜角度，最后所得角度直接除以线条的总数量
        angle /= len(lines)
        # 图像旋转校正
        rows, cols = img.shape[:2]  # 获取原图像的长和宽
        # 获取旋转矩阵，第一个参数是确定中心位置，相对中心位置旋转，第二个是旋转的角度
        M = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle * 180 / np.pi, 1)
        # 相对旋转矩阵旋转
        self.image = cv2.warpAffine(img, M, (cols, rows))
        # 显示图像
        self.show_image()
        # 解锁其它菜单栏项
        self.edit_menu.entryconfig('缩小区域', state='normal')
        self.edit_menu.entryconfig('水平定位', state='normal')
        self.edit_menu.entryconfig('垂直定位', state='normal')
        # 后台存储图像方便返回上一张图像
        self.image_test.append(self.image.copy())

    def test2(self):
        # 水平定位块
        self.image_exmple = self.image.copy()
        img = self.image  # 获取需要处理的图像
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 将图像灰度化
        # 高斯滤波，去除噪声
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        # 二值化，将图像的灰度图转化为只有0和255两个值方便后续处理，后面两个参数是让二值化为标准二值化，该黑的黑，该亮的亮
        ret, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        # 膨胀操作，填充边缘
        kernel = np.ones((3, 3), np.uint8)  # 3X3模版
        dilation = cv2.dilate(thresh, kernel, iterations=1)
        # 查找轮廓 第二个参数是是"轮廓检索模式"，此处为只检测最外层的轮廓，
        # 第三个参数是"轮廓表示方法"，就是矩形的四个定点，这个无需了解
        contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # 遍历轮廓
        flag = True  # 一般机读卡的水平定位块都是很长一段，而且分上下两端，所以取一段就行了，设定flag防止取两段
        for contour in contours:
            # 计算轮廓的面积，通过面积来确定定位块
            area = cv2.contourArea(contour)
            # 获取定位块的坐标：x坐标，y坐标，w宽度，h高度
            x, y, w, h = cv2.boundingRect(contour)
            # 如果面积和宽高在一定范围内，则认为是机读卡水平定位块
            if 300 < w and 5 < h < 30:
                # 在图像上标识出定位块的位置，rectangle是绘制矩形，中间两个坐标是从左上上到右下（或者反过来），第四个参数是颜色，最后一个是线条宽度
                cv2.rectangle(img, (x - 30, y), (x + w + 30, y + h), (255, 0, 0), 1)
                # 将坐标存储起来
                self.Horizontal_Tmp.append(y)
                if flag:
                    x1 = x - 30
                    y1 = (w + 75) / 23
                    i = 1
                    while x1 < x + w + 30:
                        self.Horizontal_Answer.append((i, x1 + y1 // 2))
                        i += 1
                        x1 += y1
                        if i == 24:
                            self.Horizontal_Example = x + w + 30

                    flag = False

        if self.Horizontal_Example == 0:
            tk.messagebox.showinfo("出错", "建议此样本不要使用缩小区域！")
        self.image = img
        self.show_image()
        self.image_test.append(self.image.copy())
        self.image = self.image_exmple
        self.edit_menu.entryconfig("锁定答题区域", state="normal")

    def test3(self):
        # 垂直定位块，类似方法同test2
        self.image_exmple = self.image.copy()
        img = self.image
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 高斯滤波，去除噪声
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        # 二值化
        ret, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        # 膨胀操作，填充边缘
        kernel = np.ones((3, 3), np.uint8)  # 3X3模版
        dilation = cv2.dilate(thresh, kernel, iterations=1)
        # 查找轮廓
        contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # 遍历轮廓
        i = 0
        for contour in contours:
            # 计算轮廓的面积
            area = cv2.contourArea(contour)
            # 获取定位块的坐标
            x, y, w, h = cv2.boundingRect(contour)
            # 如果面积和宽高在一定范围内，则认为是机读卡垂直定位块
            # if 30 < w < 50 and h < 20 and 300 < area < 500:
            if x >= self.Horizontal_Example:
                if 28 < w < 50 and h < 20 and 300 < area < 500:
                    # 在图像上标识出定位块的位置，rectangle是绘制矩形
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 1)
                    y_center = y + h // 2
                    # 将中心坐标存储起来
                    if self.Horizontal_Tmp[1] < y_center < self.Horizontal_Tmp[0]:
                        self.Vertical_Answer.append((i, y_center))
                        i += 1
                    else:
                        self.Vertical_Answer.append((0, y_center))

        self.image = img
        self.show_image()
        self.image_test.append(self.image.copy())
        self.image = self.image_exmple
        self.edit_menu.entryconfig("锁定答题区域", state="normal")

    def test4(self):
        # 锁定答题区域
        # 读取图像
        img = self.image
        # 将图像转换为灰度图像
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 高斯滤波，去除噪声
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        # 二值化
        ret, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        # 膨胀操作，填充边缘
        kernel = np.ones((3, 3), np.uint8)  # 3X3模版
        dilation = cv2.dilate(thresh, kernel, iterations=1)
        # 查找轮廓
        contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # 遍历轮廓
        for contour in contours:
            # 计算轮廓的面积
            area = cv2.contourArea(contour)
            # 获取坐标
            x, y, w, h = cv2.boundingRect(contour)
            x_center = x + w // 2
            y_center = y + h // 2
            # 如果面积和宽高在一定范围内,则锁定，这种方法肯定有一定的误差
            if 200 < area < 500:
                # 通过定位块进一步判断
                for i,j in self.Horizontal_Answer:
                    for k,l in self.Vertical_Answer:
                        if x < j < x + w + 5:
                            if y < l < y + h + 5:
                                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 1)
                                if (k + 2) % 7 == 0:
                                    cv2.putText(img, "A", (x_center,y_center), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1)
                                    self.Answer.append((i, k, "A"))
                                elif (k + 3) % 7 == 0:
                                    cv2.putText(img, "B", (x_center,y_center), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 1)
                                    self.Answer.append((i, k, "B"))
                                elif (k + 4) % 7 == 0:
                                    cv2.putText(img, "C", (x_center,y_center), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 1)
                                    self.Answer.append((i, k, "C"))
                                elif (k + 5) % 7 == 0:
                                    cv2.putText(img, "D", (x_center,y_center), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 1)
                                    self.Answer.append((i, k, "D"))

        if len(self.Answer) == 0:
            tk.messagebox.showinfo("出错", "建议此样本不要使用缩小区域！")
        self.Answer.sort(key=lambda x: (x[0], -x[1])) # 排序
        self.Horizontal_Answer.clear()
        self.Vertical_Answer.clear()
        self.Horizontal_Tmp.clear()
        self.image = img
        self.show_image()
        self.image_test.append(self.image.copy())
        self.edit_menu.entryconfig("输出答案", state="normal")

    def test5(self):
        # 缩小区域
        img = self.image  # 读取需要处理的图像
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 灰度化
        blur = cv2.GaussianBlur(gray, (5, 5), 0)  # 高斯滤波，去除噪声
        edges = cv2.Canny(blur, 50, 150, apertureSize=3)  # Canny边缘检测，中间两个是阈值
        # 膨胀操作，填充边缘
        kernel = np.ones((3, 3), np.uint8)  # 3X3模版
        dilation = cv2.dilate(edges, kernel, iterations=1)  # 标准3X3膨胀
        # 查找轮廓
        contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # 找到最大的轮廓
        max_contour = max(contours, key=cv2.contourArea)
        # 计算轮廓的外接矩形并绘制矩形框，这里没有绘制怕影响图像后续处理，也不需要绘制
        # rect = cv2.minAreaRect(max_contour)
        # box = cv2.boxPoints(rect)
        # box = np.int0(box)
        # cv2.drawContours(img, [box], 0, (0, 0, 255), 2)
        # 提取定位块坐标
        x, y, w, h = cv2.boundingRect(max_contour)
        answer_area = self.image[y:y + h, x:x + w]
        self.image = answer_area
        self.show_image()
        self.image_test.append(self.image.copy())

    def developer(self):
        self.canvas.delete("all")  # 清除画布上的所有东西
        font = ("Arial", 20, "bold")  # 设置字体，参数分别是：字型、字体大小、加粗
        # 在画布上写入字体
        self.canvas.create_text(250, 150, text="第七组（机读卡答题区域定位系统）", font=font, fill="red")
        self.canvas.create_text(250, 200, text="郝健均：水平定位块模型构建，击中击不中变换定位", font=font)
        self.canvas.create_text(250, 250, text="钟国宇：垂直定位块模型构建，击中击不中变换定位", font=font)
        self.canvas.create_text(320, 300, text="张佳男：Hough直线变换获取机读卡的倾斜角度，实现图像旋转校正", font=font)
        self.canvas.create_text(250, 350, text="毛克日：标记答题区域", font=font)
        self.canvas.create_text(250, 400, text="尹德：需求分析和数据收集，UI设计", font=font)

    def character(self):
        self.canvas.delete("all")  # 清除画布上的所有东西
        font = ("Arial", 20, "bold")  # 设置字体，参数分别是：字型、字体大小、加粗
        self.canvas.create_text(250, 150, text="特色", font=font, fill="red")
        self.canvas.create_text(250, 200, text="1.快速准确定位", font=font)
        self.canvas.create_text(250, 250, text="2.自动识别", font=font)
        self.canvas.create_text(250, 300, text="3.高效节省人工成本", font=font)
        self.canvas.create_text(250, 350, text="4.方便数据管理", font=font)
        self.canvas.create_text(250, 400, text="5.实现智能化评卷", font=font)

    def use(self):
        self.canvas.delete("all")  # 清除画布上的所有东西
        font = ("Arial", 20, "bold")  # 设置字体，参数分别是：字型、字体大小、加粗
        self.canvas.create_text(250, 150, text="使用说明", font=font, fill="red")
        self.canvas.create_text(250, 200, text="1.先打开图片并选择图片", font=font)
        self.canvas.create_text(250, 250, text="2.然后再校正图片", font=font)
        self.canvas.create_text(250, 300, text="3.如果需要缩小区域则先缩小区域", font=font)
        self.canvas.create_text(250, 350, text="4.接着水平定位和垂直定位，顺序不限", font=font)
        self.canvas.create_text(250, 400, text="5.最后锁定答题区域", font=font)

    def Show_Answer(self):
        tmp = 0
        for i, j, k in self.Answer:
            x = i // 6  # 水平的话是每6个格子循环一次
            x1 = i % 6  # 获取题号的序号
            x0 = x1 + x * 5 # 根据序号获取每行对应的题号
            y = j // 7  # 垂直的话是每7个格子循环一次，获取行号的倒序
            hhh = [4, 3, 2, 1, 0]   # 由于是倒序，所以需要将0，1，2，3，4转化为4，3，2，1，0，获取行号
            x0 = x0 + 20 * hhh[y]   # 20是每行的题号的个数，hhh[y]是行号
            if tmp != x0:   # 如果有重复的序号，则取第一个序号，即有多选的话只获取一个选项
                self.Real_Answer.append((x0, k))
            tmp = x0

        self.Real_Answer.sort(key=lambda x: x[0])   # 将获取后的答案根据序号进行排序，注意获取的答案的形式是（序号，选项）
        n = 1   # 根据此选项来进行换行操作，每20次换一次行
        m = 1   # 从1到100保存题号，顺便判断中途有无没有填涂的答案
        for i, j in self.Real_Answer:
            if n == 21: # 换行操作
                self.text.insert("end", "\n")
                n = 1

            if m != i:  # 判断中间是否有没有填涂的答案
                while m < i:
                    self.text.insert("end", "{0}.{1}\t".format(m, " "))
                    m += 1
                    n += 1
                    if n == 21: # 换行操作
                        self.text.insert("end", "\n")
                        n = 1
                self.text.insert("end", "{0}.{1}\t".format(i, j))   # 打印答案
            else:
                self.text.insert("end", "{0}.{1}\t".format(i, j))   # 打印答案

            n += 1
            m += 1

        # 不重要，将后面没有填涂的答案也打印出来
        while m <= 100:
            if n == 21:
                self.text.insert("end", "\n")
                n = 1

            self.text.insert("end", "{0}.{1}\t".format(m, " "))
            m += 1
            n += 1

        self.Real_Answer.clear()
        self.Answer.clear()


if __name__ == "__main__":
    test = tk.Tk()
    app = App(test)
    test.mainloop()
    