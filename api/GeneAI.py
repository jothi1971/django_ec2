import google.generativeai as genai
import os

def create_content(model,search_string):
    print("create content called ")
    print(model)
    print(search_string)
    genai.configure(api_key=os.environ["AI_API_KEY"])
    model = genai.GenerativeModel(model)
    response = model.generate_content(search_string)
    print(response.text)
    
    return response.text

    
