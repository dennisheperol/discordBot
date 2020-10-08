import psycopg2

import secrets.secrets as secret


def wrapper(func, args):
    try:
        connection = psycopg2.connect(user=secret.db_username,
                                      password=secret.db_password,
                                      host=secret.db_host,
                                      port=secret.db_port,
                                      database=secret.db_database)
        cursor = connection.cursor()

        db = {'connection': connection, 'cursor': cursor}
        return func(db, args)

    except (Exception, psycopg2.Error) as error:
        print("Error in operation", error)

    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()

