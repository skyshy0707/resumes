import os

class Config:

    BASE_URL_API = "http://127:0.0.1:9006/api"
    BASE_URL_FRONTEND = "http://127:0.0.1:9000"
    GENERAL_KEY_LENGTH = 512

    class basic_auth:
        ALGORITHM = "sha512"
        SECRET_KEY = "328fcc6169f5579f7ac43e3353df3ca5e3ac11f1bfc454ce9ebf3ebbba666b492b53eb156ed7ba510e1407625631927a19cb5ed6f47186f0a20fe9249030484e"
        
    class jwt_auth:
        ALGORITHM = "HS512"
        SECRET_KEY = "25734bc4d158316e3b6729a30f374de85c9efa6fb0f975513da1795551ea98219b91f7a2a7fb18be573dc1ba491dd4eb5ad197bbe824e9140bd0033f032af18a"
        EXPIRES_IN = 172800


    class openai:

        API_KEY = ""

    class db:
        POSTGRES_DB_USER = os.getenv("POSTGRES_DB_USER")
        POSTGRES_DB_HOST = os.getenv("POSTGRES_DB_HOST")
        POSTGRES_DB_NAME = os.getenv("POSTGRES_DB")