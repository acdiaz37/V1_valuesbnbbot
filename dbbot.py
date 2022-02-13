import sqlite3 as sql


def createDB():
    conn = sql.connect("bnbvalues.db")
    conn.commit()
    conn.close()

def createTable():
    conn = sql.connect("bnbvalues.db")
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE bnbcontracts(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nameContract TEXT NOT NULL,
            contract TEXT NOT NULL
        )
        """
        )
    conn.commit()
    conn.close()

def insertContract(nameContract, contract):
    conn = sql.connect("bnbvalues.db")
    cursor = conn.cursor()
    cursor.execute(f"""
            INSERT INTO bnbcontracts(nameContract, contract) 
            VALUES ('{nameContract}', '{contract}');
        """
        )
    conn.commit()
    conn.close() 

def  countRows():
    conn = sql.connect("bnbvalues.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT COUNT(*) FROM bnbcontracts;
        """
        )
    data = cursor.fetchall()
    conn.commit()
    conn.close()     
    return data

def alldata():
    conn = sql.connect("bnbvalues.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT * FROM bnbcontracts;
        """
        )
    data = cursor.fetchall()
    conn.commit()
    conn.close() 
    print(data)
    return data

def deleteRowNameContract(field):
    try:
        conn = sql.connect("bnbvalues.db")
        cursor = conn.cursor()
        cursor.execute(
            f"""DELETE FROM bnbcontracts
            WHERE nameContract = '{field}';
            
            """
            )
        conn.commit()
        conn.close()
        print ('deleted')
        return 'OK'
    except ValueError as ve:        
        print ('error')
        return ve
