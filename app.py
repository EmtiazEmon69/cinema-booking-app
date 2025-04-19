from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# ✅ Step 2: Connect to SQLite
def connect_db():
    conn = sqlite3.connect('cinema.db')
    conn.row_factory = sqlite3.Row
    return conn

# ✅ Step 3: Initialize DB (Tables)
def init_db():
    conn = connect_db()
    with conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS movies (
                movie_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                director TEXT,
                genre TEXT,
                duration INTEGER,
                showtimes TEXT
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS bookings (
                booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT,
                contact TEXT,
                movie_id INTEGER,
                showtime TEXT,
                FOREIGN KEY (movie_id) REFERENCES movies(movie_id)
            )
        ''')
    conn.close()

# ✅ Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin123':
            session['logged_in'] = True
            return redirect(url_for('view_bookings'))
        else:
            flash('Invalid credentials!')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ✅ View Bookings (Protected)
@app.route('/')
@app.route('/bookings')
def view_bookings():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    conn = connect_db()
    bookings = conn.execute('''
        SELECT b.booking_id, b.customer_name, b.contact, b.showtime, m.title AS movie_title
        FROM bookings b
        JOIN movies m ON b.movie_id = m.movie_id
    ''').fetchall()
    conn.close()
    return render_template('bookings.html', bookings=bookings)

# ✅ Add Movie (Protected)
@app.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title']
        director = request.form['director']
        genre = request.form['genre']
        duration = request.form['duration']
        showtimes = request.form['showtimes']

        conn = connect_db()
        conn.execute('''
            INSERT INTO movies (title, director, genre, duration, showtimes)
            VALUES (?, ?, ?, ?, ?)
        ''', (title, director, genre, duration, showtimes))
        conn.commit()
        conn.close()
        return redirect(url_for('view_bookings'))

    return render_template('add_movie.html')

# ✅ List Movies (Public)
@app.route('/movies')
def list_movies():
    conn = connect_db()
    movies = conn.execute("SELECT * FROM movies").fetchall()
    conn.close()
    return render_template('movies.html', movies=movies)

# ✅ Book Ticket (Public)
@app.route('/book_ticket/<int:movie_id>', methods=['GET', 'POST'])
def book_ticket(movie_id):
    conn = connect_db()
    movie = conn.execute('SELECT * FROM movies WHERE movie_id = ?', (movie_id,)).fetchone()

    if request.method == 'POST':
        customer_name = request.form['customer_name']
        contact = request.form['contact']
        showtime = request.form['showtime']

        conn.execute('''
            INSERT INTO bookings (customer_name, contact, movie_id, showtime)
            VALUES (?, ?, ?, ?)
        ''', (customer_name, contact, movie_id, showtime))
        conn.commit()
        conn.close()
        return redirect(url_for('view_bookings'))

    conn.close()
    return render_template('book_ticket.html', movie=movie)

# ✅ Run app and initialize DB
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
