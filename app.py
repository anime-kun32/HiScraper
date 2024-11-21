@app.route('/api/list', methods=['GET'])
def list_api():
    letter = request.args.get('letter')
    page = request.args.get('page')
    
    if not letter or not page:
        return jsonify({"message": "Welcome to the API! Use parameters 'letter' and 'page' to scrape data."})
    
    target_url = f"https://hianime.to/az-list/{letter}?page={page}"
    
    try:
        response = requests.get(target_url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        films = []
        film_elements = soup.find_all('div', class_='film-poster')
       _elements:
            poster_img = film.find('img', class_='film-poster-img').get('data-src', '').strip()
            film_title = film.find('a', class_='film-poster-ahref').get('title', '').strip()
            film_url = film.find('a', class_='film-poster-ahref').get('href', '').strip()
            film_id = film_url.split('/')[-1]
            detail_section = film.find_next('div', class_='film-detail')
            film_name = detail_section.find('h3', class_='film-name').get_text(strip=True)
            film_type = detail_section.find('span', class_='fdi-item').get_text(strip=True)
            duration = detail_section.find('span', class_='fdi-duration').get_text(strip=True)
            films.append({
                "title": film_title,
                "url": film_url,
                "poster": poster_img,
                "id": film_id,
                "name": film_name,
                "type": film_type,
                "duration": duration,
            })
        return jsonify({"data": films})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
