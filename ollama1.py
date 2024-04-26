import streamlit as st
import ollama

def main():
    st.title("我的第一個自然語言對話程式")
    
    #設置用戶輸入框
    user_input = st.text_area("您想問什麼？","")
    
    #當使用者按下送出按鈕後的處理
    if st.button("送出"):
        if user_input:
            #使用ollama模型，進行對話
            response = ollama.chat(model='mistral',messages=[{'role': 'user', 'content': user_input}])
            
            #顯示回答
            st.text("回答：")
            st.write(response['message']['content'])
        else:
            st.warning("請輸入問題！")
            
if __name__ == "__main__":
    main()