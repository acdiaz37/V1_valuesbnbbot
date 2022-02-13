from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters
from xpathvalues import getting_value
from dbbot import countRows, insertContract, alldata, deleteRowNameContract

REGINPUT = 0
DELINPUT = 0

def start(update, context):
   update.message.reply_text('''WELCOME ☺☺☺ \n\n
   /bnb PARA MOSTRAR CONTRATOS 💰\n
   /reg PARA REGISTRAR CONTRATOS📜 \n
   /del PARA BORRAR CONTRATOS🗑️ \n''')   

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
    updater.start_polling()
    updater.idle()