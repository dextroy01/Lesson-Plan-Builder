import pandas as pd
from google import genai
from google.genai import types
import json
from schemas import GeminiConfigurations, GeminiOutputFormat, GeminiPromptAnatomy

class PromptBuilder:
    def __init__(self, client: genai.Client, configurations: GeminiConfigurations, prompt_anatomy : GeminiPromptAnatomy):
        self.client = client
        self.configurations = configurations
        self.prompt_anatomy = prompt_anatomy
        self.final_prompt = ""
        self.past_lessons: str | None = None
        
    def read_past_lessons(self, filepath: str) -> None:
        self.past_lessons = ""
        past_lessons_data = pd.read_csv(filepath)
        for index, row in past_lessons_data.iterrows():
            self.past_lessons += (f"lesson {index}:\n {row.to_string()}\n\n")
    
    def create_final_prompt(self) -> None:
        for key, value in self.prompt_anatomy.model_dump().items():
            self.final_prompt += f"{key}: {value}\n\n"
        self.final_prompt += f"past lessons:\n\n{self.past_lessons}"

    def call_gemini(self) -> str:   
        configurations_dict = self.configurations.model_dump()
        gemini_version = configurations_dict.pop("gemini_version")
        response = self.client.models.generate_content(model = gemini_version, 
                                                       contents = self.final_prompt,
                                                       config = types.GenerateContentConfig(**configurations_dict, response_schema = GeminiOutputFormat))     
        output = response.parsed 
        return output  

    def call_deep_research(self,) -> str:
        pass
        
if __name__ == "__main__":
   

    config_file_path = "test_config.json"
    with open(config_file_path, "r") as file:
        config_dict = json.load(file)

    model_configurations = GeminiConfigurations(**config_dict["Gemini Configurations"])
    prompt_anatomy = GeminiPromptAnatomy(**config_dict["Prompt Anatomy"])
    
    master_client = genai.Client(api_key = my_api_key)
    data_filepath = "test_data.csv"

    prompt_builder = PromptBuilder(master_client, model_configurations, prompt_anatomy)
    prompt_builder.read_past_lessons(data_filepath)
    
    final_prompt = prompt_builder.create_final_prompt()

    print("Input Prompt")
    print(final_prompt)
    
    try:
        output = prompt_builder.call_gemini(final_prompt)
        print("\nGemini Output")
        print(output)
    except Exception as exception_message:
        print(f"error:  {exception_message}")

