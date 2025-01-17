## Shoten Fast

Shorten Fast es una aplicación backend, para acortar urls el cual está creado en Python, Django y Django Rest Framework.

Algunas de las características con las que cuenta el proyecto son:

- Autentificación por medio de tokens JWT.
- Confirmación de usuario por medio de correo electrónico haciendo uso de la api de Resend.
- Acorta urls y genera códigos qr.
- Al estar registrado puede asignar un título a cada url acortado y ver todos los que ha creado así como eliminarlos.
- Se creó un Dockerfile para que la aplicación pueda ser lanzada y ejecutada por medió de Docker.
- Se cuenta unit test para cada enpoint.

Para usar este proyecto de manera local se deberá clonar este repositorio por medio del siguiente comando.

```Bash
git clone git@github.com:ChronosArx/shorten_fast.git
```

Posteriormente se deberá de crear un entorno virtual mediante el siguiente comando.

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

Con el entorno virtual creado es momento de instalar las dependencias.

```Bash
pip install -r requirements.txt
```

El proyecto necesita de algunas variables de entorno que son todas las siguientes:

```env
DJANGO_EVN=?
SECRET_KEY=?
EXPIRE_TIME_TOKEN_MINUTES=?
EXPIRE_TIME_TOKEN_DAYS=?
DATABASE_ENGINE=?
DOMAIN_URL=?
RESEND_API_KEY=?
ALLOWED_HOSTS=?
CORS_ALLOWED_ORIGINS=?
```

Todas las variables de entorno son necesarias para que funcione el proyecto. Para ejecutarlo en modo desarrollo no es necesario colocar manualmente todas, ya que tienen un valor por defecto a excepción de RESEND_API_KEY que si se necesitara un valor de manera explícita.

A continuación una explicación de lo que es cada una de las variables de entorno:

- **DJANGO_ENV**: Tiene por defecto el valor de development y es para cambiar entre entorno de pruebas y hacer uso del archivo de configuración correspondiente.

- **SECRET_KEY**: Es la llave secreta que será usada para la firma de los tokens JWT, se recomienda usar un generador de claves aleatorias para que sean mucho más seguros los tokens.

- **EXPIRE_TIME_TOKEN_MINUTES**: Es el tiempo que dura el token de acceso a la api se debe colocar un número entero y debe ser un número pequeño para mayor seguridad en recomendación entre 5 y 15.

- **EXPIRE_TIME_TOKEN_DAYS**: Es el tiempo que dura el refresh token el cual es de larga duración, debe ser un número entero.

- **DOMAIN_URL**: Es el dominio propio y es el cual se usará para crear los urls acortados y el cómo se guardarán en la base de datos, por defecto se establece como http://localhost:8000.

- **DATABASE_URL**: Es la url de conexión para la base de datos y por defecto se establece una base de datos sqlite cuando se está en modo de desarrollo.

- **CORS_ALLOWED_ORIGINS**: Es una lista con los orígenes (direcciones url) permitidos para hacer consultas al backend.

- **ALLOWED_HOSTS**: Esta es una lista de los nombres de hosts o dominio por los cuales se es permitido hacer las consultas al backend y es solo necesaria para el modo de producción.

- **RESEND_API_KEY**: Es una api key que es proveída por resend para poder realizar el envío de correos electrónicos.

Cuando las variables de entorno se encuentren correctamente configuradas es momento de ejecutar el servidor con el siguiente comando.

> **NOTA**: Todas las variables de entorno tienen un valor por defecto a excepción de RESEND_API_KEY.

```Bash
py manage.py runserver
```

## Usando Docker

Este proyecto también se puede ejecutar usando Docker, para poder ejecutar el proyecto en docker primero se debe crear una imagen del proyecto, esta imagen se puede crear con el siguiente comando:

> ⚠️ **Advertencia**Asegúrese de encontrarse dentro de la carpeta del proyecto para ejecutar los siguientes comandos.

```Bash
docker build -t shorten:1 .
```

Para verificar que la imagen fue creada correctamente ejecute el siguiente comando y debería de aparecer la imagen:

```Bash
docker images
```

Con esto listo se puede ejecutar el contenedor con el siguiente comando:

```Bash
docker run -p8000:8443 --name shorten-fast --env-file .env shorten:1
```

Una vez ejecutado el proyecto ya sea por medio del contenedor de docker o por el entorno virtual creado podrá acceder a la documentación de la api por medio de la siguiente URL.

```
http://localhost:8000/docs
```

De igual manera se puede interactuar con el backend por medio de la documentación de swagger en [Linkzips Docs](https://linkzips.com/api/docs/) o por medio de una interfaz gráfica en [Linkzips](https://shorten-fast-production.up.railway.app).
