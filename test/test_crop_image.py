import unittest
import sys
sys.path.append(".")

from crop_image import *

class TestCropImage(unittest.TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass

    def test_get_impact_size(self):
        """
        Test that the impact size enum can be got from valid string
        """
        data = ["VERY_SMALL", "SMALL", "MEDIUM", "LARGE", "VERY_LARGE"]
        for impact in data:
            with self.subTest(impact=impact):
                result = get_impact_size(impact)
                self.assertEqual(LANDSLIDE_IMPACT_SIZE(result).value, LANDSLIDE_IMPACT_SIZE[impact].value)

    def test_get_rect(self):
        """
        Test that the image is cropped correctly according to the center point and the size to be cropped
        """
        blank_image = np.zeros((7500, 7900, 3), np.uint8)
        row, col = 400, 400
        size = (700, 700)
        expected_shape = (700, 700, 3)

        cropped_image = get_rect(blank_image, row, col, size)

        self.assertEqual(cropped_image.shape, expected_shape)

if __name__ == "__main__":
    unittest.main()