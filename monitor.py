import socket
import datetime
import requests
import json
import os

# ==================== 配置 ====================
NODE_IP = "c83s2.portablesubmarines.com"      # 修改这里
NODE_PORT = 39179                 # 修改这里
FEISHU_WEBHOOK = "https://open.feishu.cn/open-apis/bot/v2/hook/5f984282-4adc-4280-9dd0-a14695daa98a"  # 修改这里
# ============================================

def check_node():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    try:
        s.connect((NODE_IP, int(NODE_PORT)))
        return True
    except:
        return False

# 1. 状态检测与日志组装
is_ok = check_node()
timestamp = (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
status_str = "OK" if is_ok else "FAIL"
log_entry = f"{timestamp} | {status_str}\n"

# 测试
# 2. 写入日志文件
with open("log.txt", "a") as f:
    f.write(log_entry)

# 3. 失败时发送飞书通知
if not is_ok:
    payload = {
        "msg_type": "text", 
        "content": {"text": f"⚠️ 节点连接失败\n时间: {timestamp}\nIP: {NODE_IP}:{NODE_PORT}"}
    }
    requests.post(FEISHU_WEBHOOK, json=payload)
