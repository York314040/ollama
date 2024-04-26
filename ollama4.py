import streamlit as st
from gtts import gTTS
import base64
from tempfile import NamedTemporaryFile
import speech_recognition as sr

# 假設 ollama 有類似功能
import ollama

def autoplay_audio(file_path: str):
    """ 將音頻文件轉為Base64並在網頁上自動播放 """
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio controls autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(md, unsafe_allow_html=True)

def recognize_speech():
    """ 使用麥克風識別語音並返回文字 """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("請說話...")
        audio_data = r.listen(source)
        try:
            text = r.recognize_google(audio_data, language='zh-TW')
            return text
        except sr.UnknownValueError:
            return "無法識別語音"
        except sr.RequestError:
            return "請求出錯"

def main():
    st.title("我的對話機器人會說話")

    # 錄製語音並轉換為文字
    if st.button("點擊錄音"):
        question = recognize_speech()
        st.write("您的問題：", question)

        # 使用ollama模型進行對話
        response = ollama.chat(model='mistral', messages=[{'role': 'user', 'content': question}])

        # 顯示回答
        st.text("回答：")
        st.write(response['message']['content'])

        tts = gTTS(text=response['message']['content'], lang='zh-tw', slow=False)
        with NamedTemporaryFile(suffix=".mp3", delete=False) as temp:
            tempname = temp.name
            tts.save(tempname)
            autoplay_audio(tempname)

if __name__ == "__main__":
    main()
