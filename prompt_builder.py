import pandas as pd
from google import genai
from google.genai import types
import json
import time
import os
from dotenv import load_dotenv
from schemas import GeminiOutputFormat, GeminiPromptAnatomy
from data_interface import DataInterface

class PromptBuilder:
    def __init__(self, client: genai.Client,  prompt_anatomy : GeminiPromptAnatomy):
        self.client = client
        self.prompt_anatomy = prompt_anatomy
        self.past_lessons = ""
        self.final_prompt = ""
        
        
    def get_past_lessons(self, past_lessons : list) -> None:
        for id, row in enumerate(past_lessons):
            lesson = f"Lesson {id}:\n"
            lesson += f"Title: {row[0]}\n"
            lesson += f"Lesson Body: {row[1]}\n"
            lesson += f"Lesson Review {row[2]}\n"
            lesson += "-----------------------------------------\n"
            self.past_lessons += lesson
    

    def create_final_prompt(self) -> None:
        for key, value in self.prompt_anatomy.model_dump().items():
            self.final_prompt += f"{key}: {value}\n\n"
        self.final_prompt += f"past lessons:\n\n{self.past_lessons}"
    
    
    def call_deep_research(self,):
            interaction = self.client.interactions.create(agent = "deep-research-pro-preview-12-2025",
                                                    input = self.final_prompt, 
                                                    background = True,
                                                    response_format = GeminiOutputFormat.model_json_schema(), 
                                                    response_mime_type = "application/json")
            print(f"research started: {interaction.id}")

            while True:
                interaction = self.client.interactions.get(interaction.id)
                if interaction.status == "completed":
                    print("Success: Created gemini deep research lesson")
                    return (interaction.outputs[-1].text)
                elif interaction.status == "failed":
                    print(f"Research failed: {interaction.error}")
                    break
                print(".", end = "", flush = True)
                time.sleep(10)
            
   
    def format_using_gemini(self, raw_lesson_plan: str) -> GeminiOutputFormat:   
        response = self.client.models.generate_content(model = "gemini-3-flash-preview", 
                                                       contents = raw_lesson_plan,
                                                       config = {'response_schema' : GeminiOutputFormat,
                                                                 'response_mime_type': 'application/json',
                                                                 'system_instruction': "Take the following lesson plan and extract it into the required JSON schema. Turn the body into html so it can be displayed as html"})     
        output = response.parsed 
        print("Success: Used Gemini to format deep research lesson")
        return output  

       
if __name__ == "__main__":

    print("In prompt builder\n")
    
    load_dotenv()
    gemini_api_key = os.getenv("GEMINI_API_KEY")

    file_path = "test_config.json"
    email_configurations,  gemini_prompt_anatomy = DataInterface.read_config_data(file_path)
    master_client = genai.Client(api_key = gemini_api_key)
    database = DataInterface("testdatabase.db")
    
    
    test_1 = False
    test_2 = True 

    if test_1:
        prompt_builder = PromptBuilder(master_client, gemini_prompt_anatomy)
        past_lessons = database.fetch_all_lesson_data()
        prompt_builder.get_past_lessons(past_lessons)
        prompt_builder.create_final_prompt()

        print("final prompt\n")
        print(prompt_builder.final_prompt)

        output = prompt_builder.call_deep_research()

        print("Deep research output\n")
        print(output)
    
    elif test_2:
        print("Test 2\n")

        example_html = r"""
            <div style="font-family: sans-serif;">
                <h2>Test Lesson Title</h2>
                <p>This is a test of the lesson body.</p>
                <p><strong>Test Review:</strong> Test successful.</p>
            </div>
        """
        prompt_builder = PromptBuilder(master_client, gemini_prompt_anatomy)
        output = prompt_builder.format_using_gemini(example_html)

        print("Example output:\n")
        print(output)
        print(type(output))
    