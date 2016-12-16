#!/usr/local/bin/python


from myapp import app, logger
logger.info('starting flask')
app.run(host='0.0.0.0',port=5000)
