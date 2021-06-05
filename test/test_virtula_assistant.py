import unittest
from utils.virtual_assistant import VirtualAssistant


class TestVirtualAssistant(unittest.TestCase):

    def test_va(self):
        command = "elsa open notepad"
        VirtualAssistant().start_assistant(command)


if __name__ == '__main__':
    unittest.main()
