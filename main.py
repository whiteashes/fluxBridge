from flask import Flask, request
from telegram.ext import Updater, updater, Filters, CommandHandler
import json
import re
import emoji

token=""
app = Flask(__name__)

# msg = {"checkId": "",
#             "checkName": "",
#             "level":"",
#             "message": "",
#             "queueTime":0,
#             "sourceMeasurement": "",
#             "timestamp": 0
#     }


msg = {"checkId": "",
            "checkName": "",
            "level":"",
            "message": "",
            
            "_field":0,
            "sourceMeasurement": "",
            "timestamp": 0
    }


msgTmp = {"sourceMeasurement": "",
          "timestamp":0}

@app.route('/')
def hello_world():
    return 'Hello world!'

def removeJobIfExists(name,context):
    currentJobs = context.job_queue.get_jobs_by_name(name)
    if not currentJobs:
        return False 
    
    for job in currentJobs:
        job.schedule_removal()
    
    return True


def pushToBot(context):
    job = context.job
    
    if(msg["sourceMeasurement"]!=msgTmp["sourceMeasurement"] or msg["timestamp"]!=msgTmp["timestamp"]):
        
        if(msg["level"]=="crit"):
            text = emoji.emojize(':red_circle: ')+"CRITICAL LEVEL | "+list(msg)[3]+": "+str(msg[list(msg)[3]])
            
            
        if(msg["level"]=="warn"):
            text = emoji.emojize(':warning: ')+"WARNING LEVEL | "+msg[list(msg)[3]]+": "+str(msg[list(msg)[3]])
        
        context.bot.send_message(context.job.context,text=text+"\n\n"+json.dumps(msg))
        msgTmp["sourceMeasurement"] = msg["sourceMeasurement"]
        msgTmp["timestamp"] = msg["timestamp"]
    
    return


def start(update,context):
    update.message.reply_text("Usage: /set <seconds> to set a timer")
    return


def callback_timer(update,context):
    chat_id = update.message.chat_id
    try:
        # args[0] should contain the time for the timer in seconds
        interval = int(context.args[0])
        if interval < 0:
            update.message.reply_text('Please type positive integers.')
            return
 
        job_removed = removeJobIfExists(str(chat_id), context)
        context.job_queue.run_repeating(pushToBot, interval, context=chat_id, name=str(chat_id))
 
        text = 'Timer successfully set! Now '+str(interval)+' seconds.'
        
        if job_removed:
            text += ' Old one was removed.'
        update.message.reply_text(text)
 
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /set <seconds>')
        

def callback_stop(update,context):
    chat_id = update.message.chat_id
    job_removed = removeJobIfExists(str(chat_id),context)
    
    text = 'Stopped. Job removed.' if job_removed else 'No active timer'
    update.message.reply_text(text)
   # context.job_queue.run_once(stopMessage,0,context=update.message.chat_id)
    return


@app.route('/notify',methods=['POST'])
def notify():

    if request.method == 'POST':
        print("notification received",flush=True)
        
        msg["checkId"] = request.json["_check_id"]
        msg["checkName"] = request.json["_check_name"]
        msg["level"] = request.json["_level"]
        msg["message"] = request.json["_message"]
         
        msg["queueTime"] = request.json["queuetime"]
        msg["sourceMeasurement"] = request.json["_source_measurement"]
        msg["timestamp"] = request.json["_status_timestamp"]
        
    return {'result':"OK 201"}


updater = Updater(token)

updater.dispatcher.add_handler(CommandHandler("start",start))
updater.dispatcher.add_handler(CommandHandler("set",callback_timer))
updater.dispatcher.add_handler(CommandHandler("stop",callback_stop))

updater.start_polling()

if __name__ == '__main__':
    app.run()
