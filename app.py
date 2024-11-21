from flask import Flask, request, jsonify
from flask_cors import CORS  # Import Flask-CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Welcome endpoint
@app.route('/api/list', methods=['GET'])
def list_api():
    # Welcome message if no params are provided
    letter = request.args.get('letter')
    page = request.args.get('page')
    
    if not letter or not page:
        return jsonify({"message": "Welcome to the API! Use parameters 'letter' and 'page' to scrape data."})
    
    # Build the target URL
    target_url = f"https://hianime.to/az-list/{letter}?page={page}"
    
    try:
        # Send a GET request to the target URL
        response = requests.get(target_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract the required data
        films = []
        film_elements = soup.find_all('div', class_='film-poster')  # Locate each film block

        for film in film_elements:
            # Film poster and details
            poster_img = film.find('img', class_='film-poster-img').get('data-src', '').strip()
            film_title = film.find('a', class_='film-poster-ahref').get('title', '').strip()
            film_url = film.find('a', class_='film-poster-ahref').get('href', '').strip()
            
            # Extracting the anime ID
            film_id = film_url.split('/')[-1]  # Get the last component of the URL as ID
            
            # Additional film information
            detail_section = film.find_next('div', class_='film-detail')
            film_name = detail_section.find('h3', class_='film-name').get_text(strip=True)
            film_type = detail_section.find('span', class_='fdi-item').get_text(strip=True)
            duration = detail_section.find('span', class_='fdi-duration').get_text(strip=True)

            # Append the data to the list
            films.append({
                "title": film_title,
                "url": film_url,
                "poster": poster_img,
                "id": film_id,  
                "name": film_name,
                "type": film_type,
                "duration": duration,
            })
        
        # Retu the scraped data as JSON
        return jsonify({"data": films})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
