import unittest

from prosody_console.commands import Muc

class MucTestCase(unittest.TestCase):

    def test_create(self):
        self.assertEqual(Muc.create("room@example.com").show(), "muc:create('room@example.com')")

    def test_set_affiliation(self):
        self.assertEqual(Muc.set_affiliation("room@example.com", "user@example.com", Muc.Affiliation.member).show(),
                         "muc:room('room@example.com'):set_affiliation(true, 'user@example.com', 'member')")

    def test_destroy(self):
        self.assertEqual(Muc.destroy("room@example.com").show(),
                        "muc:room('room@example.com'):destroy()")

    def test_save(self):
        self.assertEqual(Muc.save_function("room@example.com", True).show(),
                        "muc:room('room@example.com'):save(muc:room('room@example.com'), true)")


if __name__ == '__main__':
    unittest.main()
