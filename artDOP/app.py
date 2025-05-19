from bottle import Bottle, route, run, template, static_file, request, response
from datetime import datetime
import re

app = Bottle()

# In-memory storage for news items
news_items = [
    {
        'title': 'Gallery Opening',
        'content': 'We are excited to announce the opening of our new gallery space next month!',
        'date': '2025-05-15',
        'email': 'info@artvisualgallery.com'
    },
    {
        'title': 'New Exhibition',
        'content': 'A special exhibition featuring modern impressionists will begin June 1st.',
        'date': '2025-05-10',
        'email': 'info@artvisualgallery.com'
    }
]

@app.route('/')
def index():
    return template('views/index.tpl')

@app.route('/collection')
def collection():
    return template('views/collection.tpl')

@app.route('/contact')
def contact():
    return template('views/contact.tpl')

@app.route('/news')
def news():
    return template('views/news.tpl', news_items=news_items)

@app.route('/submit_contact', method='POST')
def submit_contact():
    name = request.forms.get('name')
    email = request.forms.get('email')
    message = request.forms.get('message')
    # Here you can add logic to save the data (e.g., to a database)
    return f"Thank you, {name}, your message has been received!"

@app.route('/submit_news', method='POST')
def submit_news():
    title = request.forms.get('title')
    content = request.forms.get('content')
    email = request.forms.get('email')

    # Validation
    if not title or len(title) < 3:
        response.status = 400
        return "Title must be at least 3 characters long."
    if not content or len(content) < 10:
        response.status = 400
        return "Content must be at least 10 characters long."
    if not email or not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
        response.status = 400
        return "Invalid or missing email address."

    date = datetime.now().strftime("%Y-%m-%d")
    news_item = {'title': title, 'content': content, 'date': date, 'email': email}
    news_items.append(news_item)
    return f"Thank you! Your news item '{title}' has been submitted."

@app.route('/static/<filename:path>')
def serve_static(filename):
    return static_file(filename, root='static/')

if __name__ == '__main__':
    run(app, host='localhost', port=8080, debug=True)