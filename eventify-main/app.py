from flask import Flask, render_template, request, redirect, url_for, session
from login import Login
from register import Register
import os
from werkzeug.utils import secure_filename
from create_event import create
from db_connecetion import get_connection
from show_events import show
app = Flask(__name__)
app.secret_key = "12345" 

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    global email
    error = None  # Ensure error is always defined

    if request.method == 'POST':
        email = request.form["email"]
        password = request.form["password"]
        check = Login(email).check_user(password)

        if check == "user":
            session["email"] = email  # Store email in session
            return redirect(url_for('events'))
        elif check == "admin":
            session["email"] = email
            return redirect(url_for('admin_dashboard'))
        else:
            error = "Invalid email or password"

    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        user = request.form.get('user_type')

        if Register(name, email, password, user):
            return redirect(url_for('login'))
        else:
            return render_template('register.html', error="Email already exists!")

    return render_template('register.html')

@app.route('/events', methods=['POST', 'GET'])
def events():
    email = session.get("email")
    if not email:
        return redirect(url_for("login"))  
    location = request.form.get("location")
    events = show(location)
    login_instance = Login(email)
    name = login_instance.name()
    return render_template("events.html", events=events, selected_location=location, name=name)

@app.route('/explore')
def explore():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT title, description, date_time, image FROM events")
    events = cursor.fetchall()
    
    event_list = []
    for event in events:
        event_dict = {
            "title": event[0],
            "description": event[1],
            "date_time": event[2],
            "image": event[3]
        }
        event_list.append(event_dict)
    return render_template('event_detail.html',events=event_list)
    
@app.route('/admin_dashboard', methods=['GET', 'POST'])
def admin_dashboard():
   if request.method == 'POST':
      return redirect(url_for('create_event')) 

   email = session.get("email")  
   if not email:
      return redirect(url_for('login')) 

   login_instance = Login(email)  
   event_list = login_instance.admin_events() 
   count = login_instance.event_count()
   name = login_instance.name()[0]
   return render_template('admin_dashboard.html', events=event_list, event_count=count,name=name)

@app.route('/create_event', methods=['GET', 'POST'])
def create_event():
    if request.method == 'POST':
        title = request.form.get("title")
        date = request.form.get("date_time")
        location = request.form.get("location")
        description = request.form.get("description")
        image = request.files.get("image")

        # Validate required fields
        if not all([title, date, location, description]):
            return "All fields are required!", 400

        email = session.get("email")
        if not email:
            return redirect(url_for('login'))

        image_data = image.read() if image and image.filename else None  # Read image as binary

        try:
            # Ensure create() function correctly inserts image_data
            create(title, date, location, description, image_data, email)
        except Exception as e:
            return f"Error saving event: {str(e)}", 500

        return redirect(url_for('admin_dashboard'))

    return render_template('create_event.html')


@app.route('/edit_event/<string:event_title>', methods=['POST', 'GET'])
def edit_event(event_title):
    conn = get_connection()
    cursor = conn.cursor(buffered=True)  # Use a buffered cursor to avoid unread results

    cursor.execute("SELECT title, date_time, image, location, description FROM events WHERE title=%s", (event_title,))
    event_data = cursor.fetchone()  # Ensure the first row is retrieved
    cursor.fetchall()  # Fetch any remaining results to clear unread data

    if not event_data:
        cursor.close()
        conn.close()
        return "Event not found", 404

    event = {
        "title": event_data[0],
        "event_datetime": event_data[1],
        "image_name": event_data[2],
        "location": event_data[3],
        "description": event_data[4]
    }

    cursor.close()  # Close cursor after fetching data
    conn.close()

    if request.method == 'POST':
        title = request.form.get('title')
        date = request.form.get('date_time')
        location = request.form.get('location')
        description = request.form.get('description')
        image = request.files.get("image")

        image_filename = event["image_name"]  # Retain existing image by default

        if image and image.filename:
            filename = secure_filename(image.filename)
            app.config["UPLOAD_FOLDER"] = "static/uploads"

            if event["image_name"]:
                image_path = os.path.join(app.config["UPLOAD_FOLDER"], event["image_name"])
                if os.path.exists(image_path):
                    os.remove(image_path)

            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            image.save(filepath)
            image_filename = filename  # Update to new image filename

        conn = get_connection()
        cursor = conn.cursor(buffered=True)  # Use buffered cursor for safety

        cursor.execute(
            "UPDATE events SET title=%s, date_time=%s, location=%s, description=%s, image=%s WHERE title=%s",
            (title, date, location, description, image_filename, event_title)
        )

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('admin_dashboard'))

    return render_template('admin_edit.html', event=event)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    email = session.get("email")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("select user_id from users where email=%s",(email,))
    num = cursor.fetchone()
    cursor.execute("""
    SELECT events.title, events.date_time
    FROM ticket_purchases
    JOIN events ON ticket_purchases.event_number = events.event_number
    WHERE ticket_purchases.user_id = %s;
""", (num))
    events = cursor.fetchall()
    
    event_list = []
    for event in events:
        event_dict = {
            "title": event[0],
            "date": event[1],
        }
        event_list.append(event_dict)
    return render_template('dashboard.html',events=event_list)

@app.route('/buy_ticket/<int:event_id>', methods=['POST', 'GET'])
def buy_ticket(event_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        email = session.get("email")
        cursor.execute("SELECT full_name, user_id FROM users WHERE email=%s", (email,))
        n = cursor.fetchone()
        name = n[0] if n else "Guest"
        user_id = n[1] if n else None

        cursor.execute("SELECT title FROM events WHERE event_number=%s", (event_id,))
        title = cursor.fetchone()
        title = title[0] if title else "Unknown Event"

        if request.method == 'POST' and user_id is not None:
            cursor.execute("INSERT INTO ticket_purchases(user_id, event_number) VALUES(%s, %s)", (user_id, event_id))
            conn.commit()  # Fix commit location
            return redirect(url_for('events'))

    except Exception as e:
        print(f"Error: {e}")

    finally:
        cursor.close()
        conn.close()

    return render_template('buy_ticket.html', name=name, email=email, title=title)

if __name__ == "__main__":
    app.run(debug=True)
