# -*- coding: utf-8 -*-
"""
@Time ： 2023/12/8
@Auth ： Schwaze Katze
@File ：CourseSpider2.py
@IDE ：Pycharm(CE)
@Motto：ABC(Always Be Coding)
"""

import json

from selenium.webdriver.common.by import By
from splinter import Browser
from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
import time
import re
import os


def read_cookie():
    with open("cookies.json", "r") as f:
        cookies = json.load(f)  # 将文件字符串转换成python对象
        return cookies


def save_cookie(cookies):
    with open("cookies.json", "w") as f:
        f.write(json.dumps(cookies))  # json.dumps：convert dict into str
        f.close()


class Spider_Dean_Office:
    def __init__(self, driver='edge', driver_dir=None, user_id=None, user_password=None, course=None):
        # System Initiating

        """
        if driver_dir:  # 添加驱动路径
            if driver == 'edge':
                self.driver = './edgedriver/' + driver_dir
            elif driver == 'chrome':
                self.driver = './chromedriver/' + driver_dir
            else:
                self.driver = './' + driver_dir
        else:
            self.driver_dir = './edgedriver/msedgedriver.exe'
        """
        self.current_path = os.path.dirname(os.path.abspath(__file__))
        # Browser Data
        if driver == 'edge':
            local_service = Service(executable_path="./edgedriver/msedgedriver.exe")
            self.browser = Browser(driver_name='edge', service=local_service)
        elif driver == 'chrome':
            # local_service = Service(executable_path=self.driver)  #
            # 参考:https://splinter.readthedocs.io/en/latest/drivers/chrome.html
            self.browser = Browser(driver_name='chrome')
        # Web data
        self.url = "http://jwgl.usst.edu.cn/sso/jziotlogin"
        if user_id and user_password:
            self.user_id = user_id
            self.user_password = user_password
        else:
            self.user_id = ""
            self.user_password = ""
        if course:
            self.courseInfo = course
        else:
            self.courseInfo = []

    def log(self, log, path=None):
        """
        Output the Log.
        :param log: Type of Log
        :param path: Prescribed route
        :return:
        """
        log_dict = {"Success": "目标课程选上成功", "Lesson_Chosen": "检测到目标课程已选上",
                    "Lesson_Repeated": "检测到重复选课行为"}
        if log not in log_dict.keys():
            log_content = "Unknown Operation"
        else:
            log_content = log_dict[log]
        if not path:
            path = self.current_path + r"./operations.log"
        with open(path, "a+") as f:
            f.write(time.strftime('[%Y-%m-%d %H:%M:%S] ') + "Operation: " + log_content + "\n")

    def quit(self):
        time.sleep(5)
        self.browser.quit()

    def visitUrl(self, url=None):
        """
        Enter in the operations.
        :return:
        """
        if url is None:
            default_url = self.url
        else:
            default_url = url
        if self.user_id == '':
            self.getPersonInfo()
        # print("absolute dir without file name", self.current_path)
        # print(self.user_id)
        # print(self.user_password)
        # """
        self.browser.reload()
        self.browser.visit(default_url)
        self.getLogin()
        self.browser.reload()
        self.getCourseSelection()
        # """

        # test
        # self.browser.get("file:///E:/School/%E6%95%99%E5%8A%A1%E5%A4%84%E6%95%B0%E6%8D%AE/jwc4.html")
        self.concurrent_search()

        # if "404" in self.browser.current_url:
        #     self.browser.get()
        # cookies_unlogged = self.browser.get_cookies()
        # print("未登录的Cookies:")  # 此处获取的是登陆前的cookies
        # print(cookies_unlogged)
        # time.sleep(60)  # 需要在60秒内，手动输入账号密码完成登录才会有cookies信息
        # cookies_logged = self.browser.get_cookies()
        # print("登录完成后的Coookies:")  # 此处获取的是登陆后的cookies
        # print(cookies_logged)
        # save_cookie(cookies_logged)  # 保存登录的cookies
        # self.browser.quit()

    def getLogin(self):
        """
        信息门户登录
        :return:
        """
        if self.browser.title == '统一身份认证':
            self.browser.find_by_xpath('//*[@id="username"]').fill(self.user_id)  # input user's ID
            self.browser.find_by_xpath('//*[@id="password"]').fill(self.user_password)  # input password
            time.sleep(1)
            self.browser.find_by_xpath('//*[@id="casLoginForm"]/p[5]/button').first.click()  # press button to login
            time.sleep(1)
        else:
            pass

    def getCourseSelection(self):
        """
        切换至选课页面
        :return:
        """
        """
        self.browser.find_by_css('#cdNav > ul > li:nth-child(3)').click()
        self.browser.find_by_css('#cdNav > ul > li.dropdown.open > ul').click()
        """
        self.browser.find_by_text("选课").click()  # click to select course
        time.sleep(1)
        self.browser.find_by_text("自主选课").click()
        time.sleep(1)
        # switch to the target handle
        window = self.browser.windows[0]
        self.browser.windows.current = window.next  # 切换至下个标签页
        # all_handles = self.browser.window_handles
        # for handle in all_handles:
        #     self.browser.switch_to.window(handle)
        #     if "xsxk" in self.browser.current_url:
        #         break

        # self.browser.find_element(By.LINK_TEXT, ' 自主选课 ').click()  # click to select course
        # js = 'return document.getElementsByClassName("dropdown-menu")[2].click()'
        # self.browser.execute_script(js)

    def getLogin_2(self):
        """
        Deserted Function
        :return:
        """
        self.browser.find_by_xpath('//*[@id="yhm"]').send_keys(self.user_id)  # input user's ID
        self.browser.find_by_xpath('//*[@id="mm"]').send_keys(self.user_password)  # input password
        time.sleep(1)
        if not self.browser.find_by_xpath('//*[@id="agreePolicy"]').is_selected():
            self.browser.find_by_xpath('//*[@id="agreePolicy"]').click()  # agree the policy
        self.browser.find_by_xpath('//*[@id="dl"]').click()  # press button to login
        time.sleep(1)

    def start(self):
        """
        Deserted Function
        :return:
        """
        self.browser.refresh()
        self.browser.get(self.url)
        self.browser.delete_all_cookies()  # delete all cookies
        cookies = read_cookie()
        for cookie in cookies:
            self.browser.add_cookie(cookie)  # add cookie

    def getPersonInfo(self, path=None):
        if not path:
            path = r"./PersonInfo.txt"
        with open(path, 'r', encoding='utf-8') as fp:
            contents = fp.readlines()
            self.user_id = contents[0].strip()
            self.user_password = contents[1].strip()
        return list((self.user_id, self.user_password))

    def getCourseInfo(self, path=None):

        if not path:
            path = r"./CourseInfo.txt"
        with open(path, 'r', encoding='utf-8') as fp:
            contents = fp.readlines()
            teacher_name = contents[0].strip()
            lesson_name = contents[1].strip()
            time_name = contents[2].strip()
            self.courseInfo.append(tuple((teacher_name, lesson_name, time_name)))

        return self.courseInfo

    def concurrent_search(self):
        """
        Concurrence with simple loop.
        :return:
        """
        if not self.courseInfo:
            self.getCourseInfo()  # Load the data
        print(self.courseInfo)
        courseInfo = self.courseInfo
        while True:
            courses = courseInfo
            if courses:
                for (teacher_name, lesson_name, time_name) in courses:
                    Shot = self.send_search(teacher_name=teacher_name, lesson_name=lesson_name, time_name=time_name)
                    if Shot:
                        courseInfo.remove(tuple((teacher_name, lesson_name, time_name)))
                        break
            else:
                break
            time.sleep(5)

    def send_search(self, teacher_name, lesson_name, time_name):
        Shot = False
        inputBox = self.browser.find_by_xpath('//*[@id="searchBox"]/div/div[1]/div/div/div/div/input')
        # //*[@id="searchBox"]/div/div[1]/div/div/div/div/input
        inputBox.clear()
        inputBox.fill(teacher_name)
        time.sleep(1)
        self.browser.find_by_xpath('//*[@id="searchBox"]/div/div[1]/div/div/div/div/span/button[1]').first.click()
        time.sleep(1)
        for i in range(1, 3):
            self.browser.find_by_xpath('//*[@id="nav_tab"]/li['+str(i)+']').first.click()  # select from general lessons
            time.sleep(1)

            courseBoxes = self.browser.find_by_css(
                '#contentBox > div.tjxk_list > div.panel.panel-info')  # box: one kind of course
            for box in courseBoxes:
                if lesson_name in box.text:  # confirm the lesson name
                    elements = box.find_by_css('a.expand_close.expand1')
                    if elements:
                        box.click()
                    time.sleep(1)
                    courseBars = box.find_by_css('tr[class="body_tr"]')  # bar: one specific course
                    time.sleep(0.3)
                    for bar in courseBars:
                        if teacher_name in bar.text and time_name in bar.text:  # confirm the teacher name
                            # print(bar.text)
                            if '已满' in bar.text:
                                continue
                            if '退选' in bar.text:
                                Shot = True
                                self.log("Success")
                                break
                            # search for location of the button and click it
                            button_box = bar.find_by_css('td[class="an"]').first
                            time.sleep(0.1)
                            btn = button_box.find_by_css('.btn').first
                            # print(btn.get_attribute('disabled'))
                            # if btn.get_attribute('disabled') == 'disabled':
                            #     Shot = True
                            #     break
                            btn.click()
                            time.sleep(0.1)
                            # deal with possible alerts
                            try:
                                alert = self.browser.find_by_css('.modal-content')
                            except:
                                alert = None
                            time.sleep(0.1)
                            if alert:
                                # Todo:写选课时间冲突的问题
                                if "最多可选" in alert.text:  # "一门课程最多可选1个志愿"
                                    print("你已经选了这门课")
                                    alert.find_by_id('btn_ok').first.click()
                                    Shot = True
                                    self.log("Lesson_Chosen")
                                    break
                                # print(alert.text)
                                # alert.find_element(By.ID, 'btn_ok').click()
        return Shot


if __name__ == '__main__':
    spider = Spider_Dean_Office()
    spider.visitUrl()
    spider.quit()
    # Sturzkampf.quit()
    # try:
    #     Sturzkampf.getUrl()
    # except Exception as e:
    #     print(e)
    # finally:
    # Sturzkampf.quit()
    # pass
