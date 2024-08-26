import requests
import uuid
from zhipuai import ZhipuAI
import streamlit as st


api_key = "你的API-key"

def run_v4_sync(input):
    msg = [
        {
            "role": "user",
            "content":input
        }
    ]
    tool = "web-search-pro"
    url = "https://open.bigmodel.cn/api/paas/v4/tools"
    request_id = str(uuid.uuid4())
    data = {
        "request_id": request_id,
        "tool": tool,
        "stream": False,
        "messages": msg
    }

    resp = requests.post(
        url,
        json=data,
        headers={'Authorization': api_key},
        timeout=300
    )
    return resp.content.decode()



def glmlong(m):
    client = ZhipuAI(api_key=api_key) # 填写您自己的APIKey
    x=run_v4_sync(m)
    response = client.chat.completions.create(
    model="glm-4-long",  # 填写需要调用的模型编码
    messages=[
        {"role": "system", "content": "你是一个搜索内容整合专家助手，你的任务是针对用户搜索内容提供1000字的概括总结，并且备注来源网址。"},
        {"role": "user", "content": x}
            ],
    stream=False,
    )
    return response.choices[0].message.content

if __name__ == '__main__':
    st.title("AIGCLINK：glm-4-long+websearch构建AI搜索最小用例")
    user_input = st.text_input("输入一些文本：")
    st.write(glmlong(user_input))