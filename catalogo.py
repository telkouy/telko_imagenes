import os

# Solicitar al usuario la marca
marca = input('Ingrese la marca (nombre de la carpeta): ').strip()

# Verificar si la carpeta existe
if not os.path.isdir(marca):
    print(f'La carpeta de la marca "{marca}" no existe.')
    exit(1)

# Estructura para guardar los modelos y sus imágenes
data = []

# Recorrer subcarpetas (modelos)
for modelo_folder in sorted(os.listdir(marca)):
    modelo_path = os.path.join(marca, modelo_folder)
    if os.path.isdir(modelo_path):
        # Extraer nombre del modelo y medidas del nombre de la carpeta
        modelo_nombre = modelo_folder
        imagenes = []
        for archivo in sorted(os.listdir(modelo_path)):
            if archivo.lower().endswith('.jpg') and 'img_02' in archivo.lower():
                imagenes.append(os.path.join(modelo_path, archivo))
        if imagenes:
            data.append({
                'modelo': modelo_nombre,
                'imagenes': imagenes
            })

# Mostrar resumen de lo encontrado
print(f'Se encontraron {len(data)} modelos en la marca {marca}.')
for item in data:
    print(f"Modelo: {item['modelo']} ({len(item['imagenes'])} imágenes)")

# Guardar la estructura para el siguiente paso (generación de HTML)
import pickle
with open('catalogo_temp.pkl', 'wb') as f:
    pickle.dump(data, f)
print('Datos guardados en catalogo_temp.pkl para el siguiente paso.') 