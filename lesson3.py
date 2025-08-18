import flet as ft
import datetime as dt

def page_main(page: ft.Page):
    page.title = "Мое первое приложение"
    page.theme_mode = ft.ThemeMode.LIGHT

    greeting_history = []

    greeting_text = ft.Text("Hello World")
    name_input = ft.TextField(label="Введите ваше имя: ")

    def update_history_view():
        history_controls = [ft.Text("История приветствий:")]
        for entry in greeting_history:
            history_controls.append(ft.Text(entry))
        history_column.controls = history_controls
        page.update()

    def clear_history(_):
        greeting_history.clear()
        update_history_view()

    clear_row = ft.Row(controls=[ft.Text("Очистить историю"), ft.IconButton(icon=ft.Icons.DELETE, on_click=clear_history),],
        alignment=ft.MainAxisAlignment.CENTER)

    def on_button_click(_):
        name = name_input.value.strip()

        if name:
            current_hour = dt.datetime.now().hour
            if 6 <= current_hour < 12:
                greeting = "Доброе утро"
            elif 12 <= current_hour < 18:
                greeting = "Добрый день"
            elif 18 <= current_hour < 24:
                greeting = "Добрый вечер"
            else:
                greeting = "Доброй ночи"

            greeting_text.value = f"{greeting}, {name}!"
            name_input.value = ""
            greet_button.text = "Поздороваться снова"

            greeting_history.append(f"{dt.datetime.now()}: {name}")
            update_history_view()
        else:
            greeting_text.value = "Введите корректное имя!"

        page.update()

    greet_button = ft.ElevatedButton("Отправить", on_click=on_button_click, icon=ft.Icons.SEND)
    clear_button = ft.IconButton(icon=ft.Icons.DELETE, on_click=clear_history)
    greet_button = ft.ElevatedButton("Поздороваться снова", on_click=on_button_click)


    history_column = ft.Column([])
    update_history_view()


    page.add(clear_row, greeting_text, name_input, greet_button, history_column)

ft.app(target=page_main)