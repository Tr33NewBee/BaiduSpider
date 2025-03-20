import json
import os.path
import traceback
import unittest

from bs4 import BeautifulSoup, Comment
from baiduspider import  BaiduSpider


import  time
class MyTestCase(unittest.TestCase):
    def test_a(self):
        s = self.fmt_time("1742275803")
        print(s)
    def fmt_time(self,ts):
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
        return  formatted_date
    def test_something(self):


        cookie = 'BIDUPSID=71684156CDE79CD28848A9CC2F52442A; PSTM=1711613513; BAIDUID=221A0DE8C25E59EEA12121CD0864BA60:FG=1; H_WISE_SIDS_BFESS=60273_60520_60359_60629_60665_60677_60681; MCITY=-%3A; BD_UPN=123253; BAIDUID_BFESS=221A0DE8C25E59EEA12121CD0864BA60:FG=1; shifen[1000971712123_93325]=1742174140; BCLID=10914472285453631277; BCLID_BFESS=10914472285453631277; BDSFRCVID=WfFOJeC62Gg4OTnJcpgkJFkZ7HxHXJ5TH6q2i9KV6F9S4KmeUp69EG0P9M8g0KAhKEqsogKK3gOTH4PF_2uxOjjg8UtVJeC6EG0Ptf8g0x5; BDSFRCVID_BFESS=WfFOJeC62Gg4OTnJcpgkJFkZ7HxHXJ5TH6q2i9KV6F9S4KmeUp69EG0P9M8g0KAhKEqsogKK3gOTH4PF_2uxOjjg8UtVJeC6EG0Ptf8g0x5; H_BDCLCKID_SF=JRkJ_I_atK83fP36qRbEbtu8hl-LhI62aKDX3buQQbQP8pcNLTDKQPb3XnOXBtJj5K3ZKJvuJhnWOMn_jqO1jRoXMHriLj5lfGAJab6HQ4t-bq5jDh0BXjksD-RCaUn4-67y0hvctb3cShPm0MjrDRLbXU6BK5vPbNcZ0l8K3l02V-bIe-t225Qh-p52f6_qJR4J3q; H_BDCLCKID_SF_BFESS=JRkJ_I_atK83fP36qRbEbtu8hl-LhI62aKDX3buQQbQP8pcNLTDKQPb3XnOXBtJj5K3ZKJvuJhnWOMn_jqO1jRoXMHriLj5lfGAJab6HQ4t-bq5jDh0BXjksD-RCaUn4-67y0hvctb3cShPm0MjrDRLbXU6BK5vPbNcZ0l8K3l02V-bIe-t225Qh-p52f6_qJR4J3q; BDRCVFR[C0p6oIjvx-c]=I67x6TjHwwYf0; delPer=0; BD_CK_SAM=1; PSINO=6; H_PS_PSSID=60273_61027_62227_62242_62325_62336_62346_62370_62421_62422_62426_62476_62482_62484_62499_62517_62456_62455_62452_62451_62557_62618_62639; BD_HOME=1; BA_HECTOR=0524al0k8ka420ag808g2k248lc7qq1jtlalr22; ZFY=Jpj1HQ58g:AF2zs5WHwIxz6zruyd35NvPC:AWCqZDy2lY:C; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; Hm_lvt_aec699bb6442ba076c8981c6dc490771=1742384582; Hm_lpvt_aec699bb6442ba076c8981c6dc490771=1742384582; HMACCOUNT=82C547EB36B7ED44; H_WISE_SIDS=60273_61027_62227_62242_62325_62336_62346_62370_62421_62422_62426_62476_62482_62484_62499_62517_62456_62455_62452_62451_62557_62618_62639; ppfuid=FOCoIC3q5fKa8fgJnwzbE0LGziLN3VHbX8wfShDP6RCsfXQp/69CStRUAcn/QmhIlFDxPrAc/s5tJmCocrihdwitHd04Lvs3Nfz26Zt2holplnIKVacidp8Sue4dMTyfg65BJnOFhn1HthtSiwtygiD7piS4vjG/W9dLb1VAdqO71sNtrfJH2UrRokTvezUwO0V6uxgO+hV7+7wZFfXG0MSpuMmh7GsZ4C7fF/kTgmvlMIA/tB2qdnJ8KkulgesR5YKU+qTqtaaBkWIZO5dn/GldC1S4QUhUhpm5KMoOoF81v2iwj13daM+9aWJ5GJCQu/SUbF5jV5AUyz/jBiIgKVObaDCHgWJZH3ZrTGYHmi7XJB9z3y2o8Kqxep5XBCsugNOW5C73e/g54kuY4PKIS71ZI76Ek4aqBDEnUMj+O8679rCuwgzS80wwjQEaGzjcnvNXIEW2pwj4BXINSNFrPHuvVnM4vTcb6V/jfwuIbTeIGhYqrYfhHGZqJNx2uWmglAIQEZY21OyYDgpfKN3zxRn6ONqHK83MkBENWBMWSAwea/+1VSNUTGfIG+NKu2s+g28sOzjnLUnUE9KukMAMTPZYfT79sbFYuntY0Ry6GX3OsRAJVdXPXKlPRQiighN2h3utZNfUsAGL2WWa3tubT9td9rGfOenGkLOGCRladXTg1IKPDQ9z3/DiqHtAIbmyu3emEg6nEYu6lQuvYr6/UJpAq7e+CnVRC2DzwICP6cu9A5mNm34ZPuoRV+zY3Fkh61Pk+8I5Srcy4myorv2+gUY9tDUBkEj/ophtFzQm10zPa4KQkP1OpJXL7SOj9mXVdRGSluqM4FuAgHCvdnqfGnnbe3vsHq3LuF7pombT65cVprejPaivGVaWugm+VA1kVl5OE/aBXOg67P9UlCyJKVyutwgoMp5Aa/ZkjblrEvPdXZFhAgvw25kAwV0TwSXSkTCwPr2BOulFwE9QqeU6hK8/4gXL7D1yhOWYXNZvRaSNIhIuBVe4+Jop0oczpupZGEQw3OLo5dsSUeQDd6vDni1evF/M7yvmL+FUAwPmWZFbvNq69O2z3wBW+ogxJUDy9IDhObhno4D7MBZG4B+pNlhGWn0jikQ5zzmAASlnix3V2XtmwNAzvtRZUfKm/j5ohXGVaLqOQwr5UIY0Yb6SLY1Idv8jX8h4522dQP4UUSOwRVQ7btSmic48edZ0zdfs3/Nuh02ISWqx07kkZMfmdnyOb+SUndpETWRO7Om0KwOcjCN9Un1A4MQ67HepT7VF; RT="z=1&dm=baidu.com&si=dae9089f-4fa0-4814-9342-86e00f3c378c&ss=m8fvfdr7&sl=1&tt=2l1&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=3dl"; baikeVisitId=d341b35c-1a1c-4352-b303-ca41dd127ff8; COOKIE_SESSION=38_0_8_9_1_24_0_0_8_8_0_4_0_0_0_0_1742384734_0_1742386880%7C9%23757_3_1742384608%7C2; H_PS_645EC=2cdaGaYVlktSJmlyDw0rL3X1M6%2FbmuAdOx1%2Fj950Vzfjx0KnsTdf%2FRHvbpo'
            #"BIDUPSID=71684156CDE79CD28848A9CC2F52442A; PSTM=1711613513; BAIDUID=221A0DE8C25E59EEA12121CD0864BA60:FG=1; H_WISE_SIDS_BFESS=60273_60520_60359_60629_60665_60677_60681; MCITY=-%3A; BD_UPN=123253; BAIDUID_BFESS=221A0DE8C25E59EEA12121CD0864BA60:FG=1; BD_HOME=1; BD_CK_SAM=1; PSINO=6; delPer=0; H_WISE_SIDS=60273_61027_62227_62242_62325_62336_62346_62329_62370_62421_62422_62426_62476_62482_62484_62499_62493_62517; H_PS_PSSID=60273_61027_62227_62242_62325_62336_62346_62329_62370_62421_62422_62426_62476_62482_62484_62499_62493_62517; BA_HECTOR=85818l802l0121ak8k0la0802h2ss21jt4dra23; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; COOKIE_SESSION=13_0_6_7_2_11_0_0_5_7_2_2_0_0_0_0_1716997748_0_1741830066%7C9%230_0_1741830066%7C1; ZFY=TaH0tiqj0MTEP6Y09fZ:Ajd3N4bKZZHPQHc0zPBuiYrY:C; BDRCVFR[C0p6oIjvx-c]=I67x6TjHwwYf0; arialoadData=false; BDRCVFR[gUg2cUtcsBT]=_M5urk4djP3fA4-ILn; H_PS_645EC=e47fEMn1gxjZX0Nli3ULFCMmNnb3EuCBKZpLovVesHGtf3k6iUMbSrD%2BWBawgQEnzGt9xDa%2B7N3vDG56"

        # 实例化BaiduSpider
        debug_file= "c.html"
        query_time = "week"
        page_n = 1
        query_word='宁德时代 储能'
        spider = BaiduSpider(cookie =cookie,debug_file=debug_file)
        # 搜索网页
        # spider.search_web(query=query_word, time=query_time, pn=page_n)
        if not os.path.isfile(debug_file):
            raise  Exception("Can't scrawl content")

        soup = BeautifulSoup(open(debug_file, "r").read(), "html.parser")
        news = soup.find_all(
            text=lambda t: isinstance(t, Comment))  # "h3",class_ ="c-title t t tts-title")#"cr-content new-pmd")
        for new in news:
            if not new.startswith("s-data"): continue
            try:
                # print(new)
                content = json.loads(new.split("s-data:")[1])
                tplData = content.get("tplData", {})
                last_modified = tplData.get('LastModTime', 0)
                if str(last_modified) =="0":continue
                title = content['title']
                title_url = content['titleUrl']
                source = content['source']
                contentText = content['contentText']
                newTimeFactorStr = content['newTimeFactorStr']

                ttsInfo = content.get("ttsInfo",{})
                # 调试使用
                # for k, v in content.items():
                #     # if k == "tplData":continue
                #     print(k + " ", v)

                first_info  = ttsInfo.get("0",{})
                first_info_ttsSourceType = first_info.get("ttsSourceType","unknow")
                first_info_titleUrl = first_info.get("titleUrl","unknow")



                st = self.fmt_time(last_modified)
                print("[+] title: ",title)
                print("[+] title_url: ",title_url)
                print("[+] source: ",source)
                print("[+] contentText: ",contentText)
                print("[+] newTimeFactorStr: ",newTimeFactorStr)
                print("[+] first_info_ttsSourceType: ",first_info_ttsSourceType)
                print("[+] first_info_titleUrl: ",first_info_titleUrl)
                print("[+] last_modified: ",last_modified ," st: "+st )
                print("==" * 20)
            except Exception as e:
                print("parse failed. skip it.",e)
                traceback.print_exc()
                pass



if __name__ == '__main__':
    unittest.main()
