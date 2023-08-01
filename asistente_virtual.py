import pyttsx3
import speech_recognition as sr
import pywhatkit
import yfinance as yf
from yahooquery import Ticker
import pyjokes
import webbrowser
import datetime
import wikipedia



#  Opciones de voz / idioma
id1 = 'com.apple.eloquence.es-MX.Eddy'
id2 = 'com.apple.eloquence.es-MX.Flo'
id3 = 'com.apple.eloquence.es-MX.Grandma'
id4 = 'com.apple.eloquence.es-MX.Grandpa'
id5 = 'com.apple.voice.compact.es-MX.Paulina'
id6 = 'com.apple.eloquence.es-MX.Reed'
id7 = 'com.apple.eloquence.es-MX.Rocko'
id8 = 'com.apple.eloquence.es-MX.Sandy'
id9 = 'com.apple.eloquence.es-MX.Shelley'



# escuchar microfono y devolver como texto
def transformar_audio_texto():

    # almacenar recognizer
    r = sr.Recognizer()

    # configurar microfono
    with sr.Microphone() as origen:

        # tiempo de espera
        r.pause_threshold = 0.8

        # informar que comenzo la grabación
        print('Ya puedes hablar')

        # guardar audio
        audio = r.listen(origen)

        try:
            # buscar en google
            pedido = r.recognize_google(audio, language="es-ar")

            # prueba de que pudo ingresar
            print("Dijiste: " + pedido)

            # devolver pedido
            return pedido
        
        # en caso que no comprenda el audio
        except sr.UnknownValueError: 

            # prueba de que no se entiende
            print('Ups, no entendi')

            # devolver error
            return 'Sigo esperando'
        
        except sr.RequestError:

            # prueba de que no se entiende
            print('Ups, no hay servicio')

            # devolver error
            return 'Sigo esperando'
        
        # error inesperado
        except:
            # prueba de que no se entiende
            print('Ups, algo ha salido mal')

            # devolver error
            return 'Sigo esperando'
        


# el asistente pueda ser escuchado
def hablar(mensaje):
 
    # encender motor
    engine = pyttsx3.init()
 
    engine.setProperty('voice', id5)
 
    # pronunciar mensaje
    engine.say(mensaje)

    '''engine.runAndWait()''' # esta es la forma correcta de iniciar 
    # el código pero por un problema interno no puedo usarlo en mi mac por
    # lo que use la siguiente línea de codigo para que funcione
    
    # iniciar ciclo de eventos sin bloquear el código
    engine.startLoop(False)
    
    # esperar hasta que se termine de hablar
    while engine.iterate():
        pass
    


# informar dia de la semana
def pedir_dia():

    # crear variable con datos de hoy
    dia = datetime.date.today()

    # crear una variable para el dia de la semana
    dia_semana = dia.weekday( )


    # diccionario
    calendario = {0: 'Lunes',
                  1: 'Martes',
                  2: 'Miércoles',
                  3: 'Jueves',
                  4: 'Viernes',
                  5: 'Sábado',
                  6: 'Domingo'}
    
    # decir el dia de la semana
    hablar(f'Hoy es {calendario[dia_semana]}')



# informar hora
def pedir_hora():

    # variable hora
    hora = datetime.datetime.now()
    hora = f'En este momento son las {hora.hour} horas con {hora.minute} minutos y {hora.second} segundos'

    # decir la hora
    hablar(hora) 


 
#saludo inicial
def saludo_inicial():

    # crear variable con datos de hora
    hora = datetime.datetime.now()
    if hora.hour < 6 or hora.hour > 20:
        momento = 'Buenas noches'
    elif 6 <= hora.hour < 13:
        momento = 'Buen día'
    else:
        momento = 'Buenas tardes'


    # saludo
    hablar(f'Hola Nicholas,{momento}, Soy Paulina, tu asistente personal. Por favor, dime en que te puedo ayudar')
    


# funcion central del asistente
def pedir_cosas():
    
    # saludo inicial
    saludo_inicial()
    
    # variable de corte
    comenzar = True
    
    # loop central
    while comenzar:

        # activar micro y guardar pedido
        pedido = transformar_audio_texto().lower()

        if 'abrir youtube' in pedido:
            hablar('Con gusto Nicholas, estoy habriendo YouTube')
            webbrowser.open('https://www.youtube.com')
            continue
        
        elif 'abrir navegador' in pedido:
            hablar('Con gusto Nicholas, estoy habriendo Google')
            webbrowser.open('https://www.google.com')
            continue

        elif 'qué día es hoy' in pedido:
            pedir_dia()
            continue

        elif 'qué hora es' in pedido:
            pedir_hora()
            continue

        elif 'busca en wikipedia' in pedido:
            hablar('Con gusto Nicholas')
            pedido = pedido.replace('busca en wikipedia a', '').strip()
            wikipedia.set_lang('es')
            try:
                resultado = wikipedia.summary(pedido, sentences=1)
                hablar(f'Wikipedia dice lo siguiente: {resultado}')
            except wikipedia.exceptions.PageError:
                hablar('No se encontró información en Wikipedia para ese término.')
            continue

        elif 'busca en google' in pedido:
            hablar('Con gusto Nicholas')
            pedido = pedido.replace('busca en google', '')
            pywhatkit.search(pedido)
            hablar('Esto es lo que he encontrado')
            continue

        elif 'reproduce' in pedido:
            hablar('Con gusto Nicholas')
            pywhatkit.playonyt(pedido)
            continue

        elif 'broma' in pedido:
            hablar(pyjokes.get_joke('es'))
            continue

        elif 'precio de las acciones' in pedido:
            accion = pedido.split('de')[-1].strip()
            cartera = {'apple': 'APPL',
                       'amazon': 'AMZN',
                       'goole': 'GOOGL'}
            try:
                '''accion_buscada = cartera[accion]
                accion_buscada = yf.Ticker(accion_buscada)
                precio_actual = accion_buscada.info['regularMarketPrice']
                hablar(f'La encontre, el precio de {accion} es {precio_actual}')'''
            
                accion_buscada = cartera[accion]
                aapl = Ticker(accion_buscada)
                print(aapl)
                precio_actual = aapl.financial_data[accion_buscada]['currentPrice']
                print(precio_actual)
 
                hablar(f'La encontre, el precio de la {accion} en {precio_actual}')
                continue

            except:
                hablar('Perdón, pero no la he encontrado')

        elif 'adiós' in pedido:
            hablar('Un gusto haberte ayudado Nicholas, adiós')
            break




pedir_cosas()
