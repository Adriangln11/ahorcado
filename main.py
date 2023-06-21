import http.server
import socketserver
import random

words = ['javascript', 'backend', 'github', 'python', 'web', 'codigo']

def select_word():
    return random.choice(words)

def show_letter(hide_word, rounds):
    content = f"<p>Palabra: {hide_word}</p>"
    content += f"<p>Intentos restantes: {rounds}</p>"
    return content

def update_hide_word(word, hide_word, letter):
    new_hide_word = ""
    for i in range(len(word)):
        if word[i] == letter:
            new_hide_word += letter
        else:
            new_hide_word += hide_word[i]
    return new_hide_word

class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

    def do_GET(self):
        if self.path == '/':
            word = select_word()
            hide_word = "_" * len(word)
            rounds = 6
            correct_letters = []

            response = """
            <html>
            <head>
                <meta charset="UTF-8">
                <link rel="stylesheet" href="https://bootswatch.com/5/darkly/bootstrap.min.css">
                <title>Miniproyectos | Ahorcado</title>
            </head>
            <body class="container d-flex flex-column align-items-center">
            """
            response += show_letter(hide_word, rounds)
            response += """
                <form class="d-flex flex-column" method="POST" action="/guess_letter">
                    <label>Ingrese una letra:</label>
                    <input type="text" name="letter" required><br>
                    <input type="hidden" name="word" value="{}">
                    <input type="hidden" name="hide_word" value="{}">
                    <input type="hidden" name="rounds" value="{}">
                    <input type="hidden" name="correct_letters" value="{}">
                    <input type="submit" value="Adivinar">
                </form>
            </body>
            </html>
            """.format(word, hide_word, rounds, correct_letters)
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(response.encode())
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == '/guess_letter':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            
            letter = post_data.split('&')[0].split('=')[1]
            word = post_data.split('&')[1].split('=')[1]
            hide_word = post_data.split('&')[2].split('=')[1]
            rounds = int(post_data.split('&')[3].split('=')[1])
            correct_letters = post_data.split('&')[4].split('=')[1].split(',')

            if letter.isalpha() and len(letter) == 1:
                if letter in correct_letters:
                    response = "<p>Ya has adivinado esa letra. Intenta con otra.</p>"
                elif letter in word:
                    correct_letters.append(letter)
                    hide_word = update_hide_word(word, hide_word, letter)
                    if "_" not in hide_word:
                        response = "<p>¡Felicidades! Has adivinado la palabra: {}</p>".format(word)
                    else:
                        response = show_letter(hide_word, rounds)
                else:
                    rounds -= 1
                    response = "<p>La letra no está en la palabra. Intentos restantes: {}</p>".format(rounds)
                    if rounds == 0:
                        response = "<p>¡Oh no! Te has quedado sin intentos. La palabra era: {}</p>".format(word)
            else:
                response = "<p>Por favor, ingresa una sola letra.</p>"
            
            response += """
                <html>
                    <head>
                        <meta charset="UTF-8">
                        <link rel="stylesheet" href="https://bootswatch.com/5/darkly/bootstrap.min.css">
                        <title>Miniproyectos | Ahorcado</title>
                    </head>
                    <body class="container d-flex flex-column align-items-center">
                        <form class="d-flex flex-column" method="POST" action="/guess_letter">
                            <label>Ingrese una letra:</label>
                            <input type="text" name="letter" required><br>
                            <input type="hidden" name="word" value="{}">
                            <input type="hidden" name="hide_word" value="{}">
                            <input type="hidden" name="rounds" value="{}">
                            <input type="hidden" name="correct_letters" value="{}">
                            <input type="submit" value="Adivinar">
                        </form>
                    </body>
                </html>
            """.format(word, hide_word, rounds, ','.join(correct_letters))

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(response.encode())
        else:
            super().do_POST()

def main():
    PORT = 8000

    with socketserver.TCPServer(("", PORT), MyRequestHandler) as httpd:
        print("Server listening on port: ", PORT)
        httpd.serve_forever()

if __name__ == "__main__":
    main()
