import os
import requests
import streamlit as st
from components.model import Model
from components import process

PLACEHOLDER_IMG_URL = "https://raw.githubusercontent.com/PratikDavidson/word-power-ai/main/assests/placeholder.PNG"
PLACEHOLDER_AUDIO_URL = "https://github.com/PratikDavidson/word-power-ai/blob/main/assests/silent_audio.mp3"

model = Model()

def default_parameters():
    st.session_state['image'] = process.image_process(requests.get(PLACEHOLDER_IMG_URL).content, False)
    st.session_state['audio'] = PLACEHOLDER_AUDIO_URL
    st.session_state['story'] = ''
    st.session_state['story_blanks'] = ''
    st.session_state['answer'] = []
    st.session_state['answer_sorted'] = []

class Backend:
    def __init__(self):
        if 'image' not in st.session_state and 'audio' not in st.session_state and 'story' not in st.session_state and 'answer' not in st.session_state and 'story_blanks' not in st.session_state and 'answer_sorted' not in st.session_state:
            default_parameters()

    @staticmethod
    def execute_workflow(pat, prompt):
        if pat == "" or prompt == "":
            st.toast('Both Personal Access Token and Topic Required!', icon="⚠️")
        else:
            os.environ["CLARIFAI_PAT"] = pat 
            image = model.generate_image(prompt)
            st.session_state['image'] = process.image_process(image, False)
            st.session_state['story'] = model.pictorial_story(image)
            st.session_state['audio'] = model.text_to_speech(st.session_state['story'])
            st.session_state['story_blanks'], st.session_state['answer'], st.session_state['answer_sorted'] = process.text_process(model.create_qa(st.session_state['story']))

    @staticmethod
    def match_answer(user_ans, actual_ans):
        if len(user_ans) != 0:
            if all(x == y for (x,y) in zip(user_ans, actual_ans)):
                st.toast('Correct Answer!', icon="✅")
            else:
                st.toast('Wrong Answer!', icon="❌")

    @staticmethod
    def reset_to_default():
        default_parameters()
