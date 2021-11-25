import requests
import unittest
from decouple import config


URL = config("URL")

def create_new_citizen(address, birth_date, citizen_id, name, occupation, surname, phone_number, is_risk):
    """For create new citizen."""
    return {
        'citizen_id': citizen_id,
        'name': name,
        'surname': surname,
        'birth_date': birth_date,
        'occupation': occupation,
        'phone_number': phone_number,
        'is_risk': is_risk,
        'address': address,
    }
    

class TestRegistration(unittest.TestCase):
    """Test /registration endpoint from WCG group project."""

    def setUp(self):
        """Initialize the citizen."""
        self.citizen1 = create_new_citizen(
            "kaosarn 666", "13-12-1970", "1234567890123", "kaopunzakung", "engineerzaza", "arwang","0980000000","False")
        self.diff_citizen1 = create_new_citizen(
            "kaosarn 666", "13-12-1970", "3214567980132", "kaopunzakung", "engineerzaza", "arwang","0980000001","False")

        self.citizen_id1 = self.citizen1.get("citizen_id")
        self.diff_citizen_id1 = self.diff_citizen1.get("citizen_id")
        requests.delete(f"{URL}/{self.citizen_id1}") # For delete the citizen1 information from wcg database.
        requests.delete(f"{URL}/{self.diff_citizen_id1}")  # For delete the diff_citizen1 information from wcg database.


    def test_create_new_citizen(self):
        """Test the POST request to create a new citizen registration."""
        
        response = requests.post(URL, data=self.citizen1)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['feedback'], "registration success!")
        
        
    def test_get_citizens_information(self):
        """Test the GET request of registration."""
        
        requests.post(URL, data=self.citizen1)
        response = requests.get(f"{URL}/{self.citizen_id1}")
        self.assertEqual(response.status_code, 200)
        
    def test_get_citizens_information_with_invalid_citizen_id(self):
        """Test the GET request of registration with invalid_citizen_id."""
        
        requests.post(URL, data=self.citizen1)
        citizen_id = "123"
        response = requests.get(f"{URL}/{citizen_id}")
        self.assertEqual(response.status_code, 404)

    def test_get_citizens_information_with_invalid_format_citizen_id(self):
        """Test the GET request of registration with invalid format citizen_id."""
        
        requests.post(URL, data=self.citizen1)
        citizen_id = "check"
        response = requests.get(f"{URL}/{citizen_id}")
        self.assertEqual(response.status_code, 404)

    def test_post_citizen_id_less_than_13_digits(self):
        """"Test the POST request to create a new citizen registration with less than 13 digits citizen_id."""

        less13_citizen = create_new_citizen(
            "404 nevada", "12-12-1969", "12345", "namee", "tester", "wong","0672839461","False")
        response = requests.post(URL, data=less13_citizen)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['feedback'], 'registration failed: invalid citizen ID')
        
        
    def test_post_citizen_id_more_than_13_digits(self):
        """"Test the POST request to create a new citizen registration with more than 13 digits citizen_id."""
        
        more13_citizen = create_new_citizen(
            "400 NYC", "11-11-1978", "123456789012345", "molo", "tester", "wuu","0857402848","False")
        response = requests.post(URL, data=more13_citizen)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['feedback'], 'registration failed: invalid citizen ID')

    def test_duplicate_citizen(self):
        """Test the POST request to create a new citizen that already exists."""
        
        requests.delete(f"{URL}/{2567890354786}")
        dup_citzen = create_new_citizen("500 LA", "06-06-2000", "2567890354786", "mark", "tester", "sosorry", "0876473254", "False")
        response1 = requests.post(URL, dup_citzen)
        self.assertEqual(response1.status_code, 201)
        self.assertEqual(response1.json()['feedback'], "registration success!")
        response2 = requests.post(URL, dup_citzen)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(response2.json()['feedback'], "registration failed: this person already registered")


    def test_empty_info(self):
        """Test the POST request to create a new citizen with empty information."""

        empty_citizen = create_new_citizen("", "", "", "", "", "","","")
        response = requests.post(URL, data=empty_citizen)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['feedback'], 'registration failed: missing some attribute')


    def test_same_info_but_different_citizen_id(self):
        """Test to registration with same information that has already registered but change the citizen_id for new registration."""

        requests.delete(f"{URL}/{self.citizen_id1}") 
        requests.delete(f"{URL}/{self.diff_citizen_id1}") 
        response1 = requests.post(URL, data=self.citizen1)
        self.assertEqual(response1.status_code, 201)
        self.assertEqual(response1.json()['feedback'], "registration success!")
        response2 = requests.post(URL, data=self.diff_citizen1)
        self.assertEqual(response1.status_code, 201)
        self.assertEqual(response1.json()['feedback'], "registration success!")

    def test_same_citizen_id_but_different_name(self):
        """Test registration with same citizen_id that has already registered but everything except citizen_id is different."""
        
        requests.delete(f"{URL}/{self.citizen_id1}") 
        response1 = requests.post(URL, data=self.citizen1)
        self.assertEqual(response1.status_code, 201)
        self.assertEqual(response1.json()['feedback'], "registration success!")
        same_id = create_new_citizen(
            "saparnput 666", "12-11-1907", "1234567890123", "kueaz", "black smith", "woo","0936401495","False")
        response2 = requests.post(URL, data=same_id)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(response2.json()['feedback'], "registration failed: this person already registered")
        
    def test_delete_citizen_information(self):
        """Test removing citizen information"""
        
        citizen = create_new_citizen("310/14 Lumpini", "05-06-2000", "7564835183641", "Icezu", "Sharp shooter", "krasoon", "0628391631", "False")
        response = requests.post(URL, data=citizen)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['feedback'], "registration success!")
        citizen_id = citizen.get("citizen_id")
        response = requests.delete(f"{URL}/{citizen_id}") 
        self.assertEqual(response.status_code, 200)
        
    def test_delete_citizen_information_with_invald_citizen_id(self):
        """Test removing citizen information with invalid citizen_id"""
        
        citizen_id = "6666666666666"
        response = requests.delete(f"{URL}/{citizen_id}") 
        self.assertEqual(response.status_code, 404)
        
    def test_delete_citizen_information_with_invald_format_citizen_id(self):
        """Test removing citizen information with invalid citizen_id"""
        
        citizen_id = "delete"
        response = requests.delete(f"{URL}/{citizen_id}") 
        self.assertEqual(response.status_code, 404)
        
if __name__ == '__main__':
    unittest.main()
