

import csv
import matplotlib.pyplot as plt
import DateChecker
from googlemaps.client import Client
from googlemaps.distance_matrix import distance_matrix
from datetime import datetime
from datetime import date

def func():

	csv_file_names = []
	csv_file_names.append( "Divvy_Trips_2013.csv" )#75,9788
	csv_file_names.append( "Divvy_Trips_2014_Q1Q2.csv" )#905,699
	csv_file_names.append( "Divvy_Trips_2014-Q3-07.csv" )#410,340
	csv_file_names.append( "Divvy_Trips_2014-Q3-0809.csv" )#700,630
	csv_file_names.append( "Divvy_Trips_2014-Q4.csv" )#437,965
	csv_file_names.append( "Divvy_Trips_2015-Q1.csv" )#202,349
	csv_file_names.append( "Divvy_Trips_2015-Q2.csv" )#893,890
	csv_file_names.append( "Divvy_Trips_2015_07.csv" )#533,711
	csv_file_names.append( "Divvy_Trips_2015_08.csv" )#495,029
	csv_file_names.append( "Divvy_Trips_2015_09.csv" )#427,095
	csv_file_names.append( "Divvy_Trips_2015_Q4.csv" )#631,365
	csv_file_names.append( "Divvy_Trips_2016_Q1.csv" )#396,913
	csv_file_names.append( "Divvy_Trips_2016_04.csv" )#231,635
	csv_file_names.append( "Divvy_Trips_2016_05.csv" )#363,319
	csv_file_names.append( "Divvy_Trips_2016_06.csv" )#477,873
	csv_file_names.append( "Divvy_Trips_2016_Q3.csv" )#1,441,811
	csv_file_names.append( "Divvy_Trips_2016_Q4.csv" )#683,832
	csv_file_names.append( "Divvy_Trips_2017_Q1.csv" )#431,691
	csv_file_names.append( "Divvy_Trips_2017_Q2.csv" )#1,119,814

	#50,000 requests per project per day
	API_keys = '***'

	stopStation_count = [station1, station2, ...]
	station = [year1, year2, ...]
	year = [month1, month2, ...]
	month = [day1, day2, ...]
	day = [00:00, ..., 23:00]
	
	stopStation_count = [station][year][month][day][hour]

	routes = []
	stations = []
	startStation_count = []
	stopStation_count = []
	total_num = 0#total number of "reantals" is 
	total_num_subscribe = 0
	
	num_API_quota = 0
	num_10000 = 0
	longestDuration = 0			
	
	duration_comparison = [0.0, 0.0]#[bycicle is faster, driving is faster]
	duration_comparison_subscriber = [0.0, 0.0]#[bycicle is faster, driving is faster]

	
	userTypes = []
	userType_ratio = []#[subscribe, ]
	genders = []
	gender_ratio = []#[#Women, #Men]
	
	for file in csv_file_names: 
		print (file)
		count = 0
		with open(file, 'r') as f:
			for line in f:
				count += 1
				if file == "done":
					data_reading_finished = True
				elif count > 1:
					total_num += 1
					if total_num >= int(Divvy_data_count):
						#print ( "Currently at %s, %s percents" % (str(total_num), str(round(total_num / total * 100, 5))))
						print ( "%s\t%s" % (str(total_num), str(round(total_num / total * 100, 5))))
						if total_num % 10000 == 0 and num_10000 != 0:
							txtFileName = file[:-4] + ( (num_10000 - 1) * 10000 ) + "-" + str( num_10000 * 10000 ) + ".txt"
							output = open(txtFileName, 'w')
							for j in range(	len(data) ):
								temp_range = len(data[0])
								for k in range(tem_range):
									output.write(str(data[j][k]))
							output.close()
						
						tripID = line.split(',')[0]
						
						startDate, startTime = line.split(',')[1].split()
						if file == "Divvy_Trips_2013.csv":
							startYear, startMonth, startDay = startDate.split("-")
						elif file[12:16] == "2014":
							startMonth, startDay, startYear = startDate.split("/")
						elif file[12:16] == "2015":
							startMonth, startDay, startYear = startDate.split("/")
						elif file[12:16] == "2016":
							startMonth, startDay, startYear = startDate.split("/")
						elif file[12:16]== "2017":
							startMonth, startDay, startYear = startDate.split("/")
						else:
							pass
						if file == "Divvy_Trips_2016_Q3.csv" or file == "Divvy_Trips_2016_Q4.csv" or file[12:16]== "2017":
							startMonth = startMonth[1:]
							startHour, startMinute, startSecond = startTime.split(":")
						else:
							startHour, startMinute = startTime.split(":")
						startYear, startMonth, startDay = int(startYear), int(startMonth), int(startDay)
						startDay_ofTheWeek = DateChecker.func(startYear, startMonth, startDay)
						startHour, startMinute = int(startHour), int(startMinute)
						
						stopDate, stopTime = line.split(',')[2].split() 
						if file == "Divvy_Trips_2013.csv":
							stopYear, stopMonth, stopDay = stopDate.split("-")
						elif file[12:16] == "2014":
							stopMonth, stopDay, stopYear = stopDate.split("/")
						elif file[12:16] == "2015":
							stopMonth, stopDay, stopYear = stopDate.split("/")
						elif file[12:16] == "2016":
							stopMonth, stopDay, stopYear = stopDate.split("/")
						elif file[12:16] == "2017":
							stopMonth, stopDay, stopYear = stopDate.split("/")
						else:
							pass
							
						if file == "Divvy_Trips_2016_Q3.csv" or file == "Divvy_Trips_2016_Q4.csv" or file[12:16]== "2017":
							stopMonth = stopMonth[1:]
							stopHour, stopMinute, stopSecond = stopTime.split(":")
						else:
							stopHour, stopMinute = stopTime.split(":")
						stopYear, stopMonth, stopDay = int(stopYear), int(stopMonth), int(stopDay)
						stopDay_ofTheWeek = DateChecker.func(stopYear, stopMonth, stopDay)
						stopHour, stopMinute = int(stopHour), int(stopMinute)
						
						bikeID = line.split(',')[3]
						duration = line.split(',')[4]
						startStation = line.split(',')[5]
						Station = startStation

						startAdress = line.split(',')[6]
						stopStation = line.split(',')[7]
						Station = stopStation

						stopAddress = line.split(',')[8]
						
						userType = line.split(',')[9]					
						if userType not in userTypes:
							userTypes.append( userType )
						else:
							pass
	
							
						gender = line.split(',')[10]					
						if gender not in genders:
							genders.append( gender )
						else:
							pass

						birthday = line.split(',')[11]				
						
						temp = googlemap_drive_duration(startAdress, stopAddress, startYear, startMonth, startDay, startHour, startMinute, total_num, API_keys)
						driving_duration = temp[0]
						driving_duration_in_traffic = temp[1]
						driving_distance = temp[2]
												
						if driving_duration[-1] == "s":
							driving_duration = float(driving_duration[:-5])
						else:
							driving_duration = float(driving_duration[:-4])
						if str(duration[0]) == '"':
							duration = duration[1:]
							duration = duration[:-1]
						else:
							pass
						duration = round(float(duration) / 60, 1)
						
						if driving_duration_in_traffic[-1] == "s":
							if driving_duration_in_traffic.split()[1] == "hour":
								driving_duration_in_traffic = round(float(driving_duration_in_traffic.split()[0]) * 60 + float(driving_duration_in_traffic.split()[2]) / 60, 1)
							else:
								driving_duration_in_traffic = float(driving_duration_in_traffic[:-5])
								driving_duration_in_traffic = round(float(driving_duration_in_traffic) / 60, 1)
						elif driving_duration_in_traffic.split()[1] == "hour":
							driving_duration_in_traffic = round(float(driving_duration_in_traffic.split()[0]) * 60 + float(driving_duration_in_traffic.split()[2]), 1)
						else:	
							driving_duration_in_traffic = float(driving_duration_in_traffic[:-4])
						
						f = open("Divvy_data.txt", 'a+')
						f.write( file )#0
						f.write("\t")
						f.write( str(total_num) )#1
						f.write("\t")
						f.write( str(duration) )#2
						f.write("\t")
						f.write( str(driving_duration) )#3
						f.write("\t")
						f.write( startDate )#4
						f.write("\t")
						f.write( startTime )#5
						f.write("\t")
						f.write( startStation )#6
						f.write("\t")
						f.write( startAdress )#7
						f.write("\t")
						f.write( stopDate )#8
						f.write("\t")
						f.write( stopTime )#9
						f.write("\t")
						f.write( stopStation )#10
						f.write("\t")
						f.write( stopAddress )#11
						f.write("\t")
						f.write( gender )#12
						f.write("\t")
						f.write( userType )#13
						f.write("\t")
						f.write( str(driving_duration_in_traffic) )#14
						f.write("\t")
						f.write( str(driving_distance) )#15
						#f.write("\t")

						f.write("\n")
						f.close()
						
						driving_duration = float( driving_duration )
						bicycle_duration = float( round(float(duration) / 60, 1) )
						if driving_duration >= bicycle_duration:
							duration_comparison[0] += 1
						else:
							duration_comparison[1] += 1
						
						if userType == "Subscribe":
							total_num_subscribe += 1
							if driving_duration >= bicycle_duration:
								duration_comparison_subscriber[0] += 1
							else:
								duration_comparison_subscriber[1] += 1	
						else:
							pass
					else:
						pass
	
def googlemap_drive_duration(startPoint, endPoint, startYear, startMonth, startDay, startHour, startMinute, total_num, API_keys):
	
	day = DateChecker.func( startYear, startMonth, startDay )

	if int(startMonth) != 12:
		num_day_2018 = (date(2018, int(startMonth) + 1, 1) - date(2018, int(startMonth), 1)).days
		num_day_2017 = (date(2017, int(startMonth) + 1, 1) - date(2017, int(startMonth), 1)).days
	else:
		num_day_2018 = (date(2019, 1, 1) - date(2018, 12, 1)).days
		num_day_2017 = (date(2018, 1, 1) - date(2017, 12, 1)).days
		
	day_count_2018 = 0
	day_count_2017 = 0
	temp_2018 = []
	temp_2017 = []
	for j in range(num_day_2018):
		if DateChecker.func( 2018, int(startMonth), j + 1 ) == day:
			temp_2018.append( [] )
			temp_2018[day_count_2018].append(2018)
			temp_2018[day_count_2018].append(int(startMonth))
			temp_2018[day_count_2018].append(j + 1)
			day_count_2018 += 1
		else:
			pass
	week_num = 0	
	for j in range(num_day_2017):
		if DateChecker.func( 2017, int(startMonth), j + 1 ) == day:
			if j + 1 == int(startDay):
				week_num = day_count_2017 + 1
			else:
				pass
			temp_2017.append( [] )
			temp_2017[day_count_2017].append(2017)
			temp_2017[day_count_2017].append(int(startMonth))
			temp_2017[day_count_2017].append(j + 1)
			day_count_2017 += 1
		else:
			pass
	
	if day_count_2018 < day_count_2017:	
		startDay_2018 = temp_2018[week_num - 1][2]
	else:	
		startDay_2018 = temp_2018[week_num][2]

	startPoint = "Divvy Station: " + startPoint
	endPoint = "Divvy Station: " + endPoint
	departureDate = datetime(int(2018), int(startMonth), int(startDay_2018), int(startHour), int(startMinute), 0, 0)
	departureDate.isoformat()
	gmaps = Client(api_key)
	data = distance_matrix(gmaps, startPoint, endPoint, "driving", departure_time = departureDate)
	try:
		driving_duration = data['rows'][0]['elements'][0]['duration']['text']
		driving_duration_in_traffic = data['rows'][0]['elements'][0]['duration_in_traffic']['text']
		driving_distance = data['rows'][0]['elements'][0]['distance']['text']
		print (driving_distance)
	except KeyError:
		print ( data )
		driving_duration = str(0) + " mins"
		driving_duration_in_traffic = str(0) + " mins"
		driving_distance = str(0) + " km"
	google_API_data = [driving_duration, driving_duration_in_traffic, driving_distance, data]
	return google_API_data				
					
					
					
					
					
					
					
					
					
					
					
					
					
					
					
func()				
					
					
					
					
					
					
					
		