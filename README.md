# Twitter Bot Automation

This project automates interactions with the Twitter API using `tweepy`. It is designed to fetch tweets, process them, and post responses. Additionally, it includes email notifications for error handling and logging capabilities.

## Features

- **Twitter API Integration**: Fetch and post tweets using Twitter API v2.
- **Error Handling**: Logs errors and sends email notifications for critical failures.
- **Rate Limit Management**: Automatically handles rate limit errors by retrying after the specified reset time.
- **Configurable Environment**: Manage sensitive credentials and configurations using an `.env` file.

## Requirements

- Python 3.8+
- Twitter Developer Account with API keys
- Gmail account for email notifications (or any SMTP-compatible email)

## Installation

1. **Fork and Clone the Repository**
   ```bash
   git clone <your-forked-repo-url>
   cd <repository-folder>
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**
   Create a `keys.env` file in the root directory with the following format:
   ```env
   # Twitter API credentials
   BEARER_TOKEN=<your_bearer_token>
   API_KEY=<your_api_key>
   API_SECRET=<your_api_secret>
   ACCESS_TOKEN=<your_access_token>
   ACCESS_SECRET=<your_access_secret>

   # Email server configuration
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   EMAIL_ADDRESS=<your_email>
   EMAIL_PASSWORD=<your_email_password>
   BOSS_EMAIL=<your_boss_email>

   # Other configurations
   USER_HANDLE=<your_twitter_handle>
   ```

5. **Run the Bot**
   ```bash
   python twitter_bot.py
   ```

## File Structure

- `twitter_bot.py`: Main script that handles Twitter API interactions, logging, and email notifications.
- `testapi.py`: Script to test Twitter API credentials.
- `app.log`: Log file for errors and events (ignored by Git).
- `keys.env`: Contains sensitive credentials (ignored by Git).
- `requirements.txt`: Python dependencies for the project.

## Contributing

1. **Fork the Repository**: Click the fork button at the top of this page.
2. **Clone Your Fork**: Clone your forked repository to your local machine.
   ```bash
   git clone <your-forked-repo-url>
   ```
3. **Create a New Branch**: Create a feature branch for your changes.
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Make Changes and Commit**:
   ```bash
   git add .
   git commit -m "Add your message"
   ```
5. **Push to Your Fork**:
   ```bash
   git push origin feature/your-feature-name
   ```
6. **Submit a Pull Request**: Open a pull request to merge your changes into the main repository.
