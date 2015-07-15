from flask import Flask
from replicator_service import ReplicatorService
from flask import request
import thread
import logging

app = Flask(__name__)
logging.basicConfig(filename='replicator.log',level=logging.DEBUG)

@app.route('/clone', methods=['GET', 'POST'])
def clone():
    email = request.args.get('email')
    logging.info("/clone")
    logging.info("email: " + email)
    try:
        srv = ReplicatorService()
        thread.start_new_thread(srv.clone, (email,))
        message = 'URL will be sent to ' + email
        logging.info(message)
    except Exception, e:
        message = "Cloning error."
        logging.info("Exception: " + str(e))

    return message


if __name__ == '__main__':
    app.run('0.0.0.0')
