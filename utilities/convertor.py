import datetime

def utc_to_normal_date(dateStr):
	return convert_datestr_to_normal_date(dateStr, "%m/%d/%Y %I:%M:%S %p %z")

def convert_datestr_to_normal_date(dateStr, format):
	dateObj = datetime.datetime.strptime(dateStr, format)
	return f'{str(dateObj.year).zfill(4)}{str(dateObj.month).zfill(2)}{str(dateObj.day).zfill(2)}'

def convert_date_to_normal_date_str(dateObj: datetime):
	return f'{str(dateObj.year).zfill(4)}{str(dateObj.month).zfill(2)}{str(dateObj.day).zfill(2)}'

def get_date(dateStr, format):
	return datetime.datetime.strptime(dateStr, format)

def get_utc_date(dateStr):
	return get_date(dateStr, "%m/%d/%Y %I:%M:%S %p %z")

# print(utcToNormalDate("03/07/2011 08:00:00 AM +0000"))