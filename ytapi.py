from googleapiclient.discovery import build
import json
import pandas as pd
import datetime
import psycopg


def API():
    # Reading credentials
    with open('apikey.txt') as a:
        api_key = a.read()

    # Calling Google's Youtube API
    # Documentation: https://github.com/googleapis/google-api-python-client/blob/main/docs/start.md
    # All supported API's :https://github.com/googleapis/google-api-python-client/blob/main/docs/dyn/index.md
    youtube = build('youtube', 'v3', developerKey=api_key)
    collection = youtube.videos()
    request = collection.list(part="snippet,contentDetails,statistics",
                              chart="mostPopular",
                              regionCode="US",
                              maxResults=50)

    # the above regionCode can be almost anything from codes -> https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2 (unless Youtube is blocked in specific country)

    response = request.execute()
    result = json.dumps(response, sort_keys=True, indent=4)
    print(result)

    def CSV_and_Pandas():
        """
        This function creates a Pandas Dataframe and CSV file with all the data from current session.
        :return:
        """

        # Creating data
        channel = []
        video_title = []
        video_comments = []
        video_likes = []
        video_viewCount = []
        video_published = []
        video_seen = []

        # Looping for data that we're interested in
        for video in response["items"]:
            # Doing this because sometimes vidoes have blocked like count, none comments etc. and it's not showing in response
            try:
                channel.append(video['snippet']['channelTitle'])
            except KeyError:
                channel.append("No channel")

            try:
                video_title.append(video['snippet']['title'])
            except KeyError:
                video_title.append("No title")

            try:
                video_comments.append(video['statistics']['commentCount'])
            except KeyError:
                video_comments.append(0)

            try:
                video_likes.append(video['statistics']['likeCount'])
            except KeyError:
                video_likes.append(0)

            try:
                video_viewCount.append(video['statistics']['viewCount'])
            except KeyError:
                video_viewCount.append(0)

            try:
                video = video['snippet']['publishedAt']
                # video = video.replace('T', ' ')
                video = video.replace('Z', '')
                published_date = datetime.datetime.fromisoformat(video)
                video_published.append(published_date)
            except KeyError:
                video_published.append(datetime.datetime.now())

            scrape_time = str(datetime.datetime.now())
            scrape_time = scrape_time[0:19]
            scrape_time = datetime.datetime.fromisoformat(scrape_time)
            video_seen.append(scrape_time)

        # Creating Pandas DataFrame
        videos_info = pd.DataFrame({
            "Channel": channel,
            "Title": video_title,
            "Views": video_viewCount,
            "Comments": video_comments,
            "Likes": video_likes,
            "Published date": video_published,
            "Video seen": video_seen})

        print(videos_info.head)

        # Creating CSVs
        videos_info.to_csv('videos.csv', mode='a')
        daf = pd.read_csv('videos.csv')
        daf.dropna(inplace=True)
        daf.drop(columns='Unnamed: 0', inplace=True)
        daf.reset_index(drop=True, inplace=True)
        daf.to_csv('database.csv', mode='a')

    def DB_Postgres():
        """
        This function connects to an existing database and inserts data from current sesion.
        :return:
        """

        # Connecting to a postgres database
        # First time using, you have to create a database by typing in command line CREATE DATABASE ytapi
        with psycopg.connect("dbname=ytapi user=postgres") as conn:

            # Open a cursor to perform database operations
            with conn.cursor() as cur:
                # Execute a command: this creates a new table
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS YTpopular_videos (
                        video_id serial PRIMARY KEY, 
                        Channel VARCHAR(255) NOT NULL,
                        Title VARCHAR(255) UNIQUE,
                        Views INT NOT NULL,
                        Comments INT NOT NULL,
                        Likes INT NOT NULL,
                        Published_date TIMESTAMP,
                        Video_seen TIMESTAMP
                        )
                    """)

                # Looping for data that we're interested in
                for video in response["items"]:
                    # Doing this because sometimes vidoes have blocked like count, none comments etc. and it's not showing in response
                    try:
                        channel = video['snippet']['channelTitle']
                    except KeyError:
                        channel = "No channel"

                    try:
                        title = video['snippet']['title']
                    except KeyError:
                        title = "No title"

                    try:
                        comments = video['statistics']['commentCount']
                    except KeyError:
                        comments = 0

                    try:
                        likes = video['statistics']['likeCount']
                    except KeyError:
                        likes = 0

                    try:
                        views = video['statistics']['viewCount']
                    except KeyError:
                        views = 0

                    try:
                        video = video['snippet']['publishedAt']
                        # video = video.replace('T', ' ')
                        video = video.replace('Z', '')
                        published_date = datetime.datetime.fromisoformat(video)
                    except KeyError:
                        published_date = datetime.datetime.now()

                    scrape_time = str(datetime.datetime.now())
                    scrape_time = scrape_time[0:19]
                    scrape_time = datetime.datetime.fromisoformat(scrape_time)

                    # Pass data to fill a query placeholders and let Psycopg perform
                    # the correct conversion (no SQL injections!)
                    cur.execute(
                        "INSERT INTO YTpopular_videos (Channel, Title, Views, Comments, Likes, Published_date, Video_seen) VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING",
                        (channel, title, views, comments, likes, published_date, scrape_time))
                print('\nAdding to the database')

                # Make the changes to the database persistent
                conn.commit()

    # Execute functions
    CSV_and_Pandas()
    DB_Postgres()


if __name__ == "__main__":
    API()
