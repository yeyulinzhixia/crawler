# Pixiv图片自动下载脚本

## 功能：获取收藏的图片和热门图片

- 首次使用将通过selenium获取cookie信息，settings.py中设置图片存储的文件夹
- 以后使用可以注释掉bookmark.py中的`self.get_cookie()`