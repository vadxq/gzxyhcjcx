from flask import jsonify
from flask import request


from .req import get_info
from . import main


@main.route('/api/info', methods=['POST'])
def accept_info():
    json_info = request.get_json(True)
    if json_info:
        code = json_info.get('code')
        sfzh = json_info.get('sfzh')
    else:
        return jsonify({
            'status': 0,
            'message': 'bad request'
        })
    if code and sfzh:
        accept = get_info(code, sfzh)
        return jsonify(accept)
    return jsonify({
        'status': 0,
        'message': 'bad request2'
    })
