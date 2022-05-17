import pymysql


connection = pymysql.connect(
                user     = "jcavalca466",
                password = "jcavalca466985",
                host     = "localhost",
                db       = "jcavalca466",
)


with open("DB_drop.sql", "r") as file:
        create_queries = file.readlines()
        for create_query in create_queries:
                with connection.cursor() as cursor:
                        cursor.execute(create_query)
                connection.commit()

