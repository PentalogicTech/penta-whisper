from flask import request, jsonify, Blueprint
from app.routes.task import process_audio

apiCalls_bp = Blueprint('audio_bp', __name__)

#### METODO POST ####

@apiCalls_bp.route('/api/process-audio', methods=['POST'])
def process_audio_route():
    audio_link = request.json.get('audio_link')

    if not audio_link:
        return 'No se proporcionó un enlace válido', 400

    task = process_audio.delay(audio_link)
    return jsonify({'task_id': task.id}), 202

# METODO GET

@apiCalls_bp.route('/api/task/<task_id>', methods=['GET'])
def get_task_status(task_id):
    task = process_audio.AsyncResult(task_id)

    if task.state == 'PENDING':
        response = {
            'status': 'Pendiente'
        }
    elif task.state == 'SUCCESS':
        response = {
            'status': 'Completado',
            'result': task.result
        }
    else:
        response = {
            'status': 'FAILED!'
        }

    return jsonify(response)