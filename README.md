# boa-transformation-vis
Visualizador de cambios en la relación de dominación para un par de costos debido a una transformación

### ⚠️ Código desorganizado ⚠️

## Instrucciones
Cambiar variables al inicio del archivo main.py para determinar parámetros de la visualización.
- **X, Y**: Coordenadas del punto base con el cual se comparan los otros puntos
- **RANGE_X, RANGE_Y**: Rango en ejes X e Y de la visualización. Ambos rangos comienzan en 0.
- **PRECISION**: Cuantos puntos se simulan por eje en cada intervalo [i, i+1).
- **DEPTH**: Profundidad de búsqueda binaria en modo _border_
- **t**: Nombre de la transformación a usar.
- **args**: Diccionario de argumentos para la función a usar.

Al ejecutar el código, por defecto se utilizará el modo **full**. Se puede especificar el modo de visualización de la siguiente manera:
```python main.py MODE```

Actualmente se tienen los siguientes modos:
- **full**: Visualización completa de todos los puntos en el rectángulo definido por los rangos, según la precisión.
- **border**: Solamente se visualiza el borde entre los puntos dominados y los no dominados.