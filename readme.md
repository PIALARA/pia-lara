# PIA LARA

## Instalación y Configuración del Entorno

El proyecto ahora utiliza [uv](https://docs.astral.sh/uv/) como gestor de paquetes. La configuración del proyecto, junto con sus dependencias, está declarada de forma estandarizada en el archivo `pyproject.toml`. Además, usamos un archivo `.python-version` para fijar la versión de Python del proyecto (por ejemplo, `3.12`).

### 1. Instalar uv

Si aún no tienes `uv` instalado en tu sistema, puedes hacerlo con los siguientes comandos:

- **Linux y macOS**:
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

- **Windows**:
  ```powershell
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```

### 2. Clonar el repositorio

```bash
git clone git@github.com:PIALARA/pia-lara.git
cd pia-lara
```

### 3. Gestión del entorno y dependencias

Existen dos formas de trabajar con el proyecto, dependiendo de tus necesidades:

#### A. Enfoque moderno (Recomendado)

Con `uv`, no necesitas crear ni activar el entorno virtual a mano. El siguiente comando creará automáticamente el entorno virtual (`.venv`), instalará o descargará la versión correcta de Python (basada en el archivo `.python-version`) e instalará todas las dependencias listadas en el `pyproject.toml`:

```bash
uv sync
```

Para gestionar dependencias en el futuro:
- **Añadir una dependencia:** `uv add <nombre_paquete>`
- **Eliminar una dependencia:** `uv remove <nombre_paquete>`

Para ejecutar Flask en este entorno:
```bash
uv run flask --app pialara --debug run
```

#### B. Enfoque tradicional

Si necesitas exportar las herramientas o usar el flujo más tradicional, puedes compilar el `pyproject.toml` en un `requirements.txt` usando `uv`:

```bash
uv pip compile pyproject.toml -o requirements.txt
```

Luego, puedes crear un entorno virtual e instalar las dependencias compuestas desde ese archivo:

```bash
uv venv
source .venv/bin/activate  # En Linux/Mac
# En Windows: .\.venv\Scripts\activate

uv pip install -r requirements.txt
```

Y ejecutar Flask en el entorno virtual activo:
```bash
flask --app pialara --debug run
```

## Herramientas de Desarrollo (Ruff)

El proyecto incluye **Ruff**, un linter y formateador de código extremadamente rápido. La configuración reside en el `pyproject.toml`. 

Comandos útiles para la calidad de código:

- **Comprobar errores** en el código (Linter):
  ```bash
  uv run ruff check .
  ```
- **Corregir errores automáticamente** (siempre que sea posible):
  ```bash
  uv run ruff check --fix .
  ```
- **Formatear el código**:
  ```bash
  uv run ruff format .
  ```

### Integración Continua (CI) con GitHub Actions

Se ha implementado un *workflow* de GitHub Actions (`.github/workflows/ruff.yml`) para asegurar la calidad del código. Cada vez que se realiza un *push* o se abre una *pull request* hacia las ramas `master` o `develop`, GitHub ejecutará automáticamente Ruff para comprobar:
1. Que no haya errores de linting (`ruff check`).
2. Que el código cumpla enteramente con el formato del proyecto (`ruff format --check`).

Si tu código no está correctamente formateado antes de subirlo, los checks de GitHub Actions fallarán. ¡Recuerda pasar siempre los comandos locales antes de hacer tus *commits*!

## Migraciones

Para ejecutar las migraciones, una vez activado el entorno virtual, desde el raíz, ejecutaremos el script adecuado:

``` python
python3 migrations/sylabus_migration.py
```

## Preparación de las variables de entorno

Hay que crear en el raíz del repositorio un archivo nombrado `.ini` y configurar las variables de entorno:

``` title=".ini"
[PROD]
SECRET_KEY = eac5e91171438960ddec0c9c469a4c3dd42e96aea462afc5ab830f78527ad80e
PIALARA_DB_URI = mongodb+srv://usuario:contraseña@host
PIALARA_DB_NAME = pialara
BUCKET_NAME = pialara
GRADIO_URL = http://localhost:8080/gradio

[LOCAL]
SECRET_KEY = eac5e91171438960ddec0c9c469a4c3dd42e96aea462afc5ab830f78527ad80e
PIALARA_DB_URI = localhost
PIALARA_DB_NAME = prelara
BUCKET_NAME = prelara
GRADIO_URL = http://localhost:8080/gradio

aws_access_key_id=clave_aws
aws_secret_access_key=secret_aws
aws_session_token=token_aws
```

Si da algún error con *Python* y la librería BSON, se recomienda actualizar (*upgrade*) la versión de PyMongo, la cual instala su propia versión de BSON que evita los errores.

## Estructura de la aplicación

El código principal de la aplicación está en el directorio `pialara`.

### Blueprints

En el directorio blueprints se van a agrupar las funcionalidades para tenerlo todo separado. Por ejemplo, auth tendrá su blueprint, syllabus (frases) tendrá su blueprint, etc.

Cuando se crea un blueprint, es necesario agregarlo en ```__init__.py``` para que la aplicación lo cargue.

### Vistas

Cada *Blueprint* va a tener asociado un directorio con su mismo nombre dentro del directorio templates que contendrá sus vistas.

Por ejemplo, el *Blueprint* `auth` va a tener el directorio `templates/auth` para guardar sus vistas.

### Modelos

Se van a usar modelos para acceder a la base de datos. Cada modelo representa a una colección y tiene que extender de la clase base que se ha creado  `MongoModel`. Un ejemplo de implementación para crear un modelo que va a acceder a las colecciones de Usuario sería:

```python
from pialara.models.MongoModel import MongoModel

class Usuario(MongoModel):
    collection_name = 'users'
```

Es necesario hacer override de la propiedad collection_name y asignarle una cadena con el nombre de la colección.

Una vez tenemos el modelo creado, lo podemos instanciar de la siguiente manera:

```python
u = Usuario()
```

Con esto, tendríamos todos los métodos que se han heredado de MongoModel a nuestra disposición sin tener que haberlos implementado. Por ejemplo, podríamos recuperar todos los usuarios con:

```python
db.users.find()
```

#### Métodos de MongoModel

Los métodos de MongoModel no son más que wrappers de los ofrecidos por la librería PyMongo. Es decir, el método `user.find(...parametros...)` sería lo mismo que hacer `db.users.find(...parametros...)`

- `find(self, params=None)`
- `update_one(self, mongo_filter, new_values, upsert=False)`
- `update_many(self, mongo_filter, new_values, upsert=False)`
- `insert_one(self, values)`
- `insert_many(self, values)`

#### Ejemplos de uso de los modelos

**Ejemplo para insertar un documento**

```python
u.insert_one({ "nombre": "Test", "email": "test@test.com" })
```

**Ejemplo para insertar multiples documentos**

```python
u.insert_many([{ "nombre": "Test", "email": "test2@test2.com" },{ "nombre": "Test", "email": "test3@test3.com" }])
```

**Ejemplo para actualizar un documento**
```python
u.update_one({"email":"test3@test3.com"}, { "$set": {"nombre": "Test33"}})
```

**Ejemplo para actualizar un documento y si no existe lo crea**
```python
u.update_one({"email":"test3@test3.com"}, { "$set": {"nombre": "Test33"}}, upsert=True)
```

**Ejemplo para actualizar multiples documentos**
```python
u.update_many({"nombre": "Test"}, { "$set": {"email":"asddasd@asdads.com"}})
```

**Ejemplo para actualizar multiples documentos y si no existen los crea**
```python
u.update_many({"nombre": "Test"}, { "$set": {"email":"asddasd@asdads.com"}}, upsert=True)
```

#### Proteger ruta por roles

Se ha creado un decorador en el fichero decorators.py para poder usarlo y asi comprobar que el usuario esta logueado y tiene un rol determinado

Su uso sería para comprobar que tiene el rol `admin` para la ruta `/profile` seria:

```python
from pialara.decorators import rol_required
@bp.route('/profile')
@rol_required("admin")
def profile():
    return render_template('auth/profile.html')
```
