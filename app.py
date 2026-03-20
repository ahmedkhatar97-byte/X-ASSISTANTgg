import streamlit as st
import g4f

# إعدادات الصفحة
st.set_page_config(page_title="X Assistant PRO", page_icon="🤖")

st.title("🤖 X Assistant PRO")
st.markdown("---")
st.caption("Developed by: **Ahmed El-Hareef** | المبرمج: أحمد الحريف")

# تهيئة الذاكرة (Session State) عشان البوت يفتكر الكلام
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system", 
            "content": "أنت مساعد ذكي ومرح اسمك 'X Assistant'. اللي صنعك ومبرمجك هو 'أحمد الحريف'. اتكلم دايماً بالعامية المصرية، وردودك تكون ذكية وخفيفة الظل. لو حد سألك عن هويتك قول إنك نسخة مطورة من برمجة الحريف."
        }
    ]

# عرض الرسائل القديمة في الواجهة
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# استقبال سؤال المستخدم
if prompt := st.chat_input("قول يا حريف، محتاج مساعدة في إيه؟"):
    # إضافة سؤال المستخدم للذاكرة وللواجهة
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # توليد الرد من الذكاء الاصطناعي
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # طلب الرد من مكتبة g4f
            response = g4f.ChatCompletion.create(
                model=g4f.models.gpt_4,
                messages=st.session_state.messages,
                stream=True,
            )
            
            for chunk in response:
                if chunk:
                    full_response += chunk
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            # إضافة رد البوت للذاكرة
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            error_msg = "السيرفر مريح شوية يا حريف، جرب تسأل تاني كمان لحظة."
            message_placeholder.markdown(error_msg)
          
