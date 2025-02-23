import openai
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import time
import os
import chainlit as cl

# Cargar las variables de entorno
from dotenv import load_dotenv
load_dotenv()

# Obtener la clave de API de OpenAI desde las variables de entorno
openai.api_key = os.getenv('OPENAI_API_KEY')

# Cargar el modelo preentrenado para embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')

# Cargar el índice FAISS previamente guardado
index = faiss.read_index("../data/cooked/mi_indice.index")

# Leer los documentos originales desde el archivo
with open('../data/cooked/texto_extraido.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Función para buscar documentos relevantes en FAISS
def buscar_documentos(query, k=5):
    # Obtener el embedding para la consulta utilizando el modelo
    query_embedding = model.encode([query], convert_to_numpy=True)

    # Buscar en el índice de FAISS los documentos más cercanos
    D, I = index.search(query_embedding, k)

    # Recuperar los textos de los documentos más cercanos
    documents = [lines[i] for i in I[0]]
    return documents

# Función para crear un hilo de conversación en OpenAI
def create_thread(openai_client):
    """
    Crea un nuevo hilo de conversación en OpenAI.
    """
    return openai_client.beta.threads.create()

# Función para enviar un mensaje a OpenAI y obtener la respuesta
def process_data(openai_client, assistant_id, thread_id, message):
    """
    Envía un mensaje a un asistente de OpenAI y procesa su respuesta.
    """
    openai_client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=message,
    )

    run = openai_client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
    )

    run_status = openai_client.beta.threads.runs.retrieve(
        thread_id=thread_id,
        run_id=run.id
    )

    while True:
        run_status = openai_client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )
        if run_status.status == "completed":
            break
        elif run_status.status == "failed":
            print("Error, no se encontró una respuesta del asistente.")
            return "No se encontró una respuesta del asistente."
        else:
            time.sleep(3)

    response_messages = openai_client.beta.threads.messages.list(thread_id=thread_id)
    
    assistant_response = None
    for message in response_messages.data:
        assistant_response = "\n".join([block.text.value for block in message.content])
        break

    return assistant_response

# Función para generar una respuesta utilizando los documentos recuperados
def generar_respuesta(query):
    # Obtener documentos relevantes de FAISS
    documents = buscar_documentos(query)
    
    # Crear el contexto para el asistente, concatenando los documentos relevantes
    contexto = "\n".join(documents)

    # Inicializa el cliente de OpenAI
    openai_client = openai

    # Crear el hilo
    thread = create_thread(openai_client)
    thread_id = thread.id  # Accede al ID del hilo correctamente

    # Enviar la consulta al asistente
    assistant_response = process_data(openai_client, assistant_id="asst_lahRwaFfzCaBYGUe3wuK9qT4", thread_id=thread_id, message=f"Basado en los siguientes documentos, por favor, responde a la consulta: '{query}'\n\n{contexto}")

    return assistant_response


# Configuración de Chainlit para manejar la interacción del chatbot
@cl.on_message
async def main(message: str):
    # Llamar a la función para generar una respuesta basada en la consulta
    respuesta = generar_respuesta(message.content)  # Usamos message.content para obtener el texto

    # Enviar la respuesta al usuario
    await cl.Message(content=respuesta).send()
