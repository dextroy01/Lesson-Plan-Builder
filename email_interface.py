import smtplib
from data_interface import DataInterface
import os
from dotenv import load_dotenv
from email.message import EmailMessage
from schemas import EmailConfigurations, GeminiOutputFormat
from imap_tools import MailBox, AND

class EmailInterface:
    def send_email(lesson_plan: GeminiOutputFormat, email_configuration : EmailConfigurations, password : str) -> None:
        message = EmailMessage()
        message["From"] = email_configuration.my_inbox
        message["To"] = email_configuration.receiver
        message["Subject"] = f"Todays Lesson: {lesson_plan.title}"
        message.set_content(lesson_plan.body)
        
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(email_configuration.my_inbox, password)
            server.send_message(message)
        print("Success: sent email")


    def format_gemini_output() -> dict:
        pass


    def read_review_email(lesson_title : str, email_data : EmailConfigurations, password : str) -> str | None:
        email_username = email_data.my_inbox

        with MailBox("imap.gmail.com").login(email_username, password, "Inbox") as mb:
            generator = mb.fetch(AND(subject = f"Re: Todays Lesson: {lesson_title}"))

            email_reply = next(generator, None)
            if email_reply is None: 
                print('No reply email')
                return None
            
            print("Succes found reply email")
            return email_reply.text
    
    def format_reply() -> str:
        pass
    
if __name__ == "__main__":
    print("In email interface\n")
    
    load_dotenv()
    gmail_api_key = os.getenv("GMAIL_API_KEY")

    file_path = "test_config.json"
    email_configurations, gemini_configurations, gemini_prompt_anatomy = DataInterface.read_config_data(file_path)
    test_gemini_output = GeminiOutputFormat(**{"title": "gmail title test 2", "test": True, "body": "gmail body test 2 body"})
    
    
    test_1 = False
    test_2 = False
    test_3 = True
    
    if test_1:
        print("test 1\n")
        EmailInterface.send_email(test_gemini_output,email_configurations,gmail_api_key)
    elif test_2:
        print("test 2\n")
        lesson_title = "non existent title"
        fake_reply = EmailInterface.read_review_email(lesson_title, email_configurations, gmail_api_key)
        print(fake_reply)
    elif test_3:
        print("test 3\n")

        lesson_title = test_gemini_output.title
        real_reply = EmailInterface.read_review_email(lesson_title, email_configurations, gmail_api_key)
        print(real_reply)
    
    
    