## Shoten Fast

Shorten Fast es un backend, para acortar urls el cual esta creado en Python, Django y Django Rest Framework.
Para usar este proyecto de manera local se debera clanar este repositorio por medio del siguiente comando.

```Bash
git clone git@github.com:ChronosArx/shorten_fast.git
```

Posteriormente de haber clando el repositorio se debera de crear un entorno virtual mediante el siguiente comando.

```Bash
pip -m venv venv
```

Una vez creado es necesario activar el entorno virtual.

- En Windows:

```Powershell
.\venv\Scripts\activate
```

- En linux y Mac:

```Bash
source ./venv/bin/activate
```

Con el entrono vitural creado es momento de instalar las dependencias.

```Bash
pip install -r requirements.txt
```

Antes de ejecutar el servidor este proyecto necesita de algunas variables de entorno para poder funcionar de manera correcta, las variables de entorno necesarias son las siguientes.

```env
DEBUG=?
SECRET_KEY=?
EXPIRE_TIME_TOKEN_MINUTES=?
EXPIRE_TIME_TOKEN_DAYS=?
DATABASE_ENGINE=?
DOMAIN_URL=?
```

DEBUG: Este por defecto es TRUE y coloca el servidor en modo de desarrollo.

SECRET_KEY: Es la llave secreta que sera usada para la firam de los tokens JWT, se recomienda usar un generador de claves aleatorias para que sean mucho más seguros los tokens.

EXPIRE_TIME_TOKEN_MINUTES: Es el tiempo que dura el token de acceso a la api se debe colocar un numero entero y debe ser un numero pequeño para mayor seguridad en recomendación entre 5 y 15.

EXPIRE_TIME_TOKEN_DAYS: Es el tiempo que dura el refresh token el cual es de larga duración, debe ser un número entero.

DOMAIN_URL: Es el dominio propio y es el cual se usara para crear los urls acortados y el como se guardaran en la base de datos, por defecto se establece como http://localhost:8000.

DATABASE_URL: Es la url de conexión para la base de datos y por defecto se establece una base de datos sqlite cuando se esta en mod de debug.

Cuando las variables de entorno se encuentren correctamente configuradas es momento de ejecutar el servidor con el siguiente comando.

```Bash
py manage.py runserver
```

## Usando Doker

Este proyecto tambien se puede ejecutar usando Docker, para poder ejecutar el proyecto en docker primero se debe crear una imagen del proyecto, esta imagen se puede crear con el siguiente comando:

> ⚠️ **Advertencia**: Asegureze de encontrase dentro de la carpeta del pryecto para ejecutar los siguientes comandos.

```Bash
docker build -t shorten:1 .
```

Para verificar que la imagen fue creada correcta mente ejecute el siguiente comando y deberia de aparecer la imagen:

```Bash
docker images
```

Con esto listo se puede ejecutar el contenedor con el siguiente comando:

```Bash
docker run -p8000:8443 --name shorten-fast --env-file .env shorten:1
```

Una vez ejecutado el proyecto ya sea por medio del contendor de docker o por el entorno virtual creado podra acceder a la documentación de la api por medio de la siguiente Url.
```
http://localhost:8000/docs
```
