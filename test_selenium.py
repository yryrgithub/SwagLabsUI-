#导包
import pytest
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(scope="module")
def browser():
    # 启用谷歌浏览器
    driver = webdriver.Chrome()
    # 最大化窗口
    driver.maximize_window()
    # 隐式等待10秒
    driver.implicitly_wait(10)
    # 打开url
    driver.get('https://www.saucedemo.com/')
    # yield而不是return 方便后后面做teardown
    yield driver
    driver.quit()
    print("关闭浏览器")
# fixture使用，定义set_data方法，配置多个参数
@pytest.fixture(scope="function")
def set_data():
    # data = {
    #     "username": "standard_user",
    #     "password": "secret_sauce",
    # }
    data = [
        {"username": "visual_user", "password": "123"},
        {"username": "locked_out_user", "password": "233"},
        {"username": "problem_user", "password": "445"},
        {"username": "error_user", "password":""},
        {"username": "standard_user", "password": "secret_sauce"}
    ]
    return data


def test_login_with_fail(browser,set_data):
    for dat in set_data:
        print(f"测试登录")
        ele_username = browser.find_element(By.CSS_SELECTOR,'#user-name')
        ele_username.clear()
        ele_username.send_keys(dat['username'])
        print(f"已输入用户名：{dat['username']}")
        ele_password = browser.find_element(By.CSS_SELECTOR,'#password')
        ele_password.clear()
        ele_password.send_keys(dat['password'])
        print(F"已输入密码：{dat['password']}")

        browser.find_element(By.CSS_SELECTOR,'#login-button').click()
        try:
            WebDriverWait(browser, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '#contents_wrapper'))
            )
            print("登录成果，进入商品页面！！！")
            assert 'inventory' in browser.current_url
            print(f"url验证通过:{browser.current_url}")
        except TimeoutException:
            assert "Epic sadface: Username and password do not match any user in this service" == browser.find_element(By.CSS_SELECTOR, '.error-message-container').text
            # print("用户名或者密码错误")



def test_login(browser,set_data):
    print(f"测试登录,{set_data[0]['username']}")
    browser.find_element(By.CSS_SELECTOR,'#user-name').send_keys(set_data[0]['username'])
    print(f"已输入用户名,{set_data[0]['username']}")
    browser.find_element(By.CSS_SELECTOR,'#password').send_keys(set_data[0]['password'])
    print(f"已输入密码,{set_data[0]['password']}")
    sleep(10)
    browser.find_element(By.CSS_SELECTOR,'#login-button').click()
    print(f" √ 已点击登录按钮")
    try:
        WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '#contents_wrapper'))
        )
        print(" √ 登录成功，进入商品页面！！！")
        assert 'inventory' in browser.current_url
        print(f"url验证通过:{browser.current_url}")
    except TimeoutException:
        print(f"登录失败！！！")







