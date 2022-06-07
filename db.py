import pymysql

def executeSelect(query):
    connection = pymysql.connect(
        user="jcavalca466",
        password="jcavalca466985",
        host="localhost",
        db="jcavalca466",
        port=9090,  # comment out this if running on frank
    )
    with connection.cursor() as cursor:
        cursor.execute(query)
    connection.commit()
    return cursor.fetchall()