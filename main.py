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

from ui import Loader
conf = {
        "input": {"name": "源文件", "type": "readfile", "extension": ("PDF & PPT", ".pdf .pptx")},
        "output": {"name": "保存路径", "type": "savefile"},
        "background_color": {"name": "背景颜色", "type": "color", "default": "255,255,255"},
        "border": {"name": "留白", "type": "str", "default": "0.0"},
        "zoom": {"name": "缩放等级", "type": "str", "default": "1.0"},
        "thresh": {"name": "阈值", "type": "str", "default": "1.0"},
        "split": {"name": "拆分", "type": "str", "default": "true"},
        "names": {"name": "页名称", "type": "str"},
        "visual": {"name": "显示裁切框", "type": "str", "default": "false"},
        "mute": {"name": "显示保存文件", "type": "str", "default": "false"},
    }
root = tk.Tk()
Loader(master=root, conf=conf, execution=parse_and_crop, title="PDF/PPT自动裁边")
root.mainloop()