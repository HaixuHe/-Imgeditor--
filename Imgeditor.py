from tkinter import *
import tkinter.filedialog
from tkinter import messagebox
from PIL import Image,ImageTk
import os,sys
class image():
    def __init__(self, root):
        self.root = root
        self.root.iconbitmap('')
        self.root.title('图片转换工具')
        self.root.geometry('380x380+420+250')
        self.filename = ''   # 图片路径
        self.size_x = 0   # 图片的宽
        self.size_y = 0   # 图片的长
        self.type = ''   # 图片的格式
        self.storage = 0   # 存储空间
        self.j = 0   # 判断保持横纵比是否选上
        self.print_image=''
        self.keep_xy = FALSE
        self.suffix = '.jpg'  # 默认保存成jpg文件
        '''
            choice
        '''
        self.image_choice = LabelFrame(root, text='图像选择', font=('黑体', 11), padx=6, pady=6)
        self.image_choice.place(relx=0.05, rely=0.05)
        self.image_msg = Text(self.image_choice, height=1, width=40)  # 文件选择框
        self.image_msg.pack(side=LEFT)
        choose_bottom = Button(self.image_choice, text='选择', font=('黑体', 9), width=5, command=self.choose)
        choose_bottom.pack()
        '''
            image_information
        '''
        image_information= LabelFrame(root, text='图像信息', font=('黑体', 11), padx=6, pady=6)
        image_information.place(relx=0.05, rely=0.2)
        self.image_info = Label(image_information, justify=LEFT, text='', width=20, height=4)   # 图像信息
        self.image_info.pack()
        self.label_img = Label(image_information, image='')   # 图像缩略图
        self.label_img.pack()
        '''
            size_edit
        '''
        self.var1 = StringVar()
        self.var2 = StringVar()
        image_edit = LabelFrame(root, text='图像大小编辑', font=('黑体', 11), padx=6, pady=6)
        image_edit.place(relx=0.5, rely=0.2)
        Label(image_edit, text='高度:').grid(column=0, row=0)
        self.length=Entry(image_edit,textvariable=self.var1, width=10)
        self.length.grid(column=1, row=1)
        Label(image_edit, text='宽度:').grid(column=0, row=1)
        self.width = Entry(image_edit,textvariable=self.var2, width=10)
        self.width.grid(column=1, row=0)
        ch3 = Checkbutton(image_edit, text='保持横纵比', command=self.judge)
        ch3.grid(column=1, row=5)
        ensure=Button(image_edit, text='刷\n新', command=self.reflesh)
        ensure.grid(column=2, rowspan=3, row=0)
        '''
            image_storage
        '''
        self.mix_st = StringVar()
        image_storage = LabelFrame(root, text='图像存储', font=('黑体', 11), padx=6, pady=6)
        image_storage.place(relx=0.5, rely=0.48)
        Label(image_storage, text='存储限制').pack(side=LEFT)
        self.mix_storage = Entry(image_storage, textvariable=self.mix_st, width=10)
        self.mix_storage.pack(side=LEFT)
        Label(image_storage, text='kb').pack()
        limit_button=Button(root,text='生成图片',width=22,relief=RIDGE,command=self.limit)
        limit_button.place(relx=0.5, rely=0.62)



        self.var_key = IntVar()
        ty=LabelFrame(root,text='格式选择')
        ty.place(relx=0.05,rely=0.7)
        a1=Radiobutton(ty, text="JPGE  ", variable=self.var_key, value=0,command=self.key_type)
        a1.grid(row=0,column=0)
        a2 = Radiobutton(ty, text="PNG   ", variable=self.var_key, value=1,command=self.key_type)
        a2.grid(row=0, column=1)
        a3 = Radiobutton(ty, text="GIF   ", variable=self.var_key, value=2,command=self.key_type)
        a3.grid(row=0, column=2)
        a4 = Radiobutton(ty, text="ICO  ", variable=self.var_key, value=3,command=self.key_type)
        a4.grid(row=0, column=3)
        a5 = Radiobutton(ty, text="BMP   ", variable=self.var_key, value=4,command=self.key_type)
        a5.grid(row=1, column=0)
        a6 = Radiobutton(ty, text="PSD  ", variable=self.var_key, value=5,command=self.key_type)
        a6.grid(row=1, column=1)
        a7 = Radiobutton(ty, text="TIFF  ", variable=self.var_key, value=6,command=self.key_type)
        a7.grid(row=1, column=2)
        a8 = Radiobutton(ty, text="TGA   ", variable=self.var_key, value=7,command=self.key_type)
        a8.grid(row=1,column=3)
        '''
            save
        '''
        choose_bottom = Button(root, text='保存图片', font=('黑体', 10), width=8, height=4,command=self.save)
        choose_bottom.place(relx=0.75, rely=0.72)
    def key_type(self):
        save_type={0:'.jpg',1:'.png',2:'.gif',3:'.ico',4:'.bmp',5:'.psd',6:'.tif',7:'.tga'}
        self.suffix = save_type.get(self.var_key.get())


    def limit(self):
        mix=float(self.mix_storage.get())
        im = Image.open(self.filename)
        b = self.get_FileSize(self.filename)
        size = im.size
        size1, size2 = size
        path=self.filename
        self.type=self.suffix.split('.')[1]
        while b > mix:
            size1, size2 = self.small(size1), self.small(size2)
            size = size1, size2
            im.thumbnail(size, Image.ANTIALIAS)
            path = os.path.split(self.filename)[0] + '/test_storage.' + self.type
            im.save(path)
            b = self.get_FileSize(path)
        self.print_image = Image.open(path)
        Image.MAX_IMAGE_PIXELS = None  # 不检查图片
        init_image = Image.open(path)  # 打开图片
        self.size_x = init_image.size[0]  # 获取图片的宽
        self.size_y = init_image.size[1]  # 获取图片的高
        self.type = init_image.format  # 获取图片的格式
        self.storage = round(os.path.getsize(path) / 1024, 1)  # 获取图片的储存大小
        string = '分辨率：{}×{}\n横纵比：{} : 1\n格式：{}\n大小：{}kb'.format(self.size_x, self.size_y,
                                                                round(self.size_x / self.size_y, 2),
                                                                self.type, self.storage)
        self.image_info.configure(text=string)
        out = init_image.resize((int(80 * (self.size_x / self.size_y)), 80))  # 缩略图
        image_show = ImageTk.PhotoImage(out)
        self.label_img.configure(image=image_show)
        self.label_img.image = image_show
        self.var1.set(self.size_y)
        self.var2.set(self.size_x)

    def get_FileSize(self,picture):
        f1 = os.path.getsize(picture)
        f2 = f1 / float(1024)
        return f2

    # 按比例减小分辨率
    def small(self,SIZE):
        SIZE *= 0.9
        return SIZE
    def reflesh(self):
        try:
            len = int(self.length.get())
            if self.keep_xy is TRUE:
                wid = int(int(len)*(self.size_x / self.size_y))
                self.var2.set(wid)
            else:
                wid = int(self.width.get())
            refresh_image = Image.open(self.filename)
            self.print_image = refresh_image.resize((wid, len))
            # 将生成的图片进行保存，以便计算占空间大小
            path = os.path.split(self.filename)[0]+'/test_xy.'+self.type
            self.print_image.save(path)
            Image.MAX_IMAGE_PIXELS = None  # 不检查图片
            init_image = Image.open(path)  # 打开图片
            self.size_x = init_image.size[0]  # 获取图片的宽
            self.size_y = init_image.size[1]  # 获取图片的高
            self.type = init_image.format  # 获取图片的格式
            self.storage = round(os.path.getsize(path) / 1024, 1)  # 获取图片的储存大小
            string = '分辨率：{}×{}\n横纵比：{} : 1\n格式：{}\n大小：{}kb'.format(self.size_x, self.size_y,
                                                                  round(self.size_x / self.size_y, 2),
                                                                  self.type, self.storage)
            self.image_info.configure(text=string)
            out = init_image.resize((int(80 * (self.size_x / self.size_y)), 80))  # 缩略图
            image_show = ImageTk.PhotoImage(out)
            self.label_img.configure(image=image_show)
            self.label_img.image = image_show
            self.var1.set(self.size_y)
            self.var2.set(self.size_x)
            self.mix_st.set(self.storage)
        except:
            messagebox.showinfo('提示', '请输入正确的图片或信息！')
    def judge(self):
        self.j += 1
        if self.j % 2 == 1:
            self.width.config(state=DISABLED)
            self.keep_xy = TRUE
        else:
            self.width.config(state=NORMAL)
            self.keep_xy = FALSE


    def choose(self):
        try:
            filenames = tkinter.filedialog.askopenfilenames()
            self.filename = filenames[0]
            self.image_msg.delete('1.0', END)
            self.image_msg.insert(END, self.filename)
            Image.MAX_IMAGE_PIXELS = None   # 不检查图片
        except:
            pass
        try:
            self.print_image=init_image = Image.open(self.filename)   # 打开图片
            self.size_x = init_image.size[0]   # 获取图片的宽
            self.size_y = init_image.size[1]   # 获取图片的高
            self.type = init_image.format   # 获取图片的格式
            self.storage = round(os.path.getsize(self.filename)/1024, 1)   # 获取图片的储存大小
            string = '分辨率：{}×{}\n横纵比：{} : 1\n格式：{}\n大小：{}kb'.format(self.size_x, self.size_y,
                                                                       round(self.size_x / self.size_y, 2),
                                                                       self.type, self.storage)
            self.image_info.configure(text=string)
            out = init_image.resize((int(80*(self.size_x / self.size_y)),80))   # 缩略图
            image_show = ImageTk.PhotoImage(out)
            self.label_img.configure(image=image_show)
            self.label_img.image = image_show
            self.var1.set(self.size_y)
            self.var2.set(self.size_x)
            self.mix_st.set(self.storage)

        except OSError:
            messagebox.showinfo('提示', '请先选择正确的图片格式！')
        except ValueError:
            messagebox.showinfo('提示', '不能正确打开图片！')

    def save(self):
        try:
            file = tkinter.filedialog.asksaveasfilename(title=u'保存文件')
            if self.suffix == '.jpg':
                self.print_image = self.print_image.convert('RGB')
            self.print_image.save(str(file) + self.suffix)
            filename1 = os.path.split(self.filename)[0] + '/test_storage.' + self.type
            if os.path.exists(filename1):
                os.remove(filename1)
            filename2 = os.path.split(self.filename)[0] + '/test_xy.' + self.type
            if os.path.exists(filename2):
                os.remove(filename2)
            messagebox.showinfo('提示', '保存成功！')
        except KeyError:
            messagebox.showinfo('提示', '无法保存成{}格式'.format(self.suffix))
        except AttributeError:
            messagebox.showinfo('提示', '请先选择要更改的图片！')
        except OSError:
            messagebox.showinfo('提示', '请选择图片格式！')

if __name__ == '__main__':
    window = Tk()
    image(window)
    window.mainloop()