import streamlit as st
from components import st_backend

st.set_page_config(page_title="Word Power AI", layout="centered")

K = st_backend.Backend()

header = st.container()
body = st.container()

with st.sidebar:
    pat = st.text_input('Enter Personal Access Token:', type='password')
    prompt = st.text_input('Enter a topic:')
    st.button('Generate Story', on_click = K.execute_workflow, args=(pat,prompt))

with header:
    st.markdown("<h1 style='text-align: center;'>Word Power AI</h1>", unsafe_allow_html=True)
    st.subheader('', divider='gray')

with body:
    st.image(st.session_state['image'], use_column_width=True)
    st.audio(st.session_state['audio'], format="audio/mp3")
    st.subheader('', divider='gray')
    st.subheader('Story:')
    st.write(st.session_state['story_blanks'])
    options = st.multiselect('Select answers in order of blanks:', st.session_state['answer_sorted'])
    st.write('You selected:', dict(enumerate(options,start=1)))
    submit, reset, *_ = st.columns(7)
    with submit:
        st.button('Submit', on_click = K.match_answer, args=(options, st.session_state['answer']))
    with reset:
        st.button('Reset', on_click = K.reset_to_default)

