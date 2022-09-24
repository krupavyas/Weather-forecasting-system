import socketserver
import http.server
import ssl
import json

def getResponse(user_input):
    api_url = "https://api.openweathermap.org/data/2.5/weather"
    r = requests.post(url = api_url, params = {'q':user_input, 'APPID':'7bc5a8a3a2b38f505bdb7b30f287b614', 'units':'metric'})
    if r.status_code == 200:
        response = json.loads(r.content)
        temp = response['main']['temp']
        return 'The current temperature for ' + user_input + ' is: ' + str(temp)
    return 'I was not able to get the temperature :-(!'

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        post_data = self.rfile.read(int(self.headers['Content-Length']))
        json_data = json.loads(post_data)

        chat_id = json_data['message']['from']['id']
        user_input = json_data['message']['text']

        bot_output = getResponse(user_input)

        url = "https://api.telegram.org/bot5707677152:AAH8blt46ltsRTojZZKAzdkfnflrRg-w9bk/sendMessage"

        r = requests.post(url = url, params = {'chat_id' : chat_id, 'text' : bot_output})
        if r.status_code == 200:
            self.send_response(200)
            self.end_headers() 

    def do_GET(self):
        self.send_response(200)
        self.end_headers()

server = socketserver.TCPServer(('0.0.0.0', 8443), MyHandler)
server.socket = ssl.wrap_socket(server.socket,
                                ca_certs = "SSL/ca_bundle.crt",
                                certfile = "SSL/certificate.crt",
                                keyfile = "SSL/private.key",
                                server_side = True
                                )

server.serve_forever()