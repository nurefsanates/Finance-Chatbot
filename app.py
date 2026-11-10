import streamlit as st
from graph.langgraph_builder import build_graph

st.set_page_config(page_title="Finans Asistanı", page_icon="📈", layout="wide")

st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=League+Spartan&display=swap" rel="stylesheet">
    <style>
        body {
            background-color: #ffffff;
            font-family: 'League Spartan', sans-serif;
        }
        .stApp {
            background: linear-gradient(to right, #813FB4, #439E54);
            color: #fff;
        }
        /* Başlık ve açıklamalar beyaz */
        .css-1d391kg, .css-1v3fvcr { /* st.write ve st.title için */
            color: #FFFFFF;
            font-family: 'League Spartan', sans-serif;
        }
        /* Input alanı */
        .stTextInput>div>div>input {
            background-color: #FFFFFF !important;
            color: #000000 !important;
            font-family: 'League Spartan', sans-serif;
        }
        /* Placeholder rengi (input içi yazı) */
        .stTextInput>div>div>input::placeholder {
            color: #999999 !important;  /* açık gri */
            opacity: 1 !important;
        }
        /* Buton */
        button {
            background-color: #813FB4 !important; /* Buton arkaplanı */
            color: #000000 !important;           /* Yazı siyah */
            font-family: 'League Spartan', sans-serif;
            font-weight: bold;
        }
        button:hover {
            background-color: #ffffff !important;
            color: #000000 !important;
        }
    </style>
""", unsafe_allow_html=True)


st.title("Finans Asistanı 🧱")
st.write("Örnek bir aracı kurum platformuyla ilgili sorularınızı cevaplandırır (demo).")

if "history" not in st.session_state:
    st.session_state.history = []

# Form kullanıyoruz
with st.form(key="question_form", clear_on_submit=True):  # clear_on_submit=True inputu temizler
    question = st.text_input("Bir soru sorun:", key="question_input")
    submit = st.form_submit_button("Sor")

if submit and question:
    graph = build_graph()
    output = graph.invoke({"question": question})
    answer = output["answer"]
    st.session_state.history.append({"question": question, "answer": answer})

# Anlık cevabı göster
if submit and question:
    st.markdown(f"**Cevap:** {answer}")

# Önceki soru-cevapları göster
if st.session_state.history:
    st.markdown("---")
    st.markdown("**Geçmiş Sorular:**")
    
for qa in reversed(st.session_state.history[:-1]):  # Son soruyu tekrar göstermemek için [:-1]
    with st.expander(f"Soru: {qa['question']}"):
        st.markdown(f"**Cevap:** {qa['answer']}")