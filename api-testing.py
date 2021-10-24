import requests
import unittest

register = "https://wcg-apis.herokuapp.com/registration"
clear = "https://wcg-apis.herokuapp.com/citizen"


def create_new_citizen(address, birth_date, citizen_id, name, occupation, surname):
    """For create new citizen."""
    return {
        'address': address,
        'birth_date': birth_date,
        'citizen_id': citizen_id,
        'name': name,
        'occupation': occupation,
        'surname': surname
    }


class TestAPIService(unittest.TestCase):
    """Test /registration endpoint from WCG group project."""

    def setUp(self):
        """Initialize the citizen."""
        self.citizen1 = create_new_citizen(
            "kaosarn 666", "13-12-1970", "1234567890123", "kaopunzakung", "engineerzaza", "arwang")
        self.diff_citizen1 = create_new_citizen(
            "kaosarn 666", "13-12-1970", "3214567980132", "kaopunzakung", "engineerzaza", "arwang")

        requests.delete(clear, data=self.citizen1) # For delete the citizen1 information from wcg database.
        requests.delete(clear, data=self.diff_citizen1) # For delete the diff_citizen1 information from wcg database.

    def test_get_citizens_information(self):
        """Test the GET request of registration."""

        self.response = requests.get(register)
        self.assertEqual(self.response.status_code, 200)

    def test_new_register(self):
        """Test the POST request to create a new citizen registration."""

        self.response = requests.post(register, data=self.citizen1)
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(self.response.json(), {
            "feedback": "registration success!"
        })

    def test_invalid_citizen_id(self):
        """Test citizen_id that less and more than 13 digit can be registration."""

        less13_citizen = create_new_citizen(
            "404 nevada", "12-12-1969", "12345", "namee", "tester", "wong")
        self.response1 = requests.post(register, data=less13_citizen)
        self.assertEqual(self.response1.json(), {
                         'feedback': 'registration failed: invalid citizen ID'})
        more13_citizen = create_new_citizen(
            "400 NYC", "11-11-1978", "123456789012345", "molo", "tester", "wuu")
        self.response2 = requests.post(register, data=more13_citizen)
        self.assertEqual(self.response2.json(), {
                         'feedback': 'registration failed: invalid citizen ID'})

    def test_duplicate_citizen(self):
        """Test registration with information that already registered."""
        
        requests.delete(clear, data=self.citizen1)
        self.response1 = requests.post(register, data=self.citizen1)
        self.assertEqual(self.response1.json(), {
            "feedback": "registration success!"})
        self.response2 = requests.post(register, data=self.citizen1)
        self.assertEqual(self.response2.json(), {
            'feedback': 'registration failed: this person already registered'})

    def test_empty_info(self):
        """Test registration with empty information."""

        empty_citizen = create_new_citizen("", "", "", "", "", "")
        self.response = requests.post(register, data=empty_citizen)
        self.assertEqual(self.response.json(), {
                         'feedback': 'registration failed: missing some attribute'})

    def test_same_info_but_different_citizen_id(self):
        """Test registration with same information that has registered but change the citizen_id for new registration."""

        requests.delete(clear, data=self.citizen1)
        self.response1 = requests.post(register, data=self.citizen1)
        self.assertEqual(self.response1.json(), {
            "feedback": "registration success!"})
        self.response2 = requests.post(register, data=self.diff_citizen1)
        self.assertEqual(self.response2.json(), {
            'feedback': 'registration success!'})

    def test_same_citizen_id_but_different_name(self):
        """Test registration with same citizen_id that has registered but everything except citizen_id is different."""
        
        requests.delete(clear, data=self.citizen1)
        self.response1 = requests.post(register, data=self.citizen1)
        self.assertEqual(self.response1.json(), {
            "feedback": "registration success!"})
        same_id = create_new_citizen(
            "saparnput 666", "12-11-1907", "1234567890123", "kueaz", "black smith", "woo")
        self.response2 = requests.post(register, data=same_id)
        self.assertEqual(self.response2.json(), {
            'feedback': 'registration failed: this person already registered'})


if __name__ == '__main__':
    unittest.main()
