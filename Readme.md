# 🧠 Proyecto RAG con Chainlit, FAISS y OpenAI
# Árbitro de Ajedrez (Normas FIDE)

Este proyecto implementa un sistema de **Retrieval-Augmented Generation (RAG)** usando **Chainlit** como interfaz, **FAISS** para búsqueda de similitud y **OpenAI Assistants** para generar respuestas personalizadas.

---

## 🚀 Características principales

- 🔍 Búsqueda rápida de documentos usando FAISS.
- 🤖 Respuestas generadas con modelos de OpenAI.
- 💬 Interfaz interactiva a través de **Chainlit**.
- 🛠️ Personalización del flujo conversacional y los mensajes.

---

## 📦 Instalación

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/tu-usuario/tu-repo.git
   cd tu-repo
    ```
2. **Crear y activar un entorno virtual:**

    ````
    conda create -n prueba_rag_tailor python=3.9
    conda activate prueba_rag_tailor
    ````

3. **Instalar las dependencias**
    ```
    pip install -r requirements.txt
    ````
4. **Configurar las variables de entorno: Crea un archivo .env y añade tu clave de API de OpenAI**
    ````
     OPENAI_API_KEY=tu_clave_de_api
    ````

---

## ⚙️ Ejecución
1. Inicia la aplicación con Chainlit:
    ````
    chainlit run app-chainlit.py
    ````
2. Accede a la app en tu navegador:
    ````
    http://localhost:8000
    ````

---

## 📚 Uso

- 💡 Escribe una consulta en el chat.
- 📄 El sistema buscará documentos relacionados.
- 🤖 OpenAI generará una respuesta basada en los documentos más relevantes.
