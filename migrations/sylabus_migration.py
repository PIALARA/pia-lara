import bson
from pymongo import MongoClient
from werkzeug.security import generate_password_hash
import os
import configparser
from datetime import datetime

config = configparser.ConfigParser()
config.read(os.path.abspath(os.path.join(".ini")))

# DB_URI = config['PROD']['PIALARA_DB_URI']
# DB_NAME = config['PROD']['PIALARA_DB_NAME']
DB_URI = config['LOCAL']['PIALARA_DB_URI']
DB_NAME = config['LOCAL']['PIALARA_DB_NAME']

db = MongoClient(DB_URI)[DB_NAME]

sylabus = [
    {
        "_id": bson.objectid.ObjectId("637a078e8659dd172e6afaf5"),
        "texto": "Esto es una prueba",
        "creador": {
            "id": bson.objectid.ObjectId("6379fc6871880707a2c89537"),
            "nombre": "Rocio",
            "rol": "admin"
        },
        "tags": [
            "dislalia",
            "paralisis facial",
            "futbol",
            "madrid"
        ],
        "audios": [
            {
                "id": bson.objectid.ObjectId("637a08118659dd172e6afafa")
            },
            {
                "id": bson.objectid.ObjectId("637a08208659dd172e6afafb")
            },
            {
                "id": bson.objectid.ObjectId("637a08388659dd172e6afafc")
            }
        ],
        "fecha_creacion": datetime.today()
    },

    {
        "_id": bson.objectid.ObjectId("638348e9b3ba0b56509dfa1b"),
        "texto": "Esto es una prueba 2",
        "creador": {
            "id": bson.objectid.ObjectId("637fd98b2950843403bd5d8a"),
            "nombre": "Mario",
            "rol": "cliente"
        },
        "tags": [
            "dislalia",
            "paralisis facial",
            "futbol",
            "madrid"
        ],
        "audios": [
            {
                "id": bson.objectid.ObjectId("6379ff018659dd172e6afadc"),

            }
        ],
        "fecha_creacion": datetime.today()
    },
    {"texto":"El perro corrió detrás del gato en el jardín.", "tags":["perro", "jardín", "gato"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"La niña saltó alegremente en la cama de hojas.", "tags":["niña", "cama", "hojas"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"La oscuridad cubría el cielo nocturno.", "tags":["oscuridad", "cielo", "nocturno"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"El mar se agitaba con las olas crecientes.", "tags":["mar", "olas", "crecientes"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"La brisa fresca me despejó la mente.", "tags":["brisa", "mente", "despejada"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"La lluvia tamborileaba en el tejado del cobertizo.", "tags":["lluvia", "tejado", "cobertizo"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"La arena caliente quemaba mis pies descalzos.", "tags":["arena", "pies", "descalzos"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"La luna llena brillaba en el horizonte.", "tags":["luna", "horizonte", "llena"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"Los pájaros cantaban en los árboles.", "tags":["pájaros", "árboles", "cantando"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"La flor roja destacaba en el jardín.", "tags":["flor", "jardín", "roja"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"El viento aullaba en la tormenta.", "tags":["viento", "tormenta", "aullando"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"La llama del fuego parpadeaba en la chimenea.", "tags":["llama", "fuego", "chimenea"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"La taza de té humeaba en mis manos.", "tags":["taza", "té", "humo"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"Los rayos del sol se filtraban a través de las nubes.", "tags":["rayos", "sol", "nubes"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"La brisa marina traía el aroma del mar.", "tags":["brisa", "mar", "aroma"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"La ciudad estaba llena de gente.", "tags":["ciudad", "gente", "llena"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"Los pájaros cantaban en los árboles.", "tags":["pájaros", "árboles", "cantaban"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"El sol brillaba en el cielo azul.", "tags":["sol", "cielo", "brillaba"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"Los niños jugaban en el parque.", "tags":["niños", "parque", "jugaban"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"La brisa fresca soplaba suavemente.", "tags":["brisa", "suavemente", "soplaba"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"Las flores perfumaban el aire.", "tags":["flores", "aire", "perfumaban"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"La naturaleza se desplegaba a mi alrededor.", "tags":["naturaleza", "alrededor", "desplegaba"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"El agua cristalina del río reflejaba el paisaje.", "tags":["agua", "río", "cristalina"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"El aire estaba cargado de energía.", "tags":["aire", "energía", "cargado"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"La vida era plena y llena de posibilidades.", "tags":["vida", "posibilidades", "llena"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"La alegría y el gozo inundaban mi corazón.", "tags":["alegría", "gozo", "inundaban"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"La belleza del mundo me llenaba de asombro.", "tags":["belleza", "mundo", "llenaba"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"La bondad de las personas me inspiraba.", "tags":["bondad", "personas", "inspiraba"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"La gratitud llenaba mi ser.", "tags":["gratitud", "ser", "llenaba"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"La paz y la tranquilidad me envolvían.", "tags":["paz", "tranquilidad", "envolvían"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"La armonía y la armonía me rodeaban.", "tags":["armonía", "armonía", "rodearan"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"La felicidad y el amor me llenaban.", "tags":["felicidad", "amor", "llenaban"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"La esperanza y la fe me sostenían.", "tags":["esperanza", "fe", "sostenían"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"La vida era un regalo maravilloso.", "tags":["vida", "regalo", "maravilloso"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"Estaba agradecido por cada momento.", "tags":["agradecido", "momento", "cada"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"La pelota golpeó el poste y salió fuera.", "tags":["futbol", "pelota", "poste", "salir"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"Los jugadores corrían tras el balón.", "tags":["futbol", "jugadores", "correr", "balón"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"El delantero envió un pase preciso a su compañero.", "tags":["futbol", "delantero", "pase", "compañero"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"El arquero voló por el aire para atrapar el tiro.", "tags":["futbol", "arquero", "volar", "atrapar"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"La multitud coreaba el nombre de su equipo.", "tags":["futbol", "multitud", "corear", "equipo"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"Los entrenadores gritaban instrucciones desde la línea de banda.", "tags":["futbol", "entrenadores", "gritar", "línea de banda"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"El árbitro sopló el pito para marcar una falta.", "tags":["futbol", "árbitro", "soplar", "marcar falta"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"Los jugadores se reunieron en el centro del campo para un saque de banda.", "tags":["futbol", "jugadores", "reunirse", "saque de banda"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"La defensa logró despejar el balón del área peligrosa.", "tags":["futbol", "defensa", "despejar", "área peligrosa"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"El atacante remató fuerte y marcó un golazo.", "tags":["futbol", "atacante", "rematar", "golazo"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"La afición saltó de sus asientos y celebró el tanto.", "tags":["futbol", "afición", "saltar", "celebrar tanto"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"El equipo visitante intentaba igualar el marcador en los minutos finales.", "tags":["futbol", "equipo", "intentar", "igualar marcador"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"La tensión se cortaba con un cuchillo en el estadio.", "tags":["futbol", "tensión", "cortar", "estadio"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"El delantero se lanzó al suelo en busca de un penal.", "tags":["futbol", "delantero", "lanzar", "buscar penal"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"La pelota ingresó lentamente en la red tras un tiro de esquina.", "tags":["futbol", "pelota", "ingresar", "red"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"Los atletas se preparaban para la competencia.", "tags":["deporte", "atletas", "preparar", "competencia"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"La multitud llenaba el estadio con su entusiasmo.", "tags":["deporte", "multitud", "llenar", "estadio"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"El árbitro sopló el pito para iniciar el partido.", "tags":["deporte", "árbitro", "soplar", "iniciar partido"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"Los jugadores se esforzaban al máximo en la cancha.", "tags":["deporte", "jugadores", "esforzarse", "cancha"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"La atleta cruzó la meta en primer lugar.", "tags":["deporte", "atleta", "cruzar", "meta"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"El equipo celebró su victoria con un abrazo colectivo.", "tags":["deporte", "equipo", "celebrar", "victoria"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"La jugadora lanzó la pelota hacia la canasta con fuerza.", "tags":["deporte", "jugadora", "lanzar", "pelota"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"El entrenador motivaba a sus jugadores desde la línea de banda.", "tags":["deporte", "entrenador", "motivar", "línea de banda"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"Los aficionados coreaban el nombre de sus ídolos.", "tags":["deporte", "aficionados", "corear", "ídolos"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"La competencia era feroz en la piscina olímpica.", "tags":["deporte", "competencia", "feroz", "piscina"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"Los nadadores salieron disparados desde la plataforma.", "tags":["deporte", "nadadores", "disparar", "plataforma"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"La gimnasta realizó una rutina impecable en el suelo.", "tags":["deporte", "gimnasta", "realizar", "rutina"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"La atleta de lanzamiento de peso lanzó la pesa lejos.", "tags":["deporte", "atleta", "lanzamiento", "peso"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"Los corredores se pusieron en fila en la línea de salida.", "tags":["deporte", "corredores", "ponerse", "fila"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"La tensión se cortaba con un cuchillo en la pista de atletismo.", "tags":["deporte", "tensión", "cortar", "pista"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"El futbol es el deporte rey en el mundo.", "tags":["futbol", "deporte", "rey"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"La afición al futbol es apasionada en todos los rincones del planeta.", "tags":["futbol", "afición", "apasionada"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"Los jugadores de futbol son admirados y respetados en todos los países.", "tags":["futbol", "jugadores", "admirados"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"El futbol es un deporte que une a las personas de todas las edades y orígenes.", "tags":["futbol", "deporte", "unir"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"El equipo de futbol local lucha por la victoria en cada partido.", "tags":["futbol", "equipo", "lucha"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"La final de la Copa del Mundo de Futbol es uno de los eventos más seguidos en el mundo.", "tags":["futbol", "final", "Copa del Mundo"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"El futbol es un deporte que requiere habilidad, fuerza y resistencia.", "tags":["futbol", "deporte", "requerir"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"Los aficionados al futbol se visten con la camiseta de su equipo favorito.", "tags":["futbol", "aficionados", "vestir"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"La pelota de futbol es uno de los elementos más importantes en el juego.", "tags":["futbol", "pelota", "elemento"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"Las habilidades del futbol se pueden mejorar a través de entrenamiento y práctica.", "tags":["futbol", "habilidades", "mejorar"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"El futbol es un deporte que puede jugarse en diferentes tipos de superficies.", "tags":["futbol", "deporte", "jugarse"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"Los partidos de futbol atraen a miles de espectadores en los estadios.", "tags":["futbol", "partidos", "atraer"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"El futbol es un deporte que se juega en equipo y requiere trabajo en conjunto.", "tags":["futbol", "deporte", "trabajo en conjunto"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"La Federación Internacional de Futbol (FIFA) es la entidad encargada de regular el juego.", "tags":["futbol", "Federación Internacional", "encargada"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"El futbol es un deporte que ha evolucionado mucho a lo largo de la historia.", "tags":["futbol", "deporte", "evolucionar"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"El sol brillaba en el cielo.", "tags":["sol", "cielo", "brillar"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"La lluvia caía suavemente sobre el parque.", "tags":["lluvia", "parque", "caer"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"Los pájaros cantaban en los árboles.", "tags":["pájaros", "árboles", "cantar"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"La brisa fresca soplaba en mi rostro.", "tags":["brisa", "rostro", "soplar"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"La ciudad estaba llena de vida.", "tags":["ciudad", "vida", "llena"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"Las flores perfumaban el aire.", "tags":["flores", "aire", "perfumar"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"La vida era un regalo maravilloso.", "tags":["vida", "regalo", "maravilloso"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"El agua del río reflejaba el paisaje.", "tags":["agua", "río", "reflejar"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"La naturaleza se desplegaba a mi alrededor.", "tags":["naturaleza", "alrededor", "desplegar"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"La alegría y el gozo me inundaban.", "tags":["alegría", "gozo", "inundar"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"La belleza del mundo me dejaba sin aliento.", "tags":["belleza", "mundo", "dejar sin aliento"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"La bondad de las personas me inspiraba.", "tags":["bondad", "personas", "inspirar"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"La gratitud llenaba mi corazón.", "tags":["gratitud", "corazón", "llenar"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"La paz y la tranquilidad me envolvían.", "tags":["paz", "tranquilidad", "envolver"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"La armonía y la belleza me rodeaban.", "tags":["armonía", "belleza", "rodear"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"La felicidad y el amor me llenaban.", "tags":["felicidad", "amor", "llenar"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"La esperanza y la fe me sostenían.", "tags":["esperanza", "fe", "sostener"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"Estaba agradecido por cada momento.", "tags":["agradecido", "momento", "cada"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"La vida era una aventura emocionante.", "tags":["vida", "aventura", "emocionante"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()},
    {"texto":"Me sentía lleno de gratitud y alegría.", "tags":["gratitud", "alegría", "lleno"], "creador": {"id":{"$oid": "6379fc6871880707a2c89537"}, "nombre": "Rocio", "rol": "admin"}, "fecha_creacion": datetime.today()}

]

sylabusValidator = {
    "$jsonSchema": {
        "required": [
            'texto',
            'creador',
            'fecha_creacion'
        ],
        "properties": {
            "texto": {
                "bsonType": 'string'
            },
            "creador": {
                "bsonType": 'object'
            },
            "tags": {
                "bsonType": 'array'
            },
            "fecha_creacion": {
                "bsonType": 'date'
            }
        }
    }
}

try:
    db.drop_collection("sylabus")
    db.create_collection("sylabus", validator=sylabusValidator)
    db.sylabus.insert_many(sylabus)
except Exception as e:
    print(e)