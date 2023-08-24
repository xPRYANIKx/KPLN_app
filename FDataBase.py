import json

import psycopg2
import psycopg2.extras
import time
import math
import re
from flask import url_for, flash
from werkzeug.security import generate_password_hash


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def add_user(self, form_data):
        try:
            # Получаем данные из формы регистрации
            first_name = form_data.get('first_name')
            last_name = form_data.get('last_name')
            email = form_data.get('email')
            user_role = form_data.get('user_role')
            user_priority = form_data.get('user_priority')
            password = generate_password_hash(form_data.get('password'))

            query = """INSERT INTO users (first_name, last_name, email, user_priority, password, user_role_id)
                            VALUES (%s, %s, %s, %s, %s, (SELECT role_id FROM user_role WHERE role_name = %s LIMIT 1))"""
            values = (first_name, last_name, email, user_priority, password, user_role)
            # Check to same email value in db
            self.__cur.execute(f"SELECT email FROM users WHERE email = '{values[2]}'")
            res = self.__cur.fetchone()
            if res:
                flash(message=['Логин уже есть в базе', ''], category='error')
                return False

            self.__cur.execute(query, values)
            self.__db.commit()
            self.__cur.close()
        except Exception as e:
            flash(message=['Ошибка добавления пользователя в БД', str(e)], category='error')
            return False

        flash(message=['Пользователь внесен', ''], category='success')
        return True

    def get_user(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE user_id = {user_id} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                flash(message=['Пользователь не найден', ''], category='error')
                return False

            return res
        except Exception as e:
            flash(message=['Ошибка получения данных из БД', str(e)], category='error')

        return False

    # def get_name(self):
    #     try:
    #         self.__cur.execute(f"SELECT * FROM users WHERE user_id = {user_id} LIMIT 1")
    #         res = self.__cur.fetchone()
    #         if not res:
    #             flash(f'❌ Пользователь не найден', category='error')
    #             print("Пользователь не найден")
    #             return False
    #
    #         return res
    #     except Exception as e:
    #         flash(f'❗ Ошибка получения данных из БД {str(e)}', category='error')
    #         print("Ошибка получения данных из БД " + str(e))
    #
    #     return False

    def get_user_by_email(self, email):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE email = '{email}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                flash(message=['Пользователь не найден', ''], category='error')
                return False

            return res
        except Exception as e:
            flash(message=['Ошибка получения данных из БД', str(e)], category='error')

        return False

    def updateUserAvatar(self, avatar, user_id):
        if not avatar:
            return False

        try:
            binary = sqlite3.Binary(avatar)
            self.__cur.execute(f"UPDATE users SET avatar = ? WHERE id = ?", (binary, user_id))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка обновления аватара в БД: " + str(e))
            return False
        return True
