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

    email_configurations, gemini_configurations, gemini_prompt_anatomy = DataInterface.read_config_data(configurations_filepath)
    previous_lesson_review = EmailInterface.read_review_email(email_configurations, gmail_api_key)
    DataInterface.write_review_data(previous_lesson_review)

    prompt_builder = PromptBuilder(gemini_client, gemini_configurations, gemini_prompt_anatomy)
    prompt_builder.read_past_lessons()
    prompt_builder.create_final_prompt()
    raw_lesson_plan = prompt_builder.call_deep_research()
    
    formatted_lesson_plan = EmailInterface.format_gemini_output(raw_lesson_plan)
    DataInterface.write_lesson_data(formatted_lesson_plan)
    EmailInterface.send_email(formatted_lesson_plan)


if __name__ == "__main__":
    main()