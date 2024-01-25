from flask import Flask, request, jsonify
import os


app = Flask(__name__)

@app.route('/tvars', methods=['POST'])
def write_user_and_port():
    try:
        data = request.get_json()
        username = str(data['username'])
        email = str(data['email'])

        #Uses os module to write files
        terraform_vars_path = os.path.join('/scripts', 'terraform.tvars')
        with open(terraform_vars_path, 'w') as f:
            f.write(f'username = "{username}"\n')
            f.write(f'email = "{email}"\n')

        return jsonify({'message': 'Username written to Terraform variable file'}), 200

    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
