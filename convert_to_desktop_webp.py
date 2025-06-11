import os
import shutil
from PIL import Image
from datetime import datetime
import argparse

def get_desktop_path():
    """Obtiene la ruta del escritorio del usuario"""
    # Para Windows
    desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
    if os.path.exists(desktop):
        return desktop
    # Alternativa para Windows en español
    desktop = os.path.join(os.path.expanduser('~'), 'Escritorio')
    if os.path.exists(desktop):
        return desktop
    # Si no encuentra ninguna, usar el home del usuario
    return os.path.expanduser('~')

def create_output_folder():
    """Crea una carpeta con timestamp en el escritorio"""
    desktop = get_desktop_path()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder_name = f"telko_imagenes_webp_{timestamp}"
    output_path = os.path.join(desktop, folder_name)
    os.makedirs(output_path, exist_ok=True)
    return output_path

def convert_to_webp(input_path, output_path, quality=80):
    """Convierte una imagen a formato WebP"""
    try:
        with Image.open(input_path) as img:
            # Convertir a RGB si es necesario
            if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                img = img.convert('RGB')
            
            # Guardar como WebP
            img.save(output_path, 'WEBP', quality=quality)
            
            # Calcular reducción de tamaño
            original_size = os.path.getsize(input_path)
            new_size = os.path.getsize(output_path)
            reduction = ((original_size - new_size) / original_size) * 100
            
            return {
                'success': True,
                'original_size': original_size,
                'new_size': new_size,
                'reduction': reduction
            }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def process_directory(source_dir, output_base_dir, quality=80):
    """Procesa todos los archivos de imagen en un directorio y sus subdirectorios"""
    # Extensiones de imagen soportadas
    image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')
    
    stats = {
        'total_images': 0,
        'converted': 0,
        'failed': 0,
        'total_original_size': 0,
        'total_new_size': 0
    }
    
    print(f"\nProcesando directorio: {source_dir}")
    print(f"Destino: {output_base_dir}\n")
    
    for root, dirs, files in os.walk(source_dir):
        # Calcular la ruta relativa desde el directorio fuente
        rel_path = os.path.relpath(root, source_dir)
        if rel_path == '.':
            rel_path = ''
        
        # Crear el directorio correspondiente en el destino
        dest_dir = os.path.join(output_base_dir, rel_path)
        
        # Procesar archivos de imagen
        image_files = [f for f in files if f.lower().endswith(image_extensions)]
        
        if image_files:
            os.makedirs(dest_dir, exist_ok=True)
            
        for file in image_files:
            stats['total_images'] += 1
            input_path = os.path.join(root, file)
            output_filename = os.path.splitext(file)[0] + '.webp'
            output_path = os.path.join(dest_dir, output_filename)
            
            print(f"Convirtiendo: {os.path.relpath(input_path, source_dir)}")
            
            result = convert_to_webp(input_path, output_path, quality)
            
            if result['success']:
                stats['converted'] += 1
                stats['total_original_size'] += result['original_size']
                stats['total_new_size'] += result['new_size']
                print(f"  ✓ Reducción: {result['reduction']:.1f}%")
            else:
                stats['failed'] += 1
                print(f"  ✗ Error: {result['error']}")
    
    return stats

def print_summary(stats, output_folder):
    """Imprime un resumen de la conversión"""
    print("\n" + "="*50)
    print("RESUMEN DE CONVERSIÓN")
    print("="*50)
    print(f"Total de imágenes encontradas: {stats['total_images']}")
    print(f"Imágenes convertidas exitosamente: {stats['converted']}")
    print(f"Imágenes con error: {stats['failed']}")
    
    if stats['converted'] > 0:
        total_reduction = ((stats['total_original_size'] - stats['total_new_size']) / 
                          stats['total_original_size'] * 100)
        print(f"\nTamaño total original: {stats['total_original_size']/(1024*1024):.2f} MB")
        print(f"Tamaño total convertido: {stats['total_new_size']/(1024*1024):.2f} MB")
        print(f"Reducción total: {total_reduction:.1f}%")
        print(f"Espacio ahorrado: {(stats['total_original_size'] - stats['total_new_size'])/(1024*1024):.2f} MB")
    
    print(f"\nArchivos convertidos guardados en:")
    print(f"{output_folder}")

def main():
    parser = argparse.ArgumentParser(description='Convertir imágenes a WebP y guardar en el escritorio')
    parser.add_argument('--quality', type=int, default=80, 
                       help='Calidad de las imágenes WebP (0-100, default: 80)')
    parser.add_argument('--source', default='.', 
                       help='Directorio fuente (default: directorio actual)')
    
    args = parser.parse_args()
    
    # Crear carpeta de salida en el escritorio
    output_folder = create_output_folder()
    
    # Procesar el directorio
    stats = process_directory(args.source, output_folder, args.quality)
    
    # Mostrar resumen
    print_summary(stats, output_folder)
    
    # Abrir la carpeta en el explorador de Windows
    if os.name == 'nt':  # Windows
        os.startfile(output_folder)

if __name__ == '__main__':
    main() 