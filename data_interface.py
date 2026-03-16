from schemas import EmailConfigurations, GeminiPromptAnatomy, GeminiConfigurations
import sqlite3
import json

class DataInterface:

    def __init__(self, database_name : str):
        self.db_name = database_name
        self.connection = sqlite3.connect(database_name)
        self.cursor = self.connection.cursor()
        self._build_table()


    def _build_table(self) -> None:
        self.cursor.execute("""  
            CREATE TABLE IF NOT EXISTS lessons(
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       lesson_date TEXT,
                       lesson_title TEXT,
                       lesson_body TEXT,
                       lesson_review TEXT
                       )""")
        self.connection.commit()
        print(f"Success: Connected to {self.db_name} and verified columns")

        
    def read_all_lesson_data(self) -> list:
        sql = "SELECT lesson_title, lesson_body, lesson_review FROM LESSONS"
        self.cursor.execute(sql)
        all_lesson_data = self.cursor.fetchall()
        return all_lesson_data
    
    
    def write_lesson_data(self, lesson_date: str, lesson_title: str, lesson_body: str) -> None:
        sql = """
            INSERT INTO lessons (lesson_date, lesson_title, lesson_body)
            VALUES (?, ?, ?)
        """

        self.cursor.execute(sql, (lesson_date, lesson_title, lesson_body))
        self.connection.commit()
        print("Success: added lesson data")


    def write_review_data(self, lesson_review : str) -> None:
        sql = """
            UPDATE lessons
            SET lesson_review = ?
            WHERE id = (SELECT MAX(id) from lessons)
        """
        self.cursor.execute(sql, (lesson_review,))
        self.connection.commit()
        print("success: added review")

    
    def read_most_recent_title(self) -> str:
        sql = "SELECT lesson_title FROM lessons ORDER BY id DESC LIMIT 1"
        self.cursor.execute(sql)

        most_recent_title = self.cursor.fetchone()

        if most_recent_title is None:
            return "No lesson found"
        
        return most_recent_title[0]



    def read_config_data(filepath : str) -> tuple[EmailConfigurations, GeminiConfigurations, GeminiPromptAnatomy]:
        with open(filepath, "r") as file:
            config_dict = json.load(file)
        gemini_configurations = GeminiConfigurations(**config_dict["Gemini Configurations"])
        prompt_anatomy = GeminiPromptAnatomy(**config_dict["Prompt Anatomy"])
        email_configurations = EmailConfigurations(**config_dict["Email_Data"])
        return email_configurations, gemini_configurations, prompt_anatomy
    

if __name__ == "__main__":

    test_1 = False
    test_2 = True

    if test_1 :
        database_name = "testdatabase.db"
        test_database = DataInterface(database_name)

        test_database.write_lesson_data("Test date 1", "Test title 1", "Test body 1")
        test_database.write_review_data("Test review 1")

        most_recent_title_1 = test_database.read_most_recent_title()

        test_database.write_lesson_data("Test date 2", "Test title 2", "Test body 2")
        test_database.write_review_data("Test review 2")

        most_recent_title_2 = test_database.read_most_recent_title()

        print(f"Test:\n 1st title should be: Test title 1\n 1st title is {most_recent_title_1}")
        print(f"Test:\n 2nd title should be: Test title 2\n 2nd title is {most_recent_title_2}")
    elif test_2:
        database_name = "testdatabase.db"
        test_database = DataInterface(database_name)

        test_database.write_lesson_data("Test date 3", "Test title 3", "Test body 3")
        test_database.write_review_data("Test review 3")