# coding=utf-8
import schedule
import time
import threading
from Model import sign

def qd_52pojie():
    sitename = '52pojie.cn'
    login = r"https://www.52pojie.cn/member.php?mod=logging&action=login"
    afterlogin = r"https://www.52pojie.cn/"
    signurl = r"https://www.52pojie.cn"
    xpath = [
        '//*[@id="um"]/p[2]/a[1]'
    ]
    options = [
        'lang=zh_CN.UTF-8',
        '--disable-gpu',
    ]
    dosign = sign.SIGN(options=options,sitename=sitename,login=login,afterlogin=afterlogin,signurl=signurl,xpath=xpath)
    dosign.run()

def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread=job_thread.start()

if __name__ == "__main__":
    schedule.clear()
    schedule.every(1).days.at('08:00').do(run_threaded, qd_52pojie)
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+': 启动监控...')

    while True:
        schedule.run_pending()
        # print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        time.sleep(1)

