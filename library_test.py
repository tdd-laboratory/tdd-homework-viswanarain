import unittest
import library

NUM_CORPUS = '''
On the 5th of May every year, Mexicans celebrate Cinco de Mayo. This tradition
began in 1845 (the twenty-second anniversary of the Mexican Revolution), and
is the 1st example of a national independence holiday becoming popular in the
Western Hemisphere. (The Fourth of July didn't see regular celebration in the
US until 15-20 years later.) It is celebrated by 77.9% of the population--
trending toward 80.                                                                
'''

class TestCase(unittest.TestCase):

    # Helper function
    def assert_extract(self, text, extractors, *expected):
        actual = [x[1].group(0) for x in library.scan(text, extractors)]
        self.assertEquals(str(actual), str([x for x in expected]))

    # First unit test; prove that if we scan NUM_CORPUS looking for mixed_ordinals,
    # we find "5th" and "1st".
    def test_mixed_ordinals(self):
        self.assert_extract(NUM_CORPUS, library.mixed_ordinals, '5th', '1st')

    # Second unit test; prove that if we look for integers, we find four of them.
    def test_integers(self):
        self.assert_extract(NUM_CORPUS, library.integers, '1845', '15', '20', '80')

    # Third unit test; prove that if we look for integers where there are none, we get no results.
    def test_no_integers(self):
        self.assert_extract("no integers", library.integers)

    # Fourth unit test; prove that we correctly extract date format like "2015-07-25"
    def test_dates(self):
        self.assert_extract('I was born on 2015-07-25.', library.dates_iso8601, '2015-07-25')

    # Fifth unit test; prove that out of bound date and month values are handled
    def test_invalid(self):
        self.assert_extract("I was born on 2015-13-32 ", library.dates_iso8601)

    # Sixth unit test; prove that we correctly extract date format like "25 Jan 2017"
    def test_dates_fmt2(self):
        self.assert_extract('I was born on 25 Jan 2017.', library.dates_fmt2, '25 Jan 2017')

    # Seventh unit test; prove that input for out of bound year is getting handled
    def test_dates_fmt3(self):
        self.assert_extract('I was born on 10000-03-01.', library.dates_iso8601,'10000-03-01')

    # Eight unit test; prove that timestamp separated by space delimiter is handled
    def test_dates_fmt4(self):
        self.assert_extract("The timestamp is 2018-06-22 18:22:19.123.", library.dates_iso8601, '2018-06-22 18:22:19.123')

    # Ninth unit test; prove that timestamp having a delimiter 'T' between date and time portion is handled
    def test_dates_fmt5(self):
        self.assert_extract("The timestamp is 2018-06-22T18:22:19.123.", library.dates_iso8601, '2018-06-22T18:22:19.123')

    # Tenth unit test; prove that the out of bound value for hour is handled
    def test_time_fmt1(self):
        self.assert_extract("The timestamp is 2018-06-22T25:22:19.123.", library.dates_iso8601, '2018-06-22T25:22:19.123')

    # Eleventh unit test; prove that the out of bound value for minutes is handled
    def test_time_fmt2(self):
        self.assert_extract("The timestamp is 2018-06-22T23:64:19.123.", library.dates_iso8601, '2018-06-22T23:64:19.123')

    # Twelveth unit test; prove that the out of bound value for seconds is handled
    def test_time_fmt3(self):
        self.assert_extract("The timestamp is 2018-06-22T23:19:62.123.", library.dates_iso8601, '2018-06-22T23:19:62.123')

    # Thirteenth unit test; prove that time format like "hhmmss" is getting handled
    def test_time_fmt4(self):
        self.assert_extract('I was born at 180003 ', library.dates_iso8601, '180003')

    # Fourteenth unit test; prove that timestamp for zulu timezone is handled
    def test_time_fmt5(self):
        self.assert_extract('The Zulu timezone is 2018-06-21T04:17:48Z.', library.dates_iso8601, '2018-06-21T04:17:48Z')

    # Fifteenth unit test; prove that timestamp for MDT timezone is handled
    def test_time_fmt6(self):
        self.assert_extract('The MDT timezone is 2018-06-21T04:17:48MDT ', library.dates_iso8601, '2018-06-21T04:17:48MDT')

    # Sixteenth unit test; prove that timestamp containing UTC offset is handled
    def test_time_fmt7(self):
        self.assert_extract('The UTC offset equivalent of MDT is is 2018-06-21T04:17:48+00.00.', library.dates_iso8601,'2018-06-21T04:17:48+00.00')

    # Seventeenth unit test; prove that an invalid time zone is handled
    def test_time_fmt8(self):
        self.assert_extract('The MDT timezone is 2018-06-21T04:17:48MDTS ', library.dates_iso8601, '2018-06-21T04:17:48MDTS')

    # Eighteenth unit test; prove that the date format '25 Jun, 2017' is handled
    def test_dates_fmt6(self):
        self.assert_extract('I was born on 25 Jun, 2017 ', library.dates_fmt2, '25 Jun, 2017')

    # Ninteenth unit test; prove that numbers are extracted as comma seperated values
    def test_numbers_fmt1(self):
        self.assert_extract('Income of bob in rupees is 123,456,789', library.numbers_fmt1, '123,456,789')


if __name__ == '__main__':
    unittest.main()
