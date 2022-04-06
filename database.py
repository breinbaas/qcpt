import psycopg2
from .secrets import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
from leveelogic.objects.soilprofile1 import SoilProfile1

class Database:
    def __init__(self):
        self.conn = psycopg2.connect(f"dbname='{DB_NAME}' user='{DB_USER}' password='{DB_PASSWORD}' host='{DB_HOST}' port='{DB_PORT}'")     
        

    def select(self, sql):
        cur = self.conn.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        cur.close()        
        return row

    def execute(self, sql):
        cur = self.conn.cursor()
        try:
            cur.execute(sql)
            self.conn.commit()
            cur.close() 
        except Exception as e:
            return False       
        
        return True

    def get_cpt_interpretation(self, cpt_id: int) -> SoilProfile1:
        """Get the cpt interpretation data or None if cpt_id is not known"""
        row = self.select(f"SELECT raw FROM cpt_interpretations WHERE cpt_id={cpt_id}")
        if row:
            return SoilProfile1.from_short_string(row[0])
        else:
            return None

    def add_cpt_interpretation(self, cpt_id: int, interpretation: str):
        """If existing then update (if interpretation is not empty string) or remove (if interpretation is empty string) else add"""
        if self.get_cpt_interpretation(cpt_id):
            if interpretation != "":
                sql = f"UPDATE cpt_interpretations SET raw='{interpretation}' WHERE cpt_id={cpt_id}"
            else:
                sql = f"DELETE FROM cpt_interpretations WHERE cpt_id={cpt_id}"
            return self.execute(sql)
        elif interpretation != "":
            sql = f"INSERT INTO cpt_interpretations (cpt_id, raw) VALUES ({cpt_id}, '{interpretation}')"
            return self.execute(sql)
        



# if __name__ == "__main__":
#     db = Database()
#     print(db.get_cpt_interpretation(1))
#     print(db.add_cpt_interpretation(2, 'test3'))


