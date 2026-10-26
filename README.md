# U4S8 — Bojórquez Rodríguez Alejandro

## Demo en vivo (producción)
https://u4s8-bojorquez-rodriguez-alejandro.onrender.com

## Qué hace este proyecto
Este proyecto consiste en una aplicación web interactiva desarrollada como vitrina de servicios profesionales. Permite a cada usuario registrado gestionar su propio catálogo de servicios de forma dinámica mediante operaciones CRUD (Crear, Leer, Actualizar y Eliminar). Además, cuenta con un sistema de autenticación de usuarios, interfaz estilizada responsiva, así como funciones de búsqueda y paginación para facilitar la navegación del catálogo.

## Stack técnico
Django + MySQL (Aiven) + Tailwind CSS + Render

## Cómo se prueba el aislamiento por usuario
El aislamiento por usuario se garantiza desde la capa de modelo y vistas en Django. Cada registro de servicio guarda una llave foránea (`ForeignKey`) asociada al usuario autenticado (`request.user`). Al realizar consultas en las vistas, se aplican filtros como `Servicio.objects.filter(usuario=request.user)`, asegurando que cada usuario únicamente pueda visualizar, editar o eliminar los datos asociados a su propia cuenta. Si un usuario intenta acceder directamente a un servicio que no le pertenece, el sistema bloquea el acceso o retorna un error 404/403.

## Historial de unidades
- Unidad 1: portafolio estático con HTML5 + Tailwind
- Unidad 2: modelo Servicio migrado a MySQL, deploy dinámico en Render
- Unidad 3: CRUD completo con ModelForms + autenticación y sesiones
- Unidad 4: paginación, búsqueda, UI review y defensa final