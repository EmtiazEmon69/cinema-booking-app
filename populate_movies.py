import sqlite3

# Connect to SQLite DB
conn = sqlite3.connect('cinema.db')

# Sample movie data
movies = [
    ("The Matrix", "The Wachowskis", "Sci-Fi", 136, "2:00 PM, 6:00 PM", "https://m.media-amazon.com/images/I/51EG732BV3L.jpg"),
    ("Inception", "Christopher Nolan", "Thriller", 148, "1:30 PM, 5:00 PM", "https://m.media-amazon.com/images/I/81p+xe8cbnL._AC_SL1500_.jpg"),
    ("Toy Story", "John Lasseter", "Animation", 81, "11:00 AM, 3:00 PM", "https://m.media-amazon.com/images/I/51NKhnjhpGL.jpg"),
    ("Titanic", "James Cameron", "Romance", 195, "4:00 PM, 7:30 PM", "https://m.media-amazon.com/images/I/71c05lTE03L.jpg"),
    ("Avengers: Endgame", "Anthony & Joe Russo", "Action", 181, "12:00 PM, 6:00 PM", "https://m.media-amazon.com/images/I/81ExhpBEbHL._AC_SL1500_.jpg"),
    ("Frozen", "Chris Buck, Jennifer Lee", "Animation", 102, "10:00 AM, 2:00 PM", "https://m.media-amazon.com/images/I/81Ro+qI9uVL._AC_SL1500_.jpg"),
    ("Joker", "Todd Phillips", "Drama", 122, "3:00 PM, 8:00 PM", "https://m.media-amazon.com/images/I/81aA7hEEykL._AC_SL1500_.jpg"),
    ("Interstellar", "Christopher Nolan", "Sci-Fi", 169, "1:00 PM, 6:00 PM", "https://m.media-amazon.com/images/I/91kFYg4fX3L._AC_SL1500_.jpg"),
    ("Finding Nemo", "Andrew Stanton", "Animation", 100, "11:30 AM, 4:00 PM", "https://m.media-amazon.com/images/I/51Qvs9i5a%2BL.jpg"),
    ("Black Panther", "Ryan Coogler", "Action", 134, "12:30 PM, 7:00 PM", "https://m.media-amazon.com/images/I/81tLZ7zkrJL._AC_SL1500_.jpg")
]

# Insert data
with conn:
    conn.executemany('''
        INSERT INTO movies (title, director, genre, duration, showtimes, poster)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', movies)

print("✅ 10 sample movies added to the database.")
conn.close()
