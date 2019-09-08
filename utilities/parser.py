import datetime

def parse_date(date):
    """
    Parse date with format yyyymmdd
    """
    year_start = int(date[0:4])
    month_start = int(date[4:6])
    day_start = int(date[6:8])
    parsed = datetime.datetime(year_start, month_start, day_start)

    return parsed
