import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# Cargar el conjunto de datos
data = pd.read_csv("spam.csv")

# Preprocesamiento de datos
data["text"] = data["text"].str.lower()
data["text"] = data["text"].str.replace("[^a-zA-Z0-9]", "")
data["text"] = data["text"].str.split()
data["text"] = data["text"].apply(lambda x: " ".join([word for word in x if word not in stopwords]))

# Extracción de características
vectorizer = TfidfVectorizer(stop_words="english")
features = vectorizer.fit_transform(data["text"])

# Calcular la probabilidad previa de spam
P_spam = data["spam"].sum() / len(data)

# Calcular la probabilidad de las características del correo electrónico dado que es spam
P_caracteristicas_spam = features[data["spam"] == 1].sum(axis=0) / features[data["spam"] == 1].sum()

# Calcular la probabilidad de las características del correo electrónico dado que no es spam
P_caracteristicas_no_spam = features[data["spam"] == 0].sum(axis=0) / features[data["spam"] == 0].sum()

# Calcular la probabilidad posterior de que el correo electrónico sea spam
P_spam_caracteristicas = (P_spam * P_caracteristicas_spam) / (P_spam * P_caracteristicas_spam + (1 - P_spam) * P_caracteristicas_no_spam)

# Clasificación
clasificaciones = np.where(P_spam_caracteristicas > 0.5, "spam", "no spam")

# Evaluación
precision = np.sum(clasificaciones == data["spam"]) / len(clasificaciones)
recall = np.sum(clasificaciones == data["spam"]) / data["spam"].sum()

print("Precisión:", precision)
print("Recuperación:", recall)