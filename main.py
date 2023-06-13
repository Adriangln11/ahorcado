import random

# Lista de palabras para el juego
words = ['javascript', 'backend', 'github', 'python', 'web', 'codigo']

# Función para seleccionar una palabra al azar
def select_word():
    return random.choice(words)

# Función para mostrar el tablero del juego
def show_letter(hide_word, rounds):
    print("Palabra: ", end="")
    for letra in hide_word:
        print(letra, end=" ")
    print("\nIntentos restantes: ", rounds)

# Función para actualizar la palabra oculta con las letras adivinadas
def update_hide_word(word, hide_word, letter):
    new_hide_word = ""
    for i in range(len(word)):
        if word[i] == letter:
            new_hide_word += letter
        else:
            new_hide_word += hide_word[i]
    return new_hide_word

# Función principal del juego
def main():
    word = select_word()
    hide_word = "_" * len(word)
    rounds = 6
    correct_letters = []

    print("Bienvenido al juego del ahorcado!")

    while True:
        show_letter(hide_word, rounds)

        # Pedir al jugador que ingrese una letra
        letter = input("Ingrese una letra: ").lower()

        if letter.isalpha() and len(letter) == 1:
            if letter in correct_letters:
                print("Ya has adivinado esa letra. Intenta con otra.")
                continue
            elif letter in word:
                correct_letters.append(letter)
                hide_word = update_hide_word(word, hide_word, letter)
                if "_" not in hide_word:
                    print("¡Felicidades! Has adivinado la palabra:", word)
                    break
            else:
                rounds -= 1
                print("La letra no está en la palabra. Intentos restantes:", rounds)
                if rounds == 0:
                    print("¡Oh no! Te has quedado sin intentos. La palabra era:", word)
                    break
        else:
            print("Por favor, ingresa una sola letra.")

# Iniciar el juego
main()
