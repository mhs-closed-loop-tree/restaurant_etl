import unittest
import pre_process


class TestMapMethod(unittest.TestCase):

    def test_map_near_empty(self):
        row = ['7', '', '', '', '', '', '', '', '', '',
               '', '', '', '', '', '', '', '', '']
        res = pre_process.map(row)
        self.assertIsNotNone(res)
        self.assertEqual(res['camis'], 7)

    def test_map_alignment(self):
        row = ['2', 'dba', 'boro', 'building', 'street', 'zipcode',
               'phone', 'cuisine description', 'inspection_date',
               'action', 'violation code', 'violation description',
               'critical flag', 'score', 'grade', 'grade date',
               'record date', 'inspection type']

        expected = {
            "camis": 2,
            "dba": 'Dba',
            "boro": 'Boro',
            "building": 'Building',
            "street": 'Street',
            "zipcode": 'zipcode',
            "phone": 'phone',
            "cuisine_description": 'Cuisine Description',
            "inspection_date": 'inspection_date',
            "action": 'action',
            "violation_code": 'violation code',
            "violation_description": 'violation description',
            "critical_flag": 'critical flag',
            "score": 'score',
            "grade": 'grade',
            "grade_date": 'grade date',
            "record_date": 'record date',
            "inspection_type": 'inspection type'
        }
        res = pre_process.map(row)
        self.assertEqual(res, expected)

    def test_map_titlecase(self):
            row = ['2', 'UPPER', 'lower', 'spaced words', 'apost\'s stay',
                   '', '', '', '', '', '', '', '', '', '', '', '', '']

            res = pre_process.map(row)
            self.assertEqual(res['dba'], 'Upper')
            self.assertEqual(res['boro'], 'Lower')
            self.assertEqual(res['building'], 'Spaced Words')
            self.assertEqual(res['street'], 'Apost\'s Stay')

    def test_map_encoding(self):
            row = ['2', '', '', '', '', '', '', '', '', '', '',
                   '38 ÂºF', '', '', '', '', '', '']
            res = pre_process.map(row)
            self.assertEqual(res['violation_description'], '38 ºF')


if __name__ == '__main__':
    unittest.main()
