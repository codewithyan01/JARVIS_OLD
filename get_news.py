import requests
from main import speak


def get_news():

    api_key = "77872eedf3b045e38357592cba4704f1"

    url = f"https://newsapi.org/v2/top-headlines?country=in&category=technology&apiKey={api_key}"

    response = requests.get(url)

    data = response.json()

    if data["status"] != "ok":
        speak("Sorry sir, I couldn't fetch news.")
        return

    articles = data["articles"]

    if len(articles) == 0:
        speak("No news available right now sir.")
        return

    speak("Here are the top headlines sir.")

    for i in range(3):
        title = articles[i]["title"]
        speak(title)
 
 
 
 
 
#  r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
#         if r.status_code == 200:
#             # Parse the JSON response
#             data = r.json()
            
#             # Extract the articles
#             articles = data.get('articles', [])
            
#             # Print the headlines
#             for article in articles:
#                 speak(article['title'])