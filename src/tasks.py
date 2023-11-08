import sys
import mariadb

def create_schema(cur):
    cur.execute("CREATE DATABASE demo")
    print("demo database created")
    cur.execute("""CREATE TABLE demo.tasks (
                        id INT(11) unsigned NOT NULL AUTO_INCREMENT,
                        description VARCHAR(500) NOT NULL,
                        completed BOOLEAN NOT NULL DEFAULT 0,
                        PRIMARY KEY (id)
                    )""")
    print("tasks table created")

def drop_schema(cur):
    cur.execute("DROP DATABASE demo")
    print("demo database and tasks table dropped")

def add_task(cur, description):
    cur.execute("INSERT INTO demo.tasks (description) VALUES (?)",[description])
    print(f"Task (id={cur.lastrowid}) added successfully")
 
def update_task(cur, description, id):
    cur.execute("UPDATE demo.tasks set completed = ? WHERE id = ?",[description,id])
    print(f"Task (id={id}) status updated")

def show_tasks(cur):
    cur.execute("SELECT * FROM demo.tasks")
    # Print the results stored in the cursor
    for id, description, completed in cur: 
        print(f"id = {id}, description = {description}, completed = {completed}")

def delete_task(cur, id):
    cur.execute("DELETE FROM demo.tasks WHERE id = ?",[id])
    print(f"Task (id={id}) deleted")

def main():
    try:
        args = sys.argv[1:]

        if (len(args) == 0):
            raise ValueError("Invalid arguments")

        action = args[0]

        conn = mariadb.connect(
            host="127.0.0.1",
            user="user",
            password="Password123!",
            autocommit=True
        )

        cur = conn.cursor()

        match action:
            case "create":
                create_schema(cur)
            case "drop":
                drop_schema(cur)
            case "add":
                description = args[1]
                add_task(cur, description)
            case "updateStatus":
                task_id = args[1]
                completed = args[2]
                update_task(cur, task_id, completed)
            case "show":
                show_tasks(cur)
            case "delete":
                task_id = args[1]
                delete_task(cur, task_id)
            case _:
                raise ValueError(f"Invalid action argument: {action}")
    except Exception as e:
        print(e)
    finally:
        conn.close()

if __name__ == "__main__":
    main()