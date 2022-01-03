from App import app
if __name__ == '__main__':
    # app.debug = True
    # loghandler = logging.FileHandler('flask.log')
    # app.logger.addHandler(loghandler)
    app.run(debug=True, port=5000)
