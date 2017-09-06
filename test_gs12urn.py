import unittest
from gs12urn import gs12urn


class MockNode(object):
    """
    A mock object to fake an XML node.
    """
    def __init__(self, text):
        self.text = text

    def __unicode__(self):
        return self.text


class Testgs1ToUrn(unittest.TestCase):
    """Tests the main convert values logic."""

    def test_convert_gtin_value_to_urn(self):
        res = gs12urn.convert_value_to_urn(MockNode('0120339822120127212170080000016'), 'urn:epc:tag:sgtin-198:0.', '')
        self.assertEqual(res, 'urn:epc:tag:sgtin-198:0.0339822.212012.2170080000016')

    def test_convert_sscc_value_to_urn(self):
        res = gs12urn.convert_value_to_urn(MockNode('00303398220017116004'), '', 'urn:epc:tag:sscc-96:0.')
        self.assertEqual(res, 'urn:epc:tag:sscc-96:0.0339822.3001711600')
