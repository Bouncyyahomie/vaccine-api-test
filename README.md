# Vaccine api-test registration API from WCG Group 

   
## List of Test Cases for Registration

| ID | Name                                                          | Description                                                                                                          | Status |
|----|---------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------|--------|
| 1  | test_create_new_citizen                                       | Test the POST request to create a new citizen registration.                                                          | Pass   |
| 2  | test_get_citizens_information                                 | Test the GET request of registration.                                                                                | Pass   |
| 3  | test_get_citizens_information_with_invalid_citizen_id         | Test the GET request of registration with invalid_citizen_id.                                                        | Pass   |
| 4  | test_get_citizens_information_with_invalid_format_citizen_id  | Test the GET request of registration with invalid format citizen_id.                                                 | Pass   |
| 5  | test_post_citizen_id_less_than_13_digits                      | Test the POST request to create a new citizen registration with less than 13 digits citizen_id.                      | Pass   |
| 6  | test_post_citizen_id_more_than_13_digits                      | Test the POST request to create a new citizen registration with more than 13 digits citizen_id.                      | Pass   |
| 7  | test_duplicate_citizen                                        | Test the POST request to create a new citizen that already exists.                                                   | Pass   |
| 8  | test_empty_info                                               | Test the POST request to create a new citizen with empty information.                                                | Pass   |
| 9  | test_same_info_but_different_citizen_id                       | Test to registration with same information that has already register but change the citizen_id for new registration. | Pass   |
| 10 | test_same_citizen_id_but_different_name                       | Test registration with same citizen_id that has already registered but everything except citizen_id is different.    | Pass   |
| 11 | test_delete_citizen_information                               | Test removing citizen information                                                                                    | Pass   |
| 12 | test_delete_citizen_information_with_invald_citizen_id        | Test removing citizen information with invalid citizen_id                                                            | Pass   |
| 13 | test_delete_citizen_information_with_invald_format_citizen_id | Test removing citizen information with invalid citizen_id                                                            | Pass   |