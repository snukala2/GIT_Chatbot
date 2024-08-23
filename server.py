import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import json
import nltk
from nltk.chat.util import Chat, reflections

# Define chatbot patterns and responses
patterns_responses = [
    (r'Hi|Hello|Hey', ['Hello! How can I assist you today?', 'Hi there! What can I do for you?']),
    (r'What is your name?', ['I am a chatbot created by you.', 'I am a bot. You can call me Chatbot.']),
    (r'How are you?', ['I am just a program, but I am doing well. How can I help you?', 'I am doing great, thanks for asking!']),
    (r'What can you do?', ['I can chat with you and answer some basic questions.', 'I am here to assist you with some simple tasks.']),
    (r'quit|exit|bye', ['Goodbye! Have a great day!', 'See you later!']),
    # GITAM CATS IT Services
    (r'What are the current IT issues?', ['We are experiencing issues with network connectivity, server backup, and data reporting.']),
    (r'Network issues|Network problem', ['Our network team is working on connectivity problems. Please be patient as we resolve this.']),
    (r'Server backup issues|server issues', ['There are some delays with server backups. Our team is addressing the issue.']),
    (r'Storage issues|storage problem', ['We are having issues with server storage. This is being handled by our IT team.']),
    (r'Data reporting issues|loading issues', ['We are facing some challenges with data reporting. Our team is on it.']),
    # Account and Access
    (r'I forgot my password|forgot password', ['Please contact the IT support team for password recovery assistance.']),
    (r'How do I reset my password?', ['To reset your password, follow the instructions on our password reset page or contact IT support.']),
    (r'Can I change my username?', ['Username changes are not typically allowed. Please contact IT support for any special requests.']),
    # Technical Support
    (r'How do I install software|install software?', ['You can find installation guides on our IT support website or contact us for help.']),
    (r'My computer is slow|network slow|slow network', ['Try restarting your computer or contact IT support if the issue persists.']),
    (r'I have a software bug|bug issue|bug', ['Please describe the issue in detail so we can assist you effectively.']),
    # Network and Connectivity
    (r'How do I connect to the Wi-Fi?|wifi connection', ['Use the Wi-Fi settings on your device to connect to the GITAM network.']),
    (r'Wi-Fi is not working', ['Check your device settings or contact IT support if you need further assistance.']),
    # Hardware Issues
    (r'My printer is not working|printer issue|printer problem', ['Check the connections and ensure the printer is on. If issues persist, contact IT support.']),
    (r'Monitor is blank|monitor not working', ['Ensure the monitor is plugged in and turned on. If the problem continues, please contact support.']),
    # IT Policies
    (r'What are the IT policies?', ['Our IT policies can be found on the university’s IT services website.']),
    (r'How do I request new software?|software request', ['Submit a request through our IT service portal or contact IT support.']),
    # General Information
    (r'What is the helpdesk number?|helpdesk number', ['The helpdesk number is 123-456-7890.']),
    (r'What are the office hours?|office timings', ['Our office hours are Monday to Friday, 9 AM to 5 PM.']),
    # Miscellaneous
    (r'Can you help with my email?', ['Please specify the issue with your email, and I will do my best to assist.']),
    (r'Where can I find user guides?|user guides', ['User guides are available on our IT support website or through our helpdesk.']),
    (r'I need help with my laptop|issue in my laptop', ['Please provide details about the issue with your laptop so we can assist you.']),
    # IT Services Details
    (r'What services does GITAM CATS provide?', ['We offer support for network issues, hardware problems, software installations, and more.']),
    (r'How do I report a technical issue?|technical issue', ['You can report technical issues through our IT support portal or contact the helpdesk.']),
    # Security
    (r'How do I secure my account?|Account privacy', ['Use a strong password and enable two-factor authentication for added security.']),
    (r'What should I do if I suspect a security breach?', ['Immediately report the issue to IT support and change your passwords.']),
    # Additional Support
    (r'I need more help', ['Please describe your issue in detail, and I will direct you to the appropriate support.']),
    (r'Can I speak to a human?', ['I can assist with many issues, but if you need further help, I will connect you with a support agent.']),
]

# Create a Chat object
chatbot = Chat(patterns_responses, reflections)

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
