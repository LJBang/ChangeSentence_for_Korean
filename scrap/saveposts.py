import psycopg2
import dbinfo

class Databases():
    def __init__(self):
        self.db = psycopg2.connect(host=dbinfo.host, 
                            dbname=dbinfo.dbname, 
                            user=dbinfo.user, 
                            password=dbinfo.password, 
                            port=dbinfo.port)
        self.cursor = self.db.cursor()

    def __del__(self):
        self.cursor.close()
        self.db.close()
        
    def execute(self, query, args={}):
        self.cursor.execute(query, args)
        row = self.cursor.fetchall()
        return row
    
    def commit(self):
        self.cursor.commit()

class CRUD(Databases):
    def insertDB(self, table, column, data):
        sql = f"INSERT INTO {table}({column}) VALUES ({data});"
        try:
            self.cursor.execute(sql)
            #self.db.commit()
        except Exception as e:
            print("!!!!INSERT DB ERROR", e)
    
    def insertCommit(self):
        self.db.commit()

    def readDB(self, table, column):
        sql = f"SELECT {column} from {table}"
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
        except Exception as e:
            result = ("!!!!READ DB ERROR", e)
        return result

if __name__ == "__main__":
    db = CRUD()
    key = '인문학'
    content = '글 내용입니다. 사과, 배, 치즈 그리고 고양이가 있습니다.'
    db.insertDB(table='fruits', column='keyword, content', data=f"""'{key}', '{content+"1"}'""")
    db.insertDB(table='fruits', column='keyword, content', data=f"""'{key}', '{content+"2"}'""")
    db.insertDB(table='fruits', column='keyword, content', data=f"""'{key}', '{content+"3"}'""")
    db.insertCommit()
    print(db.readDB(table='fruits', column='*'))