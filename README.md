# Financial Reporting Demo

Sistema de reporteo financiero con Django, flujo de trabajo de 8 etapas y control de acceso por roles.
*Django-based financial reporting system with an 8-stage workflow and role-based access control.*

> **Nota:** es una versión pública y simplificada de una arquitectura que uso en producción en mi trabajo. **Todos los datos son sintéticos** y no incluye información de ninguna empresa ni cliente real.

## Qué problema resuelve

Los reportes financieros para clientes institucionales suelen generarse de forma manual en hojas de cálculo: es lento, difícil de auditar y propenso a errores. Este proyecto muestra cómo pasar de ese proceso a una aplicación web estructurada, donde cada reporte avanza por etapas definidas y cada persona ve solo lo que le corresponde.

## Qué incluye

- **Flujo de trabajo de 8 etapas** para el ciclo de vida de un reporte.
- **Control de acceso por roles:** cada rol tiene permisos distintos sobre cada etapa.
- **Generación automática de reportes** con Django y HTML.
- **Datos sintéticos** para poder demostrar el sistema públicamente.
- **Despliegue automatizado en Render.**

## Tecnologías

Python · Django · HTML · CSS · SQLite · Git · Render

## Cómo correrlo localmente

El código está en la carpeta `financial_demo/`.

```bash
git clone https://github.com/Say1309/financial-reporting-demo.git
cd financial-reporting-demo/financial_demo
python -m venv venv
source venv/bin/activate        # en Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Después abre http://127.0.0.1:8000 en tu navegador.


## Lo que aprendí

- Diseñar un flujo de trabajo con estados y permisos, no solo pantallas.
- Separar la lógica de negocio de la presentación en Django.
- Preparar una versión pública de un sistema real sin exponer información confidencial.

## Autora

**Sayuri Mota** · [LinkedIn](https://www.linkedin.com/in/ingrid-sayuri-mota-de-la-rosa) · [GitHub](https://github.com/Say1309)
