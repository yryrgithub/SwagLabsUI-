"""
test_login.py
只输出你指定的信息到测试报告
"""

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_login_scenarios(browser, login_data):
    """
    测试登录功能
    只打印指定的信息到报告
    """
    data = login_data
    username = data["username"]
    password = data["password"]
    expected = data["expected"]
    should_succeed = data["should_succeed"]

    # ===== 只打印你要求的信息 =====
    print(f"\n🔍 测试用户: {username} - {'成功' if should_succeed else '失败'}")
    print(f"📋 测试数据:")
    print(f"   - 用户名: {username}")
    print(f"   - 密码: {'*' * len(password)}")
    print(f"   - 预期结果: {'✅ 成功' if should_succeed else '❌ 失败'}")
    if not should_succeed:
        print(f"   - 预期错误: {expected}")

    # 执行测试
    browser.find_element(By.CSS_SELECTOR, '#user-name').send_keys(username)
    browser.find_element(By.CSS_SELECTOR, '#password').send_keys(password)
    browser.find_element(By.CSS_SELECTOR, '#login-button').click()

    # 验证结果
    if should_succeed:
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.inventory_list'))
        )
        print(f"\n✅ 测试结果: 登录成功！")
    else:
        error = WebDriverWait(browser, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-test="error"]'))
        )
        actual_error = error.text
        assert actual_error == expected
        print(f"\n✅ 测试结果: 登录失败（符合预期）")

    print(f"\n✨ 测试用例执行完成！\n")