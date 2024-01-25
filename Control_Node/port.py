from flask import Flask, request, jsonify
import subprocess
import os
import random
from subprocess import run
#used_ports = []

app = Flask(__name__)

@app.route('/port', methods=['POST'])
def write_userandport():
    try:
      data = request.get_json()
      username = str(data['username'])
      email = str(data['email'])
      port = str(random.randint(1025, 49151))

      port_path = os.path.join('/ansible', 'port.txt')
      with open(port_path, 'w') as f:
          f.write(port + '\n')

      username_path = os.path.join('/ansible', 'username.txt')
      with open(username_path, 'w') as f:
          f.write(username + '\n')

      email_path = os.path.join('/ansible', 'email.txt')
      with open(email_path, 'w') as f:
          f.write(email + '\n')

      return jsonify({'message': 'port and user written'}), 200

    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
