from flask import request, jsonify, Flask
import multiprocessing
import logging


from src.client.email import EmailClient
from src.entities.event import Event, parse_event
from src.logic.validator import EmailValidator
from src.logic.solver import Solver as MainSolver
from src.settings import Settings
from src.postman import Postman
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
settings = Settings()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# mail configuration
email_client = EmailClient(logger, app, settings)
postman = Postman(email_client, logger)

@app.route('/')
def index():
    return "Dneska uz nic nedelam"

@app.route('/get_event', methods=['POST'])
def get_event():
    try:
        data = request.get_json()
        oris_id = data.get('oris_id', None)
        courses_str = data.get('courses_str', None)
        event = Event()
        
        logger.info(f"Processing oris_id: {oris_id}")
    
        if not event.add_dat_from_oris(oris_id):
            msg = f'Oris ID {oris_id} not found'
            logger.error(msg)
            return jsonify({'message': msg}), 501
        if not event.add_data_from_courses_file(courses_str):
            msg = f'Invalid courses format starting with {courses_str[:50]}'
            logger.error(msg)
            return jsonify({'message': msg}), 502
    
        logger.info(f"Event {event.id} successfully processed")
        return jsonify(event.export_input_data_to_dict()), 200
    except Exception as e:
        msg = f'Endpoint get_event failed with {e}'
        logger.error(msg)
        return jsonify({'message': msg}), 500
    

@app.route('/solve', methods=['POST'])
def solve():
    try:
        data = request.get_json()
        json_event = data.get('event', None)
        email = data.get('email', None)
        if not EmailValidator(email).validate():
            msg = f'Invalid email {email}'
            logger.error(msg)
            return jsonify({'message': msg}), 502
        logger.info(f"Processing event {json_event['id']} for {email}")
        event = parse_event(json_event)
        if not event:
            msg = f'Invalid event format'
            logger.error(msg)
            return jsonify({'message': msg}), 501
        multiprocessing.Process(target=solve_and_send, args=[event, email]).start()
        logger.info("solve_event method successfully processed")
        return jsonify({'message': 'OK'}), 200
    except Exception as e:
        msg = f'Endpoint solve_event failed with {e}'
        logger.error(msg)
        return jsonify({'message': msg}), 500
    
def solve_and_send(event:Event, email:str):
    """
        function for multiprocessing
    """
    try:
        logger.info(f"Creating startgrid for event {event.id}")
        event = MainSolver().solve(event)
        int_cat = event.get_not_empty_categories_with_interval_start().values()
        logger.info(f"event {event.id} solved!\tclub: {event.organizator}\t athletes: {sum([cat.get_category_count() for cat in int_cat])}\t length: {max([cat.get_last_athlete_startime() for cat in int_cat])}")
        postman.deliver_startgrid(email, event)
    except Exception as e:
        msg = f'Endpoint solve_and_send failed: {str(e)}'
        postman.send_email(
                    receiver=settings.MAIL_USERNAME,
                    subject='Error in startgrid delivery',
                    message=f'Error in startgrid delivery for event {event.id} to {email}: {str(e)} \n\n {event.export_input_data_to_dict()}'
                )
        logger.error(msg)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)