from flask import request, jsonify, Flask
from os import getenv
import multiprocessing

from src.logic.event import Event, parse_event
# from src.logic.email_sender import EmailSender
from src.logic.validator import EmailValidator
from src.logic.solver import Solver as MainSolver

app = Flask(__name__)


@app.route('/')
def index():
    return "Dneska uz nic nedelam"

# @app.route('/api/get_event', methods=['POST'])
# def get_event():
#     if request.headers.get('X-Auth-Token') != getenv('FLASK_SECURITY_KEY'):
#         return jsonify({'message': 'Unauthorized'}), 401
#     try:
#         data = request.get_json()
#         # logging.getLogger(__name__).info("get_event method accepted")
#         oris_id = data.oris_id
#         courses_str = data.courses_str
#         event = Event()
    
#         if not event.add_dat_from_oris(oris_id):
#             return jsonify({'message': 'Oris ID not found'}), 501
#         if not event.add_data_from_courses_file(courses_str):
#             return jsonify({'message': 'Invalid courses format'}), 502
    
#         # logging.getLogger(__name__).info("get_event method successfully processed")
#         return jsonify(event.export_input_data_to_dict()), 200
#     except Exception as e:
#         # logging.getLogger(__name__).critical(f'get_event failed with {e}')
#         return jsonify({'message': str(e)}), 500
    

# @app.route('/api/solve', methods=['POST'])
# def solve():
#     if request.headers.get('X-Auth-Token') != getenv('FLASK_SECURITY_KEY'):
#         return jsonify({'message': 'Unauthorized'}), 401
#     try:
#         data = request.get_json()
#         # logging.getLogger(__name__).info("solve_event method accepted")
#         json_event = data.event
#         email = data.email
#         if not EmailValidator(email).validate():
#             return jsonify({'message': 'Invalid email'}), 502
#         event = parse_event(json_event)
#         if not event:
#             return jsonify({'message': 'Invalid event format'}), 501
#         multiprocessing.Process(target=solve_and_send, args=[event, email]).start()
#         # logging.getLogger(__name__).info("solve_event method successfully processed")
#         return jsonify({'message': 'OK'}), 200
#     except Exception as e:
#         # logging.getLogger(__name__).critical(f'solve_event failed with {e}')
#         return jsonify({'message': str(e)}), 500
    
    
# def solve_and_send(event:Event, email:str):
#     """
#         function for multiprocessing
#     """
#     try:
#         event = MainSolver().solve(event)
#         int_cat = event.get_not_empty_categories_with_interval_start().values()
#         # logging.getLogger(__name__).info(f"event {event.id} solved!\tclub: {event.organizator}\t athletes: {sum([cat.get_category_count() for cat in int_cat])}\t length: {max([cat.get_last_athlete_startime() for cat in int_cat])}")
#     #     EmailSender().send(email, event)
#     except Exception as e:
#         pass
#     #     # logging.getLogger(__name__).critical(f'solve_and_send failed with {e}')
#     #     ...

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)