# Scraper API

This is a Python-based web scraper deployed on Vercel. It scrapes data from a specific URL, parses the HTML, and returns the data as JSON.

## API Endpoints

- **GET /api/list**: Base endpoint with a welcome message.
- **GET /api/list?letter={letter}&page={page}**: Scrapes data for the given letter and page.

### Example
- Request: `/api/list?letter=k&page=1`
- Response:
  ```json
  {
    "data": [
      {
        "title": "Kite",
        "url": "/16204",
        "poster": "https://cdn.noitatnemucod.net/thumbnail/300x400/100/746d993e054e200c4e3148dd90df225c.jpg",
        "name": "Kite",
        "type": "OVA",
        "duration": "52m"
      }
    ]
  }
