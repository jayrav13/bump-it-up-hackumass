from model import db, Data

data = Data.query.all()
baseline = []
avg = [0,0,0]

for index, elem in enumerate(data):
	if index < int(len(data) * 0.1):
		baseline.append(elem.acc_y)
		avg[0] = avg[0] + elem.acc_y
		avg[1] = avg[1] + 1
		avg[2] = avg[0] / avg[1]
	else:
		if elem.acc_y - avg[2] > 0.20:
			elem.bump = abs((elem.acc_y - avg[2]) / avg[2])
		else:
			elem.bump = 0

for elem in data:
	if elem.bump == 1:
		print elem.acc_y

db.session.commit()
