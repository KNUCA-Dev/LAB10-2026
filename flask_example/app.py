from flask import Flask, render_template, request, jsonify
import os
import json

app = Flask(__name__)

# Шлях до папки з фотографіями
PHOTOS_DIR = os.path.join(app.static_folder, 'photos')

# Шлях до файлу з результатами голосування
VOTES_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'votes.txt')

def load_votes():
    """Завантажує результати голосування з файлу."""
    if not os.path.exists(VOTES_FILE):
        return {}
    try:
        with open(VOTES_FILE, 'r') as f:
            return json.load(f)
    except (IOError, json.JSONDecodeError):
        return {}

def save_votes(votes):
    """Зберігає результати голосування у файл."""
    with open(VOTES_FILE, 'w') as f:
        json.dump(votes, f, indent=4)

def get_photos():
    """Повертає список фотографій з папки."""
    photos_path = os.path.join(app.root_path, 'static', 'photos')
    photos = []
    if not os.path.exists(photos_path):
        os.makedirs(photos_path)
    for filename in os.listdir(photos_path):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            photos.append(filename)
    return photos

@app.route('/')
def index():
    """Відображає головну сторінку з фотографіями."""
    photos = get_photos()
    votes = load_votes()
    return render_template('index.html', photos=photos, votes=votes)

@app.route('/vote', methods=['POST'])
def vote():
    """Обробляє голос користувача."""
    photo_id = request.form.get('photo_id')
    if not photo_id:
        return jsonify({'error': 'Photo ID is required'}), 400

    votes = load_votes()

    if photo_id in votes:
        votes[photo_id] += 1
    else:
        votes[photo_id] = 1

    save_votes(votes)
    return jsonify(votes)

@app.route('/results')
def results():
    """Відображає сторінку з результатами голосування."""
    votes = load_votes()
    photos = get_photos()

    # Сортування результатів для кращого відображення
    sorted_votes = sorted(votes.items(), key=lambda item: item[1], reverse=True)

    return render_template('results.html', votes=sorted_votes, all_photos=photos)

if __name__ == '__main__':
    # Створення файлу голосування, якщо він не існує
    if not os.path.exists(VOTES_FILE):
        save_votes({"image (4).png": 10, "image (5).png": 7, "image (6).png": 6})
    app.run(debug=True)