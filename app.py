from flask import Flask, render_template_string, request, redirect, flash
import requests
from requests.auth import HTTPBasicAuth
import os

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "your_secret_key")

WP_URL = os.getenv("WP_URL")
WP_USER = os.getenv("WP_USER")
WP_APP_PASSWORD = os.getenv("WP_APP_PASSWORD")

FORM_TEMPLATE = """
<!doctype html>
<title>Create WordPress Page</title>
<h1>Create New WordPress Page</h1>
<form method=post>
  <label>Title: <input type=text name=title required></label><br>
  <label>Content:<br><textarea name=content rows=10 cols=50 required></textarea></label><br>
  <input type=submit value=Create>
</form>
{% with messages = get_flashed_messages() %}
  {% if messages %}
    <ul>
    {% for message in messages %}
      <li>{{ message }}</li>
    {% endfor %}
    </ul>
  {% endif %}
{% endwith %}
"""

@app.route('/', methods=['GET', 'POST'])
def create_page():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        url = f"{WP_URL}/wp-json/wp/v2/pages"
        auth = HTTPBasicAuth(WP_USER, WP_APP_PASSWORD)
        data = {
            "title": title,
            "content": content,
            "status": "publish"
        }

        response = requests.post(url, auth=auth, json=data)

        if response.status_code == 201:
            flash("Page created successfully!")
        else:
            flash(f"Failed to create page: {response.status_code} - {response.text}")

        return redirect('/')

    return render_template_string(FORM_TEMPLATE)

if __name__ == '__main__':
    app.run(debug=True)
