"""
Module tests
"""
import os
import sys
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
try:
    import jumany
except ImportError:
    import python_module as jumany

def get_jumanrc():
    """ Get testable jumanrc """
    mod_dir = os.path.join(os.path.dirname(__file__), "..")
    candidates = [
        os.path.join(mod_dir, "jumanrc"),
        os.path.join(mod_dir, "../dist/juman-7.01_ext_win64/jumanrc"),
    ]
    for rc in candidates:
        if os.path.exists(rc):
            return rc
    return None

_TEST_STR = "吾輩は猫である。"
_TEST_EXPECT = [
    ("吾輩", "名詞"), ("は", "助詞"), ("猫", "名詞"), ("である", "判定詞"), ("。", "特殊")
]

class test_jumany_open(unittest.TestCase):
    """ test open and close"""
    def test_open_fail(self):
        """  Fail to jumany.open_lib()    """
        jumany.close_lib()
        self.assertFalse(jumany.open_lib("hoge"))
        msg = jumany.get_error_msg()
        self.assertTrue(len(msg) > 0)

    def test_open_success(self):
        """  Success to jumany.open_lib()    """
        jumanrc = get_jumanrc()
        self.assertTrue(jumany.open_lib(jumanrc))
        msg = jumany.get_error_msg()
        self.assertTrue(len(msg) == 0)
        jumany.close_lib()

class test_jumany_main(unittest.TestCase):
    """ For jumany main"""

    def setUp(self):
        jumanrc = get_jumanrc()
        jumany.open_lib(jumanrc)

    def tearDown(self):
        #jumany.close_lib()
        pass

    def test_analyze_normal(self):
        """  jumany.analyze() in nomal use  """
        res = jumany.analyze(_TEST_STR)
        self.assertEqual(len(_TEST_EXPECT), len(res))
        self.assertEqual(7, len(res[0]))
        for expect, result in zip(_TEST_EXPECT, res):
            self.assertEqual(expect[0], result[0])
            self.assertEqual(expect[1], jumany.get_hinsi(result[3]))

    def test_analyze_just_word(self):
        """  jumany.analyze() for just_word==True  """
        res = jumany.analyze(_TEST_STR, just_word=True)
        self.assertEqual(len(_TEST_EXPECT), len(res))
        for expect, result in zip(_TEST_EXPECT, res):
            self.assertEqual(expect[0], result)

    def test_analyze_remove_space1(self):
        """  jumany.analyze() for remove_space==False  """
        res = jumany.analyze(" \r\t\n", remove_space=False)
        self.assertEqual(2, len(res))

    def test_analyze_remove_space2(self):
        """  jumany.analyze() for remove_space==True  """
        res = jumany.analyze(" \r\t\n", remove_space=True)
        self.assertEqual(0, len(res))

if __name__ == "__main__":
    unittest.main()
