import os
import csv
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import json

# Load question-answer pairs from the dataset
def load_qa_dataset(filename):
    qa_pairs = []
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            question = row['question'].strip().lower()
            answer = row['answer'].strip()
            qa_pairs.append((question, answer))
    return qa_pairs

# Create a chatbot that responds based on the dataset
class DatasetChatbot:
    def __init__(self, qa_pairs):
        self.qa_pairs = qa_pairs

    def respond(self, message):
        message = message.strip().lower()
        for question, answer in self.qa_pairs:
            if question in message:
                return answer
        return "I'm not sure how to respond to that."

# Create a chat object with the dataset
qa_pairs = load_qa_dataset('qa_dataset.csv')
chatbot = DatasetChatbot(qa_pairs)

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Serve index.html
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            try:
                with open('index.html', 'r') as file:
                    self.wfile.write(file.read().encode())
            except IOError:
                self.send_error(404, 'File Not Found: %s' % self.path)
        elif self.path.endswith(".jpg"):
            # Serve image files
            try:
                with open(self.path[1:], 'rb') as file:
                    self.send_response(200)
                    self.send_header('Content-type', 'image/jpeg')
                    self.end_headers()
                    self.wfile.write(file.read())
            except IOError:
                self.send_error(404, 'File Not Found: %s' % self.path)
        else:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        if self.path == '/chat':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode()
            params = urllib.parse.parse_qs(post_data)
            user_message = params.get('message', [''])[0]
            response = chatbot.respond(user_message)
            response_data = {'response': response}
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode())

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    # Change the working directory to where index.html is located
    os.chdir('C:/Users/502881/Desktop/Chatbot')
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
