from model import db, Data

data = Data.query.all()

f = open('result.csv', 'w')

print data

for elem in data:
	f.write(str(elem.acc_x) + "," + str(elem.acc_y) + "," + str(elem.acc_z) + "," + str(elem.lat) + "," + str(elem.lng) + "," + str(elem.time) + "," + str(elem.bump) + "\n")

f.close()
