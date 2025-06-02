import json
import random
import re

def load_responses(filepath='data/responses.json'):
    """
    Carga las preguntas y respuestas desde un archivo JSON con el nuevo formato.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get("opciones", []), data.get("default_responses", ["Lo siento, no tengo una respuesta para eso."])
    except FileNotFoundError:
        print(f"Error: El archivo {filepath} no fue encontrado.")
        return [], ["Error al cargar respuestas."]
    except json.JSONDecodeError:
        print(f"Error: No se pudo decodificar el archivo JSON {filepath}.")
        return [], ["Error al cargar respuestas."]

def get_response_from_keywords(user_input, options_data, default_responses):
    """
    Busca una respuesta basada en la entrada de texto libre del usuario,
    comparando con las keywords de cada opción.
    """
    user_input = user_input.lower()

    for option in options_data:
        for keyword in option.get("keywords", []):
            # Usamos re.search para buscar la palabra clave en la entrada del usuario
            # re.escape(keyword) es para escapar caracteres especiales si los hubiera
            if re.search(r'\b' + re.escape(keyword.lower()) + r'\b', user_input):
                return random.choice(option.get("responses", default_responses))

    # Si no se encuentra ninguna coincidencia con las keywords, devuelve una respuesta por defecto
    return random.choice(default_responses)

def get_response_from_label(label, options_data, default_responses):
    """
    Obtiene una respuesta basada en la etiqueta seleccionada directamente.
    """
    label_lower = label.lower()
    for option in options_data:
        if option.get("label", "").lower() == label_lower:
            return random.choice(option.get("responses", default_responses))
    # Esto no debería pasar si la etiqueta viene de los botones generados
    return random.choice(default_responses)