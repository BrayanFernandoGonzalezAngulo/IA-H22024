class Nodo {
    int valor;
    Nodo izquierdo;
    Nodo derecho;

    public Nodo(int valor) {
        this.valor = valor;
        izquierdo = null;
        derecho = null;
    }
}

class Arbol {
    Nodo raiz;

    public Arbol() {
        raiz = null;
    }

    public boolean estaVacio() {
        return raiz == null;
    }

    public void insertar(int valor) {
        raiz = insertarNodo(raiz, valor);
        System.out.println("Insertado el nodo " + valor);
    }

    private Nodo insertarNodo(Nodo nodo, int valor) {
        if (nodo == null) {
            nodo = new Nodo(valor);
            return nodo;
        }

        if (valor < nodo.valor) {
            nodo.izquierdo = insertarNodo(nodo.izquierdo, valor);
        } else if (valor > nodo.valor) {
            nodo.derecho = insertarNodo(nodo.derecho, valor);
        }

        return nodo;
    }

    public boolean buscarNodo(int valor) {
        return buscarNodo(raiz, valor);
    }

    private boolean buscarNodo(Nodo nodo, int valor) {
        if (nodo == null) {
            return false;
        }

        if (valor == nodo.valor) {
            return true;
        } else if (valor < nodo.valor) {
            return buscarNodo(nodo.izquierdo, valor);
        } else {
            return buscarNodo(nodo.derecho, valor);
        }
    }

    public void imprimirArbol() {
        imprimirArbol(raiz);
    }

    private void imprimirArbol(Nodo nodo) {
        if (nodo != null) {
            imprimirArbol(nodo.izquierdo);
            System.out.print(nodo.valor + " ");
            imprimirArbol(nodo.derecho);
        }
    }
}

public class Tarea1_Gonzalez_Brayan {
    public static void main(String[] args) {
        Arbol arbol = new Arbol();
        System.out.println("----------Metodo insertarNodo:----------");
        arbol.insertar(5);
        arbol.insertar(3);
        arbol.insertar(7);
        arbol.insertar(2);
        arbol.insertar(4);
        arbol.insertar(6);
        arbol.insertar(8);
        System.out.print("----------Metodo imprimirArbol:----------");
        System.out.print("\nEl arbol es: ");
        arbol.imprimirArbol();
        System.out.print("\n----------Metodo buscarNodo:----------");
        int valorbuscado = 4;
        boolean encontrado = arbol.buscarNodo(valorbuscado);
        System.out.println("\nEl nodo " + valorbuscado + " se encuentra en el arbol: " + encontrado);
        System.out.print("----------Metodo estaVacio:----------");
        boolean vacio = arbol.estaVacio();
        System.out.println("\nEl arbol está vacio: " + vacio);
        System.out.println("----------Fin de la ejecución----------");
        System.out.println("----------Autor: Brayan Fernando Gonzalez Angulo----------");
    }
}