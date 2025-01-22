import requests
from bs4 import BeautifulSoup
from telegram import Bot
import time
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Telegram Bot Configuration
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
bot = Bot(token=TELEGRAM_TOKEN)

# Expanded Keywords for News Search
KEYWORDS = [
    # General Tech Topics
    "Tech", "AI", "technology news", "latest in tech", "tech trends",
    "hiring in tech", "firing in tech companies", "startup news", 
    "innovation in technology", "technology layoffs", "tech updates",

    # AI Topics
    "Artificial Intelligence", "AI advancements", "Machine Learning",
    "Deep Learning", "NLP", "Natural Language Processing", "Generative AI",
    "AI ethics", "AI regulations", "AI in healthcare", "AI in finance", 
    "AI-powered tools", "AI research",

    # Programming and Development
    "Python programming", "Java programming", "C programming", 
    "C++ programming", "JavaScript programming", "TypeScript", 
    "Rust programming", "Go programming", "Kotlin programming", 
    "Swift programming", "programming tutorials", "coding bootcamps", 
    "software development", "web development", "mobile development", 
    "open-source projects", "programming trends", "new programming languages",

    # Job Opportunities
    "internships", "job opportunities", "tech internships", 
    "developer internships", "AI research internships", 
    "machine learning internships", "remote jobs", 
    "freelance opportunities", "entry-level tech jobs", 
    "software engineer hiring", "tech job openings",

    # Startups and Innovations
    "startup culture", "tech startups", "emerging technologies", 
    "innovative companies", "disruptive technology", "venture capital news",

    # Cloud Computing and Cybersecurity
    "cloud computing", "AWS news", "Azure updates", "Google Cloud Platform",
    "cybersecurity news", "data breaches", "cyber threats", 
    "ransomware attacks", "IT security trends",

    # Blockchain and FinTech
    "blockchain technology", "cryptocurrency news", "DeFi", "NFTs", 
    "financial technology", "fintech news", "blockchain startups", 
    "crypto regulations",

    # Miscellaneous
    "IoT", "Internet of Things", "AR news", "VR news", 
    "augmented reality", "virtual reality", "quantum computing",
    "robotics news", "autonomous vehicles", "electric vehicles", 
    "sustainable technology", "renewable energy tech"
]

# Function to scrape Google News
def scrape_google_news(keywords):
    search_url = f"https://www.google.com/search?q={'%20OR%20'.join(keywords)}&tbm=nws"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    news = []
    for item in soup.select(".dbsr"):  # Google News result items
        title = item.select_one(".nDgy9d").text if item.select_one(".nDgy9d") else "No title"
        url = item.a["href"]
        snippet = item.select_one(".Y3v8qd").text if item.select_one(".Y3v8qd") else "No snippet"
        news.append({"title": title, "url": url, "snippet": snippet})
    
    return news

# Function to send news to Telegram channel
def send_to_telegram(news_items):
    for item in news_items:
        message = f"📰 *{item['title']}*\n{item['snippet']}\n🔗 {item['url']}"
        bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode="Markdown")

# Main function to scrape and forward news
def main():
    print("Fetching news...")
    news_items = scrape_google_news(KEYWORDS)
    if news_items:
        print(f"Found {len(news_items)} articles. Sending to Telegram...")
        send_to_telegram(news_items)
    else:
        print("No relevant news found.")

# Run the script periodically
if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception as e:
            print(f"Error occurred: {e}")
        print("Waiting for the next cycle...")
        time.sleep(3600)  # Run every hour
