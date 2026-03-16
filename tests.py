from google import genai
from dotenv import load_dotenv
from google.genai import types
from pydantic import BaseModel
import os

class Gemini_Output_Format(BaseModel):
   test: bool
   body: str
   other: int

class Agent_Caller:

   ''''''''''''''''''''''
   Gemini test code
    '''''''''''''''''''''
   load_dotenv()


   client = genai.Client(api_key = os.getenv("GEMINI_API_Key"))


   config_dict = {'system_instruction': 'this is test', 'response_mime_type': 'application/json'}

   model_config = types.GenerateContentConfig(**config_dict, response_schema = Gemini_Output_Format)


   def call_gemini(self) -> str:
      response = Agent_Caller.client.models.generate_content(model = "gemini-3-flash-preview", 
                                                             contents = "This is a test, confrim that is true",
                                                             config = self.model_config)   
      output = response.parsed  
      return output  
   
   def call_deep_research() -> None:
      response = Agent_Caller.client.interactions.create(agent="deep-research-pro-preview-12-2025",
                                                        input="this is a test of deep research",  # Pass the heavy prompt
                                                        background=True,  
                                                        response_format=Gemini_Output_Format.model_json_schema(), 
                                                        response_mime_type="application/json"
                                                                                           )
      print(f"research started: {response.id}")


if __name__ == "__main__":
   
   print("In agent caller\n")



   #Agent_Caller.call_deep_research()


   #print("pydantic test")
   #pydantic_test = Gemini_Output_Format(test=True, body="test", other=5)
   #print(pydantic_test)
   #print(pydantic_test.model_dump())


   print("\ngemini test")
   new_agent = Agent_Caller()
   output = new_agent.call_gemini()
   print(output)
   

   #dict = {"cat": "meow", "dog":"roof"}
   #my_string = ""
   #for key, value in dict.items():
   #   my_string += f"{key}: {value}\n"
   #print(my_string)
   #print(dict)

   #popped = dict.pop("cat")

   #print(dict)

   #print(f"\npopped : {popped}")