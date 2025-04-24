import os
from convert_to_webp import process_directory
import time

def get_total_size(directory):
    """Calcula el tamaño total de todos los archivos en el directorio y subdirectorios"""
    total_size = 0
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size

def main():
    # Directorio raíz del repositorio
    root_directory = "."
    
    # Verificar si el directorio existe
    if not os.path.exists(root_directory):
        print(f"Error: El directorio {root_directory} no existe")
        return
    
    # Calcular tamaño inicial
    initial_size = get_total_size(root_directory)
    print(f"Tamaño inicial del repositorio: {initial_size / (1024*1024):.2f} MB")
    print("----------------------------------------")
    
    # Procesar todo el directorio con calidad 80
    # delete_original=True para eliminar los archivos originales después de la conversión
    process_directory(root_directory, quality=80, delete_original=True)
    
    # Calcular tamaño final
    final_size = get_total_size(root_directory)
    reduction = ((initial_size - final_size) / initial_size) * 100
    
    print("----------------------------------------")
    print(f"Resumen final:")
    print(f"Tamaño inicial: {initial_size / (1024*1024):.2f} MB")
    print(f"Tamaño final: {final_size / (1024*1024):.2f} MB")
    print(f"Reducción total: {reduction:.2f}%")
    print("Proceso completado!")

if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print(f"Tiempo total de ejecución: {end_time - start_time:.2f} segundos") 