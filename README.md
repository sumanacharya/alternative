# Email Shield Service

A FastAPI-based microservice that analyzes email addresses for potential security risks using Google dorking. The service searches for email mentions across various platforms and provides detailed information about where the email has been exposed.

## Features

- Email address validation
- Google dorking search across multiple platforms
- Detailed search results including URLs and snippets
- Asynchronous processing for better performance
- Rate limiting and timeout protection
- Health check endpoint

## Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- A SerpAPI key (get it from [SerpAPI](https://serpapi.com/))

## Installation

1. Clone the repository:
```bash
git clone <your-repository-url>
cd email-service
```

2. Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root:
```bash
echo "SERPAPI_KEY=your_serpapi_key_here" > .env
```

## Running the Service

1. Start the FastAPI server:
```bash
python3 -m uvicorn app:app --reload --port 8000
```

The service will be available at `http://127.0.0.1:8000`

## API Documentation

Once the service is running, you can access:
- Interactive API documentation: `http://127.0.0.1:8000/docs`
- OpenAPI specification: `http://127.0.0.1:8000/openapi.json`

### Endpoints

#### 1. Analyze Email
```http
POST /v1/analyze/email
Content-Type: application/json

{
    "email": "user@example.com"
}
```

Response:
```json
{
    "total_mentions": 9750000,
    "pastebin_mentions": 8,
    "github_mentions": 12600,
    "stackoverflow_mentions": 4080,
    "total_results": [
        {
            "title": "Example Page Title",
            "link": "https://example.com/page",
            "snippet": "Text snippet containing the email...",
            "source": "example.com"
        }
    ],
    "pastebin_results": [...],
    "github_results": [...],
    "stackoverflow_results": [...]
}
```

#### 2. Health Check
```http
GET /health
```

Response:
```json
{
    "status": "healthy"
}
```

## Development

### Project Structure
```
email-service/
├── app.py              # FastAPI application and endpoints
├── search.py           # Google dorking search implementation
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (not in git)
└── README.md          # This file
```

### Adding New Features

1. Create a new branch:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes and commit:
```bash
git add .
git commit -m "Description of your changes"
```

3. Push to GitHub:
```bash
git push origin feature/your-feature-name
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Security

- Never commit your `.env` file or expose your SerpAPI key
- The service includes timeout protection to prevent abuse
- All email addresses are validated before processing

## Support

For support, please open an issue in the GitHub repository. 