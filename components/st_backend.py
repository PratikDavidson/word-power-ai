import os
import sys
import requests
import streamlit as st
from components.model import Model
from components import process

PLACEHOLDER_IMG_URL = "https://raw.githubusercontent.com/PratikDavidson/word-power-ai/main/assests/placeholder.jpg"
PLACEHOLDER_AUDIO_URL = "https://github.com/PratikDavidson/word-power-ai/blob/main/assests/silent_audio.mp3"

model = Model()

def default_parameters():
    st.session_state['image'] = process.image_process(requests.get(PLACEHOLDER_IMG_URL).content, False)
    st.session_state['audio'] = PLACEHOLDER_AUDIO_URL
    st.session_state['story'] = ''
    st.session_state['story_state'] = False
    st.session_state['story_blanks'] = ''
    st.session_state['answer'] = []
    st.session_state['answer_sorted'] = []
    st.session_state['multiselect'] = []

class Backend:
    def __init__(self):
        if ('image' not in st.session_state and 'audio' not in st.session_state 
            and 'story' not in st.session_state and 'answer' not in st.session_state 
            and 'story_blanks' not in st.session_state and 'answer_sorted' not in st.session_state
            and 'story_state' not in st.session_state and 'multiselect' not in st.session_state):
            default_parameters()

    @staticmethod
    def execute_workflow(pat, prompt):
        if pat == "" or prompt == "":
            st.toast('Both Personal Access Token & Topic Required!', icon="⚠️")
        else:
            os.environ["CLARIFAI_PAT"] = pat 
            try:
                image = model.generate_image(prompt)
                st.session_state['image'] = process.image_process(image, False)
                st.session_state['story'] = model.pictorial_story(image)
                st.session_state['audio'] = model.text_to_speech(st.session_state['story'])
                st.session_state['story_blanks'], st.session_state['answer'], st.session_state['answer_sorted'] = process.text_process(model.create_qa(st.session_state['story']))
            except:
                _, value, _ = sys.exc_info()
                response_code = value.args[0]
                if response_code.find('CONN_KEY_INVALID') != -1:
                    st.warning('Please Enter Valid Personal Access Token!', icon="⚠️")
                if response_code.find('RPC_REQUEST_TIMEOUT') != -1:
                    st.info('REQUEST_TIMEOUT! Please refresh and try after sometime.', icon="⌛")
            
    @staticmethod
    def match_answer(user_ans, actual_ans):
        if len(user_ans) != 0:
            if all(x == y for (x,y) in zip(user_ans, actual_ans)):
                st.toast('Correct Answer!', icon="✅")
                st.session_state['story_state'] =True
            else:
                st.toast('Wrong Answer!', icon="❌")

    @staticmethod
    def reset_story():
        st.session_state['story_state'] = False
        st.session_state['multiselect'] = []
