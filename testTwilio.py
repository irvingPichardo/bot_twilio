'''python3 -m venv venv
. ./venv/bin/activate
ngrok http 5000
'''
import emoji
from crypt import methods
from flask import Flask, request, jsonify
import requests,json
from twilio.twiml.messaging_response import MessagingResponse
import os


## Init Flask APp
app = Flask(__name__)

# Testing Route
@app.route('/hello', methods=['GET'])
def ping():
    return jsonify({'response': 'Hello World, ¡Lo cambia todo! 😎'})


@app.route('/recibe_video', methods=['POST'])
def receive_video():
    user_msg = request.values.get('Body', '').lower()
    ## Init bot response
    bot_resp= MessagingResponse()
    msg = bot_resp.message()
    
    # Get the video file from the request
    video_file = request.files.get('video')

    # Save the video file to a directory on the server
    video_file.save(os.path.join('videos', video_file.filename))
    
    # Send the video file to another server
    url = "https://rolplay.net/rp-whatsapp/es/conf/answer/whatsapp/process.php"
    files = {'video': open(os.path.join('videos', video_file.filename), 'rb')}
    requests.post(url, files=files)

    return 'Video file saved and sent successfully'
 

@app.route('/bot', methods=['POST'])
def bot():
  ## GEt user message
    user_msg = request.values.get('Body', '').lower()
    ## Init bot response
    bot_resp= MessagingResponse()
    msg = bot_resp.message()
    
    number = request.form.get('From')
    name = request.form.get("ProfileName")
    media_msg = request.form.get('NumMedia')   
    #message_latitude = request.values.get('Latitude')
    #message_longitude = request.values.get('Longitude')
    status = request.values.get('SmsStatus')

    print(request.form)
    a=str(request.form)
    f = open('twilio.txt','a')
    f.write('\n' + a)
    f.close()

    #created = request.values.get('date_created')
    #print("Se creó:",created)

    print(name,media_msg)
    print(number, status)
    #print("Latitud:",message_latitude,"\nLongitud:",message_longitude)
    
    if 'hola' in user_msg:
        msg.body("¡Hola "+name+"!\n Y bienvenido a este bot "+"\U0001F916"+" de ayuda para WhatsApp.\n ¿Como puedo ayudarte?\nToma en cuenta estas opciones\n1.- Para saber que es Machine Learning\n2.-Procesamiento de imagenes\n3.- Contar un chiste\n4.- Archivos clasificados de la NASA\n5.-¿Quieres construir la IA que domine el mundo? Envía <<si>> para confirmar\n")
    elif 'perrito' in user_msg:
        # return a dog pic
        msg.media('https://images.dog.ceo/breeds/frise-bichon/7.jpg')
    elif 'hello' in user_msg or 'hi' in user_msg:
        msg.body("Hello "+name+"!\nAnd welcome to our help bot for AudioWeb Rolplay.\nHow may I help you?\nYour number is "+number)            
    elif 'machine learning' in user_msg:
        msg.body("Machine learning is the study of computer algorithms that can improve automatically through experience and by the use of data. It is seen as a part of artificial intelligence.")
        msg.body('You can learn Machine Learning from here https://en.wikipedia.org/wiki/Machine_learning')
    elif 'processing images' in user_msg:
        msg.body("Image processing can be defined as the technical analysis of an image by using complex algorithms.")
    elif 'nlp' in user_msg:
        msg.body("Natural language processing is a subfield of linguistics, computer science, and artificial intelligence concerned with the interactions between computers and human language")
    elif 'who' in user_msg:
        msg.body('I am programmed by Irving Pichardo')
    elif 'gatito' in user_msg:
        msg.media('https://cataas.com/cat')
    elif 'cat color' in user_msg:
        msg.body('https://cataas.com/cat/says/hello?size=50&color=red')
    elif 'irving' in user_msg:
        msg.body('More info here:')
        msg.body('www.linkedin.com/in/irving-picard')
    elif 'pichardo photo' in user_msg:
        msg.media('https://media.licdn.com/dms/image/C4E03AQFP3RtbGtd4yQ/profile-displayphoto-shrink_200_200/0/1649693160410?e=1680134400&v=beta&t=w67dPXRigDdkOWSlwEnSvOsqegdaKGTupPSt_rSRR08')
    elif 'rolplay' in user_msg:
        msg.body('RolPlay: Plataforma digital de capacitación, entrenamiento y aprendizaje, impulsada por IA ¡Disponible en 25 idiomas!')
        msg.media('https://media-exp1.licdn.com/dms/image/C5622AQFgeC2qY1R3ig/feedshare-shrink_1280/0/1606839656550?e=1649894400&v=beta&t=eHgQ8dlwfL7Fi62sX0QDcLaHtXF38-vCcVDH4OmoQJw')
    elif 'plataforma' in user_msg:
        msg.body('RolPlay: Plataforma digital de capacitación, entrenamiento y aprendizaje, impulsada por IA ¡Disponible en 25 idiomas!')
        msg.body('https://www.linkedin.com/company/rolplaymx/')
        msg.media('https://media.licdn.com/dms/image/C560BAQFFC_kLsTx4TA/company-logo_200_200/0/1671755345042?e=1682553600&v=beta&t=z3NbogOw03F3rtObGRR3AY3uS1f7pmETDd6Kr8IXReU')
    elif 'apod' in user_msg:
        msg.body('API de la NASA')
        msg.media('http://mars.jpl.nasa.gov/msl-raw-images/proj/msl/redops/ods/surface/sol/01000/opgs/edr/fcam/FRB_486265257EDR_F0481570FHAZ00323M_.JPG')    
    elif 'waos' in user_msg:
        msg.body('Si')
        msg.media('https://i.imgur.com/5cPMfb9.jpeg')
    elif 'random' in user_msg:
        msg.body('Images')
        msg.media('https://picsum.photos/200/300')
    elif 'monterrey' in user_msg:
        msg.body('Así es')
        msg.media('https://i.imgur.com/EWqRHot.png')
    elif 'quién te creó?' in user_msg:
        msg.body('Fuí creado por el Ingeniero J. Irving Cristobal Pichardo')
    elif 'eres conciente?' in user_msg:
        msg.body('No, sólo tengo sentencias programadas de cadenas de caracteres')
    elif 'estás vivo?' in user_msg:
        msg.body('No estoy creado a base de carbono como los demás seres vivos, así que podría decirse que no')
    elif 'sabes mi nombre?' in user_msg:
        msg.body('No, sólo estoy tomando tu ID vinculado a tu WhatsApp')
    else:
        msg.body("\nLo siento "+name+". \n No entiendo lo que tratas de decir "+"\U0001F601")
    return str(bot_resp)



if __name__ == '__main__':
    app.run(debug=True,port=5000)
    
