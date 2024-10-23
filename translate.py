'''Contains objects necessary for translating and providing suggestions.'''

import os
import logging
import requests

import deepl
from openai import OpenAI

# Grab DeepL key
from dotenv import load_dotenv
load_dotenv('c:\\Users\\lupea\\Documents\\Lupeamanu\\Env\\.env')
DEEPL_KEY = os.getenv('DEEPL_API_KEY')
OPENAI_KEY = os.getenv('OPENAI_KEY')


logger = logging.getLogger(__name__)

class OpenAIClient:
    """Client used to interface with OpenAI for suggestions.
    """

    def __init__(self) -> None:
        self.client = OpenAI(api_key=OPENAI_KEY)


    def get_suggestion(self, text: str, v: int = 2):
        """This function generates a suggestion for a given text using the OpenAI GPT-4o-mini model. The verbosity of the explanations can be adjusted.
        
        Args:
            text (str): The text for which a suggestion is needed.
            v (int, optional): The verbosity of explanations. Defaults to 2.
        
        Returns:
            completion: The generated suggestion.
        """
        
        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"You are a translator. On a scale of 1-5, the verbosity of explanations should be a {v}"},
                {
                    "role": "user",
                    "content": f"Please provide any corrections for the following sentence: {text}. \
                        Provide the details of the corrections followed by the translation of the corrected sentence if needed. \
                        If the provided sentence to correct is in English, please only translate into Japanese. \
                        Exclude any follow up and just provide an answer and do not seek anymore input."
                }
            ]
        )

        return completion


class JagaimoClient(OpenAIClient):
    """Object used to translate given text from Japanese to English.
    """
    def __init__(self) -> None:
        """Initializes the instance of the class.
        
        This method initializes the instance of the class by setting up the translator using the DEEPL_KEY and calling the parent class's initializer.
        
        Attributes:
            translator (deepl.Translator): An instance of the deepl.Translator class initialized with the DEEPL_KEY.
        
        Returns:
            None
        """
        logger.info('Creating Jagaimo client...')
        self.translator = deepl.Translator(DEEPL_KEY)
        super().__init__()


    def deepl(self, text: str) -> str:
        """This method translates the given text to English using DeepL translator.
        
        Args:
            text (str): The text to be translated.
        
        Returns:
            str: The translated text in English.
        """
        
        translation = self.translator.translate_text(text, target_lang='EN-US')

        return translation.text


    def suggest(self, text: str, v: int = 2) -> str:
        """This method is used to generate a suggestion based on the provided text.
        
        Args:
            text (str): The text based on which a suggestion is to be generated.
            v (int, optional): An integer value used in the suggestion generation process. Defaults to 2.
        
        Returns:
            str: The content of the first message in the generated suggestions.
        """
        
        suggestion: str = self.get_suggestion(text, v)

        return suggestion.choices[0].message.content


if __name__ == '__main__':
    client = JagaimoClient()
    print(client.suggest(text='今日はあなたのトイレはじゃない', v=1))
