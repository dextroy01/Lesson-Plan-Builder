from pydantic import BaseModel

class GeminiOutputFormat(BaseModel):
   title: str
   test: bool
   body: str

class GeminiConfigurations(BaseModel):
    gemini_version : str
    system_instruction : str
    response_mime_type : str

class GeminiPromptAnatomy(BaseModel):
    role: str 
    task: str 
    context: str 
    output_format: str 

class EmailConfigurations(BaseModel):
    sender: str
    receiver: str
    gemini_output: dict