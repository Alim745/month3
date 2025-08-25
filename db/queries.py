CREATE_TASK = """
    CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT NOT NULL,
    completed INTEGER DEFAULT 0,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
"""



INSERT_TASK = "INSERT INTO tasks (task) VALUES (?)"

SELECT_TASK = "SELECT id, task, COMPLETED, created_at FROM tasks"

SELECT_TASK_COMPLETED = "SELECT id, task, completed, created_at FROM tasks WHERE completed = 1"
SELECT_TASK_UNCOMPLETED = "SELECT id, task, completed, created_at FROM tasks WHERE completed = 0"

UPDATE_TASK = "UPDATE tasks SET task = ? WHERE id = ?"

DELETE_TASK = "DELETE FROM tasks WHERE id = ?"

