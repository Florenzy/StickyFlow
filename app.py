from flask import Flask, request, render_template, redirect, url_for
import json

app = Flask(__name__)

# Путь к файлу для хранения заметок
NOTES_FILE = "notes.json"

# Функция для загрузки заметок из файла
def load_notes():
    try:
        with open(NOTES_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Функция для сохранения заметок в файл
def save_notes(notes):
    with open(NOTES_FILE, "w") as file:
        json.dump(notes, file, indent=4)

# Инициализация заметок
notes = load_notes()

@app.route('/')
def index():
    return render_template('index.html', notes=notes)

@app.route('/add', methods=['POST'])
def add_note():
    title = request.form.get('title')
    content = request.form.get('content')
    if title and content:
        notes.append({'title': title, 'content': content})
        save_notes(notes)
    return redirect(url_for('index'))

@app.route('/delete', methods=['POST'])
def delete_note():
    note_index = int(request.form.get('index'))
    if 0 <= note_index < len(notes):
        notes.pop(note_index)
        save_notes(notes)
    return redirect(url_for('index'))



@app.route('/edit', methods=['POST'])
def edit_note():
    note_index = int(request.form.get('index'))
    new_title = request.form.get('title')
    new_content = request.form.get('content')
    if 0 <= note_index < len(notes):
        if new_title:
            notes[note_index]['title'] = new_title
        if new_content:
            notes[note_index]['content'] = new_content
        save_notes(notes)  # Сохраняем изменения
    return redirect(url_for('index'))


@app.route('/change-color', methods=['POST'])
def change_color():
    note_index = int(request.form.get('index'))
    new_color = request.form.get('color')
    if 0 <= note_index < len(notes) and new_color:
        notes[note_index]['color'] = new_color
        save_notes(notes)  # Сохраняем изменения
    return redirect(url_for('drag_notes'))  # Возвращаемся на экран перетаскивания



@app.route('/drag-notes')
def drag_notes():
    return render_template('drag_notes.html', notes=notes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
