import os
from PIL import Image
import argparse

def convert_to_webp(input_path, output_path, quality=80, delete_original=False):
    """
    Convierte una imagen a formato WebP manteniendo la calidad.
    
    Args:
        input_path (str): Ruta del archivo de entrada
        output_path (str): Ruta donde guardar el archivo WebP
        quality (int): Calidad de la imagen (0-100)
        delete_original (bool): Si es True, elimina el archivo original después de la conversión
    """
    try:
        # Abrir la imagen
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
            
            print(f"Convertido: {input_path}")
            print(f"Reducción de tamaño: {reduction:.2f}%")
            
            if delete_original:
                os.remove(input_path)
                print(f"Archivo original eliminado: {input_path}")
                
    except Exception as e:
        print(f"Error procesando {input_path}: {str(e)}")

def process_directory(directory, quality=80, delete_original=False):
    """
    Procesa todos los archivos de imagen en un directorio y sus subdirectorios.
    
    Args:
        directory (str): Directorio a procesar
        quality (int): Calidad de la imagen (0-100)
        delete_original (bool): Si es True, elimina los archivos originales
    """
    # Extensiones de imagen soportadas
    image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(image_extensions):
                input_path = os.path.join(root, file)
                output_path = os.path.splitext(input_path)[0] + '.webp'
                
                # Solo convertir si el archivo WebP no existe o es más antiguo
                if not os.path.exists(output_path) or os.path.getmtime(input_path) > os.path.getmtime(output_path):
                    convert_to_webp(input_path, output_path, quality, delete_original)

def main():
    parser = argparse.ArgumentParser(description='Convertir imágenes a formato WebP')
    parser.add_argument('directory', help='Directorio a procesar')
    parser.add_argument('--quality', type=int, default=80, help='Calidad de la imagen (0-100)')
    parser.add_argument('--delete-original', action='store_true', help='Eliminar archivos originales después de la conversión')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.directory):
        print(f"Error: El directorio {args.directory} no existe")
        return
    
    process_directory(args.directory, args.quality, args.delete_original)

if __name__ == '__main__':
    main() 