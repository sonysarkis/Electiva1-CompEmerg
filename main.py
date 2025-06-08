import flet as ft
from flet import Colors
from utils.chatbot_functions import load_responses, get_response_from_keywords, get_response_from_label
import random

def main(page: ft.Page):
    page.title = "Charcutería El Pavo Mio"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.END

    def show_chatbot():
        page.controls.clear()

        # --- Chatbot original aquí ---
        options_data, default_responses = load_responses()
        if not options_data:
            page.add(ft.Text("Error al cargar las opciones del chatbot. Revisa data/responses.json"))
            return

        chat_history = ft.Column(
            expand=True,
            scroll="always",
            horizontal_alignment=ft.CrossAxisAlignment.START,
            key="chat_history"
        )

        txt_input = ft.TextField(
            hint_text="¿Qué deseas consultar hoy? 🧀🥓",
            expand=True,
            on_submit=lambda e: send_message_from_text(e.control.value)
        )

        def add_message(sender: str, message: str, is_user: bool):
            if is_user:
                text_style = ft.TextStyle(color=Colors.AMBER_200)
                alignment = ft.CrossAxisAlignment.END
            else:
                text_style = ft.TextStyle(color=Colors.WHITE, weight=ft.FontWeight.BOLD, size=13)
                alignment = ft.CrossAxisAlignment.START

            chat_history.controls.append(
                ft.Row(
                    [ft.Text(f"{sender}: {message}", selectable=True, style=text_style)],
                    alignment=alignment
                )
            )
            page.update()
            chat_history.scroll_to(offset=99999)

        def send_message_from_text(user_text: str):
            user_text = user_text.strip()
            if not user_text:
                return

            add_message("Cliente", user_text, is_user=True)
            txt_input.value = ""

            if user_text.lower() == 'salir':
                add_message("CharcuBot", "¡Gracias por visitarnos! Que disfrutes tus productos frescos. 🧀🥓", is_user=False)
                page.update()
                return

            bot_response = get_response_from_keywords(user_text, options_data, default_responses)
            add_message("CharcuBot", bot_response, is_user=False)

        def send_message_from_option(e):
            selected_label = e.control.text
            add_message("Cliente", selected_label, is_user=True)
            bot_response = get_response_from_label(selected_label, options_data, default_responses)
            add_message("CharcuBot", bot_response, is_user=False)

        option_buttons = []
        max_buttons = 5
        for i, option in enumerate(options_data):
            if i >= max_buttons:
                break
            button_label = option.get("label")
            if button_label:
                option_buttons.append(
                    ft.ElevatedButton(
                        text=button_label,
                        on_click=send_message_from_option,
                        color=Colors.WHITE,
                        bgcolor=Colors.BROWN_900
                    )
                )

        options_container = ft.Column(
            [
                ft.Text(
                    "Selecciona una opción o pregunta por nuestros productos frescos:",
                    weight=ft.FontWeight.BOLD,
                    color=Colors.AMBER_200
                ),
                ft.Row(
                    controls=option_buttons,
                    spacing=5,
                    alignment=ft.MainAxisAlignment.CENTER
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        page.add(
            ft.Container(
                content=chat_history,
                expand=True,
                alignment=ft.alignment.top_left,
                padding=10,
                bgcolor=Colors.GREY_900
            ),
            ft.Divider(height=1, color=Colors.AMBER_700),
            options_container,
            ft.Row(
                controls=[
                    txt_input,
                    ft.IconButton(
                        icon=ft.Icons.SEND,
                        on_click=lambda e: send_message_from_text(txt_input.value),
                        tooltip="Enviar Mensaje",
                        bgcolor=Colors.AMBER_700,
                        icon_color=Colors.BROWN_900
                    )
                ]
            )
        )

        add_message(
            "CharcuBot",
            "¡Bienvenido a la Charcutería El Pavo Mio! 🦃🧀 Pregunta por nuestros productos frescos o selecciona una opción. Escribe 'salir' para terminar.",
            is_user=False
        )

        page.update()

    # --- Interfaz de bienvenida ---
    bienvenida = ft.Column(
        [
            ft.Container(
                content=ft.Image(
                    src="assets/charcuteria.jpg",
                    width=350,
                    height=200,
                    fit=ft.ImageFit.COVER,
                    border_radius=10
                ),
                alignment=ft.alignment.center,
                padding=10
            ),
            ft.Container(
                content=ft.Text(
                    "¡Bienvenido a la Charcutería El Pavo Mio!",
                    size=30,
                    weight=ft.FontWeight.BOLD,
                    color=Colors.AMBER_200,
                    text_align=ft.TextAlign.CENTER
                ),
                alignment=ft.alignment.center,
                padding=10
            ),
            ft.Text(
                "Haz clic en el botón para hablar con nuestro asistente virtual y conocer productos, precios y más.",
                size=18,
                color=Colors.WHITE,
                text_align=ft.TextAlign.CENTER
            ),
            ft.Container(
                content=ft.ElevatedButton(
                    text="Ir al Chatbot",
                    on_click=lambda e: show_chatbot(),
                    bgcolor=Colors.AMBER_700,
                    color=Colors.BROWN_900,
                    style=ft.ButtonStyle(
                        padding=20,
                        shape=ft.RoundedRectangleBorder(radius=10)
                    )
                ),
                alignment=ft.alignment.center,
                padding=30
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True
    )

    page.add(bienvenida)

if __name__ == "__main__":
    ft.app(target=main)