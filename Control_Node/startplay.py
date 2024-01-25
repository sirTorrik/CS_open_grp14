from flask import Flask, request, jsonify
import subprocess
from subprocess import run

app = Flask(__name__)

# Flask route ffrom subprocess import runor executing Ansible playbook
@app.route('/execute-playbook', methods=['POST'])
def execute_playbook():
    try:
      # Receive the request from the web server
       data = request.get_json()

      # Check if 'playbook' and 'username' keys exist in the request
       if 'playbook' not in data:
           return jsonify({'message': 'Invalid request. Missing playbook or username.'}), 400

       playbook = str(data['playbook'])
      # Command as list of arguments
       command = ['ansible-playbook', '-i' '/ansible/hosts.ini', playbook]


      # Run the Ansible playbook with the specified username using subprocess
       result = subprocess.run(command)

      # Return the output of the playbook execution
       return jsonify({'message': 'Playbook executed successfully', 'output': result.stdout}), 200

    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Listen on all network interfaces
