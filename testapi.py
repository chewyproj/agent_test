import tweepy
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="keys.env")

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")

try:
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth)
    print("Verifying credentials...")
    api.verify_credentials()
    print("Twitter API authentication successful!")
except Exception as e:
    print(f"Twitter API authentication failed: {e}")
