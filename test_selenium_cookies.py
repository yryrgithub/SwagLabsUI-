#导包
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#启用谷歌浏览器
driver = webdriver.Chrome()
# 打开url
driver.get('https://chat.deepseek.com/')


cookie1 = {'name': 'ds_session_id', 'value': '8c3a04bfc61c41c4bfe27f089cc039e4'}
cookie2 = {'name': '.thumbcache_6b2e5483f9d858d7c661c5e276b6a6ae',
           'value': 'QSUhBr0Zzv0z2v78dt18dhHgnSKVtEFYaRP1tyVTTD7s37gBS1EG3AKZf5Q7uXajmbOKgxa7n9VttsMzUZAp8Q'}

driver.add_cookie(cookie1)
driver.add_cookie(cookie2)

# driver.add_cookie({'name': 'ds_session_id', 'value': '64e6c94cbd4b428985cbba814962b7c2; .thumbcache_6b2e5483f9d858d7c661c5e276b6a6ae=FmjwP4WC4t8N9O7L30CHtDYTE3EBOOKCAsXcO9fUGJcoQUY9MNgP/fVt48d7QlgkXqzWOIQXfZePoR2LgG+FRA%3D%3D'})
driver.refresh()
sleep(5)
# 显示等待，最多等10秒，直到页面元素加载出来
wait = WebDriverWait(driver, 10)
input_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[placeholder="给 DeepSeek 发送消息 "]')))
input_element.send_keys('selenium自动化测试如何获取cookies')

# 等待
sleep(3)
# 关闭浏览器
driver.quit()