from googlesearch import search
from bs4 import BeautifulSoup
import requests
import praw
import time

creds = {"client_id": "xxxxxxxxxxxxxx",
         "client_secret": "xxxxxxxxxxxxxxxxxxxxxxxxxxxx",
         "password": "xxxxxxxxxxxxxx",
         "user_agent": "Assign flair",
         "username": "bot_flairy"}

reddit = praw.Reddit(client_id=creds["client_id"],
                     client_secret=creds["client_secret"],
                     password=creds["password"],
                     user_agent=creds["user_agent"],
                     username=creds["username"])

tags_given = 0

while True:

    # Get the top 5 new submissions from the movie group.

    submissions = []
    for submission in reddit.subreddit("name_of_subreddit").__getattribute__("new")(limit=5):
        submissions.append(submission)

    for submission in submissions:

        # Reset the variables

        query = link = genre = genre1 = genre2 = " "

        # Change the submission title into a query

        query = submission.title
        query = query.split(")")
        query = query[0] + (") + imdb")
        if "&" in submission.title:
            query = submission.title.replace("&", "")

        # Search google and refine results to get the imdb url

        search_results = search(query, 5, 'en')
        for search_result in search_results:
            if "https://www.imdb.com/title/tt" in search_result:
                link = str(search_result)
                if len(search_result) == 37:
                    break
            link = link[:36]

        # Try to get the genre from the imdb url

        try:
            source = requests.get(link).text
            soup = BeautifulSoup(source, 'lxml')
            genre1 = soup.find("div", class_="title_wrapper")
            genre1 = genre1.text
            genre1 = genre1.strip()
            genre1 = genre1.replace("  ", "")
            genre1 = genre1.replace("\n", "")
            genre1 = genre1.split("|")
            genre1 = genre1[2]
            genre1 = genre1.replace(", ", " | ") + "  "
            genre2 = soup.find("div", class_="subtext")
            genre2 = genre2.text
            genre2 = str(genre2)
            genre2 = genre2.split("|")
            genre2 = genre2[1]
            genre2 = genre2.replace("\n", "")
            genre2 = genre2.replace(", ", " | ")
            genre2 = genre2.strip() + "  "
            genre = genre1
            catch_words = ["Episode", "TV", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
            if any(x in genre for x in catch_words):
                genre = genre2

        except:
            print("Oops")

        if submission.link_flair_text is None:
            submission.flair.select("6c8db25a-3a54-11eb-a0b6-0e9c8079b43d", genre)
            tags_given = tags_given + 1
            print("tags_given: " + str(tags_given))

    time.sleep(900)
