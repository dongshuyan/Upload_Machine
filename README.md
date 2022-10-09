## Upload_Machine

自动将本地资源发布到PT站
Upload local resources to PT trackers automatically.

## 特色

- 最适合发布追更资源，可以自动识别资源集数
- 支持Windows，Linux，Macos系统
- 自由度高，智能识别能力强

## 最佳适用场景
  
发布追更类资源，脚本可以自动判断资源的集数信息。  
初次配置好资源信息后，每次只需要将新的一集放入资源文件夹中，脚本会自动找到未发布的资源并一条龙发布。  

## Upload_Machine与Auto_Upload的区别：

Upload_Machine全部使用requests发请求来发种，所以：

- 无需安装Chrome浏览器以及相关插件
- 无需原来的Json格式的cookie文件改为在配置文件 `au.yaml`中填写F12获取的cookie
- 更轻量，更快速，更少出错的可能
- 但是无法浏览模拟发种过程
- 无法在发种前暂停自行修改信息

## 更新说明

- 20221010 修复imdb链接只记录了id的bug
- 20221008 豆瓣简介的获取改使用doubaninfo的接口
- 20221008 增加对hdpt,carpt,hdfans,hares和wintersakura的支持
- 20221007 增加对pter，hhclub和LemonHD的支持
- 20221006 增加对audience和ssd的支持
- 20221006 增加对hdsky的支持

## 功能说明

### 1.命令行实现将本地图片上传到图床

### 2.命令行实现抓取豆瓣信息

### 3.命令行实现获取本地视频截图链接

### 4.自动检测本地未发布的资源并发布到各个站点，并下载到Qbittorrent进行辅种

全平台支持了以下功能:

- 根据配置文件分析待发布资源的中英文名
- 根据配置文件分析已经发布的资源并自动找到未发布的资源
- 可选是否在资源外层套一个0day名字的文件夹
- 大量参数可以自动抓取也可以自己配置，包括且不限于 视频格式，音频格式，字幕信息，音轨信息等
- 将未发布的资源有序发布
- 自动获取待发布资源的豆瓣链接/动漫资源的bgm链接
- 自动获取待发布资源的豆瓣简介
- 自动获取待发布资源的截图并上传到图床获取bbcode
- 自动获取待发布资源的mediainfo信息
- 自动制作种子
- 根据上述信息自动发布到各个站点（分集发布/打包发布）
- 自动获取下载链接并传递给Qbittorrent自动做种
- 自动记录发布资源信息生成excel表格(csv文件)
- 自动统计目前已发布的总量(可以用来统计每月发种数量)

目前支持的平台:

- MacOS
- Windows
- Linux

目前支持的资源类型:

- 动漫
- 剧集
- 电影

目前支持的站点(排名仅代表支持的时间先后):

- piggo (猪猪网)
- hdsky (天空)
- ssd
- audience (观众)
- pter (猫站)
- hhclub (憨憨)
- lemonhd (柠檬)
- hdpt (明教)
- wintersakura (冬樱)
- carpt (车站)
- hdfans (红豆饭)
- hare (白兔)

正在适配的站点(排名不分先后):

- MT

Todolist:

- GUI（有考虑，需要学）
- 自定义站点（需要考虑做不做和怎么做）

如果有新的站点/资源类型等需求,可以加入QQ群交流(735803201)

## 安装Upload_Machine自动发种机

`Upload_Machine自动发种机`可以在任何具有 `Python`环境的系统上使用，下面讲解下在各个系统上的安装步骤

### Windows(已测试成功)

1.需要本地安装Chrome且升级到最新正式版本

2.安装python3:
[安装Python](https://www.python.org/downloads/)，一般选择最新版本的Python3及对应的Windows installer即可。安装时注意将为所有用户安装和将Python添加到PATH勾上
![安装python1](https://img.picgo.net/2022/08/07/1.png)

打开PowerShell(不是cmd)，确认Python安装成功  
![打开PowerShell](https://fapping.empornium.sx/images/2022/10/08/IMG7874.png)

![安装python2](https://img.picgo.net/2022/08/07/2.png)

以下几个插件的安装包可以去通过下面官方途径下载，也可以前往[Install文件夹](https://github.com/dongshuyan/Auto_Upload/blob/master/install)获取 或者 前往交流群的群文件获取。3.安装 `ffmpeg`，并确认安装正确:

- 下载安装 `ffmpeg` & `ffprobe`：https://github.com/BtbN/FFmpeg-Builds/releases
- 将解压后的 `ffmpeg`文件夹移动到一个相对稳定的文件夹,比如 `D:\Program Files\`
- 将上一步 `ffmpeg\bin`文件夹路径添加到系统PATH我的电脑【右击】 -> 选择 属性 -> 高级系统设置 -> 高级 -> 环境变量  -> 系统变量里面找到'Path',点击编辑 -> 新建 -> 将上一步 `ffmpeg\bin`文件夹路径路径粘贴进去 -> 确定 --> 确定 … 保存即可。一般也是 不需要重启
- 在PowerShell确认ffmpeg和ffprobe安装成功

4.安装 `mktorrent`，并确认安装正确:

- 根据自己电脑下载[64位安装包](https://github.com/q3aql/mktorrent-win/releases/download/v1.1-2/mktorrent-1.1-win-64bit-build2.7z)或者[32位安装包](https://github.com/q3aql/mktorrent-win/releases/download/v1.1-2/mktorrent-1.1-win-32bit-build2.7z)
- 使用[7-zip](http://www.7-zip.org/) or [Winrar](http://www.rarlab.com/)解压文件.
- 将 `mktorrent`文件夹移动到一个相对稳定的文件夹,比如 `D:\Program Files\`
- 将上一步 `mktorrent\bin`文件夹路径添加到系统PATH
  我的电脑【右击】 -> 选择 属性 -> 高级系统设置 -> 高级 -> 环境变量  -> 系统变量里面找到'Path',点击编辑 -> 新建 -> 将上一步 `mktorrent\bin`文件夹路径路径粘贴进去 -> 确定 --> 确定 … 保存即可。一般也是 不需要重启

5.安装 `mediainfo`，并确认安装正确

- 下载[mediainfo-cli](https://mediaarea.net/download/binary/mediainfo/22.06/MediaInfo_CLI_22.06_Windows_x64.zip)：https://mediaarea.net/en/MediaInfo/Download/Windows
- 解压zip文件并解压后的 `Mediainfo_CLIxxx`文件夹移动到一个相对稳定的位置
- 将上一步 `Mediainfo_CLIxxx`文件夹路径添加到系统PATH我的电脑【右击】 -> 选择 属性 -> 高级系统设置 -> 高级 -> 环境变量  -> 系统变量里面找到'Path',点击编辑 -> 新建 -> 将上一步 `Mediainfo_CLIxxx`文件夹路径粘贴进去 -> 确定 --> 确定 … 保存即可。一般也是 不需要重启。
- 在PowerShell确认 `mediainfo`安装成功

```bash
mediainfo -h
```

6.安装 `Upload_Machine`，在以管理员身份打开 `Windows PowerShell`中输入:

```bash
python3 -m pip install upload_machine  -i https://pypi.tuna.tsinghua.edu.cn/simple/
upload_machine -h
```

如果上述命令没反应或者报错可以尝试下面这个：

```bash
pip install upload_machine  -i https://pypi.tuna.tsinghua.edu.cn/simple/
upload_machine -h
```

7.更新 `Upload_Machine`，在 `Windows PowerShell`中输入:

```bash
python3 -m pip install --upgrade upload_machine  -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

如果上述命令没反应或者报错可以尝试下面这个：

```bash
pip install --upgrade upload_machine  -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

### Linux

0.升级 `python`至 `3.7.0`版本以上，建议 `3.9.0`
如果有 `_ssl`或者 `_ctypes`找不到，也可以试试按照下面步骤重新安装python3

```bash
# 我也使用的wget ,我下载到了Download中
wget https://www.python.org/ftp/python/3.9.0/Python-3.9.0.tgz
# 在home中解压
tar -zxf Python-3.9.0.tgz
# 进入python3.9
cd Python-3.9.0
 
# 编译文件  时间大概有1-3分钟
./configure --prefix=/usr/local/python3
 
# 编译好后，会有另外一个提示，让run ./configure xxx
./configure --enable-optimizations

# 给超级权限
sudo su

# 安装
make && make install

#退出超级权限
exit
 
# 结束
```

1.安装 `mktorrent`,`ffmpeg`和 `mediainfo`，并确认安装正确

```bash
sudo apt update 
sudo python3 -m pip install --upgrade pip
sudo apt-get install python3-pip ffmpeg mediainfo mktorrent
```

3.安装 `Upload_Machine`

```bash
python3 -m pip install upload_machine -i https://pypi.tuna.tsinghua.edu.cn/simple/
upload_machine -h
```

如果上述命令没反应或者报错可以尝试下面这个：

```bash
pip install upload_machine -i https://pypi.tuna.tsinghua.edu.cn/simple/
upload_machine -h
```

4.更新 `Upload_Machine`，，在 `Terminal.app`中输入:

```bash
python3 -m pip install --upgrade upload_machine -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

如果上述命令没反应或者报错可以尝试下面这个：

```bash
pip install --upgrade upload_machine -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

### MacOS(已测试成功)

1.安装 `Homebrew`，在Termial.app中输入:

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

2.安装 `mktorrent`,`ffmpeg`和 `mediainfo`，并确认安装正确:

```bash
brew install ffmpeg mediainfo mktorrent
ffmpeg -version
mediainfo --version
```

3.安装 `Upload_Machine`，在 `Terminal.app`中输入:

```bash
python3 -m pip install upload_machine -i https://pypi.tuna.tsinghua.edu.cn/simple/
upload_machine -h
```

如果上述命令没反应或者报错可以尝试下面这个：

```bash
pip install upload_machine -i https://pypi.tuna.tsinghua.edu.cn/simple/
upload_machine -h
```

5.更新 `Upload_Machine`，，在 `Terminal.app`中输入:

```bash
python3 -m pip install --upgrade upload_machine -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

如果上述命令没反应或者报错可以尝试下面这个：

```bash
pip install --upgrade upload_machine -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

## 配置环境&文件

### 1.本地新建一个工作目录

例如路径为:/Users/Desktop/upload_machine

### 2.在1中工作路径文件夹下，再新建两个文件夹

"screenshot_path","record_path"

- screenshot_path将用来存放视频截图，种子等临时文件
- record_path将用来存放发种记录

### 3.在文件夹中新建配置文件au.yaml
因为yaml文件有很严格的格式要求，所以建议使用sublime,vscode等编辑器进行编辑。如果使用记事本不要破坏原有格式。

详细参数说明参考[au_example.yaml](https://github.com/dongshuyan/Upload_Machine/blob/master/au_example.yaml)


建立完成后在工作目录下应该有两个文件夹以及一个au.yaml配置文件.

### 4.获取 `au.yaml`文件里面所需的站点cookie

根据下图所示方法获取cookie，并填写在 `au.yaml`配置文件中 `site info`中 `站点`中 `cookie`中。

```yaml
site info: #配置站点信息
  pter: #配置站点，目前支持的关键词有[pter,lemonhd,audience,carpt,hdsky,piggo,ssd,hdpt,ptnap,wintersakura,hdfans,hhclub]
    enable: 1 #是否开启此站点自动发种 1为开启，0为关闭
    uplver: 1 #是否开启匿名发种，1为开启，0为关闭
    cookie: 获取到的cookie #从网页F12获取的cookie
```

![获取cookie](https://ptpimg.me/mtb58j.png)

## 运行脚本

### 1.自动发种

```bash
upload_machine -yp '工作目录/au.yaml' -u
```

注意：在Windows系统发种时需要确保在制作种子期间，被发布的 `文件`或者 `文件夹`没有被其他应用占用。

### 2.本地图片自动上传图床

```bash
upload_machine -yp '工作目录/au.yaml' -iu -ih 图床名称  -iform 图片格式 -if  '图片路径1' '图片路径2'
```

图床名称目前仅支持（排名无先后）：

- ptpimg
- picgo
- chd
- imgbox
- pter
- smms

### 3.获取豆瓣信息

```bash
upload_machine -yp '工作目录/au.yaml' -di -du '豆瓣链接'
```

示例:

```bash
upload_machine -yp '工作目录/au.yaml' -di -du https://movie.douban.com/subject/26353671/
```

### 4.命令行获取本地视频截图链接

```bash
upload_machine -yp '工作目录/au.yaml' -mi -mf '视频路径' -ih 图床名称 -iform 图片格式 -in 截图数量
```

图床名称目前仅支持（排名无先后）：

- ptpimg
- picgo
- chd
- imgbox
- pter
- smms

图片格式(可以不填，默认'img'):

- img 图片原始链接
- bbcode BBcode格式链接

截图数量(可以不填，默认3张)

示例:

```bash
upload_machine 'au.yaml' -mi -mf '1.mp4' -ih picgo -iform bbcode -in 6
```

## 配置文件au.yaml详细说明

参考 [au_example.yaml](https://github.com/dongshuyan/Upload_Machine/blob/master/au_example.yaml)

## 常见错误及修复方法（更新ing）

## 交流群

群号:735803201

## Reference

[Differential 差速器](https://github.com/LeiShi1313/Differential)  (复制了上传图床部分代码)
[Differential差速器使用教程](https://leishi.io/blog/posts/2021-12/Differential/)  (Upload_Machine安装教程主要参考本文)
[mktorrent-win-builds](https://github.com/q3aql/mktorrent-win-builds)
[MKTORRENT WIN下命令行制作种子](https://blog.acesheep.com/index.php/archives/551/)
[linux 安装 Chrome](https://www.cnblogs.com/ivantang/p/6290729.html)
[windows10 环境变量设置](https://blog.csdn.net/palmer_kai/article/details/80588594)
[Linux Ubuntu系统升级Python3版本至Python3.9版本步骤](https://blog.csdn.net/u012080686/article/details/112600252)
[PYTorrent](https://github.com/ndroi/pytorrent)
