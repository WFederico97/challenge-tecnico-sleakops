from cachetools import Cache

# Crear un caché con un tamaño máximo
cache = Cache(maxsize=100)

# Limpiar el caché
cache.clear()
print("Cache cleared.")