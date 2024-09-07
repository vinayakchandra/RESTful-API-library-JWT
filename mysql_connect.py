import mysql.connector as mc


class ConnectSql:
    mydb = mc.connect(host="localhost", user="root", password="vinayak@786", database="library")
    myCursor = mydb.cursor()
    myResult = ""

    # Sql functions
    # POST
    def insertBook(self, id: int, name: str, author:str):
        self.myCursor.execute(f"INSERT INTO books(bookID, bookName, author) VALUES( {id}, '{name}', '{author}');")
        self.mydb.commit()
        return self.getBook(id)

    # GET
    def getAllBooks(self):
        self.myCursor.execute("select * from books;")
        self.myResult = self.myCursor.fetchall()
        return self.myResult

    # GET
    def getBook(self, id):
        self.myCursor.execute(f"select * from books WHERE bookID = {id};")
        self.myResult = self.myCursor.fetchall()
        return self.myResult

    # DELETE
    def deleteBook(self, id):
        book = self.getBook(id)
        self.myCursor.execute(f"DELETE FROM books WHERE bookID = {id};")
        self.mydb.commit()

        return {"deleted" : book}

    # UPDATE
    def updateBook(self, id: int, name):
        self.myCursor.execute(f"UPDATE books SET bookName = '{name}' WHERE bookID = {id};")
        self.mydb.commit()
        return self.getBook(id)


if __name__ == "__main__":
    sql = ConnectSql()
    # a = sql.deleteBook(2)
    a = sql.updateBook(1, "test")
    print(a)
