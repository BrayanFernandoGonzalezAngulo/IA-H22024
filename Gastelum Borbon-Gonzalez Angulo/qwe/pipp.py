import numpy as np  # Importar la librería NumPy para operaciones numéricas.
import pandas as pd  # Importar la librería Pandas para manejar datos en estructuras de DataFrame.
import re  # Importar la librería re para expresiones regulares.
import nltk  # Importar la librería NLTK para procesamiento de lenguaje natural.
import tkinter as tk  # Importar la librería tkinter para crear la interfaz gráfica de usuario.
import joblib as joblib # Esto es para guardar el modelo en un archivo
from tkinter import filedialog, messagebox  # Importar componentes de tkinter para diálogos de archivos y mensajes.
from sklearn.feature_extraction.text import TfidfVectorizer  # Importar el vectorizador TF-IDF de scikit-learn.
from sklearn.model_selection import train_test_split  # Importar función para dividir conjuntos de datos.
from sklearn.naive_bayes import MultinomialNB  # Importar el clasificador Naive Bayes multinomial.
from sklearn.metrics import accuracy_score, recall_score, classification_report  # Importar métricas de evaluación.

# Descargar stopwords de NLTK
nltk.download('stopwords')  # Descargar la lista de palabras vacías en inglés.
from nltk.corpus import stopwords  # Importar las stopwords.

# Crear la ventana principal
window = tk.Tk()  # Inicializar la ventana principal de la aplicación.
window.title("Clasificación de Correos Electrónicos: Spam vs No Spam")  # Establecer el título de la ventana.
window.geometry("700x700")  # Establecer las dimensiones de la ventana.
window.configure(bg="lightblue")  # Configurar el color de fondo de la ventana.

# Variables para almacenar datos y características
data = None  # Inicializar la variable para almacenar los datos cargados.
features = None  # Inicializar la variable para almacenar las características extraídas.

# Funciones para cada paso del proceso

# Función para cargar datos desde un archivo CSV
def cargar_datos():
    global data  # Hacer que la variable data sea global para poder usarla en otras funciones.
    file_path = filedialog.askopenfilename()  # Abrir un cuadro de diálogo para seleccionar un archivo.
    if file_path:  # Si se seleccionó un archivo...
        data = pd.read_csv(file_path)  # Cargar los datos desde el archivo CSV en un DataFrame.
        if 'target' not in data.columns or 'text' not in data.columns:
            messagebox.showerror("Error", "El archivo CSV debe contener las columnas 'text' y 'target'.")
            return
        registros_iniciales = len(data)  # Contar el número de registros iniciales.
        data = data.drop_duplicates()  # Eliminar registros duplicados.
        registros_unicos = len(data)  # Contar el número de registros únicos.
        eliminados = registros_iniciales - registros_unicos  # Calcular el número de registros eliminados.
        
        # Mostrar información sobre la carga de datos en el cuadro de texto.
        text_result.insert(tk.END, f"Registros iniciales: {registros_iniciales}\n")
        text_result.insert(tk.END, f"Registros sin duplicados: {registros_unicos}\n")
        text_result.insert(tk.END, f"Registros eliminados: {eliminados}\n")
        text_result.insert(tk.END, "="*80 + "\n")
        
        # Mostrar un mensaje de éxito al usuario.
        messagebox.showinfo("Carga Exitosa", f"Datos cargados: {len(data)} registros únicos.")
        label_datos.config(text=f"Datos cargados: {len(data)} registros")  # Actualizar la etiqueta de datos cargados.

# Función para preprocesar los datos
def preprocesar_datos():
    global data  # Hacer que la variable data sea global.
    data["text"] = data["text"].str.lower()  # Convertir todo el texto a minúsculas.
    data["text"] = data["text"].apply(lambda x: re.sub(r'[^a-zA-Z0-9\s]', '', x))  # Eliminar caracteres especiales.
    
    # Obtener la lista de palabras vacías en inglés y eliminar esas palabras del texto.
    stop_words = set(stopwords.words('english'))
    data["text"] = data["text"].apply(lambda x: ' '.join([word for word in x.split() if word not in stop_words]))
    
    # Contar el número de correos SPAM y NO SPAM.
    cantidad_spam = data['target'].sum()  # Sumar la columna de destino para obtener el total de correos SPAM.
    cantidad_no_spam = len(data) - cantidad_spam  # Calcular el total de correos NO SPAM.
    
    # Mostrar información sobre la cantidad de correos SPAM y NO SPAM en el cuadro de texto.
    text_result.insert(tk.END, f"Correos SPAM: {cantidad_spam}\n")
    text_result.insert(tk.END, f"Correos NO SPAM: {cantidad_no_spam}\n")
    text_result.insert(tk.END, "="*80 + "\n")
    
    # Actualizar la etiqueta de procesamiento y mostrar un mensaje de éxito.
    label_procesamiento.config(text="Datos preprocesados")
    messagebox.showinfo("Preprocesamiento Completo", "Los datos han sido preprocesados exitosamente.")

# Función para clasificar los correos
def clasificar():
    global features, data  # Hacer que las variables sean globales.
    vectorizer = TfidfVectorizer(stop_words='english')  # Crear un vectorizador TF-IDF.
    features = vectorizer.fit_transform(data["text"])  # Ajustar y transformar el texto en características TF-IDF.
    
    # Calcular las probabilidades previas de spam y no spam.
    P_spam = data["target"].sum() / len(data)  # Probabilidad de que un correo sea SPAM.
    P_no_spam = 1 - P_spam  # Probabilidad de que un correo NO sea SPAM.
    
    # Mostrar las probabilidades en el cuadro de texto.
    text_result.insert(tk.END, f"Probabilidad de que sea spam P(Spam): {P_spam} = {round(P_spam * 100, 2)} %\n")
    text_result.insert(tk.END, f"Probabilidad de que NO sea spam P(No Spam): {P_no_spam} = {round(P_no_spam * 100, 2)} %\n")
    
    # Calcular la probabilidad de características dado spam y no spam.
    P_caracteristicas_spam = features[data["target"] == 1].sum(axis=0) / features[data["target"] == 1].sum()
    P_caracteristicas_no_spam = features[data["target"] == 0].sum(axis=0) / features[data["target"] == 0].sum()
    
    # Calcular la probabilidad posterior de que un correo sea spam o no spam.
    posterior_spam = (features @ np.array(P_caracteristicas_spam).flatten()) * P_spam
    posterior_no_spam = (features @ np.array(P_caracteristicas_no_spam).flatten()) * P_no_spam
    
    # Clasificar los correos según la probabilidad posterior.
    clasificaciones = np.where(posterior_spam > posterior_no_spam, "spam", "no spam")
    data["predicted"] = clasificaciones  # Agregar las clasificaciones al DataFrame.
    
    # Calcular la precisión de la clasificación.
    precision = np.mean(clasificaciones == np.where(data["target"] == 1, "spam", "no spam"))
    
    # Mostrar la precisión en el cuadro de texto.
    text_result.insert(tk.END, f"Precisión (Naive Bayes): {precision} = {round(precision * 100, 2)} %\n")
    label_clasificacion.config(text="Clasificación completa")  # Actualizar la etiqueta de clasificación.
    text_result.insert(tk.END, "="*80 + "\n")
    
    # Mostrar un mensaje de éxito al usuario.
    messagebox.showinfo("Clasificación Completa", "Clasificación de correos completada.")

# Función para evaluar el modelo
def evaluar_modelo():
    global features, data  # Hacer que las variables sean globales.
    # Dividir los datos en conjuntos de entrenamiento y prueba.
    X_train, X_test, y_train, y_test = train_test_split(features, data["target"], test_size=0.2, random_state=42)
    
    # Crear y ajustar el modelo Naive Bayes.
    modelo_bayes = MultinomialNB()  # Inicializar el clasificador.
    modelo_bayes.fit(X_train, y_train)  # Ajustar el modelo con los datos de entrenamiento.
    joblib.dump(modelo_bayes, "modelo_spam.pkl")  # Guarda el modelo entrenado en un archivo.
    
    # Predecir las clasificaciones para el conjunto de prueba.
    y_pred = modelo_bayes.predict(X_test)
    
    # Calcular métricas de evaluación.
    precision_sklearn = accuracy_score(y_test, y_pred)  # Calcular precisión.
    recuperacion_sklearn = recall_score(y_test, y_pred)  # Calcular recuperación.
    reporte_clasificacion = classification_report(y_test, y_pred)  # Generar un reporte de clasificación.
    
    # Mostrar información sobre los datos de entrenamiento y prueba.
    text_result.insert(tk.END, f"Datos de entrenamiento: {X_train.shape}\n")
    text_result.insert(tk.END, f"Datos de prueba: {X_test.shape}\n")
    text_result.insert(tk.END, "="*80 + "\n")
    
    # Mostrar las métricas de evaluación en el cuadro de texto.
    text_result.insert(tk.END, f"Precisión (sklearn): {precision_sklearn} = {round(precision_sklearn * 100, 2)} %\n")
    text_result.insert(tk.END, f"Recuperación (sklearn): {recuperacion_sklearn} = {round(recuperacion_sklearn * 100, 2)} %\n")
    text_result.insert(tk.END, f"Reporte de clasificación (sklearn):\n{reporte_clasificacion}\n")
    text_result.insert(tk.END, "="*80 + "\n")
    
    label_evaluacion.config(text="Evaluación del modelo completa")  # Actualizar la etiqueta de evaluación.
    # Mostrar un mensaje de confirmación al usuario.
    messagebox.showinfo("Evaluación Completa", "Evaluación del modelo completada.")

def predecir_nuevos_correos():
    global features  # Asegúrate de que ya tienes el vectorizador ajustado con el archivo anterior.
    archivo_nuevo = filedialog.askopenfilename()  # Selecciona el nuevo archivo sin `target`.
    if archivo_nuevo:
        nuevos_datos = pd.read_csv(archivo_nuevo)  # Carga los nuevos correos.
        if 'text' not in nuevos_datos.columns:
            messagebox.showerror("Error", "El archivo CSV debe contener la columna 'text'.")
            return
        
        # Preprocesa el texto igual que en los correos anteriores.
        nuevos_datos["text"] = nuevos_datos["text"].str.lower()
        nuevos_datos["text"] = nuevos_datos["text"].apply(lambda x: re.sub(r'[^a-zA-Z0-9\s]', '', x))
        
        # Cargar el modelo y el vectorizador.
        modelo_bayes = joblib.load("modelo_spam.pkl")
        
        # Vectorizar los correos nuevos y predecir.
        nuevas_features = features.transform(nuevos_datos["text"])  # Vectorizar el texto.
        predicciones = modelo_bayes.predict(nuevas_features)  # Predice si es spam o no.
        
        # Mostrar resultados
        nuevos_datos["Predicción"] = np.where(predicciones == 1, "spam", "no spam")
        text_result.insert(tk.END, nuevos_datos[["text", "Predicción"]])  # Muestra resultados en el cuadro de texto.

# Componentes de la interfaz gráfica

# Etiqueta del título de la aplicación
label_titulo = tk.Label(window, text="Clasificación de Correos: Spam vs No Spam", bg="lightblue", font=("Arial", 16, "bold"))
label_titulo.pack(pady=10)  # Agregar la etiqueta al contenedor.

# Botón para cargar los datos
btn_cargar_datos = tk.Button(window, text="1. Cargar Datos", command=cargar_datos)
btn_cargar_datos.pack(pady=5)  # Agregar el botón al contenedor.
label_datos = tk.Label(window, text="", bg="lightblue")  # Etiqueta para mostrar el estado de los datos.
label_datos.pack()  # Agregar la etiqueta al contenedor.

# Botón para preprocesar los datos
btn_preprocesar = tk.Button(window, text="2. Preprocesar Datos", command=preprocesar_datos)
btn_preprocesar.pack(pady=5)  # Agregar el botón al contenedor.
label_procesamiento = tk.Label(window, text="", bg="lightblue")  # Etiqueta para mostrar el estado del procesamiento.
label_procesamiento.pack()  # Agregar la etiqueta al contenedor.

# Botón para clasificar los correos
btn_clasificar = tk.Button(window, text="3. Clasificar Correos", command=clasificar)
btn_clasificar.pack(pady=5)  # Agregar el botón al contenedor.
label_clasificacion = tk.Label(window, text="", bg="lightblue")  # Etiqueta para mostrar el estado de la clasificación.
label_clasificacion.pack()  # Agregar la etiqueta al contenedor.

# Botón para evaluar el modelo
btn_evaluar = tk.Button(window, text="4. Evaluar Modelo", command=evaluar_modelo)
btn_evaluar.pack(pady=5)  # Agregar el botón al contenedor.
label_evaluacion = tk.Label(window, text="", bg="lightblue")  # Etiqueta para mostrar el estado de la evaluación.
label_evaluacion.pack()  # Agregar la etiqueta al contenedor.

# Boton para predecir nuevos correos
btn_predecir = tk.Button(window, text="5. Predecir Nuevos Correos", command=predecir_nuevos_correos)
btn_predecir.pack(pady=5)  # Agregar el botón al contenedor.


# Cuadro de texto para mostrar los resultados y mensajes
text_result = tk.Text(window, width=80, height=20)  # Crear un cuadro de texto para mostrar resultados.
text_result.pack(pady=10)  # Agregar el cuadro de texto al contenedor.

# Iniciar el bucle principal de la aplicación
window.mainloop()  # Ejecutar el bucle principal para mantener la ventana abierta.