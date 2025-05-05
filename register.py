from db_connecetion import get_connection


def Register(full_name,email,password,user_type):
   conn = get_connection()
   cursor = conn.cursor()
   cursor.execute("insert into users(full_name,email,password,user_type) values (%s,%s,%s,%s)",(full_name,email,password,user_type))
   n = cursor.fetchone()
   if n:
      cursor.close()
      conn.close()
      return False
   conn.commit()
   cursor.close()
   conn.close()   
   return True
   