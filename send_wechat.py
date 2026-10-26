import requests
import json
import os  

# ================= 配置区 =================
# 从环境变量中读取配置（如果没有，就使用默认值方便本地测试）
APP_ID = os.environ.get("WX_APP_ID", "你的APPID")
APP_SECRET = os.environ.get("WX_APP_SECRET", "你的APPSECRET")
OPEN_ID = os.environ.get("WX_OPEN_ID", "你的OPENID")
TEMPLATE_ID = os.environ.get("WX_TEMPLATE_ID", "你的TEMPLATE_ID")
# ==========================================

def get_access_token(app_id, app_secret):
    """获取微信 access_token"""
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={app_id}&secret={app_secret}"
    response = requests.get(url, timeout=10)
    data = response.json()
    
    if "access_token" in data:
        return data["access_token"]
    else:
        raise Exception(f"获取 access_token 失败: {data}")

def send_template_message(access_token, open_id, template_id, title, content):
    """发送模板消息"""
    url = f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={access_token}"
    
    # 这里的 key (title, content, time) 必须和你刚才在网页上填的模板变量名一致
    payload = {
        "touser": open_id,
        "template_id": template_id,
        "data": {
            "title": {
                "value": title
            },
            "content": {
                "value": content
            },
            "time": {
                "value": "刚刚" # 这里你可以改成具体时间，比如 datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        }
    }
    
    # 微信接口要求使用 utf-8 编码发送 json
    headers = {"Content-Type": "application/json; charset=utf-8"}
    response = requests.post(url, data=json.dumps(payload, ensure_ascii=False).encode('utf-8'), headers=headers)
    result = response.json()
    
    if result.get("errcode") == 0:
        print("✅ 消息发送成功！")
    else:
        print(f"❌ 消息发送失败: {result}")

if __name__ == "__main__":
    try:
        print("正在获取 access_token...")
        token = get_access_token(APP_ID, APP_SECRET)
        
        print("正在发送消息...")
        send_template_message(
            access_token=token,
            open_id=OPEN_ID,
            template_id=TEMPLATE_ID,
            title="GitHub 提醒",
            content="早上好，该看今天的日程了！"
        )
    except Exception as e:
        print(f"发生错误: {e}")
