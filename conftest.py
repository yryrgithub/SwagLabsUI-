"""
conftest.py
只保留最基本的 fixture
"""

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="function")
def browser():
    """浏览器 fixture"""
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    driver.implicitly_wait(10)
    driver.get('https://www.saucedemo.com/')
    yield driver
    driver.quit()


@pytest.fixture(params=[
    ("visual_user", "123", "Epic sadface: Username and password do not match any user in this service"),
    ("locked_out_user", "234", "Epic sadface: Username and password do not match any user in this service"),
    ("problem_user", "345", "Epic sadface: Username and password do not match any user in this service"),
    ("error_user", "dff", "Epic sadface: Username and password do not match any user in this service"),
    ("standard_user", "secret_sauce", "inventory"),
], ids=[
    "visual_user_错误密码",
    "locked_out_user_错误密码",
    "problem_user_错误密码",
    "error_user_错误密码",
    "standard_user_成功登录"
])
def login_data(request):
    """测试数据 fixture"""
    username, password, expected = request.param
    return {
        "username": username,
        "password": password,
        "expected": expected,
        "should_succeed": expected == "inventory"
    }
