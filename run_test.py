"""
run_tests.py
正确捕获控制台输出的运行脚本
"""

import pytest
from datetime import datetime

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 开始执行测试")
    print("=" * 60)

    # 生成带时间戳的报告文件名
    report_file = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"

    # 关键参数说明：
    # -s              : 显示所有print输出
    # --capture=sys   : 捕获sys.stdout/stderr
    # --show-capture=stdout : 在报告中显示捕获的输出
    pytest.main([
        "test_login.py",
        "-v",
        f"--html={report_file}",
        "--self-contained-html",
        "-s",                    # 显示print输出
        "--capture=sys",         # 捕获系统输出
        "--show-capture=stdout", # 在报告中显示stdout
    ])

    print(f"\n📊 测试报告: {report_file}")
    print("=" * 60)