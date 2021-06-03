import tkinter as tk
from tkinter import Text, ttk
from tkinter.constants import DISABLED, RIGHT, NORMAL, END
import tkinter.filedialog
import tkinter.font as tkFont
from PIL import Image, ImageTk, ImageFont, ImageDraw
from tkinter.colorchooser import askcolor
import sys

class StdSimulator():
    def __init__(self, box) -> None:
        self.box = box
        self.stdout = sys.stdout
        self.stderr = sys.stderr
    
    def write(self, msg):
        self.box.insert(END, msg)
        self.box.see(END)
    
    def flush(self):
        pass

def text_on_image(img, text, pos, size=16, color='#000000'):
    imgdraw = ImageDraw.Draw(img)
    imgfont = ImageFont.truetype("msyh.ttc",size=size)
    textw, texth = imgdraw.textsize(text, font=imgfont)
    left_top = (pos[0]-int(textw/2), pos[1]-int(texth/2))
    imgdraw.text(left_top, text, fill=color, font=imgfont)
    return img

class Loader(tk.Frame):
    def __init__(self, master=None, conf={}, execution=None, title=None, help_msg=None):
        super().__init__(master)
        self.master = master
        self.conf = conf
        self.execution = execution
        self.title = title

        self.pack(fill='both', expand=1)
        self.resources = {}
        self.fontStyle = tkFont.Font(size=10, family='微软雅黑')
        self.fontStyle_anchor = tkFont.Font(size=16)
        self.create_widgets()
        # self.font = tk.Font(family='', size=40,weight='',slant='',underline='',overstrike='')
        if self.title is not None:
            self.master.title(self.title)
        self.help_msg = help_msg
    def add_resource(self, obj, name):
        if name in self.resources:
            print('Name [{0}] Repeated.'.format(name))
            print('Current used name:', list(self.resources.keys()))
            raise ValueError
        self.resources[name] = obj
    
    def add_entry(self, default, width, layout, name, master=None):
        if master is None:
            master = self
        resource = tk.Entry(master, width=width)
        if type(default) is str:
            resource.insert(0, default)
        resource.grid(**layout)
        self.add_resource(resource, name)

    def add_label(self, text, layout, name, master=None):
        if master is None:
            master = self
        resource = tk.Label(master, text=text, font=self.fontStyle)
        resource.grid(**layout)
        self.add_resource(resource, name)

    def add_button(self, text, command, layout, size, name, image=None, master=None):
        if master is None:
            master = self
        resource = {}
        if image is not None:
            width, height = size
            image = image.resize((width,height))
            if text is not None:
                image = text_on_image(image, text, (int(width/2), int(height/2)), size=16, color='#000000')
            img = ImageTk.PhotoImage(image)
            resource['img'] = img
            resource['button'] = tk.Button(master, text=text, command=command, borderwidth=0)
            resource['button'].config(image=img)
        else:
            resource['button'] = tk.Button(master, text=text, command=command)
        resource['button'].grid(**layout)
        self.add_resource(resource, name)
    
    def add_textbox(self, width, layout, name, master=None):
        if master is None:
            master = self
        resource = tk.Text(master, width=width, state=NORMAL)
        resource.grid(**layout)
        # vsb = tk.Scrollbar(self, orient="vertical", command=resource.yview)
        # resource.configure(yscrollcommand=vsb.set)
        self.add_resource(resource, name)
        # self.add_resource(vsb, name + '_scroll')


    def choose_file(self, dst, choose_type='readfile', extension=None, initial_file=None):
        default_extension = ("所有文件", '.*')
        args = {"filetypes": []}
        if extension is not None:
            args['filetypes'].append(extension)
        args['filetypes'].append(default_extension)
        if initial_file is not None:
            args['initialfile'] = initial_file

        # print('args:', args)
        filename = ''
        if choose_type == 'readfile':
            filename = tkinter.filedialog.askopenfilename(**args)
        elif choose_type == 'savefile':
            filename = tkinter.filedialog.asksaveasfilename(**args)
        elif choose_type == 'directory':
            args = {
                'initialdir': initial_file
            }
            filename = tkinter.filedialog.askdirectory(**args)
        if filename != '':
            self.resources[dst].delete(0, 'end')
            self.resources[dst].insert(0, filename)
    
    def choose_color(self, dst):
        color = askcolor()[0]
        if color is not None:
            color = [str(c) for c in color]
            color = ','.join(color)
            self.resources[dst].delete(0, 'end')
            self.resources[dst].insert(0, color)
    
    def execute(self):
        conf = {}
        for key in self.resources:
            dtype, name = key.split('_', maxsplit=1)
            if dtype == 'entry':
                conf[name] = self.resources[key].get()
        self.execution(conf)
    
    def clear(self):
        self.resources['textbox_log'].delete("1.0", 'end')
    
    def showhelp(self):
        print(self.help_msg)
    
    def create_widgets(self):
        self.rowcount = 0
        for key, value in self.conf.items():
            name = value['name']
            dtype = value['type']
            default = value.get('default', '')
            self.add_label(name, {"row": self.rowcount, "column": 0, "padx": 10, "pady": 5}, name="label_" + key)
            self.add_entry(
                default=default,
                width=None,
                layout={"row": self.rowcount, "column": 1, "padx": 0, "sticky": "we"},
                name='entry_' + key
            )
            destination = 'entry_' + key
            if dtype in ['readfile', 'savefile', 'directory']:
                extension = value.get('extension', None)
                initialfile = value.get('initial', None)
                args = {
                    "dst": destination,
                    "choose_type": dtype,
                    "extension": extension,
                    "initial_file": initialfile
                }
                self.add_button(
                    text="<选择文件",
                    command=lambda args=args:self.choose_file(**args),
                    size=(16, 16),
                    layout={"row":self.rowcount, "column": 2, "padx": 5},
                    name='{0}_choose'.format(name),
                    image=None
                )
                self.conf[key]['type'] = 'str'
            elif dtype == 'color':
                self.add_button(
                    text="<选择颜色",
                    command=lambda dst=destination:self.choose_color(dst),
                    size=(16, 16),
                    layout={"row":self.rowcount, "column": 2, "padx": 5},
                    name='{0}_choose'.format(name),
                    image=None
                )

            self.rowcount += 1
        self.add_button(
            text="清空输出>",
            command=self.clear,
            size=(16, 16),
            layout={"row":self.rowcount-2, "column": 2, "pady": 5, "sticky": "e"},
            name='clear_output'
        )
        self.add_button(
            text="显示帮助>",
            command=self.showhelp,
            size=(16, 16),
            layout={"row":self.rowcount-1, "column": 2, "pady": 5, "sticky": "e"},
            name='show_help'
        )
        self.add_button(
            text="        开始裁剪        ",
            command=self.execute,
            size=(16, 16),
            layout={"row":self.rowcount, "column": 0, "columnspan": "3", "pady": 5},
            name='execute_final'
        )
        self.add_textbox(
            width=40, 
            layout={"row":0, "column": 3, "rowspan": self.rowcount + 1, "padx": 5, "pady": 5, "sticky": "ns"},
            name="textbox_log"
        )
        sys.stdout = StdSimulator(self.resources['textbox_log'])
        sys.stderr = StdSimulator(self.resources['textbox_log'])

if __name__ == '__main__':
    conf = {
        "input": {"name": "源文件", "type": "readfile", "extension": ("PDF & PPT", ".pdf .pptx")},
        "output": {"name": "保存路径", "type": "savefile"},
        "background_color": {"name": "背景颜色", "type": "color", "default": "255,255,255"},
        "border": {"name": "留白", "type": "str", "default": "0.0"},
        "zoom": {"name": "缩放等级", "type": "str", "default": "1.0"},
        "thresh": {"name": "阈值", "type": "str", "default": "1.0"},
        "split": {"name": "拆分", "type": "str", "default": "false"},
        "names": {"name": "页名称", "type": "str"},
        "visual": {"name": "显示裁切框", "type": "str", "default": "false"},
        "mute": {"name": "显示保存文件", "type": "str", "default": "false"},
    }
    root = tk.Tk()
    Loader(master=root, conf=conf)
    root.mainloop()