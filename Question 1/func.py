from datetime import datetime
import cx_Oracle
import json 
import google.generativeai as genai
from pathlib import Path


def fetch_query(language_1, language_2, query):
        GOOGLE_API_KEY = 'AIzaSyAGR-wIqNxheCKsHoNynWXrmrgk_nGk8sc'
        genai.configure(api_key=GOOGLE_API_KEY)
        
        generation_config = {
            "temperature": 0.5,
            "top_p": 1,
            "top_k": 32,
            "max_output_tokens": 4096,
        }
        
        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            }
        ]
        model = genai.GenerativeModel(model_name="gemini-pro",
                                      generation_config=generation_config,
                                      safety_settings=safety_settings
                                      )
        
        input_prompt = f'''

        You are expert in translating language from {language_1} to {language_2}. You will be given word or sentence. Convert than from language 1 to language 2.

        '''

        
            
        output = generate_gemini_response(model,query,input_prompt)  
        # print(output)
        return output


def generate_gemini_response(model, query, input_prompt):
    prompt_parts = [input_prompt, query]
    response = model.generate_content(prompt_parts) 
    response = response.text
    return response 

# language_1='English'
# language_2= 'fren'
# query = 'I have laptop in my home'

# fetch_query(language_1, language_2, query)