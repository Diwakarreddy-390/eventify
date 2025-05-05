from db_connecetion import get_connection

conn = get_connection()
cursor = conn.cursor()

def create(title,date,location,description,image,email):
   cursor.execute("insert into events(title,date_time,location,description,image,created) values (%s,%s,%s,%s,%s,%s)",(title,date,location,description,image,email))
   conn.commit()
   conn.close()
   cursor.close()