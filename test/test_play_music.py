import unittest
from utils.virtual_assistant import VirtualAssistant


class TestVirtualAssistant(unittest.TestCase):

    def test_va(self):
        command = "elsa play national anthem of india"
        VirtualAssistant().run_elsa(command)


if __name__ == '__main__':
    unittest.main()