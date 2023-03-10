import emoji
from crypt import methods
from flask import Flask, request, jsonify
import requests,json
from twilio.twiml.messaging_response import MessagingResponse
import os
import sqlite3
import datetime


## Init Flask APp
app = Flask(__name__)

def create_table():
    conn = sqlite3.connect('instance/twilio_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS twilio_data (id INTEGER PRIMARY KEY, message_sid TEXT, 
              account_sid TEXT, from_number TEXT, to_number TEXT, media_msg TEXT,
              message_body TEXT, media_msg_type TEXT, message_status TEXT, smsstatus TEXT, 
              message_media_url TEXT, timestamp TEXT)''')
    conn.commit() 
    conn.close() 

def save_data(message_sid, account_sid, from_number, to_number, media_msg, message_body, media_msg_type, message_status, smsstatus, message_media_url, timestamp):
    conn = sqlite3.connect('instance/twilio_data.db')
    c = conn.cursor() 
    
    try:
        c.execute("INSERT INTO twilio_data (message_sid, account_sid, from_number, to_number, media_msg, message_body, media_msg_type, message_status, smsstatus, message_media_url, timestamp) VALUES (?,?,?,?,?,?,?,?,?,?,?)", 
            (message_sid, account_sid, from_number, to_number, media_msg, message_body, media_msg_type, message_status, smsstatus, message_media_url, timestamp))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()        


@app.route('/bot', methods=['POST'])
def bot():
  ## GEt user message
    ## Init bot response
    bot_resp= MessagingResponse()
    msg = bot_resp.message()
    
    # Get the values from the request form object
    message_sid = request.form.get('MessageSid')
    account_sid = request.form.get('AccountSid')
    from_number = request.form.get('From')
    to_number = request.form.get('To')
    message_body = request.values.get('Body', '').lower()
    media_msg = request.form.get('NumMedia')  
    media_msg_type = request.form.get('MediaContentType0')
    message_status = request.form.get('MessageStatus')
    smsstatus = request.values.get('SmsStatus')
    message_media_url = request.form.get('MediaUrl0')
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    name = request.form.get("ProfileName")   

    
    if(int(media_msg) == 1 and media_msg_type == 'video/mp4'):
        #message_media_url = request.form.get('MediaUrl0')
        analysis_server_url = "https://rolplay.net/rp-whatsapp/es/conf/answer/whatsapp/process.php"
        response = requests.post(analysis_server_url, data={'video_type': media_msg_type,'video_url': message_media_url})
        
        if response.status_code == 200:
            # Acci??n para c??digo 200
            # Se extrae el status_message de la respuesta
            #
            #status_message = response.json().get('status_message')
            # Se env??a un mensaje al "body" de Twilio con el status_message
            #msg.body(status_message)
            print("\n\n\n")
            print(message_media_url)
            print("\n\n\n")
            print(response.json())
            msg.body("Se ha recibido tu v??deo con ??xito.")
            #return 'Petici??n realizada con ??xito'
        elif response.status_code == 201:
            print("Se ha almacenado tu archivo multimedia, en espera de ser analizado.")
        elif response.status_code == 204:
            print("Hay un problema como tu archivo, te pedimos que vuelvas a enviarlo.")
        elif response.status_code == 400:
            # Acci??n para c??digo 400
            msg.body("Lo siento, tu archivo multimedia no se ha podido procesar o no es el solicitado.")
            #return 'Petici??n incorrecta'
        
        elif response.status_code == 404:
            # Acci??n para c??digo 404
            msg.body("Ha ocurrido un error, comunicate con el servicio t??cnico de RolPlay.")
            #return 'Recurso no encontrado'
        elif response.status_code == 429:
            # Acci??n para c??digo 400
            msg.body("El sistema se ha saturado, pedimos espere unos momentos.")
        else:
            # Acci??n para cualquier otro c??digo
             # Si la petici??n no fue exitosa, se env??a un mensaje de error al "body" de Twilio
            msg.body("Ha ocurrido un error ajeno al servidor externo, comunicate con el servicio t??cnico de RolPlay.")
        return str(bot_resp)
    
    else:
        #print("S??lo aceptamos archivos MP4")
        msg.body("S??lo aceptamos archivos en formato de v??deo.\n")
        
    #print(request.form)
    a=str(request.form)
    f = open('twilio.txt','a')
    f.write('\n' + a)
    f.close()

    
    # Save the values to the database
    
    save_data(message_sid, account_sid, from_number, to_number, media_msg, message_body, media_msg_type, message_status, smsstatus, message_media_url, timestamp)
    '''
    if save_data(message_sid, account_sid, from_number, to_number, media_msg, message_body, media_msg_type, message_status, smsstatus, message_media_url, timestamp):
        return jsonify({'status_code':201,'message': 'Data saved successfully'})
    elif():
        return jsonify({'status_code':400,'message': 'Data user failed'})
    elif():
        return jsonify({'status_code':404,'message': 'Data user failed'})
    else:
        return jsonify({'status_code':500,'message': 'Data saving failed'})
    '''
    
    if 'hola' in message_body:
        msg.body("??Hola "+name+"!\n Y bienvenido a este bot "+"\U0001F916"+" de ayuda para WhatsApp.\n ??Como puedo ayudarte?\nToma en cuenta estas opciones\n1.- Para saber que es Machine Learning\n2.-Procesamiento de imagenes\n3.- Contar un chiste\n4.- Archivos clasificados de la NASA\n5.-??Quieres construir la IA que domine el mundo? Env??a <<si>> para confirmar\n")
    elif 'perrito' in message_body:
        # return a dog pic
        msg.media('https://images.dog.ceo/breeds/frise-bichon/7.jpg')
    elif 'hello' in message_body or 'hi' in message_body:
        msg.body("Hello "+name+"!\nAnd welcome to our help bot for AudioWeb Rolplay.\nHow may I help you?\nYour number is "+from_number)            
    elif 'machine learning' in message_body:
        msg.body("Machine learning is the study of computer algorithms that can improve automatically through experience and by the use of data. It is seen as a part of artificial intelligence.")
        msg.body('You can learn Machine Learning from here https://en.wikipedia.org/wiki/Machine_learning')
    elif 'processing images' in message_body:
        msg.body("Image processing can be defined as the technical analysis of an image by using complex algorithms.")
    elif 'nlp' in message_body:
        msg.body("Natural language processing is a subfield of linguistics, computer science, and artificial intelligence concerned with the interactions between computers and human language")
    elif 'who' in message_body:
        msg.body('I am programmed by Irving Pichardo')
    elif 'gatito' in message_body:
        msg.media('https://cataas.com/cat')
    elif 'cat color' in message_body:
        msg.body('https://cataas.com/cat/says/hello?size=50&color=red')
    elif 'irving' in message_body:
        msg.body('More info here:')
        msg.body('www.linkedin.com/in/irving-picard')
    elif 'pichardo photo' in message_body:
        msg.media('https://media.licdn.com/dms/image/C4E03AQFP3RtbGtd4yQ/profile-displayphoto-shrink_200_200/0/1649693160410?e=1680134400&v=beta&t=w67dPXRigDdkOWSlwEnSvOsqegdaKGTupPSt_rSRR08')
    elif 'rolplay' in message_body:
        msg.body('RolPlay: Plataforma digital de capacitaci??n, entrenamiento y aprendizaje, impulsada por IA ??Disponible en 25 idiomas!')
        msg.media('https://media-exp1.licdn.com/dms/image/C5622AQFgeC2qY1R3ig/feedshare-shrink_1280/0/1606839656550?e=1649894400&v=beta&t=eHgQ8dlwfL7Fi62sX0QDcLaHtXF38-vCcVDH4OmoQJw')
    elif 'plataforma' in message_body:
        msg.body('RolPlay: Plataforma digital de capacitaci??n, entrenamiento y aprendizaje, impulsada por IA ??Disponible en 25 idiomas!')
        msg.body('https://www.linkedin.com/company/rolplaymx/')
        msg.media('https://media.licdn.com/dms/image/C560BAQFFC_kLsTx4TA/company-logo_200_200/0/1671755345042?e=1682553600&v=beta&t=z3NbogOw03F3rtObGRR3AY3uS1f7pmETDd6Kr8IXReU')
    elif 'apod' in message_body:
        msg.body('API de la NASA')
        msg.media('http://mars.jpl.nasa.gov/msl-raw-images/proj/msl/redops/ods/surface/sol/01000/opgs/edr/fcam/FRB_486265257EDR_F0481570FHAZ00323M_.JPG')    
    elif 'waos' in message_body:
        msg.body('Si')
        msg.media('https://i.imgur.com/5cPMfb9.jpeg')
    elif 'random' in message_body:
        msg.body('Images')
        msg.media('https://picsum.photos/200/300')
    elif 'monterrey' in message_body:
        msg.body('As?? es')
        msg.media('https://i.imgur.com/EWqRHot.png')
    elif 'qui??n te cre???' in message_body:
        msg.body('Fu?? creado por el Ingeniero J. Irving Cristobal Pichardo')
    elif 'eres conciente?' in message_body:
        msg.body('No, s??lo tengo sentencias programadas de cadenas de caracteres')
    elif 'est??s vivo?' in message_body:
        msg.body('No estoy creado a base de carbono como los dem??s seres vivos, as?? que podr??a decirse que no')
    elif 'sabes mi nombre?' in message_body:
        msg.body('No, s??lo estoy tomando tu ID vinculado a tu WhatsApp')
    else:
        msg.body("\nLo siento "+name+". \n No entiendo lo que tratas de decir "+"\U0001F601")
    return str(bot_resp)


if __name__ == '__main__':
    create_table()
    app.run(debug=True,port=5000)
    
