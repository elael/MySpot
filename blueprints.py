from flask import jsonify, request, Blueprint


def kitchen_blueprint():
    """"Encapsulates Flask WebApp for threading"""
    bp = Blueprint('ros', __name__)

    @bp.route('/param')
    def get_param_names():
        return jsonify()

    @bp.route('/param/<path:name>')
    def get_param_value(name):
        return jsonify()

    @bp.route('/param/<path:name>', methods=['POST'])
    def set_param_value(name):
        return jsonify()

    @bp.route('/params')
    def get_all_values():
        return jsonify()

    return bp
