from flask import Flask, redirect, request
from user_agents import parse
import json

app = Flask(__name__)

def handle_browser(url):
    return redirect(url)

def get_browser(user_agent):
    ua = parse(user_agent)
    return ua.browser.family

def get_url(browser_name):
    with open('library.json', 'r') as file:
        browser_dict = json.load(file)
        url = browser_dict.get(browser_name)
        if url:
            return handle_browser(url)
        else:
            return f"No URL found for browser: {browser_name}", 404

@app.route('/')
def redirect_based_on_browser():
    user_agent = request.headers.get('User-Agent')
    browser_name = get_browser(user_agent)
    print(browser_name)
    return get_url(browser_name)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)