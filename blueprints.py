from flask import jsonify, request, Blueprint

import people_counting
from kitchen_database import kitchens_at, hours
from utils import avg

kitchen_blueprint = Blueprint('kitchen', __name__)


@kitchen_blueprint.route('/kitchen')
def kitchen():
    """
    GET /kitchen
    LIVE data for availability in each kitchen
    :return: { time: '13:00',
               kitchens: [{kitchenName: 'Cadillac', availableSeats:10, fruits: [apple, banana, peach]}. ...] }

    GET /kitchen?at=14:30
    AVG data for each room at a selected interval
    :return: [{kitchenName: 'Cadillac', availableSeats:10, fruits: [..]]
    """
    if not request.args:
        return jsonify([people_counting.get_current().recursive_dict()])

    return jsonify([koch._asdict() for koch in kitchens_at(request.args['at'])])


@kitchen_blueprint.route('/history')
def get_param_value():
    """
    AVG availability of sets overall for a time interval - use for a graph
    :return: [{timeInterval: '2:30', avg:100}]
    """
    return jsonify([
        {
            'time': hour,
            'avg': avg([koch.empty_seats for koch in kitchens_at(hour)])
        }
        for hour in hours
    ])


@kitchen_blueprint.route('/history/<path:name>', methods=['POST'])
def set_param_value(name):
    new_value = request.get_json()
    return jsonify(new_value)
