import smtplib
from data_interface import DataInterface
import os
from dotenv import load_dotenv
from email.message import EmailMessage
from schemas import EmailConfigurations, GeminiOutputFormat
from imap_tools import MailBox, AND
from datetime import date

class EmailInterface:
    def send_email(lesson_plan: GeminiOutputFormat, email_configuration : EmailConfigurations, password : str, html : bool = False) -> None:
        message = EmailMessage()
        message["From"] = email_configuration.my_inbox
        message["To"] = email_configuration.receiver
        message["Subject"] = f"Todays Lesson: {lesson_plan.title}"

        if html is True:
            message.set_content(lesson_plan.body, subtype = "html")
        else:
            message.set_content(lesson_plan.body)
        
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(email_configuration.my_inbox, password)
            server.send_message(message)
        print("Success: Sent email to receivers")


    def read_review_email(lesson_title : str, email_data : EmailConfigurations, password : str) -> str | None:
        email_username = email_data.my_inbox

        with MailBox("imap.gmail.com").login(email_username, password, "Inbox") as mb:
            generator = mb.fetch(AND(subject = f"Re: Todays Lesson: {lesson_title}"))

            email_reply = next(generator, None)
            if email_reply is None: 
                print('No reply email')
                return None
            
            print("Success: Found reply email in inbox")
            raw_reply = email_reply.text
            formatted_reply = EmailInterface.format_email_reply(raw_reply)
            return formatted_reply
    
    def format_email_reply(raw_reply: str) -> str:
        normalized_text = raw_reply.replace('\r\n', '\n')
        parts = normalized_text.split('\nOn ', 1)
        formatted_reply = parts[0].strip()
        return formatted_reply
    
if __name__ == "__main__":
    print("In email interface\n")
    
    load_dotenv()
    gmail_api_key = os.getenv("GMAIL_API_KEY")

    file_path = "test_config.json"
    email_configurations, gemini_prompt_anatomy = DataInterface.read_config_data(file_path)
    test_gemini_output = GeminiOutputFormat(**{"title": "gmail title test 2", "test": True, "body": "gmail body test 2 body"})
    
    
    test_1 = False
    test_2 = False
    test_3 = False
    test_4 = False
    test_5 = True
    
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

    elif test_4:
        print("test 4:")

        example_html = r"""
            <div style="font-family: sans-serif;">
                <h2>Test Lesson Title</h2>
                <p>This is a test of the lesson body.</p>
                <p><strong>Test Review:</strong> Test successful.</p>
            </div>
        """
        test_lesson_plan = GeminiOutputFormat(**{"title": 'html test 2', "test" : True, "body" : example_html})
        EmailInterface.send_email(test_lesson_plan, email_configurations, gmail_api_key, html = True)
    elif test_5:
        print("test 5\n")
        test_lesson= GeminiOutputFormat(**{"title": "main test 1", "test": True, "body": "testing main body 1"})
        lesson_title = test_lesson.title
        real_reply = EmailInterface.read_review_email(lesson_title, email_configurations, gmail_api_key)
        print(real_reply)

    
    