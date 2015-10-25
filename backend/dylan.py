def home_route():
	data = whatever()
	#for d in data:
	#	print d[0], d[1], d[2], d[3], d[4]
	
	first = data[-1][6][11:23]
	second = data[0][6][11:23]

	first_date = data[0][6]
	second_date = data[-1][6]

	a = datetime.strptime(first_date, '%Y-%m-%dT%H:%M:%S.%fZ')
	b = datetime.strptime(second_date, '%Y-%m-%dT%H:%M:%S.%fZ')

	test = [row[1] for row in data]
	testavg = avg(test)
	testvar = variance(test, testavg)
	teststd = std(testvar)

#	var = variance(data[3])	
#	print var
	listmo = mode(test)
	print "mode: "
	print listmo
	print "avg: "
	print testavg
	print "var: "
	print testvar
	print "std: "
	print teststd

	hibound = testavg + teststd
	lobound = testavg - teststd

	print "hi: "
	print hibound
	print "lo: "
	print lobound	

	for i in data:
		if lobound >= i[1]:
			print i
		elif hibound <= i[1]:
			print i	
		else:
			pass 

	dif = b - a	
	print str(dif)
		     
	return "</br>time has passed is "+str(dif)+"</br>"+"</br>\n".join(map(str, data))


def whatever():
	con = lite.connect('points.db')
	cur = con.cursor()
	cur.execute('SELECT SQLITE_VERSION()')
	cur.execute("SELECT * FROM DATA;")
	data = cur.fetchall()

	return data

def mode(list):
	
	d = {}
	for elm in list:
		try:
			d[elm] += 1
		except(KeyError):
			d[elm] = 1
	
	keys = d.keys()
	max = d[keys[0]]
	
	for key in keys[1:]:
		if d[key] > max:
			max = d[key]

	max_k = []		
	for key in keys:
		if d[key] == max:
			max_k.append(key),
	return max_k,max

def avg(list):

	sum = 0
	
	for elm in list:
		sum += elm
		
	return sum/(len(list)*1.0)

def variance(my_list, average):
	variance = 0
    	for i in my_list:
        	variance += (average - i) ** 2
    	return variance / len(my_list)
def std(var):
	return sqrt(var)


