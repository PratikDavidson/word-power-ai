from PIL import Image
import io
import base64


def image_process(image_base64, model=True):
    if model:
        return base64.b64encode(image_base64).decode()
    return Image.open(io.BytesIO(image_base64)).resize((1024, 480))

def text_process(text):
    start_char = text.find('[')
    end_char = text.find(']')
    story_blanks = text[:start_char].strip()
    answer_list = text[start_char:end_char+1].strip('[]').replace(' ', '').split(',')
    answer_sorted = sorted(answer_list)
    return story_blanks, answer_list, answer_sorted

