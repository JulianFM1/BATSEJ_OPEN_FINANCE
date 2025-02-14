# Automatización de Cálculo de Comisiones para BATSEJ_OPEN_FINANCE


Este proyecto implementa una automatización en Python para calcular las comisiones de empresas según el uso de una API. Los datos provienen de una base de datos SQLite que se encuentra en https://github.com/jupjaramilloca/Prueba_vacante_ecosistemas y se exportan a un archivo Excel para su análisis.

## Requisitos

Es necesario tener instalado:

- Python 3.7 o superior
- SQLite3
- Librerías de Python necesarias (pueden instalarse con `setup.py` o `requirements.txt`)

## Instalación de dependencias

### Opción 1:  `setup.py`
```bash
python setup.py
```

### Opción 2:  `requirements.txt`

```bash
pip install -r requirements.txt
```

## Ejecución del script

Para ejecutar el cálculo de comisiones:

```bash
python main.py
```

## Lógica del cálculo

1. **Carga de datos:** Se extraen los registros de la base de datos SQLite.
2. **Limpieza de datos:** Se filtran empresas para que solo esten las activas y se filtran las fechas dentro del rango solicitado (julio y agosto 2024).
3. **Cálculo de comisiones:** Se aplica la lógica de cobro basada en el contrato de cada empresa aplicando los descuentos necesarios y aplicando el iva del 19%.
4. **Exportación de resultados:** Los datos se guardan en un archivo Excel dentro de la carpeta `resultado/`.

