import threading
from db_instance import SimpleDB

primary_db = SimpleDB("primary.json")
backup_db = SimpleDB("backup.json")

def sync_backup():
    """Sincroniza backup después de cualquier transacción."""
    data = primary_db.read_all()
    for key, value in data.items():
        backup_db.write_data(key, value)

def transaction(action, *args):
    """Ejecuta una transacción con sincronización."""
    if action == "create" or action == "update":
        key, value = args
        primary_db.write_data(key, value)
    elif action == "delete":
        key = args[0]
        primary_db.delete_data(key)
    elif action == "get":
        key = args[0]
        result = primary_db.get_data(key)
        print(f">>> Resultado: {result}")
        return
    elif action == "read_all":
        data = primary_db.read_all()
        print(">>> Base de datos completa:")
        for k, v in data.items():
            print(f"{k}: {v}")
        return
    else:
        print(">>> Acción inválida")
        return

    sync_backup()
    print(">>> Transacción completada y backup sincronizado.")

def user_interface():
    while True:
        print("\n--- Menú ---")
        print("1. Crear/Actualizar dato")
        print("2. Leer dato")
        print("3. Eliminar dato")
        print("4. Ver todos los datos")
        print("5. Salir")

        opcion = input("Elige una opción: ")

        if opcion == "1":
            key = input("Clave: ")
            value = input("Valor: ")
            threading.Thread(target=transaction, args=("create", key, value)).start()
        elif opcion == "2":
            key = input("Clave: ")
            threading.Thread(target=transaction, args=("get", key)).start()
        elif opcion == "3":
            key = input("Clave a eliminar: ")
            threading.Thread(target=transaction, args=("delete", key)).start()
        elif opcion == "4":
            # Para que no se bloquee, usamos un hilo también
            threading.Thread(target=transaction, args=("read_all",)).start()
        elif opcion == "5":
            print("Saliendo...")
            break
        else:
            print(">>> Opción inválida")

if __name__ == "__main__":
    print("Iniciando base de datos interactiva...")
    user_interface()
