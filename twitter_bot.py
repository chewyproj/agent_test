import tweepy
from datetime import datetime, time
import logging
import smtplib
import os
from dotenv import load_dotenv
import time

# load environment variables from .env file
load_dotenv(dotenv_path="keys.env")

# logging setup
logging.basicConfig(filename="app.log", level=logging.ERROR)

# credentials from environment variables
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
BOSS_EMAIL = os.getenv("BOSS_EMAIL")

USER_HANDLE = os.getenv("USER_HANDLE", "snafudefi")
ELON_MUSK_HANDLE = "elonmusk"

print(f"API_KEY: {API_KEY}")
print(f"API_SECRET: {API_SECRET}")
print(f"ACCESS_TOKEN: {ACCESS_TOKEN}")
print(f"ACCESS_SECRET: {ACCESS_SECRET}")
print(f"BEARER_TOKEN: {BEARER_TOKEN}")

client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_SECRET
)

processed_tweets = set()

# ---------------------------------------------------------------
# Function: verify_authentication(client)
# Verifies the Twitter API authentication credentials.
# Parameters:
#   - client: An instance of `tweepy.Client`.
# Returns:
#   - None. Prints the authentication status to the console.
# Exceptions:
#   - Handles `tweepy.errors.Unauthorized` and other exceptions.
# ---------------------------------------------------------------
def verify_authentication(client):
    try:
        print("Verifying Twitter API authentication...")
        user = client.get_me()
        print(f"Authentication successful! Authenticated as: {user.data.username}")
    except tweepy.errors.Unauthorized as e:
        print("Authentication failed: Unauthorized. Please check your credentials.")
        print(f"Error details: {e}")
    except Exception as e:
        print(f"Authentication failed: {e}")

# ---------------------------------------------------------------
# Function: check_rate_limits(client, user_id)
# Checks the rate limit for fetching tweets from a specific user.
# Parameters:
#   - client: An instance of `tweepy.Client`.
#   - user_id: The Twitter user ID to check the rate limits for.
# Returns:
#   - The remaining number of API requests allowed or `None` if an error occurs.
# ---------------------------------------------------------------
def check_rate_limits(client, user_id):
    try:
        response = client.get_users_tweets(
            id=user_id,
            max_results=5,
            tweet_fields=["id", "text"]
        )
        remaining = response.meta.get("x-rate-limit-remaining")
        reset = response.meta.get("x-rate-limit-reset")
        print(f"Rate limit remaining: {remaining}")
        if reset:
            reset_time = datetime.fromtimestamp(int(reset))
            print(f"Rate limit resets at: {reset_time}")
        return remaining
    except Exception as e:
        print(f"Failed to check rate limits: {e}")
        return None

# ---------------------------------------------------------------
# Function: is_business_hours()
# Determines whether the current time is within business hours.
# Returns:
#   - True (currently hardcoded).
# ---------------------------------------------------------------
def is_business_hours():
    return True

# ---------------------------------------------------------------
# Function: create_post(client, tweet)
# Creates and posts a tweet in response to a given tweet.
# Parameters:
#   - client: An instance of `tweepy.Client`.
#   - tweet: A dictionary containing tweet details (`id` and `text`).
# Returns:
#   - None. Posts the tweet and logs the result to the console or error log.
# Exceptions:
#   - Logs any errors encountered during the tweet creation.
# ---------------------------------------------------------------
def create_post(client, tweet):
    try:
        post_content = (
            f"🚀 Attention @{ELON_MUSK_HANDLE} 🚀\n\n"
            f"Snafu (@{USER_HANDLE}) is actively sharing updates:\n\n"
            f"{tweet['text']}\n\n"
            f"Check it out here: https://x.com/{USER_HANDLE}/status/{tweet['id']}"
        )
        print("Attempting to post the following content:")
        print(post_content)

        print("Sending request to Twitter API for posting...")
        response = client.create_tweet(text=post_content)

        print("Response from Twitter API:")
        print(response)
        if response.errors:
            print("Errors during tweet creation:")
            print(response.errors)
        else:
            print("Tweet created successfully. Response data:")
            print(response.data)

        print("Successfully posted on X!")
    except Exception as e:
        logging.error(f"Failed to post on X: {e}")
        print(f"Error during posting: {e}")

# ---------------------------------------------------------------
# Function: send_email(subject, body)
# Sends an email notification.
# Parameters:
#   - subject: The subject of the email.
#   - body: The body content of the email.
# Returns:
#   - None. Sends the email and logs the result to the console or error log.
# Exceptions:
#   - Logs any errors encountered during email sending.
# ---------------------------------------------------------------
def send_email(subject, body):
    try:
        print("Sending email notification...")
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            message = f"Subject: {subject}\n\n{body}"
            server.sendmail(EMAIL_ADDRESS, BOSS_EMAIL, message)
        print("Email sent successfully.")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")

# ---------------------------------------------------------------
# Function: fetch_tweets_v2(client, user_handle, since_id=None)
# Fetches tweets from a specific user using the Twitter API v2.
# Parameters:
#   - client: An instance of `tweepy.Client`.
#   - user_handle: The Twitter handle of the user to fetch tweets for.
#   - since_id: Optional. The ID of the last processed tweet to fetch newer tweets.
# Returns:
#   - A list of new tweets as `tweepy.Tweet` objects or an empty list if no new tweets are found.
# Exceptions:
#   - Handles rate limit errors by waiting and retrying.
#   - Logs other errors and sends an email notification.
# ---------------------------------------------------------------
def fetch_tweets_v2(client, user_handle, since_id=None):
    try:
        print("Fetching tweets using API v2...")
        user = client.get_user(username=user_handle).data
        print(f"User ID: {user.id}")

        tweets = client.get_users_tweets(
            id=user.id,
            max_results=5,
            since_id=since_id,
            tweet_fields=["id", "text"]
        )
        print(f"API Response: {tweets}")
        if tweets.data:
            print(f"Fetched {len(tweets.data)} tweets.")
            new_tweets = [tweet for tweet in tweets.data if tweet.id not in processed_tweets]
            for tweet in new_tweets:
                processed_tweets.add(tweet.id)
                print(f"New Tweet ID: {tweet.id}, Text: {tweet.text}")
            return new_tweets
        else:
            print("No new tweets to fetch.")
            return []
    except tweepy.errors.TooManyRequests as e:
        reset_time = int(e.response.headers.get("x-rate-limit-reset", time.time()))
        wait_time = reset_time - int(time.time())
        print(f"Rate limit hit. Retrying after {wait_time} seconds.")
        time.sleep(wait_time)
        return fetch_tweets_v2(client, user_handle, since_id)
    except Exception as e:
        logging.error(f"Failed to fetch tweets: {e}")
        print(f"Error details: {e}")
        send_email("Script Error: Tweet Fetching Failed", str(e))
        return []

# ---------------------------------------------------------------
# Function: main(request)
# Main function to coordinate the bot's operations.
# Parameters:
#   - request: Placeholder parameter for request data (not used in the current implementation).
# Returns:
#   - None. Fetches tweets, processes them, and posts responses.
# Exceptions:
#   - Handles any exceptions encountered in the main logic.
# ---------------------------------------------------------------
def main(request):
    print("Starting Twitter bot...")

    verify_authentication(client)

    last_tweet_id = max(processed_tweets) if processed_tweets else None
    tweets = fetch_tweets_v2(client, USER_HANDLE, since_id=last_tweet_id)
    if not tweets:
        print("No new tweets to process.")
        return

    for tweet in tweets:
        print(f"Processing tweet ID {tweet.id}: {tweet.text}")
        if is_business_hours():
            create_post(client, {"id": tweet.id, "text": tweet.text})

if __name__ == "__main__":
    while True:
        try:
            print("Starting main loop...")
            main(request=None)
        except Exception as e:
            logging.error(f"Error in main loop: {e}")
            print(f"Error occurred: {e}")
        print("Waiting for the next iteration...")
        time.sleep(60)
