import smtplib
import json
import os
from dotenv import load_dotenv
from email.message import EmailMessage
from schemas import Email_Data, Gemini_Output_Format
from imap_tools import MailBox, AND

class Email_Interface:
    def send_email(email_data : Email_Data, password : str) -> None:
        gemini_ouput = Gemini_Output_Format(**email_data.gemini_output)
    
        message = EmailMessage()
        message["From"] = email_data.sender
        message["To"] = email_data.receiver
        message["Subject"] = f"Todays Lesson: {gemini_ouput.title}"
        message.set_content(gemini_ouput.body)
        
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(email_data.sender, password)
            server.send_message(message)

    def format_email() -> str:
        pass

    def read_email(email_data : Email_Data, password : str) -> str:
        gemini_ouput = Gemini_Output_Format(**email_data.gemini_output)
        email_username = email_data.sender

        with MailBox("imap.gmail.com").login(email_username, password, "Inbox") as mb:
            for email_reply in mb.fetch(AND(subject = f"Re: Todays Lesson: {gemini_ouput.title}")):
                print(email_reply.text)

if __name__ == "__main__":
    print("In email interface\n\n")
       

    ###################
    #SMTP password. delete me
    #google_password = "rmkz byyp sitz hwlw"

    ###################

    load_dotenv()
    gmail_password = os.getenv("GMAIL_PASSWORD")

    
    with open("test_config.json", "r") as file:
        config_dict = json.load(file)
    
    test_gemini_output ={"title": "test title 4", "test": True, "body": "test 2 body"}

    email_data = Email_Data(**config_dict["Email_Data"])
    email_data.gemini_output = test_gemini_output


    try:
        Email_Interface.send_email(email_data, gmail_password)
        print("email sent as success")
    except Exception as e:
        print(f"error: {e}")

    
    
    #Email_Interface.read_email(email_data, google_password)
    
    
    