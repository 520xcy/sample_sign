# sample_sign
实现自动签到的工具，需要一点点html基础
## 主要文件
`run.py` 主文件，定时执行

`Model/sign.py` 签到脚本，内有说明

## 使用方法
`pip3 install -r requirements.txt`

需要chromedriver，安装方法可参考https://www.cnblogs.com/lfri/p/10542797.html

将要签名的网站信息填入修改`run.py`中，设定好时间，执行`python3 run.py`即可