# import argparse
import tkinter as tk
from cropper import crop
import traceback

def str2bool(string):
    positive = ['true',
        't',
        'y',
        'yes',
        '1',
        'correct',
        'accept',
        'positive'
    ]
    if string.lower() in positive:
        return True
    else:
        return False

def str2list(string):
    try:
        string = string.split(',')
        l = []
        for sp in string:
            if sp != '':
                l.append(float(sp))
        l = l[:3]
        if len(l) < 3:
            raise ValueError
        return l
    except:
        print('parse list failed.')
        raise ValueError

def empty_as_none(string):
    if string == '':
        return None
    else:
        return string

class Configuration():
    def __init__(self) -> None:
        pass

def parse_and_crop(conf):
    handlers = {
        "output": empty_as_none,
        "names": empty_as_none,
        "background_color": str2list,
        "border": float,
        "zoom": float,
        "thresh": float,
        "split": str2bool,
        "visual": str2bool,
        "mute": str2bool,
    }
    for key in conf:
        if key in handlers:
            conf[key] = handlers[key](conf[key])
    print('======= conf =======\n', '\n'.join(['{0}={1}'.format(key, value) for key, value in conf.items()]))
    if conf['input'] == '':
        print('Error, input file must be given.')
    else:
        args = Configuration()
        args.__dict__.update(conf)
        try:
            crop(args)
        except Exception:
            print(traceback.format_exc())



    

# parser = argparse.ArgumentParser(description="Remove white border in pdf")
# parser.add_argument('--input', '-i', type=str, help='path to the input pdf.')
# parser.add_argument('--output', '-o', type=str, default=None, help='path to output file, default=infile_crop.pdf')
# parser.add_argument('--background_color', '-bgc', type=str2list, default=[255, 255, 255], help='pixels that are considered as background')
# parser.add_argument('--border', '-b', type=float, default=0.0, help='a value in pixel that specifies the border to given.')
# parser.add_argument('--zoom', '-z', type=float, default=1.0, help='bigger is better, however also slower.')
# parser.add_argument('--thresh', '-t', type=float, default=1, help='threshold that a pixel is considered as background')
# parser.add_argument('--split', '-s', action='store_true', default=False, help='auto split the file, default names as out_1.pdf, ...')
# parser.add_argument('--names', '-n', type=str, default=None, help='specify the name of the cropped pdf.')
# parser.add_argument('--visual', '-v', default=False, action='store_true', help='display cropbox.')
# parser.add_argument('--mute', '-m', default=False, action='store_true', help='do not display output file path.')
# args = parser.parse_args()


import os
import json
from ui import Loader
defaults = {
    "input": "",
    "output": "",
    "background_color": "255,255,255",
    "border": "0.0",
    "zoom": "1.0",
    "thresh": "1.0",
    "split": "true",
    "names": "",
    "visual": "false",
    "mute": "false"
}
config_path = 'config.json'
if os.path.isfile(config_path):
    with open(config_path, 'r', encoding='utf-8') as f:
        updater = json.load(f)
        defaults.update(updater)
else:
    with open(config_path, 'w+', encoding='utf-8') as f:
        json.dump(defaults, f, ensure_ascii=False, indent=4)

conf = {
        "input": {"name": "源文件", "type": "readfile", "extension": ("PDF & PPT", ".pdf .pptx")},
        "output": {"name": "保存路径", "type": "savefile", "initial": "output.pdf"},
        "background_color": {"name": "背景颜色", "type": "color", "default": "255,255,255"},
        "border": {"name": "留白", "type": "str", "default": "0.0"},
        "zoom": {"name": "缩放等级", "type": "str", "default": "1.0"},
        "thresh": {"name": "阈值", "type": "str", "default": "1.0"},
        "split": {"name": "拆分", "type": "str", "default": "true"},
        "names": {"name": "页名称", "type": "str"},
        "visual": {"name": "显示裁切框", "type": "str", "default": "false"},
        "mute": {"name": "显示保存文件", "type": "str", "default": "false"},
    }

introduction = [
"==== 使用说明 ====",
"- 源文件：输入的文件，可以为PDF或者PPT，如果是PPT，会首先自动调用PowerPoint将给定的PPT转变为PDF然后进行裁剪（PPT裁剪第一次需要调用COM对象因此速度稍慢，建议耐心等待，裁切一次后速度会恢复到正常水平",
"- 保存路径：保存的文件名，仅适用于非拆分模式。如果留空，则保存路径为源文件所在目录，保存的文件名为\"源文件名_crop.pdf\"",
"- 背景颜色：哪一种颜色会被认为是背景",
"- 留白：不紧贴有效内容裁切，预留一个给定大小的白边。",
"- 缩放等级：裁切是基于视觉裁切的，因此裁切过程中会首先渲染PDF，采用默认值即可，更高的缩放会将PDF渲染为更高分辨率的图片从而提高裁剪精度，但计算时间也会相应增加。",
"- 阈值：像素值差异多少会被认为是前景。",
"- 拆分：是否将源文件自动拆分为每页一个的单个文件。默认文件名采取下划线+数字命名。如果源文件是PPT且PPT备注不为空，则首先采用PPT的备注作为当前页保存的文件名。",
"- 页名称：手动指定拆分模式下每一页的名称，具有最高优先级，用逗号分隔。留空则使用默认的文件名或者PPT中备注的文件名。",
"- 显示裁切框：在右侧的日志区域输出裁切框坐标",
"- 显示保存文件：显示保存的文件名。",
]
help_msg = '\n'.join(introduction)

# write defaults.
for key in defaults:
    conf[key]['default'] = defaults[key]
root = tk.Tk()
Loader(master=root, conf=conf, execution=parse_and_crop, title="PDF/PPT自动裁边", help_msg=help_msg)


print(help_msg)
root.mainloop()