# U4S8 — Bojórquez Rodríguez Alejandro

## Demo en vivo (producción)
https://u4s8-bojorquez-rodriguez-alejandro.onrender.com

## Qué hace este proyecto
Aplicación web para gestionar una vitrina de servicios profesionales. Las personas pueden crear una cuenta, iniciar sesión y administrar sus servicios mediante operaciones CRUD. El catálogo permite buscar por título, descripción o categoría y muestra los resultados en páginas de hasta 10 elementos.

## Stack técnico
Django + MySQL (Aiven) + Tailwind CSS + Render

## Cómo se prueba el aislamiento por usuario
Cada servicio tiene una llave foránea `propietario` asociada al usuario. El listado filtra con `Servicio.objects.filter(propietario=request.user)`, y las vistas de edición y eliminación buscan el servicio por su identificador y el propietario autenticado. Una cuenta distinta recibe un 404 al intentar editar o eliminar un servicio ajeno.

## Ejecución local
1. Instala las dependencias con `pip install -r requirements.txt`.
2. Crea un archivo `.env` local con las nueve variables descritas en `.env.example`, usando tus propios valores.
3. Aplica las migraciones con `python manage.py migrate`.
4. Inicia el servidor con `python manage.py runserver`.

No subas `.env` ni respaldos de la base de datos al repositorio. En producción, configura los dominios exactos en `ALLOWED_HOSTS` y `CSRF_TRUSTED_ORIGINS`, usa `DEBUG=False` y guarda secretos distintos de los locales.

## Pruebas
Ejecuta `python manage.py test` para validar búsqueda, paginación, inicio de sesión y aislamiento de servicios entre cuentas.

## Historial de unidades
- Unidad 1: portafolio estático con HTML5 + Tailwind
- Unidad 2: modelo Servicio migrado a MySQL, deploy dinámico en Render
- Unidad 3: CRUD completo con ModelForms + autenticación y sesiones
- Unidad 4: paginación, búsqueda, UI review y defensa final