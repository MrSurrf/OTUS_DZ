from flask import Flask, redirect, request
from user_agents import parse
import json

app = Flask(__name__)

def handle_browser(url):
    return redirect(url)

def get_browser(user_agent):
    ua = parse(user_agent)
    return ua.browser.family

def get_url():
    with open('library.json', 'r') as file:
        browser_dict = json.load(file)
        url = browser_dict.setdefault(browser_name)
        print(url)
        return (handle_browser(url)




# @app.route('/')
# def redirect_based_on_browser():
#     user_agent = request.headers.get('User-Agent')
#     browser, version = get_browser(user_agent)
#     print(f"Browser: {browser}, Version: {version}")


@app.route('/<path:path>')
def redirect_based_on_browser_path(path):
    user_agent = request.headers.get('User-Agent')
    browser, version = get_browser(user_agent)
    ua = parse(user_agent)
    print(f"Browser: {browser}, Version: {version}")
    return ua.browser.family, ua.browser.version_string



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
