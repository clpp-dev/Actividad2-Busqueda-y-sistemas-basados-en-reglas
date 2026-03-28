# Actividad 2 - Búsqueda y Sistemas Basados en Reglas

Sistema Inteligente de Búsqueda de Rutas en Transporte Masivo utilizando Reglas Lógicas y Motor de Inferencia.

## Información del Proyecto

### Integrantes del Grupo
- Santiago Tobar Useche
- Cristian Leandro Pérez Peláez
- **Fecha:** 14-03-2026

### Curso
- Inteligencia Artificial (JOAQUIN SANCHEZ 23022026_C1_202631)

---

## Descripción del Proyecto

Este proyecto implementa un **sistema inteligente basado en reglas lógicas** que encuentra la mejor ruta para moverse desde un punto A hasta un punto B en un sistema de transporte masivo local.

### Características Principales

✅ **Motor de Inferencia:** Utiliza `experta` para implementar un sistema experto basado en reglas  
✅ **Base de Conocimiento:** Red de transporte masivo con múltiples líneas y estaciones  
✅ **Búsqueda Inteligente:** Algoritmos de búsqueda para encontrar rutas óptimas  
✅ **Heurísticas:** Optimización por tiempo de viaje y número de transbordos  
✅ **Interfaz de Usuario:** Interacción por consola para seleccionar origen y destino  

---

## Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

- **Python 3.8 o superior** (compatible con Python 3.10+) ([Descargar Python](https://www.python.org/downloads/))
- **pip** (incluido con Python)
- **Git** (opcional, para clonar el repositorio)

> **Nota:** Si usas Python 3.10 o superior, necesitarás aplicar un parche de compatibilidad después de instalar las dependencias (ver Paso 4).

### Verificar Instalación de Python

Abre una terminal (PowerShell, CMD o Git Bash) y ejecuta:

```bash
python --version
```

Deberías ver algo como: `Python 3.x.x`

---

## Instalación y Configuración

Sigue estos pasos para configurar el proyecto en tu máquina local:

### Paso 1: Clonar o Descargar el Repositorio

**Opción A: Clonar con Git**
```bash
git clone https://github.com/clpp-dev/Actividad2-Busqueda-y-sistemas-basados-en-reglas.git
cd Actividad2-B-squeda-y-sistemas-basados-en-reglas
```

**Opción B: Descargar ZIP**
1. Descarga el archivo ZIP del repositorio
2. Extrae el contenido en una carpeta de tu elección
3. Abre una terminal en esa carpeta

### Paso 2: Crear un Entorno Virtual (venv)

Un entorno virtual aísla las dependencias del proyecto de tu instalación global de Python.

```bash
# En Windows
python -m venv venv

# En Linux/Mac
python3 -m venv venv
```

Este comando creará una carpeta llamada `venv` en tu directorio de proyecto.

### Paso 3: Activar el Entorno Virtual
```bash
# En Windows
venv\Scripts\activate

# En Linux/Mac
source venv/bin/activate
```

> **Nota:** Si encuentras un error de permisos en PowerShell, ejecuta:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

### Paso 4: Instalar Dependencias

Con el entorno virtual activado, instala las bibliotecas necesarias:

```bash
pip install -r requirements.txt
```

Este comando instalará automáticamente:
- `experta==1.9.4` - Motor de inferencia para sistema basado en reglas
- `networkx==3.1` - Biblioteca para operaciones con grafos
- `frozendict==1.2` - Dependencia de experta

#### 🔧 Parche para Python 3.10 o superior

Si estás usando **Python 3.10 o superior**, necesitas aplicar un parche de compatibilidad a `frozendict`. Ejecuta el siguiente comando:

**En Windows PowerShell:**
```powershell
(Get-Content "venv\Lib\site-packages\frozendict\__init__.py") -replace 'collections\.Mapping', 'collections.abc.Mapping' | Set-Content "venv\Lib\site-packages\frozendict\__init__.py"
```

**En Linux/Mac:**
```bash
sed -i 's/collections\.Mapping/collections.abc.Mapping/g' venv/lib/python*/site-packages/frozendict/__init__.py
```

> **¿Por qué es necesario?** En Python 3.10+, `collections.Mapping` se movió a `collections.abc.Mapping`. El paquete `frozendict==1.2` (requerido por `experta`) no es compatible con Python 3.10+ sin este parche.

### Paso 5: Verificar la Instalación

Verifica que las dependencias se instalaron correctamente:

```bash
pip list
```

Deberías ver listadas las bibliotecas `experta`, `networkx` y `frozendict`.

Para verificar que el parche funcionó correctamente (Python 3.10+), ejecuta:

```bash
python -c "from experta import *; print('✓ experta importado correctamente')"
```

Si ves el mensaje de confirmación, ¡todo está listo! Si aparece un error `AttributeError`, revisa que hayas aplicado correctamente el parche del Paso 4.

---

## Ejecución del Proyecto

### Ejecutar el Sistema

Con el entorno virtual activado, ejecuta el script principal:

```bash
python ScriptPuntoAB.py
```

### Flujo de Uso

1. **El sistema mostrará:**
   - Encabezado del programa
   - Mapa de la red de transporte con todas las líneas
   - Lista de estaciones disponibles

2. **Ingresa la información solicitada:**
   - Estación de ORIGEN
   - Estación de DESTINO

3. **El motor de inferencia ejecutará:**
   - Regla 1: Verificación de estaciones válidas
   - Regla 2: Verificación de origen/destino iguales
   - Regla 3: Búsqueda de todas las rutas posibles
   - Regla 4: Selección de la mejor ruta según heurísticas

4. **Resultados:**
   - **Mejor ruta recomendada:** Ruta óptima con tiempo estimado y transbordos
   - **Rutas alternativas:** Otras opciones disponibles (si existen)

### Ejemplo de Ejecución

```
======================================================================
    SISTEMA INTELIGENTE DE BÚSQUEDA DE RUTAS
    Sistema de Transporte Masivo
======================================================================

Ingrese la estación de ORIGEN: Portal Norte
Ingrese la estación de DESTINO: Portal Sur

======================================================================
EJECUTANDO MOTOR DE INFERENCIA BASADO EN REGLAS
======================================================================

✓ Regla 1: Verificando estaciones válidas...
  - Origen: Portal Norte
  - Destino: Portal Sur
  ✓ Ambas estaciones son válidas

✓ Regla 3: Buscando todas las rutas posibles...
  - Se encontraron 2 rutas posibles

✓ Regla 4: Aplicando heurísticas para seleccionar mejor ruta...
  - Criterio 1: Minimizar transbordos
  - Criterio 2: Minimizar tiempo de viaje

====> MEJOR RUTA RECOMENDADA:
----------------------------------------------------------------------
Estaciones: Portal Norte → Calle 100 → Calle 72 → Calle 45 → Centro → Calle 6 → Portal Sur
Tiempo total estimado: 54 minutos
Número de transbordos: 2
```

---

## Estructura del Proyecto

```
Actividad2-B-squeda-y-sistemas-basados-en-reglas/
│
├── ScriptPuntoAB.py      # Script principal ejecutable
├── requirements.txt       # Listado de dependencias
├── README.md             # Documentación del proyecto
└── venv/                 # Entorno virtual (creado después de instalación)
```

---

## 🧠 Arquitectura del Sistema

### Componentes Principales

1. **Base de Conocimiento** (`SistemaTransporteMasivo`)
   - Representa la red de transporte como un grafo
   - Almacena estaciones, conexiones y sus atributos
   - Calcula tiempos de viaje y transbordos

2. **Motor de Inferencia** (`SistemaBusquedaRutas`)
   - Hereda de `KnowledgeEngine` (experta)
   - Implementa reglas lógicas para búsqueda de rutas
   - Aplica heurísticas para optimización

3. **Reglas Implementadas:**
   - **Regla 1:** Verificar que las estaciones existan
   - **Regla 2:** Manejar caso de origen = destino
   - **Regla 3:** Buscar todas las rutas posibles (BFS)
   - **Regla 4:** Seleccionar la mejor ruta según criterios

### Heurísticas de Optimización

El sistema prioriza las rutas según:
1. **Menor número de transbordos** (prioridad alta)
2. **Menor tiempo total de viaje** (prioridad secundaria)

---

## Solución de Problemas

### Error: "AttributeError: module 'collections' has no attribute 'Mapping'" (Python 3.10+)
**Causa:** El paquete `frozendict==1.2` no es compatible con Python 3.10+ sin modificaciones.

**Solución:** Aplica el parche de compatibilidad descrito en el Paso 4:

**Windows PowerShell:**
```powershell
(Get-Content "venv\Lib\site-packages\frozendict\__init__.py") -replace 'collections\.Mapping', 'collections.abc.Mapping' | Set-Content "venv\Lib\site-packages\frozendict\__init__.py"
```

**Linux/Mac:**
```bash
sed -i 's/collections\.Mapping/collections.abc.Mapping/g' venv/lib/python*/site-packages/frozendict/__init__.py
```

> **Importante:** Este parche debe aplicarse cada vez que reinstales las dependencias.

### Error: "python no se reconoce como comando"
**Solución:** Asegúrate de que Python esté agregado al PATH del sistema o usa `py` en lugar de `python`.

### Error: "No se puede ejecutar scripts en este sistema" (PowerShell)
**Solución:** Ejecuta:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Error: "ModuleNotFoundError: No module named 'experta'"
**Solución:** 
1. Verifica que el entorno virtual esté activado (`(venv)` en el prompt)
2. Ejecuta `pip install -r requirements.txt` nuevamente

### El programa no muestra resultados
**Solución:** Asegúrate de escribir correctamente el nombre de las estaciones (case-sensitive).

---

## 🧪 Personalización

### Modificar la Red de Transporte

Puedes editar la red de transporte en el método `_inicializar_red_transporte()` en `ScriptPuntoAB.py`:

```python
# Agregar nuevas estaciones
estaciones = [
    ("Nueva Estación", "D", 2),  # (nombre, línea, tiempo_espera)
    ...
]

# Agregar nuevas conexiones
conexiones = [
    ("Estación1", "Estación2", 5, "D"),  # (origen, destino, tiempo, línea)
    ...
]
```

---

## Tecnologías Utilizadas

- **Python 3.8+** (compatible con Python 3.10+) - Lenguaje de programación
- **Experta 1.9.4** - Framework para sistemas expertos basados en reglas
- **NetworkX 3.1** - Biblioteca para análisis de grafos y redes
- **venv** - Herramienta de entornos virtuales de Python

---

## Autores

Desarrollado por estudiantes de Inteligencia Artificial de la Universidad Iberoamericana:
- Santiago Tobar Useche
- Cristian Leandro Pérez Peláez

---

## Licencia

Este proyecto es material académico desarrollado para el curso de Inteligencia Artificial.
