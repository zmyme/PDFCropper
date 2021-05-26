# 选项介绍

- 源文件：输入的文件，可以为PDF或者PPT，如果是PPT，会首先自动调用PowerPoint将给定的PPT转变为PDF然后进行裁剪（PPT裁剪第一次需要调用COM对象因此速度稍慢，建议耐心等待，裁切一次后速度会恢复到正常水平）
- 保存路径：保存的文件名，仅适用于非拆分模式。如果留空，则保存路径为源文件所在目录，保存的文件名为"源文件名_crop.pdf"
- 背景颜色：哪一种颜色会被认为是背景
- 留白：不紧贴有效内容裁切，预留一个给定大小的白边。
- 缩放等级：裁切是基于视觉裁切的，因此裁切过程中会首先渲染PDF，采用默认值即可，更高的缩放会将PDF渲染为更高分辨率的图片从而提高裁剪精度，但计算时间也会相应增加。
- 阈值：像素值差异多少会被认为是前景。
- 拆分：是否将源文件自动拆分为每页一个的单个文件。默认文件名采取下划线+数字命名。如果源文件是PPT且PPT备注不为空，则首先采用PPT的备注作为当前页保存的文件名。
- 页名称：手动指定拆分模式下每一页的名称，具有最高优先级，用逗号分隔。留空则使用默认的文件名或者PPT中备注的文件名。
- 显示裁切框：在右侧的日志区域输出裁切框坐标
- 显示保存文件：显示保存的文件名。

# 代码结构介绍
分为三个文件，main.py提供入口，ui.py为GUI相关工具，cropper.py为裁切内容。裁切采用基于视觉的方式裁切，首先渲染PDF页面，然后通过给定的背景像素值计算每一个像素与背景的差异，当差异大于某一个给定阈值时判断为前景。计算完成后寻找一个最小的外界矩形作为裁切框。PPT转PDF通过win32comtypes库调用powerpoint完成，因此需要你的系统里面安装了powerpoint，PPT备注读取采用python-pptx库，PDF渲染与裁剪采用pymupdf。