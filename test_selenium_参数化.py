# 导包
import pytest
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
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
    # yield而不是return 方便后面做teardown
    yield driver
    driver.quit()
    print("关闭浏览器")


"""
# pytest.mark.parametrize 参数化用户名，密码，期望结果  分为了多个测试用例执行
@pytest.mark.parametrize("username,password,excepted", [
    ("visual_user", "123", "Epic sadface: Username and password do not match any user in this service"),
    ("locked_out_user", "234", "Epic sadface: Username and password do not match any user in this service"),
    ("problem_user", "345", "Epic sadface: Username and password do not match any user in this service"),
    ("error_user", "dff", "Epic sadface: Username and password do not match any user in this service"),
    ("standard_user", "secret_sauce", "inventory")
])
def test_login_with_parametrize(username, password, excepted, browser):
    print(f"测试登录")
    ele_username = browser.find_element(By.CSS_SELECTOR, '#user-name')
    ele_username.clear()
    ele_username.send_keys(username)
    print(f"已输入用户名：{username}")
    ele_password = browser.find_element(By.CSS_SELECTOR, '#password')
    ele_password.clear()
    ele_password.send_keys(password)
    print(F"已输入密码：{password}")

    browser.find_element(By.CSS_SELECTOR, '#login-button').click()
    try:
        WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '#contents_wrapper'))
        )
        print("登录成果，进入商品页面！！！")
        assert excepted in browser.current_url
        print(f"url验证通过:{browser.current_url}")
    except TimeoutException:
        assert excepted == browser.find_element(By.CSS_SELECTOR, '.error-message-container').text
        print("用户名或者密码错误")

"""

# pytest.fixture(params=[])参数化
@pytest.fixture(
    params=[("visual_user", "123", "Epic sadface: Username and password do not match any user in this service"),
            ("locked_out_user", "234", "Epic sadface: Username and password do not match any user in this service"),
            ("problem_user", "345", "Epic sadface: Username and password do not match any user in this service"),
            ("error_user", "dff", "Epic sadface: Username and password do not match any user in this service"),
            ("standard_user", "secret_sauce", "inventory")],
    ids=["visual_user密码错误", "locked_out_user密码错误", "problem_user密码错误", "error_user密码错误",
         "standard_user用户名错误"])
def get_data(request):
    username, password, except_value = request.param
    yield {
        "username": username,
        "password": password,
        "excepted": except_value
    }
def test_login_with_fixture_parm(browser, get_data):
    print(f"测试登录")
    ele_username = browser.find_element(By.CSS_SELECTOR, '#user-name')
    ele_username.clear()
    ele_username.send_keys(get_data["username"])
    print(f"已输入用户名：{get_data["username"]}")
    ele_password = browser.find_element(By.CSS_SELECTOR, '#password')
    ele_password.clear()
    ele_password.send_keys(get_data["password"])
    print(F"已输入密码：{get_data["password"]}")

    browser.find_element(By.CSS_SELECTOR, '#login-button').click()
    try:
        WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '#contents_wrapper'))
        )
        print("登录成功"
              "，进入商品页面！！！")
        assert get_data['excepted'] in browser.current_url
        print(f"url验证通过:{browser.current_url}")
    except TimeoutException:
        assert get_data['excepted'] == browser.find_element(By.CSS_SELECTOR, '.error-message-container').text
        print("用户名或者密码错误")


