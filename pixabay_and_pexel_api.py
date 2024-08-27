import requests

class PexelsAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://api.pexels.com/v1/videos/'

    def fetch_popular_videos(self, per_page=50):  # Set per_page to 50
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

    def fetch_videos(self, per_page=50):  # Set per_page to 50
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

if __name__ == '__main__':
    pexels_api_key = "roNnEAsQKELBhgpGsopnggQm1V6mLybAHZUq6B4j7TvEnXzdvbWhhuvK"
    pixabay_api_key = "45632107-ccff48ac991129f5056994903"
    
    pexels_api = PexelsAPI(pexels_api_key)
    pixabay_api = PixabayAPI(pixabay_api_key)
    
    print("Pexels Popular Videos:")
    pexels_videos = pexels_api.fetch_popular_videos(per_page=50)  # Fetch 50 videos per page from Pexels
    for video in pexels_videos:
        print(video)
    
    print("\nPixabay Videos:")
    pixabay_videos = pixabay_api.fetch_videos(per_page=50)  # Fetch 50 videos per page from Pixabay
    for video in pixabay_videos:
        print(video)
