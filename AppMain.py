from Producto import Producto
from Inventario import Inventario
from Carrito import Carrito
from Factura import Factura
from GestorFacturas import GestorFacturas

class AppMain:
    def __init__(self):
        self.inventario = Inventario()
        self.inventario.addProducto(Producto("Collar de perlas", 10.0, "unidad"))
        self.inventario.addProducto(Producto("Hilo de nylon", 2.0, "metro"))

        self.carrito = Carrito()
        self.gestor_facturas = GestorFacturas()
        self.numero_factura = 1

    def mostrar_menu(self):
        print("\n--- MENÚ PRINCIPAL ---")
        print("1. Listar productos")
        print("2. Agregar producto al carrito")
        print("3. Mostrar carrito")
        print("4. Generar factura")
        print("5. Listar facturas")
        print("6. Salir")

    def ejecutar(self):
        while True:
            self.mostrar_menu()
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                self.inventario.listProductos()

            elif opcion == "2":
                self.inventario.listProductos()
                indice = int(input("Ingrese el número del producto: "))
                cantidad = int(input("Ingrese la cantidad/metros: "))
                producto = self.inventario.productos[indice - 1]
                self.carrito.addChart(producto, cantidad)

            elif opcion == "3":
                self.carrito.mostrar_carrito()

            elif opcion == "4":
                factura = self.gestor_facturas.addFactura(self.numero_factura, self.carrito)
                factura.mostrar_factura()
                self.numero_factura += 1
                self.carrito.vaciar_carrito()

            elif opcion == "5":
                self.gestor_facturas.showFacturas()

            elif opcion == "6":
                print("Saliendo de la aplicación...")
                break

            else:
                print("Opción inválida, intente de nuevo.")

if __name__ == "__main__":
    app = AppMain()
    app.ejecutar()