import os
from PIL import Image
import time
from collections import defaultdict

def get_file_size_mb(filepath):
    """Retorna el tamaño del archivo en MB"""
    return os.path.getsize(filepath) / (1024 * 1024)

def convert_to_webp(input_path, output_path, quality=80):
    """Convierte una imagen a WebP y retorna estadísticas"""
    try:
        with Image.open(input_path) as img:
            if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                img = img.convert('RGB')
            
            original_size = os.path.getsize(input_path)
            img.save(output_path, 'WEBP', quality=quality)
            new_size = os.path.getsize(output_path)
            
            return {
                'original_size': original_size,
                'new_size': new_size,
                'reduction': ((original_size - new_size) / original_size) * 100,
                'success': True
            }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def process_repository(root_dir='.', quality=80):
    """Procesa todo el repositorio y retorna estadísticas detalladas"""
    stats = {
        'total_images': 0,
        'total_original_size': 0,
        'total_new_size': 0,
        'converted_images': 0,
        'failed_images': 0,
        'by_extension': defaultdict(lambda: {'count': 0, 'original_size': 0, 'new_size': 0}),
        'errors': []
    }
    
    # Extensiones de imagen soportadas
    image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')
    
    print("\nIniciando análisis del repositorio...")
    print("----------------------------------------")
    
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith(image_extensions):
                input_path = os.path.join(root, file)
                output_path = os.path.splitext(input_path)[0] + '.webp'
                
                # Obtener extensión del archivo
                ext = os.path.splitext(file)[1].lower()
                
                # Actualizar estadísticas
                stats['total_images'] += 1
                original_size = os.path.getsize(input_path)
                stats['total_original_size'] += original_size
                stats['by_extension'][ext]['count'] += 1
                stats['by_extension'][ext]['original_size'] += original_size
                
                # Convertir imagen
                result = convert_to_webp(input_path, output_path, quality)
                
                if result['success']:
                    stats['converted_images'] += 1
                    stats['total_new_size'] += result['new_size']
                    stats['by_extension'][ext]['new_size'] += result['new_size']
                    
                    print(f"\nConvertido: {input_path}")
                    print(f"Reducción: {result['reduction']:.2f}%")
                    print(f"Original: {result['original_size']/1024:.2f} KB")
                    print(f"Nuevo: {result['new_size']/1024:.2f} KB")
                else:
                    stats['failed_images'] += 1
                    stats['errors'].append(f"{input_path}: {result['error']}")
                    print(f"\nError en {input_path}: {result['error']}")
    
    return stats

def print_summary(stats):
    """Imprime un resumen detallado de las estadísticas"""
    print("\n----------------------------------------")
    print("RESUMEN FINAL")
    print("----------------------------------------")
    print(f"Total de imágenes encontradas: {stats['total_images']}")
    print(f"Imágenes convertidas exitosamente: {stats['converted_images']}")
    print(f"Imágenes con error: {stats['failed_images']}")
    
    print("\nEstadísticas por extensión:")
    for ext, data in stats['by_extension'].items():
        if data['count'] > 0:
            reduction = ((data['original_size'] - data['new_size']) / data['original_size'] * 100) if data['new_size'] > 0 else 0
            print(f"\n{ext.upper()}:")
            print(f"  Cantidad: {data['count']}")
            print(f"  Tamaño original: {data['original_size']/(1024*1024):.2f} MB")
            print(f"  Tamaño final: {data['new_size']/(1024*1024):.2f} MB")
            print(f"  Reducción: {reduction:.2f}%")
    
    print("\nEstadísticas generales:")
    total_reduction = ((stats['total_original_size'] - stats['total_new_size']) / stats['total_original_size'] * 100)
    print(f"Tamaño total original: {stats['total_original_size']/(1024*1024):.2f} MB")
    print(f"Tamaño total final: {stats['total_new_size']/(1024*1024):.2f} MB")
    print(f"Reducción total: {total_reduction:.2f}%")
    
    if stats['errors']:
        print("\nErrores encontrados:")
        for error in stats['errors']:
            print(f"- {error}")

def main():
    start_time = time.time()
    
    # Procesar todo el repositorio con calidad 80
    stats = process_repository(quality=80)
    
    # Imprimir resumen
    print_summary(stats)
    
    execution_time = time.time() - start_time
    print(f"\nTiempo total de ejecución: {execution_time:.2f} segundos")

if __name__ == "__main__":
    main() 