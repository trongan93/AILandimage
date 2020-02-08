"""
This file is to do the File processing.
Include Class for Raw file image data
"""
import numpy as np
class FileRawData:
    """
    Raw file image processing
    """
    def __init__(self):
        super().__init__()
        self._dir_path = "/mnt/2A967D2D967CFB21/ProjectData/CubeSAT/"
    
    def __init__(self, dir_path):
        super().__init__()
        self._dir_path = dir_path

    def save_feature_raw_image(self, file_name, feature_raw_data):
        """
        save feature raw image data to file
        """
        # print(feature_raw_data.flags)
        # print(feature_raw_data.shape)
        feature_raw_data = feature_raw_data.copy(order='C')
        dir_path = self._dir_path + "/" + file_name + ".raw"
        raw_image_file = open(dir_path, 'wb')
        raw_image_file.write(feature_raw_data)
        raw_image_file.close()
        return 1
    
    def read_feature_raw_image(self, file_name, img_size):
        """
        read feature raw image data from file
        """
        dir_path = self._dir_path + "/" + file_name + ".raw"
        feature_data = np.fromfile(dir_path, np.uint8)
        # print(feature_data.shape)
        feature_data = np.reshape(np.fromfile(dir_path, np.uint8), img_size)
        return feature_data
    