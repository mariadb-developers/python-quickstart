import sys
import mariadb

def createSchema(cur):
    cur.execute("CREATE DATABASE todo")
    print("todo database created")
    cur.execute("""CREATE TABLE todo.tasks (
                        id INT(11) unsigned NOT NULL AUTO_INCREMENT,
                        description VARCHAR(500) NOT NULL,
                        completed BOOLEAN NOT NULL DEFAULT 0,
                        PRIMARY KEY (id)
                    )""")
    print("tasks table created")

def dropSchema(cur):
    cur.execute("DROP DATABASE todo")
    print("todo database and tasks table dropped")

def addTask(cur, description):
    cur.execute("INSERT INTO todo.tasks (description) VALUES (?)",[description])
    print(f"Task (id={cur.lastrowid}) added successfully")
 
def updateTask(cur, description, id):
    cur.execute("UPDATE todo.tasks set completed = ? WHERE id = ?",[description,id])
    print(f"Task (id={id}) status updated")

def showTasks(cur):
    cur.execute("SELECT * FROM todo.tasks")
    # Print the results stored in the cursor
    for id, description, completed in cur: 
        print(f"id = {id}, description = {description}, completed = {completed}")

def deleteTask(cur, id):
    cur.execute("DELETE FROM todo.tasks WHERE id = ?",[id])
    print(f"Task (id={id}) deleted")

def main():
    try:
        args = sys.argv[1:]

        if (len(args) == 0):
            raise Exception("Invalid arguments")

        action = args[0]

        conn = mariadb.connect(
            host="127.0.0.1",
            user="root",
            password="RootPassword123!",
            autocommit=True
        )

        cur = conn.cursor()

        if (action == "create"):
            createSchema(cur)
        elif (action == "drop"):
            dropSchema(cur)
        elif (action == "add"):
            description = args[1]
            addTask(cur, description)
        elif (action == "updateStatus"):
            id = args[1]
            completed = args[2]
            updateTask(cur, id, completed)
        elif (action == "show"):
            showTasks(cur)
        elif (action == "delete"):
            id = args[1]
            deleteTask(cur, id)
        else:
            raise Exception("Invalid action argument")

    except Exception as e:
        print(e)
    finally:
        conn.close()

if __name__ == "__main__":
    main()