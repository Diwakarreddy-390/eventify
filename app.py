from flask import Flask, render_template, request, redirect, url_for, session
from login import Login
from register import Register
import os
import base64
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
    print(f"Location selected: {location}")  # Debugging line
    if not location:
        location = "Default Location"  # Set a default location if needed

    events = show(location)  # This now returns a list of dictionaries
    event_list = []

    for row in events:
        

        event_list.append({
            "title": row["title"],
            "event_datetime": row["event_datetime"],
            "description": row["description"],
            "location": row["location"],
            "photo": row["photo"],
            "event_id":row["event_id"]
        })

    login_instance = Login(email)
    name = login_instance.name()

    return render_template("events.html", events=event_list, selected_location=location, name=name)

@app.route('/explore')
def explore():
    email = session.get("email")
    login_instance = Login(email)
    events = login_instance.explore()
    processed_events = []

    for event in events:
        processed_events.append({
            "title": event["title"],
            "event_datetime": event["event_datetime"],
            "image_name": event["image"],  # Optional: if storing filename
            "photo_data": event["photo"],  # Already base64 string
            "description": event["description"],
            "location": event["location"]
        })

    name = login_instance.name()
    return render_template("event_detail.html", events=processed_events, name=name)


    
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

        email = session.get("email")

        # Extract image filename and binary data separately
        image_filename = image.filename
        image_data = image.read() if image and image.filename else None  # Read image as binary

        
            # Save event details with image filename and binary data
        create(title, date, location, description, image_filename, image_data, email)
        

        return redirect(url_for('admin_dashboard'))

    return render_template('create_event.html')




@app.route('/edit_event/<string:event_title>', methods=['POST', 'GET'])
def edit_event(event_title):
    conn = get_connection()
    cursor = conn.cursor(buffered=True)

    # Fetch existing event data
    cursor.execute("SELECT title, date_time, photo, location, description, image FROM events WHERE title=%s", (event_title,))
    event_data = cursor.fetchone()
    cursor.fetchall()  # Clear remaining results

    if not event_data:
        cursor.close()
        conn.close()
        return "Event not found", 404
    photo_base64 = base64.b64encode(event_data[2]).decode('utf-8')
    photo_data = f"data:image/jpeg;base64,{photo_base64}"
    event = {
        "title": event_data[0],
        "event_datetime": event_data[1],
        "photo": photo_data,
        "location": event_data[3],
        "description": event_data[4],
        "image_name": event_data[5]
    }

    cursor.close()
    conn.close()

    # Handle POST
    if request.method == 'POST':
        title = request.form.get('title')
        date = request.form.get('date_time')
        location = request.form.get('location')
        description = request.form.get('description')
        image = request.files.get("image")

        photo_data = event["photo"]
        image_filename = event["image_name"]

        # If a new image is uploaded
        if image and image.filename != "":
            photo_data = image.read()
            image_filename = image.filename

        conn = get_connection()
        cursor = conn.cursor(buffered=True)

        cursor.execute(
            "UPDATE events SET title=%s, date_time=%s, location=%s, description=%s, photo=%s, image=%s WHERE title=%s",
            (title, date, location, description, photo_data, image_filename, event_title)
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
