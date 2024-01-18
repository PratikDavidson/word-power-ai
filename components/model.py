import base64
from clarifai.client.model import Model as M

class Model:
    def __init__(self):
        self.user_id = "openai"
        self.quality = "standard"
        self.size = "1792x1024"
        self.style = "natural"
        self.voice = "nova"
        self.input_type = "text"
        self.speed = 1.0
        self.temperature = 1.0

    def generate_image(self, prompt):
        prompt = f"Pictorial story based on topic {prompt}. DO NOT KEEP any texts or symbols."
        inference_params = dict(quality=self.quality, size=self.size, style=self.style)
        model = M(user_id=self.user_id, app_id="dall-e", model_id="dall-e-3")
        model_prediction = model.predict_by_bytes(prompt.encode(), input_type=self.input_type, inference_params=inference_params)
        image_base64 = model_prediction.outputs[0].data.image.base64
        return image_base64

    def pictorial_story(self, image_base64):
        prompt = "Generate a small story with maximum 150 words based on this pictorial story image."
        image_base64 = base64.b64encode(image_base64).decode()
        inference_params = dict(temperature=self.temperature, image_base64=image_base64)
        model = M(user_id=self.user_id, app_id="chat-completion", model_id="gpt-4-vision-alternative")
        model_prediction = model.predict_by_bytes(prompt.encode(), input_type=self.input_type, inference_params=inference_params)
        return model_prediction.outputs[0].data.text.raw

    def create_qa(self, text):
        prompt = text + "Generate fill in the blanks with maximum 10 blanks for the above story without numbering and keep the answers below separated by commas inbetween square brackets."
        model = M(user_id=self.user_id, app_id="chat-completion", model_id="gpt-4-turbo")
        model_prediction = model.predict_by_bytes(prompt.encode(), input_type=self.input_type)
        return model_prediction.outputs[-1].data.text.raw

    def text_to_speech(self, text):
        inference_params = dict(voice=self.voice, speed=self.speed)
        model = M(user_id=self.user_id, app_id="tts", model_id="openai-tts-1")
        model_prediction = model.predict_by_bytes(text.encode(), input_type="text", inference_params=inference_params)
        audio_base64 = model_prediction.outputs[0].data.audio.base64
        return audio_base64