from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters
import sqlite3 as sql
import requests
import lxml.html as html

REGINPUT = 0
DELINPUT = 0
XPATH_EXT_VALUE_CONTRACT = '//div[@class="col-md-8"]/text()'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}


def start(update, context):
   update.message.reply_text('''WELCOME ☺☺☺ \n\n
   /bnb PARA MOSTRAR CONTRATOS 💰\n
   /reg PARA REGISTRAR CONTRATOS📜 \n
   /del PARA BORRAR CONTRATOS🗑️ \n''')   

def getting_value(contract):
    try:
        URL_CONTRACT = f'https://bscscan.com/address/{contract}'
        response =  requests.get(URL_CONTRACT,headers=headers)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            valueContract = parsed.xpath(XPATH_EXT_VALUE_CONTRACT)
            try:
                print (valueContract[2])
                finalvalue = valueContract[2]
                return finalvalue
            except:
                return ['','','error value']
        else:
            return ['','','error no code 200']
    except ValueError as ve:
        print (ve)
        return ['','','error try catch']


#FUNCION MOSTRAR CONTRATOS
def bnb1(update, context):
    numrows = countRows()[0]
    tuplevalue = int(numrows[0])    
    update.message.reply_text(f'hay {tuplevalue} contratos registrados')    
    update.message.reply_text('♠♥♣♦-♠♥♣♦-♠♥♣♦')    
    contractdata = alldata() 
    print('imprimiendo contratos')
    for i in contractdata:
        print (i)
        currentValue = getting_value(i[2])
        update.message.reply_text(f'{i[0]}. 📜{i[1]} --> {currentValue}')
    update.message.reply_text('♠♥♣♦-♠♥♣♦-♠♥♣♦')    
    return ConversationHandler.END

#FUNCIONES REG
def reg1(update, context):
    update.message.reply_text('INGRESE NOMBRE Y CONTRATO A REGISTRAS 📜')
    return REGINPUT    

def reg2(update, context):
    text = update.message.text 
    splittext = text.split()
    insertContract(splittext[0], splittext[1])
    update.message.reply_text('CONTRATO REGISTRADO 👌🏻')
    return ConversationHandler.END


#FUNCIONES DEL
def del1(update, context):
    update.message.reply_text('INGRESE EL NOMBRE DE CONTRATO A BORRAR 🗑️')
    return DELINPUT    

def del2(update, context):
    text = update.message.text 
    deleteRowNameContract(text)           
    update.message.reply_text('CONTRATO BORRADO 🗑️')
    return ConversationHandler.END

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

if __name__ == '__main__':
    
    updater = Updater(token='5063445798:AAHVaXcfoQkVsISoWe3Y_9IDlPuBZVK0Z3c', use_context=True)
    dp = updater.dispatcher
    #PATERN START
    dp.add_handler(CommandHandler('start',start))
    #PATERN BNB
    dp.add_handler(ConversationHandler(
        entry_points=[CommandHandler('bnb', bnb1)],
        states={},
        fallbacks=[]
    ))
    #PATENR REG
    dp.add_handler(ConversationHandler(
        entry_points=[CommandHandler('reg', reg1)],
        states={REGINPUT: [MessageHandler(Filters.text, reg2)]},
        fallbacks=[]
    ))
    #PATENR DEL
    dp.add_handler(ConversationHandler(
        entry_points=[CommandHandler('del', del1)],
        states={DELINPUT: [MessageHandler(Filters.text, del2)]},
        fallbacks=[]
    ))
    print('en ejecucion')
    updater.start_polling()
    updater.idle()
    