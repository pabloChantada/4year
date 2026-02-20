# Tutorial de C++ - Desde Cero (para desarrolladores con experiencia)

## Introducción

C++ es un lenguaje compilado, de bajo nivel, con control total sobre la memoria. Si vienes de Julia, Java o C#, encontrarás diferencias significativas. Este tutorial se enfoca en lo que hace única a C++.

---

## 1. Características Fundamentales de C++

### 1.1 Compilado vs Interpretado
- **Java/C#**: Compilados a bytecode, ejecutados en máquina virtual (JVM/.NET)
- **Julia**: Compilado JIT (Just-In-Time) en tiempo de ejecución
- **C++**: Compilado directamente a código máquina nativo - **MÁS RÁPIDO**

```cpp
// C++ se compila a ejecutable directo
// g++ programa.cpp -o programa
// ./programa
```

### 1.2 Gestión Manual de Memoria
**LA MAYOR DIFERENCIA CON LOS LENGUAJES QUE CONOCES**

```cpp
// Java/C#: Garbage collection automático
// Java
String str = new String("hola");  // Se libera automáticamente

// C++: TÚ TIENES QUE LIBERAR LA MEMORIA
int* ptr = new int(42);  // Asignas memoria en el heap
delete ptr;               // DEBES liberarla tú mismo
ptr = nullptr;            // Buena práctica: establecer a nullptr
```

**Modernidad en C++**: Usa **smart pointers** para gestión automática:

```cpp
#include <memory>

std::unique_ptr<int> ptr(new int(42));  // Se libera automáticamente al salir del scope
// NO NECESITAS delete
```

### 1.3 Sin Recolector de Basura
- C++ **no tiene garbage collection**
- Si asignas memoria con `new`, **DEBES usar `delete`**
- Esto hace C++ MÁS RÁPIDO pero MENOS FORGIVABLE

---

## 2. Sintaxis Básica y Diferencias

### 2.1 Estructura de un Programa

```cpp
#include <iostream>      // Librería estándar (como import en Java)
#include <vector>        // Vectores dinámicos
#include <string>        // Strings

using namespace std;     // Usar el namespace std (std::cout → cout)

int main() {
    // Tu código aquí
    return 0;            // Retorna código de salida (0 = éxito)
}
```

### 2.2 Tipos de Datos

```cpp
// Tipos primitivos (IGUALES a lo que conoces)
int x = 42;              // Entero
float f = 3.14f;         // Flotante de 32 bits
double d = 3.14159;      // Flotante de 64 bits (DEFAULT)
bool b = true;           // Booleano
char c = 'A';            // Carácter único

// Strings (DIFERENTE a Java)
string str = "Hola";     // String (std::string es más fácil)
const char* cstr = "Hola";  // String de C antiguo (evita esto)

// Arrays
int arr[5] = {1, 2, 3, 4, 5};  // Array de tamaño FIJO (como en Julia)
arr[0] = 10;  // Acceso directo

// Vectores dinámicos (como listas en Java o arrays en Julia)
vector<int> vec;
vec.push_back(1);        // Agregar elemento
vec.push_back(2);
vec[0];                  // Acceso indexado
vec.size();              // Tamaño
```

### 2.3 Variables y Constantes

```cpp
// Variables normales
int x = 5;
x = 10;  // Puedes cambiar su valor

// Constantes
const int MAX = 100;     // No se puede cambiar
// MAX = 200;  // ERROR

// Variables estáticas (permanecen entre llamadas)
void contador() {
    static int count = 0;
    count++;
    cout << count << endl;  // Imprime 1, 2, 3... entre llamadas
}

// Variables globales
int global = 0;  // Accesible desde cualquier función
```

---

## 3. Funciones y Punteros

### 3.1 Funciones Básicas

```cpp
// Sintaxis: tipo_retorno nombre(parámetros) { cuerpo }

int suma(int a, int b) {
    return a + b;
}

void imprime(string mensaje) {
    cout << mensaje << endl;
}

// Función sin retorno
void saludar() {
    cout << "¡Hola!" << endl;
}

// Función sin parámetros
int obtenerNumero() {
    return 42;
}
```

### 3.2 Punteros (CONCEPTO CLAVE EN C++)

**Los punteros NO existen en Java/C#. Son referencias con aritmética.**

```cpp
int x = 5;
int* ptr = &x;   // & = dirección de x
                 // * = declara puntero

cout << *ptr;    // * dereferencia: imprime 5
cout << ptr;     // Imprime la dirección: 0x7fff5fbff8ac

// Aritmética de punteros (PODEROSA pero PELIGROSA)
int arr[3] = {10, 20, 30};
int* p = arr;     // p apunta al primer elemento
cout << *p;       // 10
p++;              // Avanza al siguiente
cout << *p;       // 20
```

### 3.3 Referencias (Versión "Segura" de Punteros)

```cpp
int x = 5;
int& ref = x;    // & crea una referencia

ref = 10;        // Modifica x
cout << x;       // 10

// Las referencias SIEMPRE apuntan a algo válido (no pueden ser nullptr)
// Los punteros SÍ pueden ser nullptr
```

### 3.4 Pasar Argumentos

```cpp
// Por valor (copia)
void cambiar_valor(int x) {
    x = 100;  // Cambia la copia, no el original
}

int a = 5;
cambiar_valor(a);
cout << a;  // Sigue siendo 5

// Por referencia (modifica el original)
void cambiar_referencia(int& x) {
    x = 100;  // Cambia el original
}

cambiar_referencia(a);
cout << a;  // Ahora es 100

// Por puntero (similar a referencia)
void cambiar_puntero(int* x) {
    *x = 100;
}

cambiar_puntero(&a);
cout << a;  // Ahora es 100
```

---

## 4. Clases y Programación Orientada a Objetos

### 4.1 Declaración de Clases

```cpp
class Persona {
private:           // Solo accesible dentro de la clase
    string nombre;
    int edad;

public:            // Accesible desde cualquier lugar
    // Constructor
    Persona(string n, int e) : nombre(n), edad(e) {}
    
    // Métodos
    void saludar() {
        cout << "Hola, soy " << nombre << endl;
    }
    
    // Getters y setters
    string getNombre() const {  // const = no modifica el objeto
        return nombre;
    }
    
    void setEdad(int e) {
        edad = e;
    }
};

// Uso
Persona p("Juan", 30);
p.saludar();
cout << p.getNombre();
```

### 4.2 Herencia

```cpp
class Animal {
public:
    virtual void hablar() {  // virtual = puede ser sobrescrito
        cout << "Sonido genérico" << endl;
    }
};

class Perro : public Animal {
public:
    void hablar() override {  // override = sobrescribe el método
        cout << "¡Guau!" << endl;
    }
};

// Polimorfismo
Animal* animal = new Perro();
animal->hablar();  // Imprime "¡Guau!"
delete animal;
```

### 4.3 Diferencias con Java/C#

```
C++:
- Sin recolector de basura
- No todo debe ser una clase
- Herencia múltiple permitida (¡Cuidado!)
- Métodos virtuales (overhead de rendimiento)

Java:
- Todo es una clase
- Una sola herencia
- Polimorfismo automático

C#:
- Similar a Java
- Propiedades automáticas
- LINQ para consultas
```

---

## 5. Contenedores STL (Standard Template Library)

### 5.1 Vector (Lista Dinámica)

```cpp
#include <vector>

vector<int> v;
v.push_back(1);
v.push_back(2);
v.push_back(3);

cout << v[0];      // 1
cout << v.size();  // 3

// Iteración
for (int x : v) {  // for-each (C++11)
    cout << x << " ";
}

// Iteradores
for (auto it = v.begin(); it != v.end(); ++it) {
    cout << *it << " ";
}
```

### 5.2 Map (Diccionario)

```cpp
#include <map>

map<string, int> edades;
edades["Juan"] = 30;
edades["María"] = 25;

cout << edades["Juan"];  // 30

// Iterar
for (auto& [nombre, edad] : edades) {  // C++17 structured binding
    cout << nombre << ": " << edad << endl;
}
```

### 5.3 Set (Conjunto)

```cpp
#include <set>

set<int> numeros;
numeros.insert(1);
numeros.insert(2);
numeros.insert(1);  // No se duplica

cout << numeros.size();  // 2

// Búsqueda
if (numeros.find(1) != numeros.end()) {
    cout << "Encontrado";
}
```

---

## 6. Manejo de Errores

### 6.1 Excepciones (Como en Java)

```cpp
#include <stdexcept>

try {
    if (x < 0) {
        throw invalid_argument("x no puede ser negativo");
    }
} catch (invalid_argument& e) {
    cout << "Error: " << e.what() << endl;
} catch (exception& e) {
    cout << "Error general" << endl;
}
```

### 6.2 Códigos de Error (Estilo C)

```cpp
int dividir(int a, int b) {
    if (b == 0) {
        return -1;  // Código de error
    }
    return a / b;
}

int resultado = dividir(10, 0);
if (resultado == -1) {
    cout << "Error en división" << endl;
}
```

---

## 7. Peculiaridades de C++ (Lo que NO esperarías)

### 7.1 Headers y Compilación

```cpp
// En un archivo "math.h"
int suma(int a, int b);  // Declaración

// En un archivo "math.cpp"
int suma(int a, int b) {
    return a + b;
}

// En "main.cpp"
#include "math.h"
int main() {
    suma(1, 2);  // Funciona
}

// COMPILACIÓN: g++ main.cpp math.cpp -o programa
```

### 7.2 Headers Guards (Evita inclusiones múltiples)

```cpp
// En "math.h"
#ifndef MATH_H
#define MATH_H

int suma(int a, int b);

#endif
```

O modernamente:

```cpp
#pragma once  // Más simple (funciona en casi todos lados)
int suma(int a, int b);
```

### 7.3 Templates (Genéricos, como en Java)

```cpp
template <typename T>
T maximo(T a, T b) {
    return (a > b) ? a : b;
}

cout << maximo(5, 10);         // 10
cout << maximo(3.14, 2.71);    // 3.14
cout << maximo("b", "a");      // "b"
```

### 7.4 Sobrecarga de Operadores

```cpp
class Vector {
    int x, y;
public:
    Vector operator+(const Vector& otro) {
        return Vector(x + otro.x, y + otro.y);
    }
};

Vector v1(1, 2);
Vector v2(3, 4);
Vector v3 = v1 + v2;  // Usa operator+
```

---

## 8. Optimizaciones de Rendimiento

```cpp
// Copia innecesaria (LENTA)
void procesar(string texto) {
    // Se hace una copia completa de texto
}

// Referencia (RÁPIDO)
void procesar(const string& texto) {
    // Sin copia, solo lectura
}

// Move semantics (C++11, MUY RÁPIDO)
void procesar(string&& texto) {
    // Se transfiere la memoria, no se copia
}
```

---

## 9. Estándares de C++

```
C++98:  Primera versión estable
C++11:  ENORME actualización (auto, lambdas, smart pointers)
C++14:  Mejoras menores
C++17:  Más mejoras (structured bindings)
C++20:  Conceptos, corrutinas
C++23:  Lo último (2023)
```

**Recomendación**: Usa **C++17** o **C++20** para proyectos nuevos.

---

## 10. Flujo de Desarrollo en C++

```
1. Escribir código (.cpp, .h)
2. Compilar: g++ main.cpp -o programa
3. Ejecutar: ./programa

// Esto es diferente a:
// Java: javac, luego java
// C#: Compilado automático en VS
// Julia: Interpretado o JIT
```

---

## 11. Comparación Rápida

| Característica | C++ | Java | C# | Julia |
|---|---|---|---|---|
| Compilado | ✓ (nativo) | ✗ (bytecode) | ✗ (IL) | ✓ (JIT) |
| Garbage Collection | ✗ | ✓ | ✓ | ✓ |
| Punteros | ✓ | ✗ | ✗ | ✗ |
| Velocidad | ★★★★★ | ★★★★ | ★★★★ | ★★★★ |
| Facilidad | ★★ | ★★★★ | ★★★★ | ★★★★ |
| Memoria | Manual | Automática | Automática | Automática |

---

## 12. Buenas Prácticas

```cpp
// ✓ USA smart pointers
std::unique_ptr<int> ptr(new int(5));

// ✗ NO uses pointers tradicionales
int* ptr = new int(5);
delete ptr;

// ✓ USA referencias cuando sea posible
void procesar(const std::string& s) { }

// ✓ USA const correctamente
const int MAX = 100;
void metodo() const { }  // No modifica el objeto

// ✓ SIEMPRE inicializa variables
int x = 0;

// ✗ NO variables sin inicializar
int x;  // Basura en memoria

// ✓ USA nombres descriptivos
int usuario_edad = 30;

// ✗ NO nombres cortos en código profesional
int ua = 30;
```

---

## 13. Compilación y Ejecución Rápida

```bash
# Compilar
g++ -std=c++17 -O2 programa.cpp -o programa

# -std=c++17: Usa estándar C++17
# -O2: Optimización nivel 2
# -g: Incluir símbolos de debug (para gdb)

# Ejecutar
./programa

# Con argumentos
./programa arg1 arg2
```

---

## Recursos Finales

1. **cppreference.com**: Documentación completa
2. **isocpp.org**: Comunidad y estándares
3. **GoingNative**: Conferencias sobre C++
4. **Stroustrup's Book**: "The C++ Programming Language" (el creador de C++)

---

## Próximos Pasos

1. Escribe un programa que lea/escriba archivos
2. Aprende sobre threads (concurrencia)
3. Domina los templates y genéricos
4. Estudia move semantics y perfect forwarding
5. Explora bibliotecas como Boost, nlohmann/json, etc.

¡Bienvenido a C++! 🚀
