# YoutubeAPI
This app connects to Youtube API to create Postgres videos database

### Info
In order to connect to Google's Cloud Youtube API, this script uses account that was 
created specifically for that goal and is unused on daily basis.
### How to use
To get started, you need to install some packages.\
`pip install pip install --upgrade google-api-python-client`\
`pip install --upgrade google-auth-oauthlib google-auth-httplib2 from googleapiclient.discovery import build`\
`pip install json`\
`pip install pandas`\
`pip install psycopg`

If you don't have Postgres database, you will need to download it from\
https://www.postgresql.org/download/ \


Then in command promt create a database by simply typing:\
`CREATE DATABASE ytapi`

Finally run the code\
`python ytapi.py`
### End result
![img.png](img.png)
