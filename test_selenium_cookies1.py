from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

# 启用谷歌浏览器
driver = webdriver.Chrome()

try:
    # 先打开网站
    driver.get('https://chat.deepseek.com/')
    time.sleep(2)

    # 加载保存的cookies
    try:
        with open('deepseek_valid_cookies.json', 'r', encoding='utf-8') as f:
            cookies = json.load(f)

        # 添加cookies
        for cookie in cookies:
            try:
                # 确保domain正确
                if 'domain' in cookie:
                    cookie['domain'] = 'chat.deepseek.com'
                driver.add_cookie(cookie)
                print(f"添加cookie: {cookie['name']}")
            except Exception as e:
                print(f"添加cookie失败 {cookie['name']}: {e}")

        # 刷新页面
        driver.refresh()
        print("页面已刷新，等待加载...")
        time.sleep(3)

    except FileNotFoundError:
        print("请先运行手动登录程序获取cookie文件")
        driver.quit()
        exit()

    # 等待页面加载，尝试多种方式定位输入框
    wait = WebDriverWait(driver, 15)

    # 方法1: 尝试多种选择器
    input_element = None
    selectors = [
        (By.CSS_SELECTOR, '[placeholder*="发送消息"]'),
        (By.CSS_SELECTOR, '[placeholder*="Message"]'),
        (By.CSS_SELECTOR, 'textarea'),
        (By.CSS_SELECTOR, '[contenteditable="true"]'),
        (By.XPATH, "//textarea"),
        (By.XPATH, "//div[@contenteditable='true']"),
        (By.CLASS_NAME, "chat-input"),
        (By.CSS_SELECTOR, ".input-area textarea")
    ]

    for by, selector in selectors:
        try:
            input_element = wait.until(EC.presence_of_element_located((by, selector)))
            print(f"成功找到输入框，使用: {by}, {selector}")
            break
        except:
            continue

    if input_element:
        # 输入内容
        input_element.send_keys('selenium自动化测试如何获取cookies')
        print("消息已输入")

        # 获取当前cookies
        current_cookies = driver.get_cookies()
        print(f"\n当前共有 {len(current_cookies)} 个cookies:")
        for cookie in current_cookies:
            print(f"  {cookie['name']}: {cookie['value'][:20]}...")
    else:
        print("未找到输入框，请检查页面是否加载成功")

        # 打印当前页面标题和URL
        print(f"页面标题: {driver.title}")
        print(f"当前URL: {driver.current_url}")

        # 截图保存
        driver.save_screenshot("page_screenshot.png")
        print("已保存页面截图: page_screenshot.png")

    time.sleep(5)

finally:
    driver.quit()