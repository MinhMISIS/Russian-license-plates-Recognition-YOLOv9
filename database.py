import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="autopark"
)

mycursor = mydb.cursor()
def select( column, table , condition = 'True' ):
    mycursor.execute("SELECT " + column + " FROM " + table + " WHERE " + condition)
    myresult = mycursor.fetchall()

    for i in range(len(myresult)):
        myresult[i] = (myresult[i][0])
    return myresult
def creat_user_guest( ):
    sql ="INSERT INTO user (user_name, type) VALUE ('','guest')"
    mycursor.execute(sql)
    mydb.commit()
def lastest_user():
    sql = "SELECT MAX(user_id) FROM user;"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return myresult[0][0]

def creat_car_guest(LP,color ,link):
    creat_user_guest()
    user_id = lastest_user()
    sql = "SELECT LOAD_FILE('%s')"%(link)
    mycursor.execute(sql)
    photo = mycursor.fetchall()[0][0]
    sql2 = "INSERT INTO car(license_plate,user_id,color ,photo) VALUES (%s,%s,%s,%s);"
    value2 = (LP,user_id,color, photo)
    mycursor.execute(sql2,value2)
    mydb.commit()
    return photo
def find_id_by_LP (LP):
    sql = "SELECT user_id FROM car WHERE license_plate = %s"
    value = (LP,)
    mycursor.execute(sql, value)
    myresult = mycursor.fetchall()
    return myresult[0][0]

def creat_transaction(LP,start_time):
    user_id = find_id_by_LP(LP)
    sql ="INSERT INTO transaction (user_id,license_plate, start_time) VALUES (%s,%s,%s)"
    value = (user_id,LP,start_time )
    mycursor.execute(sql, value)
    mydb.commit()

def cal_duration_and_cost(starttime,endtime,LP):
    sql = "SELECT TIMEDIFF(%s, %s)"
    value = (endtime, starttime)
    mycursor.execute(sql,value)
    duration = mycursor.fetchall()
    hours = duration[0][0].seconds//3600 + 1
    duration = str(duration[0][0])

    sql2 = "UPDATE transaction SET duration = %s WHERE license_plate = %s AND duration IS NULL";
    value2 = (duration, LP)
    mycursor.execute(sql2, value2)

    cost = hours * 100
    sql3 = "UPDATE transaction SET total_cost = %s WHERE license_plate = %s AND total_cost IS NULL";
    value3 = (cost, LP)
    mycursor.execute(sql3, value3)
    mydb.commit()



def update_transaction(LP, endtime):
    starttime = select("start_time","transaction","license_plate = '%s' AND end_time IS NULL" %(LP))[0].strftime("%Y-%m-%d %H:%M:%S")
    sql = "UPDATE transaction SET  end_time = %s WHERE license_plate = %s AND end_time IS NULL"
    value = (endtime, LP)
    mycursor.execute(sql, value)
    cal_duration_and_cost(starttime,endtime,LP)
    mydb.commit()
def get_transaction(LP):
    myresult=[]
    mycursor.execute("SELECT transaction_id, user_id, start_time, end_time, duration, total_cost  FROM transaction WHERE license_plate = '%s'" %(LP))
    data = mycursor.fetchall()
    i = len(data) -1
    myresult.append("CODE TRANSACTION: " + str(data[i][0]))
    myresult.append("GUEST: "+ str(data[i][1]))
    myresult.append("TIME IN: "+ data[i][2].strftime("%Y-%m-%d %H:%M:%S.%p"))
    myresult.append("TIME OUT: "+ data[i][3].strftime("%Y-%m-%d %H:%M:%S.%p"))
    myresult.append("TIME in PARK: "+ str(data[i][4]))
    myresult.append("TOTAL COST: "+ str(data[i][5]) + "RUB")
    return myresult

def check_car_in_is_available(LP):
    sql = "SELECT MAX(transaction_id) FROM transaction WHERE license_plate = %s"
    value = (LP,)
    mycursor.execute(sql, value)
    id = mycursor.fetchall()[0][0]
    if id == None:
        return True
    sql2 = "SELECT total_cost FROM transaction WHERE transaction_id = %s"
    value2 = (id,)
    mycursor.execute(sql2, value2)
    result = mycursor.fetchall()[0][0]
    if result == None:
        return False
    else:
        return True

def find_element(list_of_lists):
    # Khởi tạo biến đếm số lần xuất hiện của mỗi phần tử trong list.
    counts = {}

    for i in list_of_lists:
        if tuple(i) not in counts:
            counts[tuple(i)] = 0
        counts[tuple(i)] += 1
    max_count = 0
    max_item = list[len(i)-1]
    for item, count in counts.items():
        if count >= max_count:
            max_count = count
            max_item = item
    return list(max_item)
def check_element_in_list(list1, list2):
    """Tìm phần tử trong list bằng b.

    Args:
      list: Một list chứa các phần tử.
      b: Phần tử cần tìm.

    Returns:
      Phần tử trong list bằng b, nếu không tìm thấy thì trả về 0.
    """
    for item in list1:
        for LP in list2:
            if item == LP:
                return True
    return False

#print(creat_car_guest("A919AA199","/Applications/XAMPP/xamppfiles/var/image-autopark/Car_A919AA199.png"))
#check_car_in_is_available("A919AA199")
#creat_car_guest("A919AA199","/Applications/XAMPP/xamppfiles/var/image-autopark/img7.jpeg")
#/Applications/XAMPP/xamppfiles/var/image-autopark