from flask import jsonify, request, Blueprint

import kitchen_detection
from kitchen_detection import people_counting
from config import cfg
from kitchen_database import kitchens_at
from utils import avg

kitchen_blueprint = Blueprint('kitchen', __name__)


@kitchen_blueprint.route('/kitchen')
def kitchen():
    """
    GET /kitchen?at=14:30
    AVG data for each room at a selected interval
    :return: [{kitchenName: 'Cadillac', availableSeats:10, fruits: [..]]
    """
    print(f"p-{kitchen_detection.people_live.people_buffer}")
    print(f"a-{kitchen_detection.people_live.apple_buffer}")
    print(f"b-{kitchen_detection.people_live.banana_buffer}")
    live_data = people_counting.get_current()

    if live_data.time == request.args['at']:
        return jsonify(live_data.with_boolean_fruits().recursive_dict())

    return jsonify({'time': people_counting.get_current().time,
                    'kitchens': [koch.round()._asdict() for koch in kitchens_at(request.args['at'])]})


@kitchen_blueprint.route('/history')
def history():
    """
    AVG availability of sets overall for a time interval - use for a graph
    :return: [{timeInterval: '2:30', avg:100}]
    """
    live_data = people_counting.get_current()
    kitchens_avg = {hour: avg([koch.empty_seats for koch in kitchens_at(hour)]) for hour in cfg.hours}
    if live_data.time in cfg.hours:
        kitchens_avg.update({live_data.time: avg([koch.empty_seats for koch in live_data.kitchens])})

    return jsonify({
        'time': live_data.time,
        'kitchens': [{'time': time, 'avg': kitchens_avg} for time, kitchens_avg in kitchens_avg.items()]
    })


@kitchen_blueprint.route('/history/<path:name>', methods=['POST'])
def history_value(name):
    new_value = request.get_json()
    return jsonify(new_value)
