# coding=utf-8

# chrome_driver 如果chromedriver不在环境变量，可在此参数手工指定路径
# options chrome初始化时候的参数，如--proxy或者--headless，或者请求头
# sitename 签到的站点名，具体请查看cookies的path，如.baidu.com或www.baidu.com则输入baidu.com，去掉前面的符号
# login 预签到网站登陆页面的具体url
# afterlogin 预签到网站登陆完成后跳转到的url
# signurl 预签到网站签到按钮所在url
# xpath 预签到网站签到时候需要依次点击的元算素xpath地址，具体可用浏览器F12中在元算上右键copy>xpath来获取

import time
import pickle
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException,WebDriverException,NoSuchElementException,NoSuchWindowException

class SIGN:
    def __init__(self,chrome_driver='',options='',sitename='',login='',afterlogin='',signurl='',xpath=[]):
        self.SITENAME = sitename
        self.LOGIN = login
        self.AFTERLOGIN = afterlogin
        self.SIGNURL = signurl
        self.XPATH = xpath
        self.BASE_PATH = os.getcwd()
        self.PATH = self.setDir(self.BASE_PATH+'/Sites',self.SITENAME)

        chromeOptions = webdriver.ChromeOptions()
        #设置编码格式
        chromeOptions.add_argument('lang=zh_CN.UTF-8')
        #模拟移动设备   (移动版网站的反爬虫的能力比较弱)   模拟iPhone6
        # chromeOptions.add_argument('user-agent="Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"') 
        #取消沙盒模式，解决DevToolsActivePort文件不存在的报错
        # chromeOptions.add_argument('--no-sandbox')
        #谷歌文档提到需要加上这个属性来规避bug
        chromeOptions.add_argument('--disable-gpu')  
        #克服有限的资源问题  【但是用于Linux系统】
        # chromeOptions.add_argument('--disable-dev-shm-usage')
        #隐藏滚动条, 应对一些特殊页面  
        # chromeOptions.add_argument('--hide-scrollbars') 
        #不加载图片, 提升速度
        chromeOptions.add_argument('blink-settings=imagesEnabled=false')
        #浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
        # chromeOptions.add_argument('--headless')
        if options: chromeOptions.add_argument(options)
        if chrome_driver:
            self.BROWER = webdriver.Chrome(executable_path = chrome_driver,options=chromeOptions)
        else:
            self.BROWER = webdriver.Chrome(options=chromeOptions)
        WebDriverWait(self.BROWER, 10)
        self.BROWER.maximize_window()
        self.BROWER.implicitly_wait(6)

    def setDir(self,basepath, dir):
        newdir = basepath+'/'+dir
        if dir not in os.listdir(basepath):
            os.makedirs(newdir)
        return newdir

    def writefile(self,fileURI, str):
        with open(fileURI, 'a', encoding='UTF-8') as w:
            w.write(str)

    def log(self, str):
        print(str)
        str = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+': '+str
        self.writefile(self.PATH+'/'+self.SITENAME+'.log',str)

    def geterror(self, e):
        self.log(e)
        self.BROWER.get_screenshot_as_file(self.PATH+'/'+self.SITENAME+'.error.png')

    def getCookies(self):
        # get login taobao cookies
        url = self.AFTERLOGIN
        self.BROWER.get(self.LOGIN)
        while True:
            print("Please login in !")
            time.sleep(3)
            print(self.BROWER.current_url, url)
            while self.BROWER.current_url == url:
                Cookies = self.BROWER.get_cookies()
                cookies = {}
                for item in Cookies:
                    cookies[item['name']] = item['value']
                outputPath = open(self.PATH+'/'+self.SITENAME+'.cookies', 'wb')
                pickle.dump(cookies, outputPath)
                outputPath.close()
                return cookies


    def readCookies(self):
        # if hava cookies file ,use it
        # if not , getTaobaoCookies()
        if os.path.exists(self.PATH+'/'+self.SITENAME+'.cookies'):
            readPath = open(self.PATH+'/'+self.SITENAME+'.cookies', 'rb')
            Cookies = pickle.load(readPath)
        else:
            Cookies = self.getCookies()
        return Cookies


    def run(self):
        Cookies = self.readCookies()
        self.BROWER.get(self.SIGNURL)
        self.BROWER.delete_all_cookies()
        for cookie in Cookies:
            self.BROWER.add_cookie({
                'domain': '.'+self.SITENAME,
                'name': cookie,
                'value': Cookies[cookie],
                'path': '/',
                'expires': None
            })
        try:
            self.BROWER.get(self.SIGNURL)
            for path in self.XPATH:
                self.BROWER.find_element_by_xpath(path).click()
            pass
        except (NoSuchElementException, TimeoutException, WebDriverException,NoSuchWindowException) as e:
            self.geterror(str(e))
        except:
            self.geterror('未知错误')
        else:
            self.log('签到成功')
        finally:
            self.BROWER.quit()

