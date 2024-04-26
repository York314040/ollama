import streamlit as st
import requests
from PIL import Image
import base64
from io import BytesIO
import json
import ollama

# Streamlit App 頁面設定成繁體中文
st.set_page_config(page_title="我的對話機器人會說話", page_icon="🤖", layout="wide")

class ImageInterpreter:
    def __init__(self, model_url='http://localhost:11434/api/chat', headers=None):
        self.model_url = model_url
        self.headers = headers if headers else {}

    def encode_image_to_base64(self, image):
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode()

    def interpret_image(self, image_base64, user_input="請解析圖片內容？，用中文回答"):
        payload = {
            "model": "llava",
            "messages": [
                {
                    "role": "user",
                    "content": user_input,
                    "images": [image_base64]
                }
            ],
            "stream": False
        }
        try:
            response = requests.post(self.model_url, json=payload, headers=self.headers)
            response.raise_for_status()  # Raises an exception for HTTP errors
            result = response.json()
            return result['message']['content']
        except requests.exceptions.RequestException as e:
            return f"API 請求錯誤: {e}"

class DialogHandler:
    def chat(self, user_input):
        response = ollama.chat(model='mistral', messages=[{'role': 'user', 'content': user_input}])
        return response['message']['content']

def main():
    # Example of setting custom headers if needed
    headers = {'Authorization': 'Bearer YOUR_ACCESS_TOKEN'}
    interpreter = ImageInterpreter(headers=headers)
    dialog_handler = DialogHandler()
    
    st.title("我的對話機器人會說話")
    user_input = st.text_area("您想問什麼？", "")
    
    if st.button("送出"):
        if user_input:
            # 使用 DialogHandler 處理文字對話
            response = dialog_handler.chat(user_input)
            st.text("回答：")
            st.write(response)
        else:
            st.warning("請輸入問題！")

    st.title("圖片解讀器")
    uploaded_image = st.file_uploader("上傳圖片", type=['jpg', 'png', 'jpeg'])

    if uploaded_image is not None:
        image = Image.open(uploaded_image)
        st.image(image, caption='上傳的圖片', width=300)
        image_base64 = interpreter.encode_image_to_base64(image)
        result = interpreter.interpret_image(image_base64, user_input)
        st.subheader("圖片解讀結果：")
        st.write(result)

if __name__ == "__main__":
    main()
