import os
import io
from PIL import Image
import streamlit as st
from components.model import Model

model = Model()

def default_parameters(root_dir):
    st.session_state['image'] = Image.open(os.path.join(root_dir, "assests/placeholder.png")).resize((1024, 480))
    st.session_state['audio'] = os.path.join(root_dir, "assests/silent_audio.mp3")
    st.session_state['story'] = ''
    st.session_state['story_blanks'] = ''
    st.session_state['answer'] = []
    st.session_state['answer_sorted'] = []

def text_process(text):
    start_char = text.find('[')
    end_char = text.find(']')
    story_blanks = text[:start_char].strip()
    answer_list = text[start_char:end_char+1].strip('[]').replace(' ', '').split(',')
    answer_sorted = sorted(answer_list)
    return story_blanks, answer_list, answer_sorted

class Backend():
    def __init__(self, dir):
        self.root_dir = dir
        if 'image' not in st.session_state and 'audio' not in st.session_state and 'story' not in st.session_state and 'answer' not in st.session_state and 'story_blanks' not in st.session_state and 'answer_sorted' not in st.session_state:
            default_parameters(self.root_dir)

    @staticmethod
    def execute_workflow(pat, prompt):
        if pat == "" or prompt == "":
            st.toast('Both Personal Access Token and Topic Required!', icon="⚠️")
        else:
            os.environ["CLARIFAI_PAT"] = pat 
            image = model.generate_image(prompt)
            st.session_state['image'] = Image.open(io.BytesIO(image)).resize((1024, 480))
            st.session_state['story'] = model.pictorial_story(image)
            st.session_state['audio'] = model.text_to_speech(st.session_state['story'])
            st.session_state['story_blanks'], st.session_state['answer'], st.session_state['answer_sorted'] = text_process(model.create_qa(st.session_state['story']))

    @staticmethod
    def match_answer(user_ans, actual_ans):
        if len(user_ans) != 0:
            if all(x == y for (x,y) in zip(user_ans, actual_ans)):
                st.toast('Correct Answer!', icon="✅")
            else:
                st.toast('Wrong Answer!', icon="❌")
    
    def reset_to_default(self):
        default_parameters(self.root_dir)
