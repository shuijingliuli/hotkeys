# HTMLwallpaper
一个纯粹的网页壁纸软件，使用chatGPT生成，未做任何优化，支持本地网页文件和网址，暂不支持键鼠互动，占用系统资源大小取决于你想要加载的网页网站的优化程度

# 打包 
1.需要自己做个图标命名为icon.png放到同一目录<br />
2.安装所有python依赖<br />
3.打包命令<br />
```
pyinstaller --onefile --windowed --add-data "icon.png;." wallpaper_app.py
```


# bug
目前在托盘点击url加载后，如果不输入网址直接取消会导致程序退出，希望有能力的大佬解决这个问题

# 效果 使用聆风大佬<a href="https://www.leafone.cn/" title="聆风小站">网站</a>上的时钟效果
![image](https://github.com/shuijingliuli/HTMLwallpaper/assets/35411891/c4609974-2e31-49f9-bb1c-da2aa7b37aa0)
