from data_interface import DataInterface
from email_interface import EmailInterface
from prompt_builder import PromptBuilder
from dotenv import load_dotenv
from google import genai
import os

def main():
    load_dotenv()
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    gmail_api_key = os.getenv("GMAIL_API_KEY")
    gemini_client = genai.Client(api_key= gemini_api_key)
    configurations_filepath = "test.config.json"
    database_name = "testdatabase.db"
    database = DataInterface(database_name)

    email_configurations, gemini_configurations, gemini_prompt_anatomy = DataInterface.read_config_data(configurations_filepath)
    previous_lesson_title = database.read_most_recent_title()
    previous_lesson_review = EmailInterface.read_review_email(previous_lesson_title, email_configurations, gmail_api_key)
    DataInterface.write_review_data(previous_lesson_review)

    prompt_builder = PromptBuilder(gemini_client, gemini_configurations, gemini_prompt_anatomy) # fix me
    prompt_builder.read_past_lessons() # fix me
    prompt_builder.create_final_prompt() # fix me
    raw_lesson_plan = prompt_builder.call_deep_research() # fix me
    e
    DataInterface.write_lesson_data(formatted_lesson_plan) # fix me
    EmailInterface.send_email(formatted_lesson_plan) # fix me


if __name__ == "__main__":
    main()