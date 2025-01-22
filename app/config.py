class Config:
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "STDF Analyzer"

    UPLOAD_FOLDER: str = "uploads"
    MAX_FILE_SIZE: int = 16 * 1024 * 1024  # 16MB


config = Config()
