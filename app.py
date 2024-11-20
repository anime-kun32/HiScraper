from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/api/list', methods=['GET'])
def list_api():
    letter = request.args.get('letter')
    page = request.args.get('page')
    
    if not letter or not page:
        return jsonify({"message": "Welcome to the API! Use parameters 'letter' and 'page' to scrape data."})
    
    target_url = f"https://hianime.to/az-list/{letter}?page={page}"
    
    try:
        # Send HTTP request
        response = requests.get(target_url)
        
        if response.status_code != 200:
            return jsonify({"error": f"Failed to fetch data from {target_url}. Status code: {response.status_code}"}), 500
        
        if not response.text.strip():
            return jsonify({"error": "The target page returned no content."}), 500
        
        # Parse the HTML
        soup = BeautifulSoup(response.text, 'html.parser')  # Ensure soup is defined
        
        # Extract the required data
        films = []
        film_elements = soup.find_all('div', class_='film-poster')
        
        for film in film_elements:
            poster_img = film.find('img', class_='film-poster-img').get('data-src', '').strip()
            film_title = filmfilm-poster-ahref').get('title', '').strip()
            film_url = film.find('a', class_='film-poster-ahref').get('href', '').strip()
            film_id = film_url.split('/')[-1]
            
            detail_section = film.find_next('div', class_='film-detail')
            film_name = detail_section.find('h3', class_='film-name').get_text(strip=True)
            film_type = detail_section.find('span', class_='fdi-item').get_text(strip=True)
            duration = detail_section.find('span', class_='fdi-duration').get_text(strip=True)
            
            rating = film.find('div', class_='tick-rate')
            rating_text = rating.get_text(strip=True) if rating else "N/A"
            
            sub_episodes = film.find('div', class_='tick-item tick-sub')
            sub_episodes_count = sub_episodes.get_text(strip=True) if sub_episodes else "0"
            
            dub_episodes = film.find('div', class_='tick-item tick-dub')
            dub_episodes_count = dub_episodes.get_text(strip=True) if dub_episodes else "0"
            
            films.append({
                "title": film_title,
                "url": film_url,
                "poster": poster_img,
                "id": film_id,
                "name": film_name,
                "type": film_type,
                "duration": duration,
                "rating": rating_text,
                "sub_episodes": sub_episodes_count,
                "dub_episodes": dub_episodes_count
            })
        
        return films})
    
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
