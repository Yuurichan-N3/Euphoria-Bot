import requests
import json
import time
import random
import string
import brotli
import gzip

class WaitlistBot:
    def __init__(self):
        self.session = requests.Session()
        self.url = "https://api.getwaitlist.com/api/v1/signup"
        self.headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/json",
            "origin": "https://euphoria.finance",
            "referer": "https://euphoria.finance/",
            "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
        }
        self.waitlist_id = "12345"

    def log(self, message):
        print(f"[ {time.strftime('%Y-%m-%d %H:%M:%S')} ] | {message}")

    def generate_random_email(self):
        random_length = random.randint(6, 12)
        random_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=random_length))
        return f"{random_name}@gmail.com"

    def get_referral_link(self):
        ref_code = input("Masukkan kode referral (contoh: A7QK1EABR): ").strip()
        return f"https://euphoria.finance?ref_id={ref_code}"

    def decode_response(self, response):
        content = response.content
        content_encoding = response.headers.get('content-encoding', '').lower()

        try:
            if 'br' in content_encoding:
                decoded_content = brotli.decompress(content)
            elif 'gzip' in content_encoding:
                decoded_content = gzip.decompress(content)
            else:
                decoded_content = content

            return json.loads(decoded_content.decode('utf-8'))
        except (brotli.error, gzip.BadGzipFile, json.JSONDecodeError, UnicodeDecodeError):
            return response.text

    def signup(self, email, referral_link):
        payload = {
            "email": email,
            "referral_link": referral_link,
            "waitlist_id": self.waitlist_id
        }
        try:
            response = self.session.post(self.url, headers=self.headers, json=payload, timeout=10)
            if response.status_code == 200:
                self.log(f"Successfully signed up with email: {email}")
                return True
            else:
                self.log(f"Failed to sign up with email: {email}. Status code: {response.status_code}")
                return False
        except requests.RequestException as e:
            self.log(f"Error during request: {e}")
            return False

    def main(self):
        banner = """
╔══════════════════════════════════════════════╗
║       🌟 Euphoria BOT - Auto Signup          ║
║   Automate your waitlist registrations!      ║
║  Developed by: https://t.me/sentineldiscus   ║
╚══════════════════════════════════════════════╝
"""
        print(banner)
        self.log("Starting Waitlist Signup Bot...")
        referral_link = self.get_referral_link()
        self.log(f"Using referral link: {referral_link}")
        
        while True:
            email = self.generate_random_email()
            success = self.signup(email, referral_link)
            if success:
                self.log("Waiting 5 seconds before next signup...")
                time.sleep(5)
            else:
                self.log("Waiting 10 seconds before retrying...")
                time.sleep(10)

if __name__ == "__main__":
    bot = WaitlistBot()
    bot.main()
