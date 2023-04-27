# Import necessary modules from Flask, psycopg2, and requests libraries
from flask import Flask, render_template, jsonify, request, redirect, url_for, flash, session
import requests
import psycopg2

# Function to connect to the database
def connect_to_db():
    conn = psycopg2.connect(
        host="kashin.db.elephantsql.com",
        dbname="oxealukd",
        user="oxealukd",
        password="bxuSHvGQ5whMQ44OlXYBek0Gi88RCQmL"
    )
    return conn

# Function to create the 'users' table if it doesn't exist
def create_users_table():
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        first_name VARCHAR(255) NOT NULL,
        last_name VARCHAR(255) NOT NULL
    );''')
    conn.commit()
    conn.close()

# Call the function to create the 'users' table
create_users_table()

# Initialize the Flask app and set the secret key
app = Flask(__name__)
app.secret_key = "12345"

# Route to display all users
@app.route('/users')
def users():
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    all_users = cur.fetchall()
    conn.close()

    return render_template('users.html', users=all_users)

# Route for user registration
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']

        conn = connect_to_db()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO users (username, password, first_name, last_name) VALUES (%s, %s, %s, %s)", (username, password, first_name, last_name))
            conn.commit()
            flash("Account created successfully!", "success")
            return redirect(url_for('login'))
        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            flash("Username already exists!", "danger")
        conn.close()

    return render_template('signup.html')

# Route for user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cur.fetchone()
        conn.close()

        if user:
            session['user_id'] = user[0]
            session['username'] = user[1]
            flash("Logged in successfully!", "success")
            return redirect(url_for('home'))
        else:
            flash("Invalid credentials!", "danger")

    return render_template('login.html')

# Route for user logout
@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully!", "success")
    return redirect(url_for('login'))

# Function to fetch a random joke from JokeAPI
def get_joke():
   
    url = "https://jokeapi-v2.p.rapidapi.com/joke/Any"

    headers = {
	    "content-type": "application/octet-stream",
	    "X-RapidAPI-Key": "74bfefe667msh04af17251b4fc25p1b1813jsn720154ddf0e4",
	    "X-RapidAPI-Host": "jokeapi-v2.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    if data["type"] == "single":
        return data["joke"]
    else:
        return f"{data['setup']} {data['delivery']}"

# Route for the home page displaying a random joke
@app.route('/')
def home():
    joke = get_joke() 
    return render_template('home.html', joke=joke) 

# Route to fetch a new joke via AJAX
@app.route('/get_joke', methods=['POST'])
def get_joke_route():
    joke = get_joke() 
    return jsonify(joke=joke) 

# Route to search and fetch images from Pixabay API
@app.route('/search_image', methods=['POST'])
def search_image():
    query = request.form['query']
    url = "https://pixabay.com/api/"
    params = {
        "key": "35814311-08dba45448f39c4ea97385337",
        "q": query, 
        "per_page": 6 
    }
    response = requests.get(url, params=params) 
    data = response.json()
    images = [image["webformatURL"] for image in data["hits"]] 
    return jsonify(images=images) 

# Run the Flask app in debug mode
if __name__ == '__main__':
    app.run(debug=True)
