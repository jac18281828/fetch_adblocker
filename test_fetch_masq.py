import unittest
from unittest.mock import patch
from fetch_masq import read, blacklist, whitelist, is_excluded

class FetchMasqTestCase(unittest.TestCase):

    def setUp(self):
        # Clear the blacklist and whitelist before each test
        blacklist.clear()
        whitelist.clear()

    def test_read(self):
        # Mock the urllib.request.urlopen function to return a predefined response
        with patch('urllib.request.urlopen') as mock_urlopen:
            mock_response = [
                b'0.0.0.0 example.com\n',
                b'0.0.0.0 google.com\n',
                b'0.0.0.0 facebook.com\n',
            ]
            mock_urlopen.return_value.__enter__.return_value = mock_response

            # Call the read function
            host_set = read()

            # Assert that the expected hosts are added to the host_set
            expected_host_set = {'example.com', 'google.com', 'facebook.com'}
            self.assertEqual(host_set, expected_host_set)

    def test_is_excluded(self):
        whitelist.add('example.com')
        # Test a host that should be excluded based on the whitelist
        self.assertTrue(is_excluded('example.com'))
        self.assertTrue(is_excluded('fair.example.com'))

        # Test a host that should not be excluded based on the whitelist
        self.assertFalse(is_excluded('example.org'))

        # Test a host that contains non-ASCII characters
        self.assertTrue(is_excluded('résumé.com'))

    def test_blacklist_and_whitelist(self):
        # Add entries to the blacklist and whitelist
        blacklist.add('example.com')
        whitelist.add('example.org')

        # Call the read function with a mock host_url
        with patch('urllib.request.urlopen'):
            host_set = read('mock_host_url')

            # Assert that the blacklisted host is added to the host_set
            self.assertIn('example.com', host_set)

            # Assert that the whitelisted host is not added to the host_set
            self.assertNotIn('example.org', host_set)

    def test_read_with_comments(self):
        # Mock the urllib.request.urlopen function to return a predefined response
        with patch('urllib.request.urlopen') as mock_urlopen:
            mock_response = [
                b'# This is a comment\n',
                b'0.0.0.0 example.com # more comments\n',
                b'0.0.0.0 google.com\n',
                b'0.0.0.0 facebook.com\n',
            ]
            mock_urlopen.return_value.__enter__.return_value = mock_response

            # Call the read function
            host_set = read()

            # Assert that the expected hosts are added to the host_set
            expected_host_set = {'example.com', 'google.com', 'facebook.com'}
            self.assertEqual(host_set, expected_host_set)

    def test_read_nx_domain_prohibited(self):
        # Mock the urllib.request.urlopen function to return a predefined response
        with patch('urllib.request.urlopen') as mock_urlopen:
            mock_response = [
                b'0.0.0.0 0.0.0.0\n',
                b'0.0.0.0 a.com\n',
                b'0.0.0.0 0.0.0.0.b.com\n',
            ]
            mock_urlopen.return_value.__enter__.return_value = mock_response

            # Call the read function
            host_set = read()

            # Assert that the expected hosts are added to the host_set
            expected_host_set = {'a.com', '0.0.0.0.b.com'}
            self.assertEqual(host_set, expected_host_set)


if __name__ == '__main__':
    unittest.main()