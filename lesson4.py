import flet as ft

def page_main(page: ft.Page):
    page.title = "Мое первое приложение на flet!"
    page.theme_mode = ft.ThemeMode.LIGHT

    greeting_history = []

    greeting_text = ft.Text("Hello World")
    name_input = ft.TextField(label="Введите имя: ")

    def update_history_view():
        history_controls = [ft.Text("История приветствий: ")]
        for idx, name in enumerate(greeting_history):
            history_controls.append(
                ft.Row([ft.Text(name), 
                        ft.IconButton(icon=ft.Icons.CLOSE, on_click=lambda e, i=idx: remove_name_from_history(i))
                        ])
            )
        history_column.controls = history_controls
        page.update()

    def remove_name_from_history(index):
        if 0 <= index < len(greeting_history):
            del greeting_history[index]
            update_history_view()

    def on_button_click(_):
        name = name_input.value.strip()
        print(name)

        if name: 
            greeting_text.value = f"Hello {name}"
            name_input.value = ""
            greet_button.text = "Поздороваться снова"

            greeting_history.append(name)
            update_history_view()
        else:
            greeting_text.value = "Введите корректное имя!"

        page.update()

    greet_button = ft.ElevatedButton("Отправить", on_click=on_button_click, icon=ft.Icons.SEND)
    greet_button_icon = ft.IconButton(icon=ft.Icons.SEND, on_click=on_button_click, icon_color=ft.Colors.GREEN)


    history_column = ft.Column([])
    update_history_view()
   
    # page.add(greeting_text, name_input, greet_button, history_column)


    page.add(ft.Row([greeting_text, name_input, greet_button_icon], alignment=ft.MainAxisAlignment.CENTER), history_column)


ft.app(target=page_main)