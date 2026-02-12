import json
import os
from flask import Flask, render_template, request, redirect
app = Flask(__name__)
DB_FILE = 'db_complaint.json'
db_complaint = []
if os.path.exists(DB_FILE):
    with open(DB_FILE, 'r', encoding='utf-8') as f:
        db_complaint = json.load(f)
@app.route('/')
def index():
    return render_template('index.html', complaints=db_complaint)
@app.route('/add', methods=['POST'])
def add_complaint():
    category = request.form.get('category')
    description = request.form.get('descr')
    new_entry = {
        "id": len(db_complaint) + 1,
        "category": category,
        "text": description
    }
    db_complaint.append(new_entry)
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(db_complaint, f, ensure_ascii=False, indent=4)

    return redirect('/')
@app.route('/clear_all_data')
def clear_data():
    global db_complaint
    db_complaint = [] # Обнуляем список в памяти
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE) # Удаляем файл с диска
    return "База очищена! <a href='/'>Вернуться на сайт</a>"
if __name__ == '__main__':
    app.run(debug=True)