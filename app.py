from flask import Flask, render_template, request, jsonify
from imdb import IMDb
import random

app = Flask(__name__)
ia = IMDb()

GENRE_MAPPING = {
    'happy': 'comedy',
    'sad': 'drama',
    'action': 'action',
    'comedy': 'comedy',
    'romantic': 'romance'
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-movie', methods=['POST'])
def get_movie():
    data = request.get_json()
    mode = data.get('mode')
    genre = GENRE_MAPPING.get(mode)

    if not genre:
        return jsonify({'error': 'Invalid mode'}), 400

    try:
        # Get the top 10 results only for faster processing
        movies = ia.search_movie(genre)[:10]  
        if movies:
            selected_movie = random.choice(movies)
            movie_title = selected_movie.get('title')

            # Get movie poster only when necessary
            try:
                ia.update(selected_movie, info=['main'])  
                poster_url = selected_movie.get('full-size cover url', None)
            except Exception:
                poster_url = None

            return jsonify({
                'movie': movie_title,
                'poster': poster_url
            })
        else:
            return jsonify({'error': 'No movies found for this genre'}), 404

    except Exception as e:
        return jsonify({'error': f'Failed to fetch movies: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
