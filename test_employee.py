import unittest
from employee import Employee
from unittest.mock import patch

class TestEmployee(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('setUpClass')

    @classmethod
    def tearDownClass(cls):
        print('tearDownClass')

    # this set up is to create two employees before every test
    def setUp(self):
        print('setUp')
        self.emp_1 = Employee('Alvin', 'Escobar', 50000)
        self.emp_2 = Employee('Elvis', 'Pazmino', 60000)

    # to remove whatever data you had to start fresh on a new test
    def tearDown(self):
        print('tearDown\n')

    def test_email(self):
        print('test_email')
        self.assertEqual(self.emp_1.email, 'Alvin.Escobar@email.com')
        self.assertEqual(self.emp_2.email, 'Elvis.Pazmino@email.com')

        self.emp_1.first = 'John'
        self.emp_2.first = 'Jane'

        self.assertEqual(self.emp_1.email, 'John.Escobar@email.com')
        self.assertEqual(self.emp_2.email, 'Jane.Pazmino@email.com')

    def test_fullname(self):
        print('test_fullname')
        self.assertEqual(self.emp_1.fullname, 'Alvin Escobar')
        self.assertEqual(self.emp_2.fullname, 'Elvis Pazmino')

        self.emp_1.first = 'John'
        self.emp_2.first = 'Jane'

        self.assertEqual(self.emp_1.fullname, (self.emp_1.first + ' ' + self.emp_1.last))
        self.assertEqual(self.emp_2.fullname, (self.emp_2.first + ' ' + self.emp_2.last))

    def test_apply_raise(self):
        print('test_apply_raise')
        self.emp_1.apply_raise()
        self.emp_2.apply_raise()

        self.assertEqual(self.emp_1.pay, 50000*Employee.raise_amount)
        self.assertEqual(self.emp_2.pay, 60000*Employee.raise_amount)

    # ------ MOCKING -------
    # This is where if a website is down or not working
    # even though the GET method was called with the right url
    # and that our code behaves correctly whether the response is ok or not ok
    def test_monthly_schedule(self):
        with patch('employee.requests.get') as mocked_get:
            mocked_get.return_value.ok = True
            mocked_get.return_value.text = 'Success'

            schedule = self.emp_1.monthly_schedule('May')
            mocked_get.assert_called_with('http://company.com/Escobar/May')
            self.assertEqual(schedule, mocked_get.return_value.text)

            mocked_get.return_value.ok = False

            schedule = self.emp_2.monthly_schedule('June')
            mocked_get.assert_called_with('http://company.com/Pazmino/June')
            self.assertEqual(schedule, 'Bad response!')

if __name__ == '__main__':
    unittest.main()
