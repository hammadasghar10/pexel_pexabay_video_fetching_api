import requests
import random
import psycopg2
from psycopg2 import sql

class PexelsAPI:
    def __init__(self, api_key, db_conn):
        self.api_key = api_key
        self.base_url = 'https://api.pexels.com/v1/videos/'
        self.db_conn = db_conn

    def fetch_food_videos(self, per_page=50):
        headers = {'Authorization': self.api_key}
        query = 'food'
        params = {
            'query': query,
            'per_page': per_page,
            'page': random.randint(1, 10)
        }
        
        response = requests.get(self.base_url + 'search', headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            videos = [video['video_files'][0]['link'] for video in data['videos']]
            random.shuffle(videos)
            
            # Print and save video URLs to the database
            self.save_videos(videos)
            return True
        else:
            print(f"Failed to fetch {query} videos from Pexels. Sorry :(", response.status_code)
            return False

    def save_videos(self, videos):
        cursor = self.db_conn.cursor()
        insert_query = sql.SQL("INSERT INTO food (video_url) VALUES (%s) ON CONFLICT (video_url) DO NOTHING")
        for video in videos:
            print(f"Pexels Video URL: {video}")  # Print the video URL
            cursor.execute(insert_query, (video,))
        self.db_conn.commit()
        cursor.close()

class PixabayAPI:
    def __init__(self, api_key, db_conn):
        self.api_key = api_key
        self.base_url = 'https://pixabay.com/api/videos/'
        self.db_conn = db_conn

    def fetch_food_videos(self, per_page=50):
        params = {
            'key': self.api_key,
            'per_page': per_page,
            'page': random.randint(1, 10),
            'order': random.choice(['popular', 'latest']),
            'q': 'food'
        }
        
        response = requests.get(self.base_url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            videos = [video['videos']['medium']['url'] for video in data['hits']]
            random.shuffle(videos)
            
            # Print and save video URLs to the database
            self.save_videos(videos)
            return True
        else:
            print(f"Failed to fetch food videos from Pixabay. Sorry :(", response.status_code)
            return False

    def save_videos(self, videos):
        cursor = self.db_conn.cursor()
        insert_query = sql.SQL("INSERT INTO food (video_url) VALUES (%s) ON CONFLICT (video_url) DO NOTHING")
        for video in videos:
            print(f"Pixabay Video URL: {video}")  # Print the video URL
            cursor.execute(insert_query, (video,))
        self.db_conn.commit()
        cursor.close()

def main():
    pexels_api_key = "roNnEAsQKELBhgpGsopnggQm1V6mLybAHZUq6B4j7TvEnXzdvbWhhuvK"
    pixabay_api_key = "45632107-ccff48ac991129f5056994903"
    
    # Connect to PostgreSQL
    conn = psycopg2.connect(
        dbname="postgres",  # Replace with your database name
        user="postgres",  # Replace with your PostgreSQL username
        password="hammad",  # Replace with your PostgreSQL password
        host="localhost",  # or the appropriate hostname
        port="5432"  # Replace with your PostgreSQL port
    )
    
    pexels_api = PexelsAPI(pexels_api_key, conn)
    pixabay_api = PixabayAPI(pixabay_api_key, conn)
    
    # Fetch and save Pexels food videos
    if pexels_api.fetch_food_videos(per_page=50):
        print("Pexels food videos successfully fetched and saved to the database.")
    else:
        print("Failed to fetch Pexels food videos.")
    
    # Fetch and save Pixabay food videos
    if pixabay_api.fetch_food_videos(per_page=50):
        print("Pixabay food videos successfully fetched and saved to the database.")
    else:
        print("Failed to fetch Pixabay food videos.")

    conn.close()

if __name__ == '__main__':
    main()
