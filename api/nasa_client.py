import os
import requests
import datetime
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

load_dotenv()

class NASAClient:
    def __init__(self):
        self.api_key = os.getenv("NASA_API_KEY")
        self.base_url = "https://api.nasa.gov"
        
        # Configure session with retry strategy
        self.session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def _get(self, endpoint, params=None):
        if params is None:
            params = {}
        params['api_key'] = self.api_key
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        try:
            response = self.session.get(f"{self.base_url}{endpoint}", params=params, headers=headers, timeout=60)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {endpoint}: {e}")
            return None

    def get_apod(self):
        """Get Astronomy Picture of the Day"""
        return self._get("/planetary/apod")

    def get_neo_feed(self, start_date=None, end_date=None):
        """Get Near Earth Object Feed"""
        if not start_date:
            start_date = datetime.date.today().strftime("%Y-%m-%d")
        if not end_date:
            end_date = start_date # Default to single day
        
        return self._get("/neo/rest/v1/feed", {"start_date": start_date, "end_date": end_date})

    def get_epic_images(self, date=None):
        """Get EPIC Earth Images"""
        # Default to most recent available date usually involves checking /api/natural, 
        # but for simplicity we'll just get the latest natural images
        if date:
             return self._get(f"/EPIC/api/natural/date/{date}")
        return self._get("/EPIC/api/natural")

    def get_mars_rover_photos(self, sol=1000, rover="curiosity"):
        """Get Mars Rover Photos"""
        return self._get(f"/mars-photos/api/v1/rovers/{rover}/photos", {"sol": sol})

    def search_images(self, query):
        """Search NASA Image and Video Library (Different Base URL)"""
        url = "https://images-api.nasa.gov/search"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        try:
            response = self.session.get(url, params={"q": query, "media_type": "image"}, headers=headers, timeout=60)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error searching images: {e}")
            return None
