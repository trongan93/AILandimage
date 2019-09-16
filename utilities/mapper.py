def map_metadata_fieldname_to_general_name():
    """
    Map metadata fieldname and the corresponding satellite with user defined field name
    """
    mapper = dict()
    
    mapper[('LC08', 'WRS_PATH')] = 'WRS_PATH'
    mapper[('LC08', 'WRS_ROW')] = 'WRS_ROW'
    mapper[('LC08', 'CLOUDCOVER')] = 'CLOUD_COVER'

    mapper[('LE07', 'WRS_PATH')] = 'WRS_PATH'
    mapper[('LE07', 'WRS_ROW')] = 'WRS_ROW'
    mapper[('LE07', 'CLOUDCOVER')] = 'CLOUD_COVER'

    mapper[('LT05', 'WRS_PATH')] = 'WRS_PATH'
    mapper[('LT05', 'WRS_ROW')] = 'WRS_ROW'
    mapper[('LT05', 'CLOUDCOVER')] = 'CLOUD_COVER'

    return mapper