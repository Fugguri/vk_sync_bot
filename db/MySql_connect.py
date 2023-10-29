from datetime import date
import pymysql
from config import Config
from models import UserClient,User


class Database:
    def __init__(self,cfg:Config ):
        self.cfg:Config = cfg
        self.connection = pymysql.connect(
            host=self.cfg.tg_bot.host,
            user=self.cfg.tg_bot.user,
            port=self.cfg.tg_bot.port,
            password=self.cfg.tg_bot.password,
            database=self.cfg.tg_bot.database,
        )
        self.connection.autocommit(True)

    def cbdt(self):
        with self.connection.cursor() as cursor:
            create = """CREATE TABLE IF NOT EXISTS users
                        (id INT PRIMARY KEY AUTO_INCREMENT,
                        telegram_id BIGINT UNIQUE NOT NULL ,
                        full_name TEXT,
                        username TEXT,
                        has_acces BOOL DEFAULT false
                        );"""
            cursor.execute(create)
            self.connection.commit()

        with self.connection.cursor() as cursor:
            create =""" CREATE TABLE IF NOT EXISTS clients
                    (id INT PRIMARY KEY AUTO_INCREMENT,
                    user_id INT,
                    api_id INT,
                    api_hash TEXT,
                    phone TEXT NOT NULL,
                    ai_settings TEXT,
                    mailing_text TEXT,
                    answers BIGINT DEFAULT 0,
                    gs TEXT UNIQUE ,
                    is_active BOOL DEFAULT false,
                    FOREIGN KEY(user_id) REFERENCES users(id) )"""
            cursor.execute(create)
            self.connection.commit()


    def add_user(self, user):
        self.connection.ping()
        with self.connection.cursor() as cursor:
            cursor.execute("INSERT IGNORE INTO users (full_name, telegram_id, username) VALUES (%s, %s, %s) ",(user.full_name, user.id, user.username))
            self.connection.commit()
            self.connection.close()
            
    def create_client(self,user_id, phone, api_id, api_hash):
        self.connection.ping()
        with self.connection.cursor() as cursor:
            cursor.execute(
            "INSERT IGNORE INTO clients (user_id,phone, api_id, api_hash) VALUES ((SELECT id FROM users WHERE telegram_id=%s ), %s, %s, %s)",(user_id, phone, api_id, api_hash))
            self.connection.commit()
            self.connection.close()
        
            
    def get_user(self,telegram_id):
        self.connection.ping()
        with self.connection.cursor() as cursor:
            cursor.execute(
                """SELECT id, telegram_id, username, full_name, has_acces
                FROM users
                WHERE telegram_id=%s""",(telegram_id,))
            res = cursor.fetchone()
            self.connection.commit()
            self.connection.close()        
            user = User(*res)
        return user


    def get_client(self,id):
        self.connection.ping()
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT id, user_id, api_id, api_hash, phone, ai_settings, mailing_text,answers, gs,is_active FROM clients WHERE id=%s",(id,))
            res = cursor.fetchone()
            self.connection.commit()
            self.connection.close()        
            client = UserClient(*res)
            return client

    def get_client_by_phone(self,phone):
        self.connection.ping()
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT id, user_id, api_id, api_hash, phone, ai_settings, mailing_text,answers, gs,is_active FROM clients WHERE phone=%s",(phone))
            res = cursor.fetchone()
            self.connection.commit()
            self.connection.close()
            print(res,phone)        
            client = UserClient(*res)
            return client
        
    def get_clients(self,user_id):
        self.connection.ping()
        users = list()
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT id,user_id,api_id,api_hash,phone,ai_settings,mailing_text,answers, gs,is_active FROM clients where user_id=%s",(user_id))
            res = cursor.fetchall()
            self.connection.commit()
            self.connection.close()        
            for re in res:
                user = UserClient(*re)
                users.append(user)
            return users
    
    def get_active_clients(self):
        self.connection.ping()
        users = list()
        with self.connection.cursor() as cursor:
            cursor.execute("""SELECT c.id, c.user_id, c.api_id, c.api_hash, c.phone, c.ai_settings, c.mailing_text, c.answers, c.gs, c.is_active 
                           FROM clients as c
                           LEFT JOIN users as u on c.user_id=u.id
                           WHERE c.is_active=1 AND u.has_acces=1 """)
            res = cursor.fetchall()
            self.connection.commit()
            self.connection.close()        
            for re in res:
                user = UserClient(*re)
                users.append(user)
            return users
    
        
    def get_client_ai_settings(self,id):
        self.connection.ping()
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT ai_settings FROM clients where id=%s",(id,))
            res = cursor.fetchone()
            self.connection.commit()
            self.connection.close()        
            return res
    
    def get_client_mailing_text(self,id):
        self.connection.ping()
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT mailing_text FROM clients where id=%s",(id,))
            res = cursor.fetchone()
            self.connection.commit()
            self.connection.close()        
            return res
    
    def get_client_gs_name(self,id):
        self.connection.ping()
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT gs FROM clients where id=%s",(id,))
            res = cursor.fetchone()
            self.connection.commit()
            self.connection.close()        
            return res
    
        
    def edit_client_ai_settings(self,text, id):
        self.connection.ping()
        with self.connection.cursor() as cursor:
            cursor.execute("UPDATE clients SET ai_settings=%s WHERE id=%s",(text,id,))
            self.connection.commit()
            self.connection.close()

    def edit_client_mailing_text(self,text, id):
        self.connection.ping()
        with self.connection.cursor() as cursor:
            cursor.execute("UPDATE clients SET mailing_text=%s WHERE id=%s",(text,id,))
            self.connection.commit()
            self.connection.close()
            
    def edit_client_gs(self,text, id):
        self.connection.ping()
        with self.connection.cursor() as cursor:
            cursor.execute("UPDATE clients SET gs=%s WHERE id=%s",(text,id,))
            self.connection.commit()
            self.connection.close()
            
    def start_new_dialog_counter_update(self,phone):
        self.connection.ping()
        with self.connection.cursor() as cursor:
            cursor.execute("UPDATE clients SET answers=answers+1 WHERE phone=%s",(phone,))
        self.connection.commit()
        self.connection.close()

    def is_active(self, telegram_id):
        self.connection.ping()
        with self.connection.cursor() as cursor:
            cursor.execute(
                "SELECT is_active FROM clients WHERE telegram_id=%s", (telegram_id,))
            res = cursor.fetchone()
            self.connection.close()
        return res

    def update_all_clients(self,recepient_client_id, user_id):
        self.connection.ping()
        with self.connection.cursor() as cursor:
            cursor.execute("""UPDATE clients 
                      SET 
                      mailing_text=(SELECT mailing_text FROM clients WHERE id=%s),
                      ai_settings=(SELECT ai_settings FROM clients WHERE id=%s)
                      WHERE user_id=%s""",(recepient_client_id,recepient_client_id,user_id))
        self.connection.commit()
        self.connection.close()

    def give_access(self,username):
        self.connection.ping()
        with self.connection.cursor() as cursor:
            cursor.execute("UPDATE users SET has_acces=%s WHERE username=%s",(True,username))
            res = cursor.fetchall()
            self.connection.commit()
            self.connection.close()

    def take_access(self,username):
        self.connection.ping()
        with self.connection.cursor() as cursor:
            cursor.execute("UPDATE users SET has_acces=%s WHERE username=%s",(False,username))
            res = cursor.fetchall()
            self.connection.commit()
            self.connection.close()

    def set_client_active(self,client_id):
        self.connection.ping()
        with self.connection.cursor() as cursor:
            cursor.execute("UPDATE clients SET is_active=%s WHERE id=%s",(1,client_id))
            res = cursor.fetchall()
            self.connection.commit()
            self.connection.close()

    def delete_client(self,id):
        self.connection.ping()
        with self.connection.cursor() as cursor:
            cursor.execute("DELETE FROM clients WHERE id=%s",(id))
            res = cursor.fetchall()
            self.connection.commit()
            self.connection.close()
