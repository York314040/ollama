import streamlit as st
from gtts import gTTS
import base64
import os
import time
import speech_recognition as sr

# 假设 ollama 有类似功能
import ollama

def autoplay_audio(file_path: str):
    """将音频文件转为Base64并在网页上自动播放"""
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
    """使用麦克风识别语音并返回文字"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("请说话...")
        audio_data = r.listen(source)
        try:
            text = r.recognize_google(audio_data, language='zh-TW')
            return text
        except sr.UnknownValueError:
            return "无法识别语音"
        except sr.RequestError:
            return "请求出错"

def main():
    st.title("我的对话机器人会说话")

    # 检查并删除上一次的音频文件
    if 'last_audio_file' in st.session_state and os.path.exists(st.session_state['last_audio_file']):
        os.remove(st.session_state['last_audio_file'])

    # 录制语音并转换为文字
    if st.button("点击录音"):
        question = recognize_speech()
        st.write("您的问题：", question)

        # 使用ollama模型进行对话
        response = ollama.chat(model='mistral', messages=[{'role': 'user', 'content': question}])

        # 显示回答
        st.text("回答：")
        st.write(response['message']['content'])

        # 生成语音
        tts = gTTS(text=response['message']['content'], lang='zh-tw', slow=False)
        # 使用时间戳创建唯一的文件名
        unique_filename = f"audio_{int(time.time())}.mp3"
        tts.save(unique_filename)
        autoplay_audio(unique_filename)

        # 更新 session_state 中的最后一个音频文件名
        st.session_state['last_audio_file'] = unique_filename

if __name__ == "__main__":
    main()