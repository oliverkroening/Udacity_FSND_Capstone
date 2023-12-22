from dotenv import load_dotenv
import os
load_dotenv()
DATABASE_URL = os.environ.get("DATABASE_URL")
DATABASE_URL_TEST=os.environ.get("DATABASE_URL_TEST")
casting_assistant_token = os.environ.get("casting_assistant_token")
casting_director_token = os.environ.get("casting_director_token")
executive_director_token = os.environ.get("executive_director_token")