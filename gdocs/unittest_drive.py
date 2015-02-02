import unittest

class TestModifyDrive(unittest.TestCase):
    """
    Tests for checking the basic elementary functions of the modify_drive.py
    call like this:
    import unittest, sys; sys.path.append('path');
    from  unittest_drive import TestModifyDrive
    suite = unittest.TestLoader().loadTestsFromTestCase(TestModifyDrive); unittest.TextTestRunner(verbosity=2).run(suite)

    Copyright (C) 2015 Grigorios G. Chrysos
    available under the terms of the Apache License, Version 2.0
    """

    def import_gspread(self):
        try:
            import gspread
        except:
            raise ImportError('gspread does not exist, but it is required.')

    def random_string_gen(self, range1=12):
        import string
        import random
        return ''.join(random.choice(string.ascii_uppercase) for i in range(range1))

    def login_fail(self, random_str):
        """ The function is designed for failing the login in google drive (opposite of assertRaises).
            It uses random names to try to login.
        """
        from modify_drive import login_find_spreadsheet
        try:
            login_find_spreadsheet(random_str, random_str, self.random_string_gen(8))
            self.assertTrue(False)
        except RuntimeError:
            pass
        except:
            self.assertTrue(False)

    def test_modify_drive(self):
        from modify_drive import login_find_spreadsheet, form_cell
        self.assertRaises(ImportError, self.import_gspread()) # if gspread can be imported
        random_str = self.random_string_gen()
        self.login_fail(random_str)
        self.login_fail(random_str + '@yahoo.com')
        self.assertEqual(form_cell(1, 1), 'A1')
        self.assertEqual(1+1, 2)


if __name__ == '__main__':
    unittest.main()