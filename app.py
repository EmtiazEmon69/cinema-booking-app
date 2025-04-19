from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# ✅ Connect to SQLite
def connect_db():
    conn = sqlite3.connect('cinema.db')
    conn.row_factory = sqlite3.Row
    return conn

# ✅ Initialize DB (Tables)
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
                showtimes TEXT,
                poster TEXT
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

# ✅ Add 'poster' column (only once)
def add_poster_column():
    conn = connect_db()
    try:
        conn.execute("ALTER TABLE movies ADD COLUMN poster TEXT")
        print("✅ 'poster' column added to movies table.")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("ℹ️ 'poster' column already exists. Skipping.")
        else:
            raise
    conn.close()

# ✅ Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin123':
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials!')
            return redirect(url_for('login'))
    return render_template('login.html')

# ✅ Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ✅ Dashboard
@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('dashboard.html')

# ✅ Redirect root to login or dashboard
@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return redirect(url_for('dashboard'))

# ✅ View Bookings (Protected)
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
        poster = request.form['poster']

        conn = connect_db()
        conn.execute('''
            INSERT INTO movies (title, director, genre, duration, showtimes, poster)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (title, director, genre, duration, showtimes, poster))
        conn.commit()
        conn.close()
        return redirect(url_for('view_bookings'))

    return render_template('add_movie.html')

# ✅ List Movies (Public) — with search and genre filter
@app.route('/movies')
def list_movies():
    genre = request.args.get('genre')
    search = request.args.get('search')

    conn = connect_db()
    query = "SELECT * FROM movies WHERE 1=1"
    params = []

    if genre:
        query += " AND genre LIKE ?"
        params.append(f"%{genre}%")

    if search:
        query += " AND title LIKE ?"
        params.append(f"%{search}%")

    movies = conn.execute(query, params).fetchall()
    conn.close()
    return render_template('movies.html', movies=movies, genre=genre or '', search=search or '')

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

# ✅ Run App
if __name__ == "__main__":
    init_db()
    add_poster_column()
    app.run(debug=True)
