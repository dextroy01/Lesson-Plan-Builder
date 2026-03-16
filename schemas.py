from pydantic import BaseModel

class Gemini_Output_Format(BaseModel):
   title: str
   test: bool
   body: str

class Gemini_Configurations(BaseModel):
    gemini_version : str
    system_instruction : str
    response_mime_type : str

class Gemini_Prompt_Anatomy(BaseModel):
    role: str 
    task: str 
    context: str 
    output_format: str 

class Email_Data(BaseModel):
    sender: str
    receiver: str
    gemini_output: dict