import streamlit as st
import ollama

from gtts.lang import tts_langs #用所有語言
from gtts import gTTS
import base64 #網頁發生
from tempfile import NamedTemporaryFile 

langs = tts_langs().keys() #載入所有語言清單

def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio controls autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(
            md,
            unsafe_allow_html=True,
        )

def main():
    st.title("我的對話機器人會說話")
    lang = st.selectbox("請選擇發音的語言",options=langs,index=57) #預設繁體中文
    # 設置用戶輸入框
    user_input = st.text_area("您想問什麼？", "")
    
    # 當使用者按下送出按鈕後的處理
    if st.button("送出"):
        if user_input:
            # 使用ollama模型，進行對話
            response = ollama.chat(model='mistral', messages=[{'role': 'user', 'content': user_input}])
            
            # 顯示回答
            st.text("回答：")
            st.write(response['message']['content'])

            tts = gTTS(response['message']['content'],lang =lang ,slow=False,lang_check=True)
            with NamedTemporaryFile(suffix=".mp3",delete=False) as temp:
                tempname = temp.name
                tts.save(tempname)
                autoplay_audio(tempname)

        else:
            st.warning("請輸入問題！")

if __name__ == "__main__":
    main()
