import unittest
from datetime import datetime, timedelta
from bottle import request, response, LocalRequest, LocalResponse
from app import app as my_app, news_items

class TestNewsFunctionality(unittest.TestCase):
    def setUp(self):
        # Save original news
        self.original_news = news_items.copy()
        
        # Clear and add test data
        news_items.clear()
        news_items.extend([
            {
                'title': 'Existing News 1',
                'content': 'Valid content for existing news 1',
                'date': '2025-01-01',
                'email': 'test1@example.com'
            },
            {
                'title': 'Existing News 2',
                'content': 'Valid content for existing news 2',
                'date': '2025-01-02',
                'email': 'test2@example.com'
            }
        ])

    def tearDown(self):
        # Restore original news
        news_items[:] = self.original_news

    def _make_get_request(self, path):
        """Helper to simulate a GET request"""
        # Set up the request environment
        environ = {
            'REQUEST_METHOD': 'GET',
            'PATH_INFO': path,
            'SERVER_PROTOCOL': 'HTTP/1.1',
            'SERVER_NAME': 'localhost',
            'SERVER_PORT': '8080',
            'wsgi.url_scheme': 'http'
        }
        req = LocalRequest(environ)
        resp = LocalResponse()

        # Bind the request and response to the Bottle app
        with my_app.request_context(req.environ):
            # Call the route handler directly
            handler = my_app.match(req.environ)[0]
            result = handler()
            # If the handler returns a string (e.g., template output), Bottle sets it in the response
            if isinstance(result, str):
                resp.body.write(result.encode('utf-8'))
            resp.status = response.status_code

        return resp

    def _make_post_request(self, path, data):
        """Helper to simulate a POST request"""
        # Encode form data
        form_data = '&'.join(f"{k}={v}" for k, v in data.items())
        environ = {
            'REQUEST_METHOD': 'POST',
            'PATH_INFO': path,
            'CONTENT_TYPE': 'application/x-www-form-urlencoded',
            'CONTENT_LENGTH': str(len(form_data)),
            'wsgi.input': BytesIO(form_data.encode('utf-8')),
            'SERVER_PROTOCOL': 'HTTP/1.1',
            'SERVER_NAME': 'localhost',
            'SERVER_PORT': '8080',
            'wsgi.url_scheme': 'http'
        }
        req = LocalRequest(environ)
        resp = LocalResponse()

        # Bind the request and response to the Bottle app
        with my_app.request_context(req.environ):
            # Call the route handler directly
            handler = my_app.match(req.environ)[0]
            result = handler()
            # If the handler returns a string, Bottle sets it in the response
            if isinstance(result, str):
                resp.body.write(result.encode('utf-8'))
            resp.status = response.status_code

        return resp

    # --- Tests for news page ---
    def test_news_page_returns_200(self):
        """Test that news page returns 200 status code"""
        response = self._make_get_request('/news')
        self.assertEqual(response.status_code, 200)

    def test_news_page_displays_existing_news(self):
        """Test that page displays existing news"""
        response = self._make_get_request('/news')
        body = response.body.read()
        self.assertIn(b'Existing News 1', body)
        self.assertIn(b'Existing News 2', body)

    def test_news_page_empty_list(self):
        """Test display of empty news list"""
        news_items.clear()
        response = self._make_get_request('/news')
        body = response.body.read()
        self.assertIn(b'No News Available', body)

    # --- Tests for adding news ---
    def test_add_news_valid_data(self):
        """Test adding news with valid data"""
        initial_count = len(news_items)
        data = {
            'title': 'New Valid News',
            'content': 'This content meets all validation requirements.',
            'email': 'valid@example.com'
        }
        response = self._make_post_request('/submit_news', data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(news_items), initial_count + 1)
        self.assertEqual(news_items[-1]['title'], 'New Valid News')
        self.assertEqual(news_items[-1]['email'], 'valid@example.com')

    def test_add_news_missing_title(self):
        """Test adding news without title"""
        initial_count = len(news_items)
        data = {
            'content': 'Content without title',
            'email': 'test@example.com'
        }
        response = self._make_post_request('/submit_news', data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(news_items), initial_count)

    def test_add_news_missing_content(self):
        """Test adding news without content"""
        initial_count = len(news_items)
        data = {
            'title': 'Title without content',
            'email': 'test@example.com'
        }
        response = self._make_post_request('/submit_news', data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(news_items), initial_count)

    def test_add_news_missing_email(self):
        """Test adding news without email"""
        initial_count = len(news_items)
        data = {
            'title': 'Valid Title',
            'content': 'Valid content'
        }
        response = self._make_post_request('/submit_news', data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(news_items), initial_count)

    def test_add_news_invalid_email(self):
        """Test adding news with invalid email"""
        initial_count = len(news_items)
        data = {
            'title': 'Valid Title',
            'content': 'Valid content',
            'email': 'invalid-email'
        }
        response = self._make_post_request('/submit_news', data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(news_items), initial_count)

    def test_add_news_invalid_title_length(self):
        """Test adding news with too short title"""
        initial_count = len(news_items)
        data = {
            'title': 'Hi',
            'content': 'Valid content',
            'email': 'test@example.com'
        }
        response = self._make_post_request('/submit_news', data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(news_items), initial_count)

    def test_add_news_invalid_content_length(self):
        """Test adding news with too short content"""
        initial_count = len(news_items)
        data = {
            'title': 'Valid Title',
            'content': 'Short',
            'email': 'test@example.com'
        }
        response = self._make_post_request('/submit_news', data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(news_items), initial_count)

    def test_news_date_auto_generated(self):
        """Test that date is auto-generated"""
        data = {
            'title': 'News with date',
            'content': 'Content for date test',
            'email': 'test@example.com'
        }
        response = self._make_post_request('/submit_news', data)
        self.assertEqual(response.status_code, 200)
        news_date = datetime.strptime(news_items[-1]['date'], '%Y-%m-%d')
        self.assertAlmostEqual(
            news_date.date(),
            datetime.now().date(),
            delta=timedelta(seconds=5)
        )

if __name__ == '__main__':
    unittest.main()
