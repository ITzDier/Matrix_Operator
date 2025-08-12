import numpy as np
import sympy as sp

class Matriz:
    def __init__(self, filas=None, columnas=None):
        self.matriz = None
        if filas is not None and columnas is not None:
            self._pedir_informacion(filas, columnas)
        else:
            self._pedir_dimensiones_al_usuario()

    def _pedir_dimensiones_al_usuario(self):
        """Pide al usuario las dimensiones de la matriz."""
        while True:
            try:
                filas = int(input("Ingrese el número de filas de la matriz: "))
                columnas = int(input("Ingrese el número de columnas de la matriz: "))
                if filas <= 0 or columnas <= 0:
                    raise ValueError
                break
            except ValueError:
                print("Error: Ingrese números enteros positivos para las dimensiones.")
        self._pedir_informacion(filas, columnas)

    def _pedir_informacion(self, filas, columnas):
        """Pide al usuario las entradas de la matriz."""
        self.filas = filas
        self.columnas = columnas
        print(f"\nIngrese los {filas * columnas} elementos de la matriz ({filas}x{columnas}):")
        print("Favor de ingresar los elementos uno por uno y si es un conjunto de numeros verificarlo solo como una unidad.")
        temp_matriz = []
        for i in range(filas):
            fila_actual = []
            for j in range(columnas):
                while True:
                    entrada = input(f"Elemento [{i+1}][{j+1}]: ")
                    # Intentar convertir a número si es posible
                    try:
                        fila_actual.append(float(entrada))
                        break
                    except ValueError:
                        # Si no es un número, se trata como cadena
                        fila_actual.append(entrada)
                        break
            temp_matriz.append(fila_actual)
        # Convertir a array de NumPy para optimizar operaciones,
        # pero con dtype=object para permitir tipos mixtos.
        self.matriz = np.array(temp_matriz, dtype=object)
        try:
            self.matriz = self.matriz.astype(float)
        except ValueError:
            # Si falla, se queda como object (mezcla de tipos)
            pass
        print("Matriz creada exitosamente.")

    def visualizar(self, nombre="Matriz"):
        """Visualiza la matriz de manera clara."""
        print(f"\n--- {nombre} ({self.filas}x{self.columnas}) ---")
        for fila in self.matriz:
            print("[", end="")
            for i, elemento in enumerate(fila):
                print(f"{elemento:<8}", end="") # Formato para alinear
                if i < len(fila) - 1:
                    print(", ", end="")
            print("]")
        print("--------------------")

    # --- Operaciones entre matrices ---

    def sumar(self, otra_matriz):
        """Suma esta matriz con otra matriz."""
        print(f"\n--- Suma de Matrices ---")
        self.visualizar("Matriz 1")
        otra_matriz.visualizar("Matriz 2")

        if self.shape() != otra_matriz.shape():
            print("Error: Las matrices deben tener las mismas dimensiones para sumarse.")
            return None
        
        # Verificar si todas las entradas son numéricas
        if not (np.issubdtype(self.matriz.dtype, np.number) and np.issubdtype(otra_matriz.matriz.dtype, np.number)):
            # Intenta sumar como objetos, si no, reporta error
            try:
                resultado_matriz = self.matriz + otra_matriz.matriz
                resultado_obj = Matriz(self.filas, self.columnas) # Crear un objeto Matriz para el resultado
                resultado_obj.matriz = resultado_matriz
                print("\nResultado de la Suma:")
                resultado_obj.visualizar("Resultado")
                return resultado_obj
            except TypeError:
                print("Error: No se pueden sumar matrices con entradas no numéricas de manera hetéerognea.")
                return None
        else:
            resultado_matriz = self.matriz + otra_matriz.matriz
            resultado_obj = Matriz(self.filas, self.columnas)
            resultado_obj.matriz = resultado_matriz
            print("\nResultado de la Suma:")
            resultado_obj.visualizar("Resultado")
            return resultado_obj

    def restar(self, otra_matriz):
        """Resta otra matriz a esta matriz."""
        print(f"\n--- Resta de Matrices ---")
        self.visualizar("Matriz 1")
        otra_matriz.visualizar("Matriz 2")

        if self.shape() != otra_matriz.shape():
            print("Error: Las matrices deben tener las mismas dimensiones para restarse.")
            return None

        # Verificar si todas las entradas son numéricas
        if not (np.issubdtype(self.matriz.dtype, np.number) and np.issubdtype(otra_matriz.matriz.dtype, np.number)):
            print("Error: No se pueden restar matrices con entradas no numéricas.")
            return None
        else:
            resultado_matriz = self.matriz - otra_matriz.matriz
            resultado_obj = Matriz(self.filas, self.columnas)
            resultado_obj.matriz = resultado_matriz
            print("\nResultado de la Resta:")
            resultado_obj.visualizar("Resultado")
            return resultado_obj

    def multiplicar_por_escalar(self, escalar):
        """Multiplica la matriz por un escalar."""
        print(f"\n--- Multiplicación por Escalar (Escalar: {escalar}) ---")
        self.visualizar("Matriz Original")

        # Verificar si todas las entradas son numéricas si el escalar es numérico
        if isinstance(escalar, (int, float)) and not np.issubdtype(self.matriz.dtype, np.number):
            print("Error: No se puede multiplicar una matriz con entradas no numéricas por un escalar numérico.")
            return None
        
        # Intenta multiplicar elemento a elemento, si son cadenas, intentará concatenar
        try:
            resultado_matriz = self.matriz * escalar
            resultado_obj = Matriz(self.filas, self.columnas)
            resultado_obj.matriz = resultado_matriz
            print("\nResultado de la Multiplicación por Escalar:")
            resultado_obj.visualizar("Resultado")
            return resultado_obj
        except TypeError:
            print("Error: La operación de multiplicación por escalar no es compatible con los tipos de datos de la matriz y el escalar.")
            return None

    def multiplicar_matrices(self, otra_matriz):
        """Multiplica esta matriz por otra matriz (producto matricial)."""
        print(f"\n--- Multiplicación Matricial ---")
        self.visualizar("Matriz 1")
        otra_matriz.visualizar("Matriz 2")

        if self.columnas != otra_matriz.filas:
            print("Error: Para la multiplicación de matrices, el número de columnas de la primera matriz debe ser igual al número de filas de la segunda.")
            return None
        
        # Las entradas deben ser numéricas para el producto matricial
        if not (np.issubdtype(self.matriz.dtype, np.number) and np.issubdtype(otra_matriz.matriz.dtype, np.number)):
            print("Error: Las matrices deben contener solo entradas numéricas para realizar la multiplicación matricial.")
            return None

        resultado_matriz = self.matriz * otra_matriz.matriz # Se realiza la multiplicación matricial
        
        resultado_obj = Matriz(self.filas, otra_matriz.columnas)
        resultado_obj.matriz = resultado_matriz
        print("\nResultado de la Multiplicación Matricial:")
        resultado_obj.visualizar("Resultado")
        return resultado_obj

    # --- Operaciones Elementales ---

    def transponer(self):
        """Calcula la transpuesta de la matriz."""
        print(f"\n--- Transponer Matriz ---")
        self.visualizar("Matriz Original")

        resultado_matriz = self.matriz.T
        resultado_obj = Matriz(self.columnas, self.filas) # Filas y columnas se invierten
        resultado_obj.matriz = resultado_matriz
        print("\nMatriz Transpuesta:")
        resultado_obj.visualizar("Resultado")
        return resultado_obj

    def invertir(self):
        """Calcula la inversa de la matriz."""
        print(f"\n--- Inversa de la Matriz ---")
        self.visualizar("Matriz Original")

        if self.filas != self.columnas:
            print("Error: Solo las matrices cuadradas pueden tener inversa.")
            return None
        
        # Las entradas deben ser numéricas para la inversa
        if not np.issubdtype(self.matriz.dtype, np.number):
            print("Error: La matriz debe contener solo entradas numéricas para calcular la inversa.")
            return None

        try:
            resultado_matriz = np.linalg.inv(self.matriz.astype(float)) # Asegura tipo flotante para la inversa
            resultado_obj = Matriz(self.filas, self.columnas)
            resultado_obj.matriz = resultado_matriz
            print("\nMatriz Inversa:")
            resultado_obj.visualizar("Resultado")
            return resultado_obj
        except np.linalg.LinAlgError:
            print("Error: La matriz es singular (su determinante es cero) y no tiene inversa.")
            return None
        except ValueError as e:
            print(f"Error al calcular la inversa: {e}. Asegúrese de que todos los elementos sean convertibles a números.")
            return None

    def determinante(self, metodo="numpy"):
        """Calcula el determinante de la matriz si es cuadrada.
        metodo: 'numpy' (por defecto), 'cramer' (expansión por cofactores), o 'gauss-jordan'.
        """
        print(f"\n--- Determinante de la Matriz ---")
        self.visualizar("Matriz Original")
        if self.filas != self.columnas:
            print("Error: Solo las matrices cuadradas tienen determinante.")
            return None
        # Las entradas deben ser numéricas para el determinante
        if not np.issubdtype(self.matriz.dtype, np.number):
            print("Error: La matriz debe contener solo entradas numéricas para calcular el determinante.")
            return None

        def determinante_cramer(mat):
            n = mat.shape[0]
            if n == 1:
                return mat[0, 0]
            if n == 2:
                return mat[0, 0]*mat[1, 1] - mat[0, 1]*mat[1, 0]
            det = 0
            for j in range(n):
                submat = np.delete(np.delete(mat, 0, axis=0), j, axis=1)
                det += ((-1) ** j) * mat[0, j] * determinante_cramer(submat)
            return det

        def determinante_gauss_jordan(mat):
            mat = mat.astype(float).copy()
            n = mat.shape[0]
            det = 1
            for i in range(n):
                # Buscar el máximo en la columna i para evitar división por cero
                max_row = i + np.argmax(np.abs(mat[i:, i]))
                if mat[max_row, i] == 0:
                    return 0
                if max_row != i:
                    mat[[i, max_row]] = mat[[max_row, i]]
                    det *= -1  # Cambio de signo por intercambio de filas
                det *= mat[i, i]
                mat[i] = mat[i] / mat[i, i]
                for j in range(i+1, n):
                    mat[j] = mat[j] - mat[j, i] * mat[i]
            return det

        try:
            if metodo == "cramer":
                det = determinante_cramer(self.matriz.astype(float))
                print(f"Determinante (Cramer): {det}")
            elif metodo == "gauss-jordan":
                det = determinante_gauss_jordan(self.matriz.astype(float))
                print(f"Determinante (Gauss-Jordan): {det}")
            else:
                det = np.linalg.det(self.matriz.astype(float))
                print(f"Determinante (NumPy): {det}")
            return det
        except Exception as e:
            print(f"Error al calcular el determinante: {e}")
            return None

    def shape(self):
        """Devuelve las dimensiones de la matriz."""
        return (self.filas, self.columnas)

    def identificar_tipo_triangulo(self):
        """Determina si la matriz es triangular superior, triangular inferior, diagonal o ninguna.
        Si no es cuadrada, informa si es rectangular o cuadrada.
        """
        if self.filas != self.columnas:
            if self.filas == 1 or self.columnas == 1:
                print("La matriz es rectangular (vector fila o columna).")
                return "rectangular"
            else:
                print("La matriz es rectangular.")
                return "rectangular"
        es_superior = True
        es_inferior = True
        es_diagonal = True
        for i in range(self.filas):
            for j in range(self.columnas):
                if i > j and self.matriz[i, j] != 0:
                    es_superior = False
                if i < j and self.matriz[i, j] != 0:
                    es_inferior = False
                if i != j and self.matriz[i, j] != 0:
                    es_diagonal = False
        if es_diagonal:
            print("La matriz es diagonal (y cuadrada).")
            return "diagonal"
        elif es_superior:
            print("La matriz es triangular superior (y cuadrada).")
            return "triangular superior"
        elif es_inferior:
            print("La matriz es triangular inferior (y cuadrada).")
            return "triangular inferior"
        else:
            print("La matriz es cuadrada pero no es triangular ni diagonal.")
            return "cuadrada"
    def traspuesta(self):
        """Devuelve la matriz traspuesta (sin imprimir ni crear objeto nuevo)."""
        return self.matriz.T

class InterpoladorPolinomial:
    def __init__(self):
        self.x = []
        self.y = []
        self.polinomio = None
        self._pedir_datos()
        self._interpolar()

    def _pedir_datos(self):
        print("\n--- Interpolación Polinomial (Lagrange) ---")
        while True:
            try:
                n = int(input("¿Cuántos puntos de datos desea ingresar? (mínimo 2): "))
                if n < 2:
                    raise ValueError
                break
            except ValueError:
                print("Ingrese un número entero mayor o igual a 2.")
        for i in range(n):
            while True:
                try:
                    x_i = float(input(f"Ingrese x[{i+1}]: "))
                    y_i = float(input(f"Ingrese y[{i+1}]: "))
                    self.x.append(x_i)
                    self.y.append(y_i)
                    break
                except ValueError:
                    print("Ingrese valores numéricos válidos.")

    def _interpolar(self):
        x_sym = sp.Symbol('x')
        n = len(self.x)
        polinomio = 0
        for i in range(n):
            termino = 1
            for j in range(n):
                if i != j:
                    termino *= (x_sym - self.x[j]) / (self.x[i] - self.x[j])
            polinomio += self.y[i] * termino
        self.polinomio = sp.simplify(polinomio)
        print("\nPolinomio interpolador de Lagrange:")
        print(self.polinomio)

    def evaluar(self, valor):
        x_sym = sp.Symbol('x')
        resultado = self.polinomio.subs(x_sym, valor)
        resultado_eval = sp.N(resultado)
        # Si el resultado es real, devuelve float; si es complejo, lo muestra como tal
        if resultado_eval.is_real:
            return float(resultado_eval)
        else:
            return resultado_eval

# --- Modifica el menú y el main ---

def menu():
    print("\n--- MENÚ DE OPERACIONES CON MATRICES ---")
    print("1. Crear matriz")
    print("2. Visualizar matriz")
    print("3. Sumar dos matrices")
    print("4. Restar dos matrices")
    print("5. Multiplicar matriz por escalar")
    print("6. Multiplicar dos matrices")
    print("7. Transponer matriz")
    print("8. Invertir matriz")
    print("9. Identificar tipo de matriz")
    print("10. Calcular determinante")
    print("11. Interpolación polinomial (Lagrange)")
    print("12. Borrar matriz")
    print("13. Salir")

def seleccionar_matriz(matrices):
    if not matrices:
        print("No hay matrices creadas.")
        return None
    print("\nMatrices disponibles:")
    for idx, m in enumerate(matrices):
        print(f"{idx+1}. Matriz ({m.filas}x{m.columnas})")
    while True:
        try:
            seleccion = int(input("Seleccione el número de la matriz: "))
            if 1 <= seleccion <= len(matrices):
                return matrices[seleccion-1]
            else:
                print("Selección inválida.")
        except ValueError:
            print("Ingrese un número válido.")

def borrar_matriz(matrices):
    if not matrices:
        print("No hay matrices para borrar.")
        return
    print("\nMatrices disponibles para borrar:")
    for idx, m in enumerate(matrices):
        print(f"{idx+1}. Matriz ({m.filas}x{m.columnas})")
    while True:
        try:
            seleccion = int(input("Seleccione el número de la matriz a borrar: "))
            if 1 <= seleccion <= len(matrices):
                matrices.pop(seleccion-1)
                print("Matriz borrada exitosamente.")
                break
            else:
                print("Selección inválida.")
        except ValueError:
            print("Ingrese un número válido.")

def main():
    matrices = []
    interpoladores = []
    while True:
        menu()
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            matriz = Matriz()
            matrices.append(matriz)
        elif opcion == "2":
            matriz = seleccionar_matriz(matrices)
            if matriz:
                matriz.visualizar()
        elif opcion == "3":
            print("Seleccione la primera matriz:")
            m1 = seleccionar_matriz(matrices)
            print("Seleccione la segunda matriz:")
            m2 = seleccionar_matriz(matrices)
            if m1 and m2:
                resultado = m1.sumar(m2)
                if resultado:
                    matrices.append(resultado)
        elif opcion == "4":
            print("Seleccione la primera matriz:")
            m1 = seleccionar_matriz(matrices)
            print("Seleccione la segunda matriz:")
            m2 = seleccionar_matriz(matrices)
            if m1 and m2:
                resultado = m1.restar(m2)
                if resultado:
                    matrices.append(resultado)
        elif opcion == "5":
            matriz = seleccionar_matriz(matrices)
            if matriz:
                escalar = input("Ingrese el escalar: ")
                try:
                    escalar = float(escalar)
                except ValueError:
                    pass
                resultado = matriz.multiplicar_por_escalar(escalar)
                if resultado:
                    matrices.append(resultado)
        elif opcion == "6":
            print("Seleccione la primera matriz:")
            m1 = seleccionar_matriz(matrices)
            print("Seleccione la segunda matriz:")
            m2 = seleccionar_matriz(matrices)
            if m1 and m2:
                resultado = m1.multiplicar_matrices(m2)
                if resultado:
                    matrices.append(resultado)
        elif opcion == "7":
            matriz = seleccionar_matriz(matrices)
            if matriz:
                resultado = matriz.transponer()
                if resultado:
                    matrices.append(resultado)
        elif opcion == "8":
            matriz = seleccionar_matriz(matrices)
            if matriz:
                resultado = matriz.invertir()
                if resultado:
                    matrices.append(resultado)
        elif opcion == "9":
            matriz = seleccionar_matriz(matrices)
            if matriz:
                matriz.visualizar()
                tipo = matriz.identificar_tipo_triangulo()
                print(f"Tipo de matriz: {tipo}")
        elif opcion == "10":
            matriz = seleccionar_matriz(matrices)
            if matriz:
                print("¿Qué método desea usar para calcular el determinante?")
                print("1. NumPy (rápido y recomendado para matrices grandes)")
                print("2. Cramer (expansión por cofactores, educativo, lento para matrices grandes)")
                print("3. Gauss-Jordan (eliminación, eficiente y educativo)")
                metodo_opcion = input("Seleccione el método (1, 2 o 3): ")
                if metodo_opcion == "2":
                    matriz.determinante(metodo="cramer")
                elif metodo_opcion == "3":
                    matriz.determinante(metodo="gauss-jordan")
                else:
                    matriz.determinante(metodo="numpy")
        elif opcion == "11":
            interpolador = InterpoladorPolinomial()
            interpoladores.append(interpolador)
            while True:
                evalua = input("¿Desea evaluar el polinomio en algún valor de x? (s/n): ").lower()
                if evalua == "s":
                    try:
                        valor = float(input("Ingrese el valor de x: "))
                        resultado = interpolador.evaluar(valor)
                        print(f"P({valor}) = {resultado}")
                    except Exception as e:
                        print(f"Error al evaluar: {e}")
                else:
                    print("Regresando al menú principal...")
                    break
        elif opcion == "12":
            borrar_matriz(matrices)
        elif opcion == "13":
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida. Intente de nuevo.")

if __name__ == "__main__":
    main()