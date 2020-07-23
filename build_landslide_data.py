from model.landslideModel import LandslideRecord, LandslideDownloadImageData

import pandas as pd

def countByLandslideSize(landslideRecords):
    print(len(landslideRecords))
    countLarge = countMedium = countVerLarge = countSmall = countOther = 0
    for record in landslideRecords:
        if record.size == "Medium":
            countMedium += 1
        elif record.size == "Large":
            countLarge += 1
        elif record.size == "Very_large":
            countVerLarge += 1
        elif record.size == "Small":
            countSmall += 1
        else:
            countOther +=1
    print("Landslide number of Small size: ", countSmall)
    print("Landslide number of Medium size: ", countMedium)
    print("Landslide number of Large size: ", countLarge)
    print("Landslide number of Very large size: ", countVerLarge)
    print("Landslide number of another size: ", countOther)


def readRecordData(input_file):
    glc_data = pd.read_csv(input_file)
    # print(glc_data.shape)
    landslides = []
    for index, recordItem in glc_data.iterrows():
        landslideRecord = LandslideRecord(record_id=recordItem['id'], lat=recordItem['latitude'], lng=recordItem['longitude'],
                                          eventDate=recordItem['date_'], size=recordItem['landslide1'],
                                          country=recordItem['countrynam'], near=recordItem['near'], distance=recordItem['distance'])
        # landslideRecord.printOut()
        landslides.append(landslideRecord)
    return landslides

if __name__ == "__main__":
    input_path_from_glcdata = "./landslidedata.csv"
    landslideRecords = readRecordData(input_path_from_glcdata)
    countByLandslideSize(landslideRecords)