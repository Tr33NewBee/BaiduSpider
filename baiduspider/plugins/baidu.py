import json
import os.path
import time
import traceback
from typing import Optional
from _datetime import   datetime, timedelta, date
from zoneinfo import ZoneInfo
import  re
from bs4 import BeautifulSoup, Comment

from baiduspider import BaiduSpider


class BaiduInfoCrawler(object):
    # def test_a(self):
    #     s = self.fmt_time("1742275803")
    #     print(s)


    def __init__(self):
        self.need_update_cookie = False
        self.cookie = None
        self.blacklist=[
            "知了爱学",#站点是人工知智能搜索，需要剔除
            "法行宝",#站点是人工智能询问
            "抖音",#
            "智联招聘",
            "BOSS直聘",
            "企查查",
            "爱企查",
            "职友集",
            "天眼查",
            "猎聘",
            "名录集",
            "爱番番",
            "阿里巴巴1688",
            "1688",
            "京东",
            "淘宝",
            "黄页88",
            "九零姑娘",
            # "西门子官方网站",#这个可以不用去看？




        ]

    def fmt_time(self, ts):
        # timestamp = 1734088217
        try:
            if type(ts) == str:
                ts = int(ts)
        except:
            return ts
        # 转换为本地时间结构体
        time_struct = time.localtime(ts)  # 若需UTC时间，改用gmtime()

        # 格式化为目标字符串
        formatted_date = time.strftime("%Y年%m月%d日", time_struct)
        return formatted_date

    def is_in_current_month(self,timestamp, tz="UTC") -> bool:

        # 这里过滤一下时间
        if isinstance(timestamp,str) and timestamp == "0":return False
        # 转换为指定时区的时间
        current = datetime.now(tz=ZoneInfo(tz))
        try:
            dt = datetime.fromtimestamp(int(timestamp), tz=ZoneInfo(tz))

            # 获取当前时区时间

            # print("parse last_modified year: "+str(dt.year) +" dt.month: "+str(dt.month) +"  current.year:"+str(current.year) +" current_month: "+str(current.month))
            result = (dt.year, dt.month) == (current.year, current.month)
            return result
        except Exception:
            try:
                today = date.today()
                current_year, current_month = today.year, today.month
                target_date =  self.parse_date(timestamp)
                if target_date is None:
                    print(f"[Error]: 解析 timestamp {timestamp} 错误")

                        # return (target_date.year == current_year) and (target_date.month == current_month)
                    return  False
                # print("监测时间是否正确 target_date= ",target_date ," today: ",today)
                return (target_date.year == current_year) and (target_date.month == current_month)
            except Exception as e:


                print("解析时间错误 " + timestamp + " Exception: " + e)
                return False



    def parse_date(self,input_str):
        # 尝试解析为绝对日期（格式：YYYY年MM月DD日）
        input_str = input_str.strip()
        try:
            return datetime.strptime(input_str, "%Y年%m月%d日").date()
        except ValueError as e:
            # print(f"[error: ] {input_str}  error: {e}")
            pass

        # 尝试解析为相对时间（X天前）
        # print("监测输入的时间 ",input_str)
        match = re.match(r'^(\d+)天前$', input_str)
        # print("检查匹配度 ",match)
        if match:
            days_ago = int(match.group(1))
            return date.today() - timedelta(days=days_ago)
        match = re.match(
            r'^(?:(?P<special>前天|昨天)|(?P<days_ago>\d+)天前)(?P<time>\d{1,2}:\d{2})?$',
            input_str
        )
        if match:
            special = match.group("special")
            days_ago_str = match.group("days_ago")
            if special:
                days_ago = 2 if special == "前天" else 1  # 前天=2天前，昨天=1天前
            else:
                days_ago = int(days_ago_str)
            # 获取目标日期

            target_date = date.today() - timedelta(days=days_ago)
            return target_date
            # today = date.today()
            # current_year, current_month = today.year, today.month

        # 可根据需要扩展其他格式，例如X天后
        # 如果无法解析，抛出异常
        # raise ValueError(f"无法识别的日期格式: {input_str}")
        return None
    def check_timestamps(self,timestamps):
        current_year = datetime.now().year
        current_month = datetime.now().month

        # (dt.year, dt.month) == (current_year, current_month)
        return [
            (dt.year, dt.month) == (current_year, current_month)
            for ts in timestamps
            if (dt := datetime.fromtimestamp(ts))  # 海象运算符(Python 3.8+)
        ]
    def __remove_html_tag(self,line:str):
        return line.replace("<em>","").replace("</em>","")


    def __delete_file_exist(self,p):
        if os.path.isfile(p):
            os.remove(p)

    def __parse_render_list(self,render_list:list):
        """
        解析出render_list的内容
        Args:
            render_list:

        Returns: list

        """
        result = []
        for item in render_list:
            # print(item)
            postTimeNew = item.get("postTimeNew","0")
            if self.is_in_current_month(postTimeNew):
                # print("current ",item)
                ttsInfo = item['ttsInfo']
                title = self.__remove_html_tag(item['subTitle'])
                title_url = self.__remove_html_tag(item['subTitleUrl'])
                source = {
                    "sitename":self.__remove_html_tag(item['siteName']),
                    "url":ttsInfo['titleUrl']
                }
                contentText = self.__remove_html_tag(item['subAbs'])
                newTimeFactorStr = self.__remove_html_tag(item['postTimeNew'])
                first_info_ttsSourceType = ttsInfo['titleUrl']

                # first_info_titleUrl 在ttsInfo的ext那
                ext= json.loads( ttsInfo['ext'])

                first_info_titleUrl = ext['title']

                st = item['postTimeNew']
                last_modified =0 # 这里我们不知道，先不管。

                result.append({
                    "title": title,
                    "title_url": title_url,
                    "source": source,
                    "contentText": contentText,
                    "newTimeFactorStr": newTimeFactorStr,
                    "first_info_ttsSourceType": first_info_ttsSourceType,
                    "first_info_titleUrl": first_info_titleUrl,
                    "last_modified": st,
                    "last_modified_timestamp": str(last_modified),
                })
        return result


    def search_news(self, keyword: str, cookie=None,debug=False)->list[Optional[dict]]:
        if cookie == None:
            return []
        if self.cookie is not None:
            # 使用更新的cookie
            cookie = self.cookie
        # 实例化BaiduSpider
        debug_file = "c.html"
        query_time = "week"
        page_n = 1
        # query_word='宁德时代 储能'
        spider = BaiduSpider(cookie=cookie, debug_file=debug_file)
        # 搜索网页
        if not  debug:
            self.__delete_file_exist(debug_file)
            spider.search_web(query=keyword, time=query_time, pn=page_n)
            if not os.path.isfile(debug_file):
                raise Exception("Can't scrawl content")

        # time.sleep(random.uniform(2.5,5.6))
        with open(debug_file, "r",encoding="utf-8") as fp:
            soup = BeautifulSoup(fp.read(), "html.parser")
        news = soup.find_all(
            string=lambda t: isinstance(t, Comment))  # "h3",class_ ="c-title t t tts-title")#"cr-content new-pmd")
        result = []
        for new in news:
            if not new.startswith("s-data"): continue
            try:

                s  = new.split("s-data:")[1].replace("\\-","\\\-").replace("\n","").replace("\t","")
                content = json.loads(s)
                # content = content.replace("\\-","\\\-")
                tplData = content.get("tplData", {})
                last_modified = tplData.get('LastModTime', 0)
                renderList = content.get("renderList",[])
                # print(renderList)
                if len(renderList) >0:
                    # 解析一下renderList的内容，因为其他的不一定有
                    parse_render_list = self.__parse_render_list(renderList)
                    result.extend(parse_render_list)


                if str(last_modified) == "0": continue
                # 下面的tlData的没结果

                title = self.__remove_html_tag(content['title'])
                title_url = content['titleUrl']
                source =  content['source']#self.__remove_html_tag(content['source'])
                contentText = self.__remove_html_tag(content['contentText'])
                newTimeFactorStr =self.__remove_html_tag( content['newTimeFactorStr'])
                if newTimeFactorStr == "" or not self.is_in_current_month(newTimeFactorStr):continue

                ttsInfo = content.get("ttsInfo", {})
                # 调试使用
                # for k, v in content.items():
                #     # if k == "tplData":continue
                #     print(k + " ", v)
                # 这里过滤掉不满足月份的数据
                if  not self.is_in_current_month(last_modified):
                    continue
                # 过滤掉不需要的站点内容
                if source['sitename'] in self.blacklist:
                    continue

                first_info = ttsInfo.get("0", {})
                first_info_ttsSourceType = first_info.get("ttsSourceType", "unknow")
                first_info_titleUrl = first_info.get("titleUrl", "unknow")

                st = self.fmt_time(last_modified)
                if debug:
                    print("[+] title: ", title.replace("<em>","").replace("</em>",""))
                    print("[+] title_url: ", title_url)
                    print("[+] source: ", source)
                    print("[+] contentText: ", contentText)
                    print("[+] newTimeFactorStr: ", newTimeFactorStr)
                    print("[+] first_info_ttsSourceType: ", first_info_ttsSourceType)
                    print("[+] first_info_titleUrl: ", first_info_titleUrl)
                    print("[+] last_modified: ", last_modified, " st: " + st)
                    print("==" * 20)

                result.append({
                    "title":title,
                    "title_url":title_url,
                    "source":source,
                    "contentText":contentText,
                    "newTimeFactorStr":newTimeFactorStr,
                    "first_info_ttsSourceType":first_info_ttsSourceType,
                    "first_info_titleUrl":first_info_titleUrl,
                    "last_modified":st,
                    "last_modified_timestamp":str(last_modified),
                })

            except json.JSONDecodeError as e:
                print(f"parse failed. skip it,line:{new}\nerror:{e}")

            except Exception as e:
                traceback.print_exc()
                self.need_update_cookie = True
        return result
    def reset_cookie(self,cookie:str):
        self.cookie = cookie
#
# if __name__ == '__main__':
#     unittest.main()
