import random
import http.server
import socketserver

words = ['javascript', 'backend', 'github', 'python', 'web', 'codigo']

def select_word():
    return random.choice(words)

def update_hide_word(word, hide_word, letter):
    new_hide_word = ""
    for i in range(len(word)):
        if word[i] == letter:
            new_hide_word += letter
        else:
            new_hide_word += hide_word[i]
    return new_hide_word
class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    word = select_word()
    hide_word = " _ " * len(word)
    rounds = 6
    correct_letters = []

    def do_GET(self):
        if self.path == '/':
            contenido = f"""
            <h1>Bienvenido al juego del ahorcado!</h1>
            <p>Palabra: {self.hide_word}</p>
            <p>Intentos restantes: {self.rounds}</p>
            <form method="POST" action="/guess">
                <input type="text" name="letter" maxlength="1" required>
                <input type="submit" value="Adivinar">
            </form>
            """
            with open('index.html') as file:
                template = file.read()
                response = template.replace('{{ contenido }}', contenido)

            # Envía la respuesta al cliente
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(response, 'utf-8'))
        else:

            self.send_error(404, 'Archivo no encontrado: %s' % self.path)

    def do_POST(self):
        if self.path == '/guess':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            letter = post_data.split('=')[1]

            if letter.isalpha() and len(letter) == 1:
                if letter in self.correct_letters:
                    message = "Ya has adivinado esa letra. Intenta con otra."
                elif letter in self.word:
                    self.correct_letters.append(letter)
                    self.hide_word = update_hide_word(self.word, self.hide_word, letter)
                    if "_" not in self.hide_word:
                        message = f"¡Felicidades! Has adivinado la palabra: {self.word}"
                    else:
                        message = "Letra correcta. Sigue intentando."
                else:
                    self.rounds -= 1
                    message = f"La letra no está en la palabra. Intentos restantes: {self.rounds}"
                    if self.rounds == 0:
                        message = f"¡Oh no! Te has quedado sin intentos. La palabra era: {self.word}"
            else:
                message = "Por favor, ingresa una sola letra."

            contenido = f"""
            <h1>Bienvenido al juego del ahorcado!</h1>
            <p>Palabra: {self.hide_word}</p>
            <p>Intentos restantes: {self.rounds}</p>
            <p>{message}</p>
            <form method="POST" action="/guess">
                <input type="text" name="letter" maxlength="1" required>
                <input type="submit" value="Adivinar">
            </form>
            """

            with open('index.html') as file:
                template = file.read()
                response = template.replace('{{ contenido }}', contenido)

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(response, 'utf-8'))


def run(server_class=socketserver.TCPServer, handler_class=MyRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Servidor en ejecución en el puerto', port)
    httpd.serve_forever()

if __name__ == '__main__':
    run()
