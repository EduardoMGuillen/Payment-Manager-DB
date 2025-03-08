import customtkinter as ctk
import sqlite3
from tkinter import messagebox, ttk

# Crear la base de datos
conn = sqlite3.connect("clientes.db")
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS clientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cliente_id INTEGER UNIQUE,
                    nombre TEXT,
                    direccion TEXT,
                    telefono TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS pagos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cliente_id INTEGER,
                    mes TEXT,
                    monto REAL,
                    descripcion TEXT,
                    FOREIGN KEY(cliente_id) REFERENCES clientes(cliente_id))''')
conn.commit()
conn.close()


class PagosApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Pagos de Agua")
        self.geometry("800x600")

        self.frame = ctk.CTkFrame(self)
        self.frame.pack(fill='both', expand=True)

        self.titulo = ctk.CTkLabel(self.frame, text="Sistema de Pagos de Agua", font=("Arial", 20))
        self.titulo.pack(pady=10)

        self.btn_anadir = ctk.CTkButton(self.frame, text="Añadir Cliente", command=self.anadir_cliente)
        self.btn_anadir.pack(pady=5)

        self.btn_actualizar = ctk.CTkButton(self.frame, text="Actualizar Pagos y Ver Perfil",
                                            command=self.actualizar_pagos)
        self.btn_actualizar.pack(pady=5)

        self.btn_reporte = ctk.CTkButton(self.frame, text="Generar Reporte Mensual", command=self.generar_reporte)
        self.btn_reporte.pack(pady=5)

        self.btn_modificar = ctk.CTkButton(self.frame, text="Modificar Perfil", command=self.modificar_perfil)
        self.btn_modificar.pack(pady=5)

    def anadir_cliente(self):
        ventana = ctk.CTkToplevel(self)
        ventana.title("Añadir Cliente")
        ventana.geometry("400x300")

        ctk.CTkLabel(ventana, text="Nombre:").pack(pady=5)
        entry_nombre = ctk.CTkEntry(ventana)
        entry_nombre.pack(pady=5)

        ctk.CTkLabel(ventana, text="Dirección:").pack(pady=5)
        entry_direccion = ctk.CTkEntry(ventana)
        entry_direccion.pack(pady=5)

        ctk.CTkLabel(ventana, text="Teléfono:").pack(pady=5)
        entry_telefono = ctk.CTkEntry(ventana)
        entry_telefono.pack(pady=5)

        def guardar_cliente():
            conn = sqlite3.connect("clientes.db")
            cursor = conn.cursor()
            cursor.execute("SELECT COALESCE(MAX(cliente_id), 999) + 1 FROM clientes")
            nuevo_id = cursor.fetchone()[0]
            cursor.execute("INSERT INTO clientes (cliente_id, nombre, direccion, telefono) VALUES (?, ?, ?, ?)",
                           (nuevo_id, entry_nombre.get(), entry_direccion.get(), entry_telefono.get()))
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", f"Cliente añadido con ID {nuevo_id}")
            ventana.destroy()

        ctk.CTkButton(ventana, text="Guardar Cliente", command=guardar_cliente).pack(pady=10)

    def actualizar_pagos(self):
        ventana = ctk.CTkToplevel(self)
        ventana.title("Actualizar Pagos y Ver Perfil")
        ventana.geometry("600x500")  # Aumentado el tamaño para ajustarse al contenido

        ctk.CTkLabel(ventana, text="Buscar Cliente por ID o Nombre:").pack(pady=10)
        entry_busqueda = ctk.CTkEntry(ventana)
        entry_busqueda.pack(pady=5)

        def buscar_cliente():
            criterio = entry_busqueda.get()
            conn = sqlite3.connect("clientes.db")
            cursor = conn.cursor()
            cursor.execute("SELECT cliente_id, nombre FROM clientes WHERE cliente_id = ? OR nombre LIKE ?",
                           (criterio, f"%{criterio}%"))
            clientes = cursor.fetchall()
            conn.close()

            lista_clientes.configure(values=[f"{c[0]} - {c[1]}" for c in clientes])

        ctk.CTkButton(ventana, text="Buscar", command=buscar_cliente).pack(pady=5)

        ctk.CTkLabel(ventana, text="Seleccione Cliente:").pack(pady=10)
        lista_clientes = ctk.CTkComboBox(ventana, values=[], width=300)
        lista_clientes.set("")  # Aseguramos que esté vacío inicialmente
        lista_clientes.pack(pady=5)

        ctk.CTkLabel(ventana, text="Mes de Pago:").pack(pady=5)
        lista_meses = ctk.CTkComboBox(ventana,
                                      values=["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto",
                                              "Septiembre", "Octubre", "Noviembre", "Diciembre"], width=300)
        lista_meses.pack(pady=5)

        ctk.CTkLabel(ventana, text="Monto:").pack(pady=5)
        entry_monto = ctk.CTkEntry(ventana)
        entry_monto.pack(pady=5)

        ctk.CTkLabel(ventana, text="Descripción:").pack(pady=5)
        entry_descripcion = ctk.CTkEntry(ventana)
        entry_descripcion.pack(pady=5)

        def guardar_pago():
            cliente = lista_clientes.get().split(" - ")[0]
            conn = sqlite3.connect("clientes.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO pagos (cliente_id, mes, monto, descripcion) VALUES (?, ?, ?, ?)",
                           (cliente, lista_meses.get(), entry_monto.get(), entry_descripcion.get()))
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "Pago registrado correctamente")
            ventana.destroy()

        ctk.CTkButton(ventana, text="Guardar Pago", command=guardar_pago).pack(pady=10)

    def modificar_perfil(self):
        ventana = ctk.CTkToplevel(self)
        ventana.title("Modificar Perfil")
        ventana.geometry("600x500")

        ctk.CTkLabel(ventana, text="Buscar Cliente por ID o Nombre:").pack(pady=10)
        entry_busqueda = ctk.CTkEntry(ventana)
        entry_busqueda.pack(pady=5)

        def buscar_cliente():
            criterio = entry_busqueda.get()
            conn = sqlite3.connect("clientes.db")
            cursor = conn.cursor()
            cursor.execute("SELECT cliente_id, nombre FROM clientes WHERE cliente_id = ? OR nombre LIKE ?",
                           (criterio, f"%{criterio}%"))
            clientes = cursor.fetchall()
            conn.close()

            lista_clientes.configure(values=[f"{c[0]} - {c[1]}" for c in clientes])

        ctk.CTkButton(ventana, text="Buscar", command=buscar_cliente).pack(pady=5)

        ctk.CTkLabel(ventana, text="Seleccione Cliente:").pack(pady=10)
        lista_clientes = ctk.CTkComboBox(ventana, values=[], width=300)
        lista_clientes.set("")  # Aseguramos que esté vacío inicialmente
        lista_clientes.pack(pady=5)

        ctk.CTkLabel(ventana, text="Nombre:").pack(pady=5)
        entry_nombre = ctk.CTkEntry(ventana)
        entry_nombre.pack(pady=5)

        ctk.CTkLabel(ventana, text="Dirección:").pack(pady=5)
        entry_direccion = ctk.CTkEntry(ventana)
        entry_direccion.pack(pady=5)

        ctk.CTkLabel(ventana, text="Teléfono:").pack(pady=5)
        entry_telefono = ctk.CTkEntry(ventana)
        entry_telefono.pack(pady=5)

        def cargar_datos_cliente():
            cliente_seleccionado = lista_clientes.get()
            if cliente_seleccionado:
                cliente_id = cliente_seleccionado.split(" - ")[0]  # Obtener el ID del cliente
                conn = sqlite3.connect("clientes.db")
                cursor = conn.cursor()
                cursor.execute("SELECT nombre, direccion, telefono FROM clientes WHERE cliente_id = ?", (cliente_id,))
                cliente = cursor.fetchone()
                conn.close()

                if cliente:
                    # Cargar los datos del cliente en los campos de entrada
                    entry_nombre.delete(0, 'end')
                    entry_nombre.insert(0, cliente[0])
                    entry_direccion.delete(0, 'end')
                    entry_direccion.insert(0, cliente[1])
                    entry_telefono.delete(0, 'end')
                    entry_telefono.insert(0, cliente[2])
                else:
                    messagebox.showinfo("Cliente no encontrado", "No se encontraron resultados con ese ID.")
            else:
                messagebox.showinfo("Selección inválida", "Por favor, selecciona un cliente de la lista.")

        ctk.CTkButton(ventana, text="Cargar Datos", command=cargar_datos_cliente).pack(pady=5)

        def guardar_modificacion():
            cliente_seleccionado = lista_clientes.get()
            if cliente_seleccionado:
                cliente_id = cliente_seleccionado.split(" - ")[0]
                conn = sqlite3.connect("clientes.db")
                cursor = conn.cursor()
                cursor.execute("UPDATE clientes SET nombre=?, direccion=?, telefono=? WHERE cliente_id=?",
                               (entry_nombre.get(), entry_direccion.get(), entry_telefono.get(), cliente_id))
                conn.commit()
                conn.close()
                messagebox.showinfo("Éxito", "Perfil actualizado correctamente")
                ventana.destroy()

        ctk.CTkButton(ventana, text="Guardar Cambios", command=guardar_modificacion).pack(pady=10)

    def buscar_cliente_modificar(self, entry_busqueda, ventana):
        criterio = entry_busqueda.get()
        conn = sqlite3.connect("clientes.db")
        cursor = conn.cursor()
        cursor.execute("SELECT cliente_id, nombre FROM clientes WHERE cliente_id = ? OR nombre LIKE ?",
                       (criterio, f"%{criterio}%"))
        clientes = cursor.fetchall()
        conn.close()

        lista_clientes = ventana.winfo_children()[6]  # Obtener el ComboBox de clientes desde la ventana

        if clientes:
            # Actualizar el ComboBox con los clientes encontrados
            lista_clientes.set_values([f"{c[0]} - {c[1]}" for c in clientes])  # Esto solo se aplica a CTkComboBox
        else:
            messagebox.showinfo("No se encontraron resultados", "No se encontraron clientes con ese ID o nombre.")
            lista_clientes.set_values([])  # Limpiar la lista si no hay resultados

    def generar_reporte(self):
        ventana = ctk.CTkToplevel(self)
        ventana.title("Reporte Mensual")
        ventana.geometry("900x600")  # Tamaño ajustado para que todo quepa en la ventana
        ventana.config(bg="gray19")

        # Filtro de mes
        ctk.CTkLabel(ventana, text="Seleccione Mes:", font=("Arial", 14), text_color="white").pack(pady=(10, 5))
        lista_meses = ctk.CTkComboBox(ventana,
                                      values=["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto",
                                              "Septiembre", "Octubre", "Noviembre", "Diciembre"], width=300)
        lista_meses.pack(pady=(0, 10))

        # Filtro de estado
        ctk.CTkLabel(ventana, text="Seleccione Estado:", font=("Arial", 14), text_color="white").pack(pady=(10, 5))
        lista_estado = ctk.CTkComboBox(ventana, values=["Todos", "Pendiente", "Pagado"], width=300)
        lista_estado.pack(pady=(0, 10))

        def mostrar_reporte():
            mes_seleccionado = lista_meses.get()
            estado_seleccionado = lista_estado.get()
            conn = sqlite3.connect("clientes.db")
            cursor = conn.cursor()

            # Filtrado de los pagos según mes y estado
            if estado_seleccionado == "Todos":
                cursor.execute("""
                    SELECT c.cliente_id, c.nombre, COALESCE(p.monto, 0), 
                        CASE WHEN p.monto IS NULL THEN 'Pendiente' ELSE 'Pagado' END, p.descripcion
                    FROM clientes c
                    LEFT JOIN pagos p ON c.cliente_id = p.cliente_id AND p.mes = ?""", (mes_seleccionado,))
            else:
                cursor.execute("""
                    SELECT c.cliente_id, c.nombre, COALESCE(p.monto, 0), 
                        CASE WHEN p.monto IS NULL THEN 'Pendiente' ELSE 'Pagado' END, p.descripcion
                    FROM clientes c
                    LEFT JOIN pagos p ON c.cliente_id = p.cliente_id AND p.mes = ?
                    WHERE CASE WHEN p.monto IS NULL THEN 'Pendiente' ELSE 'Pagado' END = ?""",
                               (mes_seleccionado, estado_seleccionado))

            datos = cursor.fetchall()
            conn.close()

            # Limpiar el Treeview
            for row in tree.get_children():
                tree.delete(row)

            # Insertar los datos en el Treeview
            for dato in datos:
                item = tree.insert("", "end", values=dato)
                if dato[3] == "Pendiente":
                    tree.item(item, tags=("pendiente",))  # Etiqueta para color rojo claro
                else:
                    tree.item(item, tags=("pagado",))  # Etiqueta para color verde claro

            # Aplicar color a las filas
            tree.tag_configure("pendiente", background="#FFCCCC")  # Rojo claro
            tree.tag_configure("pagado", background="#CCFFCC")  # Verde claro

        # Crear el Treeview para mostrar los datos
        tree = ttk.Treeview(ventana, columns=("ID", "Nombre", "Pago", "Estado", "Descripción"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Nombre", text="Nombre")
        tree.heading("Pago", text="Pago")
        tree.heading("Estado", text="Estado")
        tree.heading("Descripción", text="Descripción")

        tree.pack(fill="both", expand=True)

        # Botón de generación del reporte
        ctk.CTkButton(ventana, text="Generar Reporte", command=mostrar_reporte).pack(pady=(5, 10))


if __name__ == "__main__":
    app = PagosApp()
    app.mainloop()