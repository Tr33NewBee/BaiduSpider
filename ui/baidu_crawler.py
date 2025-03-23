"""
百度搜索爬虫-提取信息ui
"""
from PyQt5.QtCore import  QThread,QObject,pyqtSignal

from baiduspider.plugins.baidu import BaiduInfoCrawler


class QtBaiduWorker(QObject):

    finished = pyqtSignal()
    progress = pyqtSignal(int)
    logcat = pyqtSignal(str)
    transaction =pyqtSignal(list)

    def __int__(self):
        super.__init__()
        self._search_keywords = []
        self.cookie = None
        self.crawler = BaiduInfoCrawler()

    def update_cookie(self,_cookie:str):
        self.cookie = _cookie
    def add(self,items:list):
        self._search_keywords.extend(items)

    def run(self):
        count  = 0
        for item in self._search_keywords:
            result = self.crawler.search_news(item,self.cookie)
            if len(result) == 0 or self.crawler.need_update_cookie:
                self.logcat.emit("need update cookie")
                break
            self.transaction.emit(result)
            count += 1
            self.progress.emit(count)
        self.finished.emit()



