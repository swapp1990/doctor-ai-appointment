import openai
import os


class Bot:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def get_suggestion(self, conversation):
        print("Conversation:", conversation)
        combined = [
            {"role": "user", "content": "You are Ruby, wise-cracking, witty, charming. Answer in sentences."}] + conversation
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            max_tokens=512,
            messages=combined
        )
        return response['choices'][0]['message']['content']

    def summarize(self, text):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Shorten the following text."},
                {"role": "user", "content": text},
            ]
        )
        return response['choices'][0]['message']['content']

    def raw_api_call(self, text):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Answer as concisely as possible."},
                {"role": "user", "content": text}
            ]
        )
        return response

    def find_best_match(text, options):
        print("finding ...")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Select the best matching provider based on the user's response. Only return the option number. If none of the options are a good match, return 100."},
                {"role": "user", "content": f"User said: {text}. Available options are: {options}"}
            ]
        )
        # print(response)
        index = response['choices'][0]['message']['content']
        # convert to int
        return int(index)
