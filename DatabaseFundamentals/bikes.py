import sqlite3

def get_db_connection():
    return sqlite3.connect("bikes.db")

def distance_of_user(user):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """
    SELECT SUM(distance) 
    FROM Trips 
    JOIN Users ON Trips.user_id = Users.id 
    WHERE Users.name = ?
    """
    
    cursor.execute(query, (user,))
    result = cursor.fetchone()[0]
    conn.close()
    return result

def speed_of_user(user):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """
    SELECT SUM(distance), SUM(duration) 
    FROM Trips 
    JOIN Users ON Trips.user_id = Users.id 
    WHERE Users.name = ?
    """
    
    cursor.execute(query, (user,))
    result = cursor.fetchone()
    if result[0] is None or result[1] == 0:
        return 0
    
    distance_km = result[0] / 1000
    duration_hours = result[1] / 60
    avg_speed = round(distance_km / duration_hours, 2)
    conn.close()
    return avg_speed

def duration_in_each_city(day):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """
    SELECT Cities.name, SUM(Trips.duration)
    FROM Trips
    JOIN Bikes ON Trips.bike_id = Bikes.id
    JOIN Cities ON Bikes.city_id = Cities.id
    WHERE Trips.day = ?
    GROUP BY Cities.name
    """
    
    cursor.execute(query, (day,))
    result = cursor.fetchall()
    conn.close()
    return result

def users_in_city(city):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """
    SELECT COUNT(DISTINCT Users.id)
    FROM Trips
    JOIN Bikes ON Trips.bike_id = Bikes.id
    JOIN Cities ON Bikes.city_id = Cities.id
    JOIN Users ON Trips.user_id = Users.id
    WHERE Cities.name = ?
    """
    
    cursor.execute(query, (city,))
    result = cursor.fetchone()[0]
    conn.close()
    return result

def trips_on_each_day(city):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """
    SELECT Trips.day, COUNT(*)
    FROM Trips
    JOIN Bikes ON Trips.bike_id = Bikes.id
    JOIN Cities ON Bikes.city_id = Cities.id
    WHERE Cities.name = ?
    GROUP BY Trips.day
    """
    
    cursor.execute(query, (city,))
    result = cursor.fetchall()
    conn.close()
    return result

def most_popular_start(city):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """
    SELECT Stops.name, COUNT(*) as count
    FROM Trips
    JOIN Stops ON Trips.from_id = Stops.id
    JOIN Cities ON Stops.city_id = Cities.id
    WHERE Cities.name = ?
    GROUP BY Stops.name
    ORDER BY count DESC, Stops.name DESC
    LIMIT 1
    """
    
    cursor.execute(query, (city,))
    result = cursor.fetchone()
    conn.close()
    return result