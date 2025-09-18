import unittest
from chronofidelius.__init__ import ChronoFidelius

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

    def test_encrypt_homophonic_even_mix_code(self):
        obj = ChronoFidelius(self.plaintext, set_seed=self.seed, include_errors=False)
        obj.encrypt_homophonic(key_type="even", mix_code=True)
        ct_dict = obj.pt_ct_dict["key_even_len_2_1opt"]
        # Assert vowels get different length codes than consonants
        self.assertTrue(all(len(code[0]) == 3 for v, code in ct_dict.items() if v in obj.vowels))
        self.assertTrue(all(len(code[0]) == 2 for c, code in ct_dict.items() if c not in obj.vowels))

    def test_encrypt_homophonic_uneven_number_allocation(self):
        freq_dict = {"A": 0.1, "B": 0.2, "C": 0.3, "D": 0.4, "E": 0.5}
        self.test_obj.encrypt_homophonic(key_type="uneven", set_frequencies=freq_dict)
        enc_dict = self.test_obj.pt_ct_dict["key_uneven_len_2_uneven"]

        all_nums = [num for codes in enc_dict.values() for num in codes]
        self.assertEqual(len(all_nums), len(set(all_nums)))  # no duplicates

    def test_encrypt_homophonic_even_distribution(self):
        """
        Test that even key encryption distributes numbers correctly.
        Checks that each character in the plaintext has codes in the key and
        that ciphertext length matches the plaintext including errors.
        """
        obj = ChronoFidelius(
            "helloWorld",
            include_errors=True,
            error_type="additions",
            set_seed=9
        )
        obj.encrypt_homophonic(key_type="even", mix_code=True)

        key_dict_name = "key_even_len_4_5opt"
        self.assertIn(key_dict_name, obj.pt_ct_dict)

        key_dict = obj.pt_ct_dict[key_dict_name]
        pt_chunk = obj.pt_ct_dict["0"]["plaintext_errors_included"]

        for char in set(pt_chunk):
            self.assertIn(char, key_dict)
            self.assertGreater(len(key_dict[char]), 0)

        ct = obj.pt_ct_dict["0"]["ciphertext_even_len_4_5opt"]
        self.assertEqual(len(ct), len(pt_chunk))


if __name__ == "__main__":
    unittest.main()
