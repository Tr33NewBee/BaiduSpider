import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QTextEdit, QLabel, QFileDialog, QGroupBox, QProgressDialog)
from PyQt5.QtCore import QTimer, QDateTime, Qt, QThread
from openpyxl.reader.excel import load_workbook
from baiduspider.plugins.baidu import BaiduInfoCrawler
from ui.baidu_crawler import QtBaiduWorker
import pandas as pd


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.search_list = []
        self.init_ui()
        self.setWindowTitle("数据工具 v1.0")
        self.setGeometry(100, 100, 800, 600)
        # 初始化进度对话框
        self.progress_dialog = None
        self.is_processing = False
        self.current_progress = 0
        self.current_item = 0
        self.total_items =0
        self.need_update_cookie = False
        self.crawled_items = set()
        self.result = []
        self.qthread = QThread()
        # 工作现成
        self.baidu_crawler = QtBaiduWorker()

    def init_ui(self):
        # 创建主部件和布局
        main_widget = QWidget()
        main_layout = QVBoxLayout()

        # 上半部分功能区
        top_group = QGroupBox("操作区域")
        top_layout = QHBoxLayout()

        # 导入按钮组
        import_layout = QVBoxLayout()
        self.btn_import_template = QPushButton("导入模板")
        self.btn_import_cookie = QPushButton("导入Cookie")
        import_layout.addWidget(self.btn_import_template)
        import_layout.addWidget(self.btn_import_cookie)

        # 操作按钮组
        control_layout = QVBoxLayout()
        self.btn_start = QPushButton("开始")
        self.btn_clear = QPushButton("清空")
        self.btn_stop = QPushButton("停止")
        self.btn_export = QPushButton("导出结果")

        control_layout.addWidget(self.btn_start)
        control_layout.addWidget(self.btn_stop)
        control_layout.addWidget(self.btn_export)
        control_layout.addWidget(self.btn_clear)

        # 将布局添加到顶部区域
        top_layout.addLayout(import_layout)
        top_layout.addStretch(1)
        top_layout.addLayout(control_layout)
        top_group.setLayout(top_layout)

        # 下半部分日志区域
        bottom_group = QGroupBox("日志信息")
        bottom_layout = QVBoxLayout()

        self.log_view = QTextEdit()
        self.log_view.setReadOnly(True)
        bottom_layout.addWidget(self.log_view)

        # 状态栏
        status_layout = QHBoxLayout()
        self.lbl_version = QLabel("版本: 1.0.0")
        self.lbl_time = QLabel()
        status_layout.addWidget(self.lbl_version)
        status_layout.addStretch(1)
        status_layout.addWidget(self.lbl_time)

        bottom_layout.addLayout(status_layout)
        bottom_group.setLayout(bottom_layout)

        # 将各部分添加到主布局
        main_layout.addWidget(top_group)
        main_layout.addWidget(bottom_group)
        main_widget.setLayout(main_layout)

        self.setCentralWidget(main_widget)

        # 连接信号槽
        self.btn_import_template.clicked.connect(self.import_template)
        self.btn_import_cookie.clicked.connect(self.import_cookie)
        self.btn_start.clicked.connect(self.start_process)
        self.btn_stop.clicked.connect(self.stop_process)
        self.btn_export.clicked.connect(self.export_result)
        self.btn_clear.clicked.connect(self.clear_result)

        # 初始化定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.update_time()

        #处理输入模板和cookie以及导出结果
        self.search_sources = set()
        #
        self.cookie = None
        #
        self.result = []


    def clear_result(self):
        self.search_sources.clear()
        self.crawled_items.clear()
        self.log_view.clear()
        self.log("请重新导入搜索模板...")


    def import_template(self):
        # 选择导入模板文件，支持这三个文件
        # file_path, _ = QFileDialog.getOpenFileName(self, "选择模板文件", "", "Excel文件 (*.txt *.xlsx *.xls)")
        file_path, _ = QFileDialog.getOpenFileName(self, "选择模板文件", "", "Excel文件 (*.xlsx *.xls)") # 不要支持txt格式，懒得解析
        if file_path:
            self.log(f"模板文件已导入: {file_path}")
            # if file_path.endswith(".txt"):
            #     with open(file_path, "r", encoding="utf-8") as fread:
            #         first_line = fread.readline()
            #         if "TEMPLATE" not in first_line:
            #             self.log("不是合法的template文件")
            #             return
            #         tag = ""
            #         for l in fread:
            #             line = l.strip()
            #             if line.startswith("**"): continue
            #             if line.startswith("#"):
            #                 tag = line.split("#")[1].strip()
            #                 self.search_sources[tag] = []
            #             else:
            #                 self.search_sources[tag].append(
            #                     line.strip()
            #                 )
            #                 self.total_items +=1
            if file_path.endswith(".xlsx") or file_path.endswith(".xls"):
                # 加载Excel文件
                wb = load_workbook(file_path)
                sheet = wb["Sheet1"] #.active  # 获取当前活动的工作表
                # print(sheet.)
                # print("all sheet names ",wb.sheetnames)

                # 遍历所有行（从第1行开始）
                def process_multi(line:str):
                    if " "in line:
                        for l in line.split(" "):
                            yield  l
                    if "/" not in line or "/" not in line: yield line
                    # 英文输入发
                    a = line.split("/")
                    b = line.split("/")
                    a.extend(b)
                    for l in a: #
                        # print("return l = ",l)
                        yield l
                # print("sheet rows ",sheet.max_row)
                for row in sheet.iter_rows(values_only=True,min_row=1):
                    # print(row)
                    tag,company,keyword= row
                    if tag == "数据类型":continue
                    if keyword is None or tag is None or company is None:continue
                    # if tag not in self.search_sources:
                    #     self.search_sources[tag] = []
                    # 保存格式就是tag + company格式
                    print("==>  line: ", row)
                    for newkeyword in process_multi(keyword):
                        sk = tag+" "+ company +" "+newkeyword
                        self.search_sources.add(
                            #保存格式就是这个 tag company newkeyword  我们直接解析出来
                          sk
                        )
                        # print(f"loaded sk {sk}")
                        # self.total_items += 1
                # 读取特定单元格的值
                # cell_value = sheet["A1"].value
                # print(cell_value)

            self.total_items = len(self.search_sources)
            if len(self.search_sources) ==0:
                self.log("加载搜索信息失败，请检查模板文件是否正确")
            else:
                self.log(f"模板解析完成，已经加载  {self.total_items} 条")

    def import_cookie(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择Cookie文件", "", "所有文件 (*.txt)")
        if file_path:
            self.log(f"Cookie文件已导入: {file_path}")
            with open(file_path,"r",encoding="utf-8") as fread:
                first_line = fread.readline()
                #self.log(f"first_line cookie {first_line}")
                if "COOKIE" not in first_line:
                    self.log("不是合法的cookie文件")
                    return
                for l in fread:
                    if l.startswith("**"):continue
                    if "Cookie=" in l.strip():
                        self.cookie = l.strip().split("Cookie=")[1].strip()
            if self.cookie is None:
                self.log("加载cookie失败")
            else:
                self.log(f"加载更新cookie完成")

    def start_process(self):
        if  self.need_update_cookie:
            self.log("请更新cookie才能继续更新数据")
            return
        if self.cookie is None or self.cookie == "":
            self.log("Cookie不可用")
            return
        elif len(self.search_sources) ==0:
            self.log("没用可用的搜索关键信息")
            return
        # 这里可以添加实际的处理逻辑
        if not self.is_processing:
            self.is_processing = True
            self.current_progress = 0
            # 创建进度对话框
            self.progress_dialog = QProgressDialog(
                "正在处理数据...",
                "取消",
                0,100,
                self
            )
            # self.progress_dialog.setRange( 0, self.total_items)
            # 添加样式
            self.progress_dialog.setStyleSheet("""
                QProgressBar {
                    border: 2px solid grey;
                    border-radius: 5px;
                    text-align: center;
                }
                QProgressBar::chunk {
                    background-color: #5BC0DE;
                    width: 10px;
                }
            """)
            #
            self.progress_dialog.setWindowTitle("处理中")
            self.progress_dialog.setWindowModality(Qt.WindowModal)
            self.progress_dialog.canceled.connect(self.cancel_process)

            # 设置对话框不可自动关闭
            self.progress_dialog.setAutoClose(False)
            self.progress_dialog.show()

            self.search_list = list(self.search_sources)

            # self.search_all_keywords =keyword

            #todo 需要更新这部分为异步操作，否则就是主线程在运行。效率太慢
            self.crawler  = BaiduInfoCrawler()
            if len(self.search_list) ==0:
                self.log("没有可用的关键词搜索")
                return

            # self.baidu_crawler.finished.connect(self.process_complete)
            # self.baidu_crawler.progress.connect(self.)
            # 启动模拟处理
            # self.qthread.started.connect(self.simulate_processing)
            self.simulate_processing()
            self.log("开始处理数据...")


    def stop_process(self):
        self.is_processing = False
        self.log("处理已停止")



    def simulate_processing(self):
        # 模拟处理进度
        if self.current_progress < self.total_items and self.is_processing:
            # 已经运行过的，可以跳过
            item = self.search_list[self.current_progress]
            if item in self.crawled_items:
                self.current_progress += 1
                return
            self.crawled_items.add(item)
            # 更新进度
            progress_value = int((self.current_progress / self.total_items) * 100)
            # 更新对话框显示
            self.progress_dialog.setValue(progress_value)
            self.progress_dialog.setLabelText(
                f"正在处理第 {self.current_progress}/{self.total_items} 条 ({progress_value}%)"
            )
            self.current_progress += 1
            search_item = " ".join(item.split(" ")[1:])

            # print(f"Search_item = {search_item}")
            data = self.crawler.search_news(search_item,self.cookie)
            self.log(f"正在处理搜索关键词：[{item}] 提取到{len(data)} 条")
            if self.crawler.need_update_cookie:
                self.is_processing=True
                self.log("请更新cookie，当前不能继续搜索。")
                self.need_update_cookie = True
                return
            # # 模拟处理延迟
            # 这里有一个需要标记的是
            self.result.extend(data)
            for news in data:
                # print(f"=> {news}")
                title = news['title']
                source =news['source']
                sitename = source['sitename']
                source_url = source['url']
                last_modified_time = news['last_modified']
                newTimeFactorStr = news['newTimeFactorStr']
                contentText = news['contentText']
                # news['search_keyword'] = newTimeFactorStr

                news['export_data'] = {
                    "搜索关键词":item,
                    "文章标题":title,
                    "文章来源":sitename,
                    "文章链接":source_url,
                    "发布时间":newTimeFactorStr,
                    "文章摘要":news['contentText']
                    # "更新时间":last_modified_time,


                }

                fmt_date = self.crawler.parse_date(newTimeFactorStr)
                print(f"解释时间格式: {newTimeFactorStr} => ",fmt_date)
                if fmt_date is not None:
                    news['export_data']['发布时间'] = fmt_date.strftime("%Y年%m月%d日")

                info =f"提取关键词成功 关键词: {item} 文章标题: {title} 文章来源: {sitename} 文章摘要:{contentText}  文章链接: {source_url} 发布时间: {newTimeFactorStr} 更新时间: {last_modified_time}"
                # print(info)
                self.log(info)

            QTimer.singleShot(50, self.simulate_processing)  # 每50ms增加1%

        else:
            self.process_complete()
        #

    def cancel_process(self):
        if self.is_processing:
            self.is_processing = False
            self.log("用户取消了处理过程")
            self.progress_dialog.close()

    def process_complete(self):
        if self.is_processing:
            self.is_processing = False
            self.progress_dialog.close()
            # 失败:{self.total_items - len(self.result)}
            self.log(f"数据处理完成 成功:{len(self.result)} ")
            print(self.result)

    def export_result(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "导出结果", "", "Excel文件 (*.xlsx)")
        if file_path:
            header= []
            export_datas =[]
            for item in self.result:
                export_data = item['export_data']
                if len(header) == 0:
                    header.extend(list(export_data.keys()))
                export_datas.append(export_data)

            df = pd.DataFrame(export_datas,columns=header)
            df.to_excel(file_path,index=False,engine="openpyxl")
            self.log(f"结果已导出到: {file_path}")

    def log(self, message):
        timestamp = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
        self.log_view.append(f"[{timestamp}] {message}")

    def update_time(self):
        current_time = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
        self.lbl_time.setText(f"当前时间: {current_time}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())