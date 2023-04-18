import sqlite3


class Customer:
    def __init__(self):
        self.conn = sqlite3.connect('data.db')
        table_create_query = '''CREATE TABLE IF NOT EXISTS Client_Data 
                        (Id INTEGER PRIMARY KEY, Firstname TEXT, Lastname TEXT, DateOfBirth TEXT, Age INT, Gender TEXT, 
                        Address TEXT, PhoneNumber TEXT, UserName TEXT, Password TEXT)
                '''
        self.cur = self.conn.cursor()
        self.conn.execute(table_create_query)
        self.conn.commit()

    def fetch(self):
        self.cur.execute("SELECT * FROM Client_Data")
        rows = self.cur.fetchall()
        return rows

    def insert(self, FirstName, LastName, DoB,
                    Age, Gender, Address, Phone, User, Password):
        self.data_insert_query = '''INSERT INTO Client_Data (Id, Firstname, Lastname, DateOfBirth, 
                Age, Gender, Address, PhoneNumber, UserName, Password) VALUES 
                (NULL,?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        self.data_insert_tuple = (FirstName, LastName, DoB,
                                    Age, Gender, Address, Phone, User, Password)
        self.cur.execute(self.data_insert_query, self.data_insert_tuple)
        self.conn.commit()

    def remove(self, id):
        self.cur.execute("DELETE FROM Client_Data WHERE Id=?", (id,))
        self.conn.commit()

    def update(self, Id, FirstName, LastName, DoB,
                    Age, Gender, Address, Phone, User, Password):
        self.cur.execute("UPDATE Client_Data SET Firstname = ?, Lastname = ?, DateOfBirth = ?, Age = ?, Gender = ?, Address = ?, PhoneNumber = ?, UserName = ?, Password = ? WHERE Id = ?",
                         (FirstName, LastName, DoB,
                            Age, Gender, Address, Phone, User, Password, Id))
        self.conn.commit()

    def __del__(self):
        self.conn.close()