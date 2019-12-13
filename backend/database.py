import pymongo
import secret
def connect():
    uri = "mongodb+srv://{}:{}@launch-emlpr.gcp.mongodb.net/test?authSource=admin&retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE".format(secret.username,secret.password)
    try:
        client = pymongo.MongoClient(uri) 
    except:
        client = pymongo.MongoClient("localhost:27017")

    try:
        db = client['LaunchDB']
    except:
        db = None
    try:
        db.authenticate(secret.username,secret.password)
        logger.info("authentication success")
    except:
        logger.debug("authentication failed")
    logger.info("db",db)
    return db