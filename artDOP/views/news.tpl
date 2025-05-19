<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Latest News</title>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/static/styles.css">
</head>
<body>
    <header>
        <div class="container">
            <h1>Art-Visual Gallery</h1>
            <nav>
                <a href="/">Home</a>
                <a href="/collection">Collection</a>
                <a href="/news">News</a>
                <a href="/contact">Contact</a>
            </nav>
        </div>
    </header>
    <main>
        <div class="container">
            <h2>Latest News</h2>
            <div class="news-list">
                % if news_items:
                    % for item in news_items:
                        <div class="news-item">
                            <h3>{{ item['title'] }}</h3>
                            <p>Posted on {{ item['date'] }} by {{ item['email'] }}</p>
                            <p>{{ item['content'] }}</p>
                        </div>
                    % end
                % else:
                    <div class="news-item">
                        <h3>No News Available</h3>
                        <p>Be the first to add a news item!</p>
                    </div>
                % end
            </div>
            <h3>Add a New News Item</h3>
            <form action="/submit_news" method="POST">
                <label for="title">Title:</label>
                <input type="text" id="title" name="title" required><br><br>
                <label for="email">Email:</label>
                <input type="email" id="email" name="email" required><br><br>
                <label for="content">Content:</label>
                <textarea id="content" name="content" required></textarea><br><br>
                <button type="submit">Submit News</button>
            </form>
        </div>
    </main>
    <footer>
        <p>© 2025 Art-Visual Gallery</p>
    </footer>
</body>
</html>