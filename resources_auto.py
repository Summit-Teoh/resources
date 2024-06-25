from selenium import webdriver
from bs4 import BeautifulSoup
import time


web = webdriver.Chrome(executable_path='.vscode\driver\chromedriver.exe')
web.get("http://xkz.mnr.gov.cn/")

# web.find_element_by_id('kw').send_keys("科比")  #模拟输入
# web.find_element_by_id('su').click()            #模拟点击
res = web.page_source
soup = BeautifulSoup(res,"lxml")
print(soup)

time.sleep(10)                                   #休眠六秒

# web.save_screenshot('./5.15/tupian/parther.png')  #对页面进行截图

web.close()
