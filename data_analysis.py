
import numpy as np
import matplotlib.pyplot as plt
import re_duration_estimation
from datetime import datetime

Visitation_Year = [2012, 2013, 2014, 2015, 2016]
Num_Visitation = [46.37, 48.33, 50.04, 52.59, 53.91]
Num_Visitation_Domestic = [45.00, 49.96, 48.71, 50.97, 52.35]

Visitation_Growth = [6.4, 4.2, 3.5, 5.1, 2.5]
Visitation_Domestic_Growth = [6.2, 4.3, 3.7, 4.6, 2.7]

fig, ax1 = plt.subplots()
ax1.bar(Visitation_Year, Num_Visitation)
ax1.set_xlabel("Year")
ax1.set_ylabel("Number of visitors(mil)")

ax2 = ax1.twinx() 
ax2.plot(Visitation_Year, Visitation_Growth, 'r')
ax2.set_ylabel("Annual Growth(%)")
 
fig.tight_layout()
plt.show()
 
f = open("Divvy_data.txt", 'r')
Divvy_data_count = 0
for j in f:
	Divvy_data_count += 1
f.close()

address = []
duration_comparison = [0.0, 0.0]
duration_comparison_subscriber = [0.0, 0.0]
duration_comparison_by_time = []
duration_comparison_by_time_by_userType = [ [], [] ]
duration_comparison_by_start_station = []
duration_difference = [ [],  []]#actual - driving_estimation

duration_hist = []



too_soon_stations = []
too_soon_stations_count = []
temp_length = [0, 0, 0]

longest_duration = [0.0, 0.0]
#longest_duration_info

count14 = 0
count17 = 0
num_n = 0
num_n14 = 0

for j in range(24):
	duration_comparison_by_time.append( [0.0, 0.0] )
	duration_comparison_by_time_by_userType[0].append( [0.0, 0.0] )
	duration_comparison_by_time_by_userType[1].append( [0.0, 0.0] )


f = open("Divvy_data.txt", 'r')
for j in range(Divvy_data_count):
	temp = f.readline().split("\t")
	#2 = duration
	#3 = driving duration
	#4 = start date
	#5 = start time
	#6 = start station
	#7 = start address
	#8 = stop date
	#9 = stop time
	#10 = stop station
	#11 = stop address
	#12 = gender
	#13 = user type
	#14 = driving duration in traffic
	#15 = driving distance

	duration_hist.append( float(temp[2]) )
	
	
	if float( temp[2] ) > longest_duration[0]:
		longest_duration[0] = float(temp[2])
		longest_duration[1] = temp[3]
		longest_duration_info = temp
	else:
		pass
	
	if temp[7] == 'Wabash Ave & 16th St':
		print temp
	if temp[7] == "State St & 16th St" or temp[11] == "State St & 16th St":
		#print "State St & 16th St"
		pass
	else:
		if ( float(temp[2]) - float( temp[3] ) ) > 0:
			duration_difference[0].append( float(temp[2]) - float( temp[3] ) )
		else:
			if ( float(temp[2]) - float( temp[3] ) ) < 10:
				if temp[7] not in too_soon_stations:
					too_soon_stations.append(temp[7])
					too_soon_stations_count.append( 1 )
				else:
					too_soon_stations_count[too_soon_stations.index(temp[7])] += 1
				
				if temp[11] not in too_soon_stations:
					too_soon_stations.append(temp[11])
					too_soon_stations_count.append( 1 )
				else:
					too_soon_stations_count[too_soon_stations.index(temp[11])] += 1
				
			else:
				duration_difference[1].append( float(temp[2]) - float( temp[3] ) )
			re_duration_estimation.func(temp[7], temp[11], temp[4], temp[5], temp[2])
		
	userType = temp[13].lower()[:8]
	#if userType != 'customer' and len(temp) == 14:
	#	print ("%s\t%s") % (userType[:8], len(temp))
	#print ( userType[-1] )
	#"dependent" would refer to someone under 16 whose parent purchased them a membership."
	#Customers are single riders, those without an annual membership. Subscribers and dependents are annual membership holders
	
	if temp[7] not in address:
		address.append(temp[7])
		duration_comparison_by_start_station.append( [0.0, 0.0] )
	else:
		pass
	
	if len(temp) == 14:
		if count14 == 0:
			pass
			#print temp
		if temp[-1] == 'Customer\n':
			num_n14 += 1
		else:
			pass
			#print temp
		count14 += 1
		temp_length[0] += 1
	elif len(temp) == 15:
		print temp
		temp_length[1] += 1		
	elif len(temp) == 17:
		temp_length[2] += 1
		if temp[-1] == '\n':
			num_n += 1
		else:
			pass
		count17 += 1
	
	
	address_index = address.index(temp[7])
	startHour = int(temp[5].split(":")[0])
	
	if float(temp[2]) >= float(temp[3]):
		duration_comparison[0] += 1.0
		duration_comparison_by_time[startHour][0] += 1
		duration_comparison_by_start_station[address_index][0] += 1
		if userType == "customer":# or userType == "subscribe" or userType == "dependent":
			duration_comparison_by_time_by_userType[0][startHour][0] += 1
			#print ("customer")
		else:
			duration_comparison_by_time_by_userType[1][startHour][0] += 1
			#print ( userType )
			#print ("customer")
	else:
		if temp[7] == "State St & 16th St" or temp[11] == "State St & 16th St":
			pass
			#print "State St & 16th St"
		else:
			duration_comparison[1] += 1.0
			duration_comparison_by_time[startHour][1] += 1
			duration_comparison_by_start_station[address_index][1] += 1
			if userType == "customer" or userType == "subscribe" or userType == "dependent":
				duration_comparison_by_time_by_userType[0][startHour][1] += 1
				#print ("customer")
			else:
				duration_comparison_by_time_by_userType[1][startHour][1] += 1
				#print ( userType )

print "longest duration trip detail..."
print longest_duration
print longest_duration_info			
			
plt.hist(duration_hist, bins = 100)
plt.xlabel("min")
plt.show()		
			
plt.plot(sorted(duration_hist))
plt.show()	

zipped = zip(too_soon_stations_count, too_soon_stations)
zipped.sort(key = lambda t: t[0])

#for j in range(len(	zipped )):
#	print zipped[j]


#print temp_length
#print num_n14
#print num_n

duration_difference_car = np.asarray(duration_difference[0])

results, edges = np.histogram(duration_difference_car, normed=True, bins = 50)
binWidth = edges[1] - edges[0]
plt.bar(edges[:-1], results*binWidth, binWidth)
plt.show()

duration_difference_divvy = np.asarray(duration_difference[1])

results, edges = np.histogram(duration_difference_divvy, normed=True, bins = 50)
binWidth = edges[1] - edges[0]
plt.bar(edges[:-1], results*binWidth, binWidth)
plt.show()
"""
plt.hist(duration_difference_car, bins = 200)
plt.xlabel('min')
plt.savefig('Divvy_vs_cars_histogram_when_car_was faster,png')
plt.show()
plt.close('all')
plt.hist(duration_difference_divvy, bins = 200)
plt.xlabel('min')
plt.savefig('Divvy_vs_cars_histogram_when_divvy_was faster,png')
plt.show()
plt.close('all')
"""
"""			
duration_comparison[0] = duration_comparison[0] / Divvy_data_count * 100
duration_comparison[1] = duration_comparison[1] / Divvy_data_count * 100

print ("Which is faster?")
print ("Divvy: %s percents of times." % round(duration_comparison[1], 2))
print ("Driving: %s percents of times." % round(duration_comparison[0], 2))

hour = []
Divvy_by_hour = []
Driving_by_hour = []
Divvy_by_hour_subscribe = []
Driving_by_hour_subscribe = []
Divvy_by_hour_non_subscribe = []
Driving_by_hour_non_subscribe = []
total = []
Num_user_by_hour = []
Num_subscribe_by_hour = []
Num_non_subscribe_by_hour = []
#subscribe_total_by_hour = []
for j in range(24):
	total_by_hour = (duration_comparison_by_time[j][0] + duration_comparison_by_time[j][1])
	duration_comparison_by_time[j][0] = duration_comparison_by_time[j][0] / total_by_hour * 100
	duration_comparison_by_time[j][1] = duration_comparison_by_time[j][1] / total_by_hour * 100
	
	subscribe_total_by_hour = ( duration_comparison_by_time_by_userType[0][j][0] + duration_comparison_by_time_by_userType[0][j][1] ) 
	non_subscribe_total_by_hour = ( duration_comparison_by_time_by_userType[1][j][0] + duration_comparison_by_time_by_userType[1][j][1] )
	
	duration_comparison_by_time_by_userType[0][j][0] = duration_comparison_by_time_by_userType[0][j][0] / subscribe_total_by_hour * 100
	duration_comparison_by_time_by_userType[0][j][1] = duration_comparison_by_time_by_userType[0][j][1] / subscribe_total_by_hour * 100
	
	#duration_comparison_by_time_by_userType[1][j][0] = duration_comparison_by_time_by_userType[1][j][0] / non_subscribe_total_by_hour * 100
	#duration_comparison_by_time_by_userType[1][j][1] = duration_comparison_by_time_by_userType[1][j][1] / non_subscribe_total_by_hour * 100
	
	duration_comparison_by_time_by_userType[0][j][0] = duration_comparison_by_time_by_userType[0][j][0] / subscribe_total_by_hour * 100
	duration_comparison_by_time_by_userType[0][j][1] = duration_comparison_by_time_by_userType[0][j][1] / subscribe_total_by_hour * 100
	
	duration_comparison_by_time_by_userType[1][j][0] = duration_comparison_by_time_by_userType[1][j][0] / subscribe_total_by_hour * 100
	duration_comparison_by_time_by_userType[1][j][1] = duration_comparison_by_time_by_userType[1][j][1] / subscribe_total_by_hour * 100
	
	#print ( "From %s:00 to %s:59" % (j, j) ) 
	#print ("Divvy: %s percents of times." % round(duration_comparison_by_time[j][1], 2))
	#print ("Driving: %s percents of times." % round(duration_comparison_by_time[j][0], 2))
	hour.append(j)
	Divvy_by_hour.append( round(duration_comparison_by_time[j][1], 2) )
	Driving_by_hour.append( round(duration_comparison_by_time[j][0], 2) )
	
	Divvy_by_hour_subscribe.append( round(duration_comparison_by_time_by_userType[0][j][1], 2) )
	Driving_by_hour_subscribe.append( round(duration_comparison_by_time_by_userType[0][j][0], 2) )
	
	Divvy_by_hour_non_subscribe.append( round(duration_comparison_by_time_by_userType[1][j][1], 2) )
	Driving_by_hour_non_subscribe.append( round(duration_comparison_by_time_by_userType[1][j][0], 2) )
	Num_user_by_hour.append(total_by_hour)
	Num_subscribe_by_hour.append( subscribe_total_by_hour )
	Num_non_subscribe_by_hour.append( non_subscribe_total_by_hour )
	total.append(Divvy_by_hour[j] + Driving_by_hour[j])
	
max_num_user_by_hour = max(Num_user_by_hour)	
#for j in range(24):	
#	Num_user_by_hour[j] = Num_user_by_hour[j] / max_num_user_by_hour * 50
	
fig, ax1 = plt.subplots()	
ax1.plot(hour, Divvy_by_hour, 'b', label = "Divvy")
ax1.plot(hour, Driving_by_hour, 'g', label = "Driving")
ax1.set_xlabel("time(HH)")
ax1.legend(bbox_to_anchor=(0.8, 0.5), loc=0, borderaxespad=0.)
#ax1.set_ylabel('exp', color='b')
#plt.plot(hour, total, 'r')

ax2 = ax1.twinx()
ax2.plot(hour, Num_user_by_hour, 'k')
ax2.set_ylabel("Total number of users")

#plt.legend(bbox_to_anchor=(0.8, 0.5), loc=3, borderaxespad=0.)
fig.tight_layout()
plt.show()

fig = plt.figure()
ax = plt.subplot(111)
ax.plot(hour, Divvy_by_hour_subscribe, 'b', label = "Divvy")
ax.plot(hour, Driving_by_hour_subscribe, 'g', label = "Driving")
ax.title("Subscribers")
ax.xlabel("time(HH)")
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(bbox_to_anchor=(0.8, 0.5), loc=3, borderaxespad=0.)
plt.show()
plt.plot(hour, Divvy_by_hour_non_subscribe, 'b')
plt.plot(hour, Driving_by_hour_non_subscribe, 'g')
plt.title("Non-Subscribers")
plt.xlabel("time(HH)")
plt.show()
"""
