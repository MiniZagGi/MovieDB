from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/file-info/<path:filename>', methods=['GET'])
def file_info(filename):
    try:
        file_stat = os.stat(filename)
        info = {
            'size': file_stat.st_size,
            'modified': file_stat.st_mtime,
            'created': file_stat.st_ctime,
            'permissions': file_stat.st_mode
        }
        return jsonify(info)
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
