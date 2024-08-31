import requests
import psycopg2
from psycopg2 import sql

class PexelsAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://api.pexels.com/v1/videos/'

    def fetch_popular_videos(self, per_page=50):
        headers = {'Authorization': self.api_key}
        params = {'per_page': per_page}
        
        response = requests.get(self.base_url + 'popular', headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            return [video['video_files'][0]['link'] for video in data['videos']]
        else:
            print("Failed to fetch the videos from Pexels. Sorry :(", response.status_code)
            return []

class PixabayAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://pixabay.com/api/videos/'

    def fetch_videos(self, per_page=50):
        params = {
            'key': self.api_key,
            'per_page': per_page
        }
        
        response = requests.get(self.base_url, params=params)

        if response.status_code == 200:
            data = response.json()
            return [video['videos']['medium']['url'] for video in data['hits']]
        else:
            print("Failed to fetch the videos from Pixabay. Sorry :(", response.status_code)
            return []

def save_video_links_to_db(links, source):
    conn = None  # Initialize conn to None
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            dbname="postgres",  # replace with your database name
            user="postgres",  # replace with your PostgreSQL username
            password="hammad",  # replace with your PostgreSQL password
            host="localhost"  # or the appropriate hostname
        )
        cursor = conn.cursor()

        # Insert video links into your existing table
        for link in links:
            cursor.execute(
                sql.SQL("INSERT INTO video_links (video_url) VALUES (%s)"),
                [link]
            )

        # Commit the transaction
        conn.commit()
        print(f"Successfully inserted {len(links)} video links from {source}.")
        
    except Exception as e:
        print("Failed to insert video links into the database:", e)
    finally:
        if conn:
            cursor.close()
            conn.close()

if __name__ == '__main__':
    pexels_api_key = "roNnEAsQKELBhgpGsopnggQm1V6mLybAHZUq6B4j7TvEnXzdvbWhhuvK"
    pixabay_api_key = "45632107-ccff48ac991129f5056994903"
    
    pexels_api = PexelsAPI(pexels_api_key)
    pixabay_api = PixabayAPI(pixabay_api_key)
    
    print("Pexels Popular Videos:")
    pexels_videos = pexels_api.fetch_popular_videos(per_page=50)
    save_video_links_to_db(pexels_videos, "Pexels")
    
    print("\nPixabay Videos:")
    pixabay_videos = pixabay_api.fetch_videos(per_page=50)
    save_video_links_to_db(pixabay_videos, "Pixabay")
