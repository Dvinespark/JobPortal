# database codes

def get_rows(sql):
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute(sql)
        results = cursor.fetchall()
    return results
