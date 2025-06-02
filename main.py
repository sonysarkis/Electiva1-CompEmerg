import flet as ft
from flet import Colors as colors
from utils.chatbot_functions import load_responses, get_response_from_keywords, get_response_from_label
import random  # Asegúrate de que random esté importado aquí si lo usas directamente

def main(page: ft.Page):
    page.title = "Mi Chatbot Intuitivo"
    page.vertical_alignment = ft.MainAxisAlignment.END  # Alinea el contenido al final de la página

    # Cargar respuestas y respuestas por defecto al inicio
    options_data, default_responses = load_responses()
    if not options_data:
        page.add(ft.Text("Error al cargar las opciones del chatbot. Revisa data/responses.json"))
        return

    # Elementos de la interfaz
    chat_history = ft.Column(
        expand=True,  # Hace que ocupe todo el espacio vertical disponible
        scroll="always",  # Permite scroll si el contenido es mucho
        horizontal_alignment=ft.CrossAxisAlignment.START,  # Alinea los mensajes a la izquierda
        key="chat_history"  # Agrega una clave para identificar el widget
    )

    txt_input = ft.TextField(
        hint_text="Escribe tu pregunta...",
        expand=True,
        on_submit=lambda e: send_message_from_text(e.control.value)  # Llama a la función al presionar Enter
    )

    def add_message(sender: str, message: str, is_user: bool):
        """Agrega un mensaje al historial del chat."""
        # Estilos para diferenciar mensajes de usuario y chatbot
        if is_user:
            text_style = ft.TextStyle(color=colors.BLUE_GREY_100)
            alignment = ft.CrossAxisAlignment.END
        else:
            text_style = ft.TextStyle(color=colors.GREEN_50)
            alignment = ft.CrossAxisAlignment.START

        chat_history.controls.append(
            ft.Row(
                [ft.Text(f"{sender}: {message}", selectable=True, style=text_style)],
                alignment=alignment
            )
        )
        page.update()
        # Scroll automático al último mensaje
        chat_history.scroll_to(offset=99999)

    def send_message_from_text(user_text: str):
        """Maneja el envío de mensajes por texto libre."""
        user_text = user_text.strip()
        if not user_text:
            return  # No hacer nada si el texto está vacío

        add_message("Tú", user_text, is_user=True)
        txt_input.value = ""  # Limpiar el campo de entrada

        if user_text.lower() == 'salir':
            add_message("ChatBot", "¡Adiós! Fue un placer conversar contigo.", is_user=False)
            page.update()
            # Puedes añadir page.window_destroy() o page.close_async() si quieres cerrar la ventana
            return

        bot_response = get_response_from_keywords(user_text, options_data, default_responses)
        add_message("ChatBot", bot_response, is_user=False)

    def send_message_from_option(e):
        """Maneja el envío de mensajes al seleccionar una opción (botón)."""
        selected_label = e.control.text  # El texto del botón es la etiqueta (label)
        add_message("Tú", selected_label, is_user=True)

        bot_response = get_response_from_label(selected_label, options_data, default_responses)
        add_message("ChatBot", bot_response, is_user=False)

    # Generar los botones de opciones dinámicamente
    option_buttons = []
    for option in options_data:
        button_label = option.get("label")
        if button_label:  # Asegúrate de que haya una etiqueta para el botón
            option_buttons.append(
                ft.ElevatedButton(
                    text=button_label,
                    on_click=send_message_from_option,
                    color=colors.WHITE,  # Color del texto del botón
                    bgcolor=colors.BLUE_600  # Color de fondo del botón
                )
            )

    # Contenedor para los botones de opciones (usamos Wrap para que se ajusten bien)
    options_container = ft.Column(
        [
            ft.Text("Selecciona una opción o escribe tu pregunta:", weight=ft.FontWeight.BOLD),
            ft.Row(
                controls=option_buttons,
                spacing=10,  # Espacio entre botones
                alignment=ft.MainAxisAlignment.CENTER
            )
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER  # Centra los botones
    )

    # Estructura de la página
    page.add(
        ft.Container(  # Un contenedor para el historial de chat con un fondo
            content=chat_history,
            expand=True,
            alignment=ft.alignment.top_left,
            padding=10,
            bgcolor=colors.BLUE_GREY_800  # Fondo oscuro para el chat
        ),
        ft.Divider(height=1, color=colors.BLUE_GREY_700),  # Una línea divisoria
        options_container,  # El contenedor de opciones
        ft.Row(  # Fila para el campo de texto y el botón de enviar
            controls=[
                txt_input,
                ft.IconButton(
                    icon=ft.Icons.SEND,
                    on_click=lambda e: send_message_from_text(txt_input.value),
                    tooltip="Enviar Mensaje"
                )
            ]
        )
    )

    # Mensaje de bienvenida inicial del chatbot
    add_message("ChatBot", "¡Hola! Soy tu chatbot personal. Selecciona una opción o escribe tu pregunta. Puedes escribir 'salir' para finalizar.", is_user=False)

if __name__ == "__main__":
    ft.app(target=main)