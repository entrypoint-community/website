from flask import Flask, jsonify
from datetime import datetime, timezone

app = Flask(__name__)

def get_date():
    # Current time in UTC
    now_utc = datetime.now(timezone.utc)
    # Convert datetime to ISO 8601 format
    iso_date = now_utc.isoformat()

    return iso_date

# Sample data for the API
members_data = [
    {"photo": "/public/imgs/entrypoint.jpeg", "name": "Alice Johnson", "position": "DevOps Engineer", "company": "Elementor", "seniority": "2"},
    {"photo": "/public/imgs/entrypoint.jpeg", "name": "Bob Smith", "position": "SRE Team Member", "company": "Elementor", "seniority": "2"},
    {"photo": "/public/imgs/entrypoint.jpeg", "name": "Carol Williams", "position": "FinOps Engineer", "company": "Elementor", "seniority": "1"},
    {"photo": "/public/imgs/entrypoint.jpeg", "name": "Alice Johnson", "position": "DevOps Engineer", "company": "Elementor", "seniority": "4"},
    {"photo": "/public/imgs/entrypoint.jpeg", "name": "Bob Smith", "position": "Developer", "company": "Elementor", "seniority": "3"},
    {"photo": "/public/imgs/entrypoint.jpeg", "name": "Carol Williams", "position": "Designer", "company": "Elementor", "seniority": "2"}
]

posts_data = [
    {"title": "Introduction to Flask", "summary": "This post introduces Flask, a lightweight WSGI web application framework.", "author": "Yuval Press", "date": get_date(), "image": "/public/imgs/entrypoint.jpeg", "url": ""},
    {"title": "API Development", "summary": "Learn how to build APIs with Flask for better data handling.", "author": "Yuval Press", "date": get_date(), "image": "/public/imgs/entrypoint.jpeg"},
    {"title": "Advanced Flask", "summary": "Explore advanced features of Flask including blueprints and application factories.", "author": "Yuval Press", "date": get_date(), "image": "/public/imgs/entrypoint.jpeg"},
        {"title": "Introduction to Flask", "summary": "This post introduces Flask, a lightweight WSGI web application framework.", "author": "Yuval Press", "date": get_date(), "image": "/public/imgs/entrypoint.jpeg"},
    {"title": "API Development", "summary": "Learn how to build APIs with Flask for better data handling.", "author": "Yuval Press", "date": get_date(), "image": "/public/imgs/entrypoint.jpeg"},
    {"title": "Advanced Flask", "summary": "Explore advanced features of Flask including blueprints and application factories.", "author": "Yuval Press", "date": get_date(), "image": "/public/imgs/entrypoint.jpeg"}
]

# Endpoint to get members
@app.route('/members', methods=['GET'])
def get_members():
    response = jsonify(members_data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# Endpoint to get posts
@app.route('/posts', methods=['GET'])
def get_posts():
    response = jsonify(posts_data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    
    return response

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="9090")
