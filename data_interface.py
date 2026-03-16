from schemas import EmailConfigurations, GeminiPromptAnatomy, GeminiConfigurations

class DataInterface:
    def read_lesson_data():
        pass
    
    def write_lesson_data():
        pass

    def write_review_data():
        pass

    def read_config_data(filepath : str) -> tuple[EmailConfigurations, GeminiConfigurations, GeminiPromptAnatomy]:
        pass