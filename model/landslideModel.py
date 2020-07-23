from abc import ABC
class LandslideData(ABC):
    def __init__(self, lat, lng, eventDate, size):
        self.lat = lat
        self.lng = lng
        self.eventData = eventDate
        self.size = size

class LandslideRecord(LandslideData):
    def __init__(self, record_id, lat, lng, eventDate, size, country, near, distance):
        self.record_id = record_id
        self.lat = lat
        self.lng = lng
        self.eventData = eventDate
        self.size = size
        self.country = country
        self.near = near
        self.distance = distance
    def printOut(self):
        print("Landslide record id ", self.record_id, " in ", self.country, ", near ", self.near, " with distance about ", self.distance , ". The correct location is [", self.lat, " : " , self.lng, "]")


class LandslideDownloadImageData(LandslideData):
    def __init__(self, startDate, endDate, cloudCover, station, downloadPath):
        self.startDate = startDate
        self.endData = endDate
        self.cloudCover = cloudCover
        self.station = station
        self.downloadPath = downloadPath