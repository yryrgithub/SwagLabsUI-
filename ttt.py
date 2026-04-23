import os
import subprocess
from pathlib import Path
from dotenv import load_dotenv

# 加载.env配置文件
load_dotenv()
# 直接指定 midscene.cmd 的绝对路径（请替换成你自己的路径）
MIDSCENE_CMD = r"C:\Users\pc\AppData\Roaming\npm\midscene.cmd"
# 确保文件存在
if not Path(MIDSCENE_CMD).exists():
    raise FileNotFoundError(f"找不到 midscene 命令: {MIDSCENE_CMD}")

# 定义 YAML 文件路径（可以使用相对路径，但要确保 cwd 正确）
yaml_file = "test_login.yaml"
yaml_abs = Path(yaml_file).resolve()
yaml_dir = str(yaml_abs.parent)
yaml_name = yaml_abs.name

# 构建命令
cmd = [MIDSCENE_CMD, yaml_name, "--summary", "report.json","--headed"]

# 执行
try:
    result = subprocess.run(
        cmd,
        cwd=yaml_dir,
        capture_output=True,
        text=True,
        timeout=300,
        encoding='utf-8'
    )
    print("返回码:", result.returncode)
    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)
except Exception as e:
    print("执行失败:", e)