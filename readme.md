# PIA LARA

## Instalación

**Consideraciones**: Uso los comandos ```python3``` y ```pip3```por que es como lo tengo configurado en mi sistema. Cada uno tendrá que saber cuál utilizar (python vs. python3 / pip vs. pip3) según el entorno de cada uno.

Clonar el repositorio 

```
git clone git@github.com:yepes/pia-lara.git
```

Dentro del directorio del repositorio, crear el entorno virtual:

```
python3 -m venv venv
```

Y activar el entorno virtual (aquí ya cada uno según windows, linux o Mac tendrá que seguir el procedimiento que se explicó en clase)

**Nota**: El directorio venv está puesto en el gitignore para que no se suba al repositorio. Si lo llamáis de otra forma, agregadlo al gitignore

Instalamos los requerimientos
```
pip3 install -r requirements.txt
```

Ejecutamos

```
flask --app pialara --debug run
```

## Estructura de la aplicación

El código principal de la aplicación está en el directorio pialara.

### Blueprints

En el directorio blueprints se van a agrupar las funcionalidades para tenerlo todo separado. Por ejemplo, auth tendrá su blueprint, syllabus (frases) tendrá su blueprint, etc.

### Vistas

Cada blueprint va a tener asociado un directorio con su mismo nombre dentro del directorio templates que contendrá sus vistas

### Modelos

TDB

### Conexión a la base de datos
TBD descripción
TBD conectar con mongo
TBD ejemplo