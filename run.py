from App import app
import os
if __name__ == '__main__':
    # app.debug = True
    # loghandler = logging.FileHandler('flask.log')
    # app.logger.addHandler(loghandler)
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
