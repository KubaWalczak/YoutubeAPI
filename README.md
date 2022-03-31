# YoutubeAPI
This app connects to Youtube API to create Postgres videos database

### Info
In order to connect to Google's Cloud Youtube API, this script uses account that was 
created specifically for that goal and is unused on daily basis.
### How to use
To get started, create google account and log into Google Cloud to create credentials. In this case we only need Api key, because we don't gather user info.\
Save API Key Token in apikey.txt file.



After that you need to install some packages.\
`pip install pip install --upgrade google-api-python-client`\
`pip install --upgrade google-auth-oauthlib google-auth-httplib2 from googleapiclient.discovery import build`\
`pip install json`\
`pip install pandas`\
`pip install psycopg`

If you don't have Postgres database, you will need to download it from\
https://www.postgresql.org/download/ 


Then in command promt create a database by simply typing:\
`CREATE DATABASE ytapi`

Finally run the code\
`python ytapi.py`
### End result
![Zrzut ekranu 2022-03-30 183939](https://user-images.githubusercontent.com/68194564/160887203-d5e690e1-891c-4b58-b767-2f67529a89af.png)
