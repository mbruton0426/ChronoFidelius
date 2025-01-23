import unittest
from __init__ import ChronoFidelius

class TestChronoFidelius(unittest.TestCase):

    def setUp(self):
        """
        Set up common resources for the test cases.
        """
        self.plaintext = "HELLO WORLD"
        self.seed = 42
        self.error_type = "additions"
        self.error_frequency = 0.1
        self.test_obj = ChronoFidelius(
            plaintext=self.plaintext,
            set_seed=self.seed,
            include_errors=True,
            error_type=self.error_type,
            error_frequency=self.error_frequency
        )

    def test_init(self):
        """
        Test the initialization of the class.
        """
        self.assertEqual(self.test_obj.plaintext, self.plaintext.upper())
        self.assertEqual(self.test_obj.seed, self.seed)
        self.assertIn("0", self.test_obj.pt_ct_dict)
        self.assertIn("plaintext", self.test_obj.pt_ct_dict["0"])
        self.assertEqual(self.test_obj.pt_ct_dict["0"]["plaintext"], "HELLOWORLD")

    def test_encrypt_homophonic_even(self):
        """
        Test the even encryption method.
        """
        self.test_obj.encrypt_homophonic(key_type="even")
        self.assertIn("key_even_len_2_1opt", self.test_obj.pt_ct_dict)
        self.assertIn("plaintext", self.test_obj.pt_ct_dict["0"])

    def test_encrypt_homophonic_uneven(self):
        """
        Test the uneven encryption method with a frequency dictionary.
        """
        freq_dict = {"A": 0.1, "B": 0.2, "C": 0.3, "D": 0.4, "E": 0.5}
        self.test_obj.encrypt_homophonic(key_type="uneven", set_frequencies=freq_dict)
        self.assertIn("key_uneven_len_2_uneven", self.test_obj.pt_ct_dict)

    def test_encrypt_homophonic_both(self):
        """
        Test the both (even + uneven) encryption method.
        """
        freq_dict = {"A": 0.1, "B": 0.2, "C": 0.3, "D": 0.4, "E": 0.5}
        self.test_obj.encrypt_homophonic(
            key_type="both", set_frequencies=freq_dict, set_alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        )
        self.assertIn("key_even_len_2_1opt", self.test_obj.pt_ct_dict)
        self.assertIn("key_uneven_len_2_uneven", self.test_obj.pt_ct_dict)

    def test_invalid_inputs(self):
        """
        Test invalid inputs to ensure proper error handling in public methods.
        """
        # Invalid plaintext type
        with self.assertRaises(TypeError):
            ChronoFidelius(plaintext=123)

        # Invalid error type
        with self.assertRaises(ValueError):
            ChronoFidelius(
                plaintext="HELLO",
                include_errors=True,
                error_type="invalid_type"
            )

        # Invalid key_type for encrypt_homophonic
        with self.assertRaises(ValueError):
            self.test_obj.encrypt_homophonic(key_type="invalid_key_type")

if __name__ == "__main__":
    unittest.main()
