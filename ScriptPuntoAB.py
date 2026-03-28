"""
Sistema Inteligente Basado en Reglas para Búsqueda de Rutas
en Sistema de Transporte Masivo

Autores: Santiago Tobar Useche, Cristian Leandro Pérez Peláez
Fecha: 14-03-2026
Curso: Inteligencia Artificial
"""

from experta import *
import networkx as nx
from collections import deque
from typing import List, Tuple, Dict


class EstacionTransporte(Fact):
    """Representa una estación en el sistema de transporte"""
    pass


class Conexion(Fact):
    """Representa una conexión entre dos estaciones"""
    pass


class Busqueda(Fact):
    """Representa el estado de la búsqueda"""
    pass


class Ruta(Fact):
    """Representa una ruta encontrada"""
    pass


class SistemaTransporteMasivo:
    """
    Clase que representa el sistema de transporte masivo
    con su red de estaciones y conexiones
    """
    
    def __init__(self):
        self.grafo = nx.Graph()
        self._inicializar_red_transporte()
    
    def _inicializar_red_transporte(self):
        """
        Inicializa la red de transporte masivo con estaciones y conexiones.
        Este ejemplo simula un sistema de metro/TransMilenio.
        """
        # Definir estaciones con sus características
        # (nombre, línea, tiempo_promedio_espera)
        estaciones = [
            # Línea A (Norte-Sur)
            ("Portal Norte", "A", 3),
            ("Calle 100", "A", 2),
            ("Calle 72", "A", 2),
            ("Calle 45", "A", 2),
            ("Centro", "A", 3),
            ("Calle 6", "A", 2),
            ("Portal Sur", "A", 3),
            
            # Línea B (Oriente-Occidente)
            ("Portal Occidente", "B", 3),
            ("Avenida 68", "B", 2),
            ("Centro", "B", 3),  # Estación de transferencia
            ("Avenida Caracas", "B", 2),
            ("Portal Oriente", "B", 3),
            
            # Línea C (Diagonal)
            ("Portal Suba", "C", 3),
            ("Calle 100", "C", 2),  # Estación de transferencia
            ("Calle 72", "C", 2),   # Estación de transferencia
            ("Avenida Caracas", "C", 2),  # Estación de transferencia
            ("Portal Usme", "C", 3),
        ]
        
        # Agregar estaciones al grafo
        for nombre, linea, tiempo_espera in estaciones:
            self.grafo.add_node(nombre, linea=linea, tiempo_espera=tiempo_espera)
        
        # Definir conexiones (aristas) con tiempos de viaje en minutos
        conexiones = [
            # Línea A
            ("Portal Norte", "Calle 100", 8, "A"),
            ("Calle 100", "Calle 72", 5, "A"),
            ("Calle 72", "Calle 45", 5, "A"),
            ("Calle 45", "Centro", 6, "A"),
            ("Centro", "Calle 6", 4, "A"),
            ("Calle 6", "Portal Sur", 10, "A"),
            
            # Línea B
            ("Portal Occidente", "Avenida 68", 7, "B"),
            ("Avenida 68", "Centro", 6, "B"),
            ("Centro", "Avenida Caracas", 5, "B"),
            ("Avenida Caracas", "Portal Oriente", 8, "B"),
            
            # Línea C
            ("Portal Suba", "Calle 100", 9, "C"),
            ("Calle 100", "Calle 72", 4, "C"),
            ("Calle 72", "Avenida Caracas", 7, "C"),
            ("Avenida Caracas", "Portal Usme", 11, "C"),
        ]
        
        # Agregar conexiones al grafo
        for origen, destino, tiempo, linea in conexiones:
            self.grafo.add_edge(origen, destino, tiempo=tiempo, linea=linea)
    
    def obtener_estaciones(self) -> List[str]:
        """Retorna lista de todas las estaciones"""
        return sorted(list(self.grafo.nodes()))
    
    def obtener_conexiones(self) -> List[Tuple]:
        """Retorna lista de todas las conexiones"""
        return list(self.grafo.edges(data=True))
    
    def calcular_tiempo_total(self, ruta: List[str]) -> int:
        """Calcula el tiempo total de viaje para una ruta dada"""
        if len(ruta) < 2:
            return 0
        
        tiempo_total = 0
        linea_actual = None
        
        for i in range(len(ruta) - 1):
            origen = ruta[i]
            destino = ruta[i + 1]
            
            # Tiempo de viaje entre estaciones
            datos_arista = self.grafo[origen][destino]
            tiempo_total += datos_arista['tiempo']
            
            # Agregar tiempo de espera si es inicio o si hay cambio de línea
            if i == 0:
                tiempo_total += self.grafo.nodes[origen]['tiempo_espera']
            else:
                linea_nueva = datos_arista['linea']
                if linea_actual != linea_nueva:
                    # Tiempo de transferencia (5 minutos adicionales)
                    tiempo_total += 5
                    tiempo_total += self.grafo.nodes[origen]['tiempo_espera']
                linea_actual = linea_nueva
        
        return tiempo_total
    
    def contar_transbordos(self, ruta: List[str]) -> int:
        """Cuenta el número de transbordos en una ruta"""
        if len(ruta) < 2:
            return 0
        
        transbordos = 0
        linea_actual = None
        
        for i in range(len(ruta) - 1):
            origen = ruta[i]
            destino = ruta[i + 1]
            linea = self.grafo[origen][destino]['linea']
            
            if linea_actual is not None and linea != linea_actual:
                transbordos += 1
            linea_actual = linea
        
        return transbordos


class SistemaBusquedaRutas(KnowledgeEngine):
    """
    Motor de inferencia basado en reglas para encontrar la mejor ruta
    en el sistema de transporte masivo
    """
    
    def __init__(self, sistema_transporte: SistemaTransporteMasivo):
        super().__init__()
        self.sistema = sistema_transporte
        self.rutas_encontradas = []
        self.origen = None
        self.destino = None
    
    def configurar_busqueda(self, origen: str, destino: str):
        """Configura el origen y destino para la búsqueda"""
        self.origen = origen
        self.destino = destino
        self.rutas_encontradas = []
        self.busqueda_iniciada = False
    
    @DefFacts()
    def cargar_conocimiento(self):
        """
        Regla inicial: Carga el conocimiento del sistema de transporte
        (estaciones y conexiones) como hechos en la base de conocimiento
        """
        # Agregar todas las estaciones como hechos
        for estacion in self.sistema.obtener_estaciones():
            yield EstacionTransporte(nombre=estacion)
        
        # Agregar todas las conexiones como hechos
        for origen, destino, datos in self.sistema.obtener_conexiones():
            yield Conexion(
                origen=origen,
                destino=destino,
                tiempo=datos['tiempo'],
                linea=datos['linea']
            )
        
        # Iniciar la búsqueda con los parámetros configurados
        yield Busqueda(estado="iniciar")
    
    @Rule(
        Busqueda(estado="iniciar"),
        salience=100
    )
    def regla_verificar_estaciones_validas(self):
        """
        Regla 1: Verificar que las estaciones de origen y destino existen
        """
        print(f"\n✓ Regla 1: Verificando estaciones válidas...")
        print(f"  - Origen: {self.origen}")
        print(f"  - Destino: {self.destino}")
        
        # Verificar que las estaciones existen
        estaciones = self.sistema.obtener_estaciones()
        if self.origen in estaciones and self.destino in estaciones:
            print(f"  ✓ Ambas estaciones son válidas")
            # Cambiar estado para continuar con la siguiente regla
            self.declare(Busqueda(estado="validado"))
        else:
            print(f"  ✗ Una o ambas estaciones no existen")
            self.declare(Busqueda(estado="error"))
    
    @Rule(
        Busqueda(estado="validado"),
        salience=50
    )
    def regla_buscar_rutas(self):
        """
        Regla 3: Buscar todas las rutas posibles usando búsqueda en anchura
        para garantizar que se encuentren las rutas más cortas
        """
        # Si origen y destino son iguales, manejar caso especial
        if self.origen == self.destino:
            print(f"\n✓ Regla 2: Origen y destino son iguales")
            self.rutas_encontradas.append({
                'ruta': [self.origen],
                'tiempo': 0,
                'transbordos': 0,
                'descripcion': 'Ya se encuentra en el destino'
            })
            self.declare(Busqueda(estado="completado"))
            return
        
        print(f"\n✓ Regla 3: Buscando todas las rutas posibles...")
        
        try:
            # Usar NetworkX para encontrar todas las rutas simples
            rutas = list(nx.all_simple_paths(
                self.sistema.grafo,
                self.origen,
                self.destino,
                cutoff=6  # Máximo 6 estaciones intermedias
            ))
            
            print(f"  - Se encontraron {len(rutas)} rutas posibles")
            
            # Analizar cada ruta
            for ruta in rutas:
                tiempo = self.sistema.calcular_tiempo_total(ruta)
                transbordos = self.sistema.contar_transbordos(ruta)
                
                self.rutas_encontradas.append({
                    'ruta': ruta,
                    'tiempo': tiempo,
                    'transbordos': transbordos,
                    'descripcion': self._generar_descripcion_ruta(ruta)
                })
            
            if not rutas:
                print("  ⚠ No se encontró ninguna ruta entre las estaciones")
        
        except nx.NetworkXNoPath:
            print("  ⚠ No existe conexión entre las estaciones")
        
        # Declarar que se completó la búsqueda
        self.declare(Busqueda(estado="rutas_encontradas"))
    
    @Rule(
        Busqueda(estado="rutas_encontradas"),
        salience=10
    )
    def regla_seleccionar_mejor_ruta(self):
        """
        Regla 4: Aplicar heurísticas para seleccionar la mejor ruta
        Criterios (en orden de prioridad):
        1. Menor número de transbordos
        2. Menor tiempo total de viaje
        """
        print(f"\n✓ Regla 4: Aplicando heurísticas para seleccionar mejor ruta...")
        
        if not self.rutas_encontradas:
            print("  ⚠ No hay rutas disponibles para evaluar")
            self.declare(Busqueda(estado="completado"))
            return
        
        # Ordenar por transbordos (ascendente) y luego por tiempo (ascendente)
        self.rutas_encontradas.sort(key=lambda x: (x['transbordos'], x['tiempo']))
        
        print(f"  - Criterio 1: Minimizar transbordos")
        print(f"  - Criterio 2: Minimizar tiempo de viaje")
        
        # Marcar búsqueda como completada
        self.declare(Busqueda(estado="completado"))
    
    def _generar_descripcion_ruta(self, ruta: List[str]) -> str:
        """Genera una descripción textual de la ruta"""
        if len(ruta) <= 1:
            return "Sin viaje necesario"
        
        descripcion = []
        linea_actual = None
        
        for i in range(len(ruta) - 1):
            origen = ruta[i]
            destino = ruta[i + 1]
            datos = self.sistema.grafo[origen][destino]
            linea = datos['linea']
            
            if linea_actual is None:
                descripcion.append(f"Tomar línea {linea} desde {origen}")
            elif linea != linea_actual:
                descripcion.append(f"Transbordar a línea {linea} en {origen}")
            
            descripcion.append(f"  → {destino} ({datos['tiempo']} min)")
            linea_actual = linea
        
        return "\n".join(descripcion)
    
    def obtener_mejor_ruta(self) -> Dict:
        """Retorna la mejor ruta encontrada"""
        if self.rutas_encontradas:
            return self.rutas_encontradas[0]
        return None
    
    def obtener_todas_rutas(self) -> List[Dict]:
        """Retorna todas las rutas encontradas"""
        return self.rutas_encontradas


def imprimir_encabezado():
    """Imprime el encabezado del programa"""
    print("=" * 70)
    print("    SISTEMA INTELIGENTE DE BÚSQUEDA DE RUTAS")
    print("    Sistema de Transporte Masivo")
    print("=" * 70)
    print("    Basado en Reglas Lógicas y Motor de Inferencia")
    print("=" * 70)
    print()


def imprimir_mapa_red(sistema: SistemaTransporteMasivo):
    """Imprime un mapa visual de la red de transporte"""
    print("\n" + "=" * 70)
    print("MAPA DE LA RED DE TRANSPORTE")
    print("=" * 70)
    
    lineas = {}
    for nodo, datos in sistema.grafo.nodes(data=True):
        linea = datos['linea']
        if linea not in lineas:
            lineas[linea] = []
        lineas[linea].append(nodo)
    
    for linea in sorted(lineas.keys()):
        print(f"\nLínea {linea}:")
        for estacion in lineas[linea]:
            print(f"  • {estacion}")


def mostrar_resultados(motor: SistemaBusquedaRutas):
    """Muestra los resultados de la búsqueda"""
    print("\n" + "=" * 70)
    print("RESULTADOS DE LA BÚSQUEDA")
    print("=" * 70)
    
    mejor_ruta = motor.obtener_mejor_ruta()
    todas_rutas = motor.obtener_todas_rutas()
    
    if not mejor_ruta:
        print("\n⚠ No se encontró ninguna ruta entre las estaciones indicadas.")
        return
    
    # Mostrar la mejor ruta
    print("\n ====> MEJOR RUTA RECOMENDADA:")
    print("-" * 70)
    print(f"Estaciones: {' → '.join(mejor_ruta['ruta'])}")
    print(f"Tiempo total estimado: {mejor_ruta['tiempo']} minutos")
    print(f"Número de transbordos: {mejor_ruta['transbordos']}")
    print(f"\nDescripción detallada:")
    print(mejor_ruta['descripcion'])
    
    # Mostrar rutas alternativas si existen
    if len(todas_rutas) > 1:
        print("\n" + "=" * 70)
        print(f"RUTAS ALTERNATIVAS ({len(todas_rutas) - 1}):")
        print("=" * 70)
        
        for i, ruta in enumerate(todas_rutas[1:], 1):
            print(f"\nRuta alternativa #{i}:")
            print(f"  Estaciones: {' → '.join(ruta['ruta'])}")
            print(f"  Tiempo: {ruta['tiempo']} min | Transbordos: {ruta['transbordos']}")


def main():
    """Función principal del programa"""
    imprimir_encabezado()
    
    # Inicializar el sistema de transporte
    print("Inicializando sistema de transporte masivo...")
    sistema = SistemaTransporteMasivo()
    print(f"✓ Red cargada: {len(sistema.obtener_estaciones())} estaciones")
    print(f"✓ Conexiones: {len(sistema.obtener_conexiones())} rutas directas\n")
    
    # Mostrar mapa de la red
    imprimir_mapa_red(sistema)
    
    # Solicitar estaciones al usuario
    print("\n" + "=" * 70)
    estaciones = sistema.obtener_estaciones()
    print("\nEstaciones disponibles:")
    for i, estacion in enumerate(estaciones, 1):
        print(f"  {i}. {estacion}")
    
    print("\n" + "-" * 70)
    
    # Entrada de datos
    while True:
        try:
            origen = input("\nIngrese la estación de ORIGEN: ").strip()
            if origen not in estaciones:
                print(f"⚠ '{origen}' no es una estación válida. Intente de nuevo.")
                continue
            
            destino = input("Ingrese la estación de DESTINO: ").strip()
            if destino not in estaciones:
                print(f"⚠ '{destino}' no es una estación válida. Intente de nuevo.")
                continue
            
            break
        except KeyboardInterrupt:
            print("\n\nPrograma interrumpido por el usuario.")
            return
    
    # Crear motor de inferencia y ejecutar búsqueda
    print("\n" + "=" * 70)
    print("EJECUTANDO MOTOR DE INFERENCIA BASADO EN REGLAS")
    print("=" * 70)
    
    motor = SistemaBusquedaRutas(sistema_transporte=sistema)
    motor.configurar_busqueda(origen, destino)
    motor.reset()
    motor.run()
    
    # Mostrar resultados
    mostrar_resultados(motor)
    
    print("\n" + "=" * 70)
    print("Búsqueda completada exitosamente ✓")
    print("=" * 70)


if __name__ == "__main__":
    main()
