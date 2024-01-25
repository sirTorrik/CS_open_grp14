from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)


@app.route('/execute-terraform', methods=['POST'])
def execute_terraform():
    try:
        
        data = request.get_json()

        
        if 'tf_script' not in data:
            return jsonify({'message': 'Invalid request. Missing Terraform script.'}), 400

        
        tf_script = str(data['tf_script'])

        
        command = ['terraform','apply', '-auto-approve', f'-var-file=terraform.tvars' ]

        
        result = subprocess.run(command, cwd='/scripts/')

        
        return jsonify({'message': 'Terraform script executed successfully', 'output': result.stdout}), 200

    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)  
