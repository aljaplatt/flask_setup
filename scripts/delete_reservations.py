from dbconfig.mongo import db
import sys

def delete_reservations():
    try:
        reservations = db.reservations
        res_results = list(reservations.find({}))
        if res_results:
            reservations = db.reservations
            result = reservations.delete_many({})
            print('RESULT: ', result)         
            print("All reservations deleted")
            return
        else:
            print('There are no reservations to delete.')
            sys.exit(0)
    except:
        print("Could not connect to db")
        sys.exit(1)

    
delete_reservations()