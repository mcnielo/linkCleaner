from flask import Flask, request, render_template
from flask_caching import Cache
import requests
from urllib.parse import urlsplit, urlparse, parse_qs

app = Flask(__name__, static_url_path='', static_folder='static')
cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache'})

@cache.memoize(timeout=3600)
def get_final_url(url):
    try:
        response = requests.get(url, allow_redirects=True, timeout=10)
        return response.url
    except requests.exceptions.RequestException:
        return url  # fallback

def clean_url(url):
    if "facebook.com/story.php" in url:
        return clean_facebook_story_url(url)
    else:
        split_url = urlsplit(url)
        return f"{split_url.scheme}://{split_url.netloc}{split_url.path}".rstrip('/')

def clean_facebook_story_url(url):
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    story_id = query.get("story_fbid", [""])[0]
    user_id = query.get("id", [""])[0]
    if story_id and user_id:
        return f"https://www.facebook.com/{user_id}/posts/{story_id}"
    return url

@app.route("/", methods=["GET", "POST"])
def index():
    cleaned_results = []
    service_id = ""
    quantity = ""
    selected_mode = "single"

    if request.method == "POST":
        selected_mode = request.form.get("mode", "single")
        service_id = request.form.get("service_id", "")
        quantity = request.form.get("quantity", "")

        if selected_mode == "single":
            input_url = request.form.get("input_url", "").strip()
            if input_url:
                final = get_final_url(input_url)
                cleaned = clean_url(final)
                cleaned_results.append(f"{service_id} | {cleaned} | {quantity}")
        elif selected_mode == "multi":
            multi_urls = request.form.get("multi_urls", "")
            for line in multi_urls.splitlines():
                url = line.strip()
                if url:
                    final = get_final_url(url)
                    cleaned = clean_url(final)
                    cleaned_results.append(f"{service_id} | {cleaned} | {quantity}")

    return render_template("index.html", cleaned_results=cleaned_results, selected_mode=selected_mode,
                           service_id=service_id, quantity=quantity)

if __name__ == "__main__":
    app.run(debug=False)
