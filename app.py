from flask import Flask, request, render_template, redirect, url_for
import json
import os

app = Flask(__name__)

# Файлы для хранения данных
NOTES_FILE = "notes.json"
CALENDAR_FILE = "calendar.json"
TASKS_FILE = "tasks.json"

# Загрузка данных из файлов
def load_data(file_name):
    if not os.path.exists(file_name):
        with open(file_name, "w") as file:
            json.dump([], file)  # Создаём пустой список, если файл отсутствует
    try:
        with open(file_name, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []  # Если файл повреждён, возвращаем пустой список

# Сохранение данных в файлы
def save_data(file_name, data):
    with open(file_name, "w") as file:
        json.dump(data, file, indent=4)

# Инициализация данных
notes = load_data(NOTES_FILE)
calendar = load_data(CALENDAR_FILE)
tasks = load_data(TASKS_FILE)

# --- Главная страница ---
@app.route('/')
def home():
    return render_template('home.html')

# --- Роуты для заметок ---
@app.route('/notes')
def notes_view():
    return render_template('index.html', notes=notes)

@app.route('/add', methods=['POST'])
def add_note():
    title = request.form.get('title')
    content = request.form.get('content')
    color = request.form.get('color') or "#fffae5"
    if title and content:
        notes.append({'title': title, 'content': content, 'color': color})
        save_data(NOTES_FILE, notes)
    return redirect(url_for('notes_view'))

@app.route('/delete', methods=['POST'])
def delete_note():
    note_index = int(request.form.get('index'))
    if 0 <= note_index < len(notes):
        notes.pop(note_index)
        save_data(NOTES_FILE, notes)
    return redirect(url_for('notes_view'))

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
        save_data(NOTES_FILE, notes)
    return redirect(url_for('notes_view'))

@app.route('/drag-notes')
def drag_notes():
    return render_template('drag_notes.html', notes=notes)

# --- Роуты для календаря ---
@app.route('/calendar')
def calendar_view():
    return render_template('calendar.html', calendar=calendar)

@app.route('/calendar/add', methods=['POST'])
def add_event():
    date = request.form.get('date')
    title = request.form.get('title')
    description = request.form.get('description')
    if date and title:
        calendar.append({'date': date, 'title': title, 'description': description or ''})
        save_data(CALENDAR_FILE, calendar)
    return redirect(url_for('calendar_view'))

@app.route('/calendar/delete', methods=['POST'])
def delete_event():
    event_index = int(request.form.get('index'))
    if 0 <= event_index < len(calendar):
        calendar.pop(event_index)
        save_data(CALENDAR_FILE, calendar)
    return redirect(url_for('calendar_view'))

@app.route('/calendar/edit', methods=['POST'])
def edit_event():
    event_index = int(request.form.get('index'))
    new_date = request.form.get('date')
    new_title = request.form.get('title')
    new_description = request.form.get('description')
    if 0 <= event_index < len(calendar):
        if new_date:
            calendar[event_index]['date'] = new_date
        if new_title:
            calendar[event_index]['title'] = new_title
        if new_description:
            calendar[event_index]['description'] = new_description
        save_data(CALENDAR_FILE, calendar)
    return redirect(url_for('calendar_view'))

# --- Роуты для задач ---
@app.route('/tasks')
def tasks_view():
    return render_template('tasks.html', tasks=tasks)

@app.route('/tasks/add', methods=['POST'])
def add_task():
    time = request.form.get('time')
    title = request.form.get('title')
    description = request.form.get('description')
    if time and title:
        tasks.append({'time': time, 'title': title, 'description': description or ''})
        save_data(TASKS_FILE, tasks)
    return redirect(url_for('tasks_view'))

@app.route('/tasks/delete', methods=['POST'])
def delete_task():
    task_index = int(request.form.get('index'))
    if 0 <= task_index < len(tasks):
        tasks.pop(task_index)
        save_data(TASKS_FILE, tasks)
    return redirect(url_for('tasks_view'))

@app.route('/tasks/edit', methods=['POST'])
def edit_task():
    task_index = int(request.form.get('index'))
    new_time = request.form.get('time')
    new_title = request.form.get('title')
    new_description = request.form.get('description')
    if 0 <= task_index < len(tasks):
        if new_time:
            tasks[task_index]['time'] = new_time
        if new_title:
            tasks[task_index]['title'] = new_title
        if new_description:
            tasks[task_index]['description'] = new_description
        save_data(TASKS_FILE, tasks)
    return redirect(url_for('tasks_view'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
