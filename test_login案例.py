"""
test_login案例.py - 登录测试用例
包含：参数化测试 + fixture复用
"""

import pytest
from typing import Dict

# 第一部分：参数化测试用例
# 格式：(用户名, 密码, 期望结果, 期望消息)
LOGIN_TEST_DATA = [
    ("admin", "123456", True, "登录成功"),  # 测试用例1：正确凭证
    ("admin", "wrong", False, "用户名或密码错误"),  # 测试用例2：密码错误
    ("user1", "pass123", True, "登录成功"),  # 测试用例3：普通用户
    ("vip", "vip@2024", True, "登录成功"),  # 测试用例4：VIP用户
    ("unknown", "123", False, "用户名或密码错误"),  # 测试用例5：用户不存在
    ("admin", "", False, "用户名或密码错误"),  # 测试用例6：空密码
]


@pytest.mark.parametrize("username,password,expected_success,expected_message", LOGIN_TEST_DATA)
def test_login_parametrize(
        username,
        password,
        expected_success,
        expected_message,
        login_api,  # 使用conftest中的fixture
        login_function,  # 使用function级别的fixture
        user_database  # 使用session级别的fixture
):
    """
    参数化测试用例：
    用一组数据测试同一个功能，避免写重复代码
    """
    print(f"\n🔄 测试用户: {username}, 密码: {password}")

    # 1. 记录测试前的密码（如果是存在的用户）
    original_password = user_database[username]["password"]
    print(f"📝 用户{username}的原密码: {original_password}")
    # 执行登录（使用fixture提供的登录函数）
    result = login_api(username, password)

    # 断言结果
    assert result["success"] == expected_success
    assert result["message"] == expected_message

    # 如果登录成功，验证token存在
    if expected_success:
        assert result["token"] is not None
        assert result["token"].startswith("token_")
        print(f"✅ 登录成功，token: {result['token']}")
    else:
        assert result["token"] is None
        print(f"❌ 登录失败，原因: {result['message']}")

    # 验证用户数据库中的数据没有被修改
    # 如果用户存在，验证密码没被修改
    if username in user_database:
        # 如果用户存在，验证密码没被修改
        assert user_database[username]["password"] == original_password, f"❌ 错误：用户{username}的密码在测试中被意外修改（现密码：{user_database[username]['password']}，原密码：{original_password}）"
        print(f"✅ 用户{username}的密码未被修改")
    else:
        # 如果用户不存在，这是正常的测试场景（如测试不存在用户）
        print(f"ℹ️ 用户{username}不存在，跳过密码验证")

        # 可选：验证用户数据库没有被意外添加或删除
    if username not in user_database and expected_success:
        # 如果测试期望成功但用户不存在，这是测试数据有问题
        pytest.fail(f"❌ 测试数据错误：期望登录成功，但用户{username}在数据库中不存在")


# 第二部分：使用fixture复用测试数据
def test_login_with_invalid_password(login_api, login_function):
    """
    测试无效密码场景
    复用login_api fixture，不用重新实现登录逻辑
    """
    print("\n🔐 测试：无效密码场景")

    # 测试多个无效密码
    invalid_passwords = ["", "123", "password", "abc123"]

    for pwd in invalid_passwords:
        result = login_api("admin", pwd)
        assert result["success"] is False
        assert result["message"] == "用户名或密码错误"
        assert result["token"] is None
        print(f"  - 密码 '{pwd}': 验证通过")


def test_login_nonexistent_user(login_api, user_database):
    """
    测试不存在的用户
    复用user_database fixture
    """
    print("\n👤 测试：不存在的用户")

    # 从user_database中获取存在的用户名
    existing_users = set(user_database.keys())

    # 测试不存在的用户名
    test_users = ["ghost", "hacker", "test", "anonymous"]

    for username in test_users:
        result = login_api(username, "any_password")
        assert result["success"] is False
        assert result["message"] == "用户名或密码错误"
        print(f"  - 用户 '{username}': 验证通过")


def test_login_successful_users(login_api, user_database):
    """
    测试所有成功登录场景
    动态生成测试数据
    """
    print("\n✨ 测试：所有有效用户登录")

    for username, info in user_database.items():
        result = login_api(username, info["password"])

        assert result["success"] is True
        assert result["message"] == "登录成功"
        assert result["token"] is not None
        assert result["role"] == info["role"]

        print(f"  - 用户 '{username}' ({info['role']}): 登录成功")


# 第三部分：使用标记控制测试执行
@pytest.mark.slow
def test_login_performance(login_api):
    """
    标记为慢速测试
    执行：pytest -m "slow"
    """
    import time

    print("\n⏱️ 性能测试：连续登录10次")
    start_time = time.time()

    for i in range(10):
        result = login_api("admin", "123456")
        assert result["success"] is True

    elapsed = time.time() - start_time
    print(f"✅ 完成10次登录，耗时: {elapsed:.3f}秒")
    assert elapsed < 5  # 确保性能达标


# 第四部分：使用fixture参数化
@pytest.fixture(params=[
    ("admin", "123456", True),
    ("admin", "wrong", False),
    ("vip", "vip@2024", True),
], ids=["admin正确", "admin错误", "vip正确"])
def login_test_case(request):
    """
    fixture参数化：
    返回不同的测试数据组合
    """
    username, password, expected = request.param
    return {
        "username": username,
        "password": password,
        "expected": expected
    }


def test_login_with_fixture_param(login_test_case, login_api):
    """
    使用参数化的fixture进行测试
    效果等同于@pytest.mark.parametrize
    """
    data = login_test_case
    print(f"\n🔄 [Fixture参数化] 测试: {data['username']}")

    result = login_api(data["username"], data["password"])
    assert result["success"] == data["expected"]