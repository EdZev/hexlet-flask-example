import psycopg2
from psycopg2.extras import RealDictCursor


class UserRepository:
    def __init__(self, db_url):
        self.db_url = db_url

    def get_connection(self):
        return psycopg2.connect(self.db_url)

    def get_content(self):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as c:
                c.execute("SELECT * FROM users_test")
                return c.fetchall()

    def find(self, id):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as c:
                c.execute("SELECT * FROM users_test WHERE id = %s", (id,))
                return c.fetchone()

    def save(self, user_data):
        with self.get_connection() as conn:
            with conn.cursor() as c:
                # print(f'user_data - {user_data}')
                if 'id' not in user_data:
                    c.execute(
                        '''
                        INSERT INTO users_test (name, email)
                        VALUES (%s, %s) RETURNING id
                        ''',
                        (user_data['name'], user_data['email'])
                    )
                    user_data['id'] = c.fetchone()[0]
                else:
                    c.execute(
                        '''
                        UPDATE users_test
                        SET name = %s, email = %s WHERE id = %s
                        ''',
                        (
                            user_data['name'],
                            user_data['email'],
                            user_data['id']
                            )
                    )
            conn.commit()
        return user_data['id']

    def destroy(self, id):
        with self.get_connection() as conn:
            with conn.cursor() as c:
                c.execute(
                    "DELETE FROM users_test WHERE id = %s",
                    (id,)
                )
            conn.commit()
