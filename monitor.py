import socket
import datetime
import requests
import json
import os

# ==================== 配置 ====================
NODE_IP = "你的代理服务器IP"      # 修改这里
NODE_PORT = 443                 # 修改这里
FEISHU_WEBHOOK = "你的飞书Webhook地址"  # 修改这里
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
