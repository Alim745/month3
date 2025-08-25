import flet as ft
from db import main_db

def main(page: ft.Page):
    page.title = 'ToDo list'
    page.theme_mode = ft.ThemeMode.LIGHT
    task_list = ft.Column()

    filter_type = "all"
    sort_type = None

    def create_task_row(task_id, task_text, completed, created_at):
        task_field = ft.TextField(value=task_text, expand=True, read_only=True)
        date_label = ft.Text(f"Создано: {created_at}")

        task_checkbox = ft.Checkbox(
            value=bool(completed),
            on_change=lambda e: toggle_task(task_id, e.control.value)
        )

        def enable_edit(_):
            if task_field.read_only == True:
                task_field.read_only = False
            else:
                task_field.read_only = True
            task_field.update()

        def save_task(_):
            main_db.update_task(task_id, task_field.value)
            task_field.read_only = True
            page.update()

        edit_button = ft.IconButton(icon=ft.Icons.EDIT, tooltip='Редактировать', on_click=enable_edit)
        save_button = ft.IconButton(icon=ft.Icons.SAVE, on_click=save_task)

        return ft.Column([
            ft.Row([task_checkbox, task_field, edit_button, save_button]),
            date_label
        ])

    def load_task():
        task_list.controls.clear()
        tasks = main_db.get_task(filter_type)

        if sort_type == "date_new":
            tasks.sort(key=lambda x: x[3], reverse=True)
        elif sort_type == "date_old":
            tasks.sort(key=lambda x: x[3])
        elif sort_type == "status_completed_bottom":
            tasks.sort(key=lambda x: x[2])
        elif sort_type == "status_completed_top":
            tasks.sort(key=lambda x: not x[2])

        for task_id, task_text, completed, created_at in tasks:
            task_list.controls.append(create_task_row(task_id, task_text, completed, created_at))
        page.update()

    def add_task(_):
        if len(task_input.value) > 100:
            page.snack_bar = ft.SnackBar(ft.Text("Максимум 100 символов!"))
            page.snack_bar.open = True
            page.update()
            return

        if task_input.value.strip():
            main_db.add_task(task_input.value)
            task_input.value = ''
            load_task()
            page.update()

    def toggle_task(task_id, is_completed):
        main_db.update_task(task_id, completed=int(is_completed))
        load_task()

    def set_filter(filter_value):
        nonlocal filter_type
        filter_type = filter_value
        load_task()

    def set_sort(sort_value):
        nonlocal sort_type
        sort_type = sort_value
        load_task()

    task_input = ft.TextField(label='Введите задачу', expand=True,)
    add_button = ft.ElevatedButton('ADD', on_click=add_task)

    filter_buttons = ft.Row(controls=[
        ft.ElevatedButton("Все", on_click=lambda e: set_filter('all')),
        ft.ElevatedButton("Завершенные", on_click=lambda e: set_filter('completed')),
        ft.ElevatedButton("Незавершенные", on_click=lambda e: set_filter('uncompleted'))
    ], alignment=ft.MainAxisAlignment.SPACE_EVENLY)

    sort_buttons = ft.Row(controls=[
        ft.ElevatedButton("Новые сверху", on_click=lambda e: set_sort("date_new")),
        ft.ElevatedButton("Старые сверху", on_click=lambda e: set_sort("date_old")),
        ft.ElevatedButton("Выполненные внизу", on_click=lambda e: set_sort("status_completed_bottom")),
        ft.ElevatedButton("Выполненные вверху", on_click=lambda e: set_sort("status_completed_top")),
    ], alignment=ft.MainAxisAlignment.SPACE_EVENLY)

    page.add(ft.Column([
        ft.Row([task_input, add_button]),
        filter_buttons,
        sort_buttons,
        task_list
    ]))

    load_task()


if __name__  == '__main__':
    main_db.init_db()
    ft.app(target=main)