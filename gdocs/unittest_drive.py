import unittest


def random_string_gen(range1=12):
    import string
    import random
    return ''.join(random.choice(string.ascii_uppercase) for i in range(range1))

# fake json key for google authorisation
json_key = {
  "private_key_id": random_string_gen(),
  "private_key": "-----BEGIN PRIVATE KEY-----\n" + random_string_gen() + "\n" + random_string_gen() + "\n" +
                 random_string_gen() + "\n" + random_string_gen() + "\n" + random_string_gen() + "\n" +
                 random_string_gen() + "\n" + random_string_gen() + "\n" + random_string_gen() + "\n" +
                 random_string_gen() + "\n" + random_string_gen() + "\n" + random_string_gen() + "\n" +
                 random_string_gen() + "\n" + random_string_gen() + "\n" + random_string_gen() +
                 "\n-----END PRIVATE KEY-----\n",
  "client_email": random_string_gen(25) + "@developer.gserviceaccount.com",
  "client_id": random_string_gen(25) +  ".apps.googleusercontent.com",
  "type": "service_account"
}

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

    # def login_fail(self, random_str):
    #     """ The function is designed for failing the login in google drive (opposite of assertRaises).
    #         It uses random names to try to login.
    #     """
    #     from modify_drive import login_find_spreadsheet
    #     try:
    #         login_find_spreadsheet(random_str, random_str, random_string_gen(8))
    #         self.assertTrue(False)
    #     except RuntimeError:
    #         pass
    #     except:
    #         self.assertTrue(False)
    #
    # def test_modify_drive(self):
    #     from modify_drive import login_find_spreadsheet, form_cell
    #     self.assertRaises(ImportError, self.import_gspread()) # if gspread can be imported
    #     random_str = random_string_gen()
    #     self.login_fail(random_str)
    #     self.login_fail(random_str + '@yahoo.com')
    #     self.login_fail(random_str + '@googlemail.com')
    #     self.assertEqual(form_cell(1, 1), 'A1')
    #     self.assertEqual(1+1, 2)

    def fake_path(self):
        from modify_drive import Spreadsheets
        try:
            val = 1
            tr = Spreadsheets('/tmp/1.json')
        except ImportError:
            val = 10
        except:
            val = 0
        return val

    def test_login(self):
        from modify_drive import form_cell
        self.assertEqual(self.fake_path(), 10)
        self.assertEqual(form_cell(1, 1), 'A1')


class TestModifyDriveMock(unittest.TestCase):
    """
    Additional tests for the modify_drive package with the use of the mock package.
    Can be run with the TestModifyDrive by importing both of them with the code above.

    """
    import mock
    import gspread

    random_mail = random_string_gen() + '@googlemail.com'
    random_pass = random_string_gen(8)


    @mock.patch.object(gspread.httpsession.HTTPSession, 'post', autospec=True)
    def test_data_request(self, mock_post):
        """
        Ensure that the HTTP request is called and with the same mail as the one provided. This function
        makes a mock of the HTTPSession class in the gspread package.
        """
        # fake the login (gspread package)
        cl = self.gspread.client.Client(auth=(self.random_mail, self.random_pass))
        cl.login()

        self.assertTrue(mock_post.called)   # if the method didn't call the HTTPSession, then no request is made.

        calls = mock_post.mock_calls        # list of the calls made to the mock of HTTPSession.
        call_str = str(calls[0])

        mail_start = call_str.find('Email')
        self.assertFalse(mail_start == -1)        # assert if there is no mail field in the first call.
        mail_start += 9       # get rid of all the characters till the beginning of the real mail.
        mail_end = call_str[mail_start:].find(', ') - 1
        # ensure that the mail provided is the same with the one in the HTTP request.
        self.assertEqual(call_str[mail_start:mail_start + mail_end], self.random_mail)



if __name__ == '__main__':
    unittest.main()