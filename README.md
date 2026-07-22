#  Movie Explorer

A full-stack Flask web application that allows users to search for movies using the TMDB API, create an account, and manage their own personal favorites list.

##  Features

*  Search movies using The Movie Database (TMDB) API
*  View detailed movie information
*  User registration and login
*  Secure password hashing with Werkzeug
*  User-specific favorites
*  Add and remove favorite movies
*  Update saved movie information
*  Protected routes using Flask sessions
*  SQLite database with repository pattern

---

##  Tech Stack

### Backend

* Python
* Flask
* SQLite
* Werkzeug
* Requests

### Frontend

* HTML5
* CSS3
* Jinja2 Templates

### Tools

* Git
* GitHub
* TMDB API

---

## Project Structure

```text
movie-explorer/
│
├── app.py
├── database.py
├── repositories/
│   ├── favorites_repo.py
│   └── users_repo.py
├── services/
│   └── tmdb_service.py
├── templates/
├── static/
├── requirements.txt
└── .env.example
```

---

##  Installation

Clone the repository:

```bash
git clone https://github.com/annasofiadr/movie-explorer.git
```

Move into the project folder:

```bash
cd movie-explorer
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment:

**Windows**

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
TMDB_API_KEY=your_tmdb_api_key
SECRET_KEY=your_secret_key
```

Run the application:

```bash
python app.py
```

Open your browser and visit:

```text
http://127.0.0.1:5000
```

---

##  How It Works

1. Register a new account.
2. Log in securely.
3. Search for movies through the TMDB API.
4. View detailed information about each movie.
5. Add or remove movies from your personal favorites list.
6. Access your favorites from any page after logging in.

---

##  Database

The application uses SQLite with two main tables:

### Users

* id
* username
* password_hash

### Favorites

* id
* user_id
* movie_id
* title
* poster_path
* rating

Each favorite is linked to its owner through the `user_id` foreign key.

---

##  Architecture

The project follows a simple layered architecture:

```text
Flask Routes
      │
      ▼
Repositories
      │
      ▼
SQLite Database

External API (TMDB)
      ▲
      │
Service Layer
```

This separation keeps the application easier to maintain, test, and extend.

---

##  Security

* Passwords are never stored in plain text.
* Passwords are hashed using Werkzeug.
* Sensitive configuration is stored in environment variables.
* User sessions protect authenticated routes.

---

##  Future Improvements

* Movie reviews
* User profile page
* Pagination
* Dark/Light theme switch
* Watchlist
* Responsive UI improvements
* Docker support
* PostgreSQL deployment
* Automated tests

---


##  Author

**Annasofia Drosou**

GitHub: https://github.com/annasofiadr
