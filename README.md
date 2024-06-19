# HTMLwallpaper
一个纯粹的网页壁纸软件，使用chatGPT生成，未做任何优化，支持本地网页文件和网址，暂不支持键鼠互动，占用系统资源大小取决于你想要加载的网页网站的优化程度

# 打包 需要自己做个图标命名为icon.png放到同一目录
pyinstaller --onefile --windowed --add-data "icon.png;." wallpaper_app.py

# bug
目前在托盘点击url加载后，如果不输入网址直接取消会导致程序退出，希望有能力的大佬解决这个问题
