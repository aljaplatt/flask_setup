from dbconfig.mongo import db
from helpers.helper import (check_uuid, count_all_items, format_reservation, check_reservation_valid,append_host,validate_limit_offset)


# create a reservation under a specific book
def add_reservation(data, book_id, host_name):
    formatted_reservation = format_reservation(data, book_id)
    valid_reservation = check_reservation_valid(formatted_reservation)
    if valid_reservation == 'forenames':
        return ({'message': 'Must provide valid forenames'}, 400)
    elif valid_reservation == 'surname':
        return ({'message': 'Must provide valid surname'}, 400)
    else: 
        try:
            reservations = db.reservations
            reservations.insert_one(formatted_reservation)
            appended_reservation = append_host(formatted_reservation, host_name)
            return ({'reservation': appended_reservation}, 201)
        except:
            return({'message': 'Could not connect to db'}, 500)

# get a list of reservations under a specific book
def get_all_reservations(book_id, host_name,limit,offset,sort, asc_desc):
    print("ARGS: ", book_id, host_name, limit, offset, sort, asc_desc)
    validation_result = validate_limit_offset(limit, offset)
    if validation_result == 'Invalid':
        return ({'message': 'Limit/Offset must be above 0'}, 400)
    valid_book_id = check_uuid(book_id)
    if valid_book_id == "Invalid ID":
        return ({'message': 'Given book ID is invalid/book does not exist'}, 404)
    try:
        reservations = db.reservations
        
        # .aggregate([
        #     {"$unwind": "$user"},
        #     {"$sort": {"user.surname": 1}},
        #       {"$group": { "_id": "$_id", "user": { "$push": "$user"}}}
        #             ])
        
        # .aggregate([
        #     {"$unwind": "$user"},
        #     {"$sort": {"user.surname": 1}},
        #       {"$group": { "surname": "$surname", "user": { "$push": "$user"}}}
        #             ])
                    
        # {"$group": { "surname": "$surname", "user": { "$push": "$user"}}}

        # .aggregate([
        #     {"$skip": offset},
        #     {"$limit": limit},
        #     {"$unwind": "user"},
        #     {"$sort": {f"user[{sort}]: {asc_desc}"}

        # ])
       
        results = reservations.find({
            "book_id": valid_book_id
        })

        # .aggregate([
        #     {"$unwind": "$user"},
        #     {"$sort": {"user.surname": 1}},
        #     {"$group": { "surname": "$surname", "user": { "$push": "$user"}}}
        #             ])
        # .limit(limit).skip(offset).sort('users'[sort], asc_desc)

        items_arr = []
        
        for result in results:
            new_result = append_host(result, host_name)
            items_arr.append(new_result)
        count = count_all_items(items_arr)
        return {"total_count": count, "items": items_arr}, 200
    except:
        return {"message": "Could not connect to db"}, 500

# get reservation by id
def get_reservation(book,id, host_name):
    validBookId = check_uuid(book)
    valid_res_id = check_uuid(id)
    if validBookId == "Invalid ID":
        return ("Given book ID is invalid/book does not exist", 404)
    elif valid_res_id == "Invalid ID":
        return ("Given reservation ID is invalid/reservation does not exist", 404)    
    else:
        try:
            book_id = book
            res_id = id
            reservations = db.reservations
            reservation = reservations.find_one({'_id':res_id,'book_id': book_id })
            result = append_host(reservation, host_name)
            return (result,200)
        except:
            return ({"message": "Could not connect to db"}, 500)



def update_reservation(book,id,data):
    validBookId = check_uuid(book)
    valid_res_id = check_uuid(id)
    if validBookId == "Invalid ID":
        return ("Given book ID is invalid/book does not exist", 404)
    elif valid_res_id == "Invalid ID":
        return ("Given reservation ID is invalid/reservation does not exist", 404)    
    else:
        try:
            book_id = book
            res_id = id
            query = {'_id':res_id,'book_id': book_id}
            new_res = {"$set": {'user':{'forenames': data['forenames'], 'surname': data['surname']}}}
            reservations = db.reservations
            result = reservations.update_one(query, new_res)
            return({'message':'Reservation updated'},200)
        except:
            return ({"message": "Could not connect to db"}, 500)




