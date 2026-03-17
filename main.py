from data_interface import DataInterface
from email_interface import EmailInterface
from prompt_builder import PromptBuilder
from dotenv import load_dotenv
from schemas import *
from google import genai
import os


def new_test():
    print("In main new test")

    load_dotenv()
    gmail_api_key = os.getenv("GMAIL_API_KEY")
    configurations_filepath = "test_config.json"
    email_configurations, gemini_prompt_anatomy = DataInterface.read_config_data(configurations_filepath)
    database_name = "main_test_database"
    main_test_database = DataInterface(database_name)
    test_lesson= GeminiOutputFormat(**{"title": "main test 1", "test": True, "body": "testing main body 1"})
    EmailInterface.send_email(test_lesson, email_configurations, gmail_api_key)
    main_test_database.insert_lesson_data(test_lesson)


def main():
    print("In main\n")

    load_dotenv()
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    gmail_api_key = os.getenv("GMAIL_API_KEY")
    gemini_client = genai.Client(api_key= gemini_api_key)
    configurations_filepath = "test_config.json"
    database_name = "main_test_database"
    database = DataInterface(database_name)
    email_configurations, gemini_prompt_anatomy = DataInterface.read_config_data(configurations_filepath)

    previous_lesson_title = database.fetch_most_recent_title()
    previous_lesson_review = EmailInterface.read_review_email(previous_lesson_title, email_configurations, gmail_api_key)
    database.update_review_data(previous_lesson_review)

    prompt_builder = PromptBuilder(gemini_client, gemini_prompt_anatomy)
    raw_past_lessons = database.fetch_all_lesson_data()
    prompt_builder.get_past_lessons(raw_past_lessons)
    prompt_builder.create_final_prompt()
    #raw_lesson_plan = prompt_builder.call_deep_research()

    raw_lesson_plan = f"This is test lesson plan title 4\nThis is test lesson plan header 4\nThis is a test lesson plan body 4"
    formatted_lesson_plan = prompt_builder.format_using_gemini(raw_lesson_plan)
    
    database.insert_lesson_data(formatted_lesson_plan.title, raw_lesson_plan)
    EmailInterface.send_email(formatted_lesson_plan, email_configurations, gmail_api_key, html = True)


if __name__ == "__main__":
    main()
    #new_test()