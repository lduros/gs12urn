"""
    gs12urn.py -- Convert GTIN and SSCC values to EPC URIs from various
    inbound XML files. Please see README.md for more information.

    Copyright (C) 2017 Loic J. Duros

    gs12urn.py is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    gs12urn.py is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import click
from lxml import etree, objectify
from bs4 import BeautifulSoup
import re

# The GTIN regular expression pattern
gtin_regex = r"^(01)(?P<indicator>\d{1})(?P<company_prefix>\d{7})(?P<product_id>\d{5})(?P<check_digit>\d{1})(21)(?P<serial>\d+)$"
gtin_re = re.compile(gtin_regex)

# The SSCC Regex pattern
sscc_regex = r"^(00)(?P<indicator>\d{1})(?P<company_prefix>\d{7})(?P<serial>\d+)$"
sscc_re = re.compile(sscc_regex)

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument('inbound-file', type=click.File('rb'))
@click.option('--node-name', default='cmn:SerialNumber', help='the XML nodename that contains the GTIN/SSCC values, with namespace, default: cmn:SerialNumber')
@click.option('--gtin-uri', default='urn:epc:tag:sgtin-198:0.', help='The beginning of the URN for GTINs. Default: urn:epc:tag:sgtin-198:0.')
@click.option('--sscc-uri', default='urn:epc:tag:sscc-96:0.', help='The beginning of the URN for SSCCs. Default: urn:epc:tag:sscc-96:0.')
def gs12urn_command(inbound_file, node_name, gtin_uri, sscc_uri):
    """
    A GTIN/SSCC to URN conversion tool.
    Example typical usage:\n
        python3 gs12urn.py ./examples/inbound-sscc.xml \n
        python3 gs12urn.py ./examples/inbound.xml
    """
    doc = BeautifulSoup(inbound_file, "lxml")
    nodes = doc.findAll([node_name.lower()])
    for node in nodes:
        convert_value_to_urn(node, gtin_uri, sscc_uri)


def convert_value_to_urn(node, gtin_urn, sscc_urn):
    """
    Matches either a GTIN or an SSCC and converts it to EPC URI accordingly.
    """
    gtin_match = re.match(gtin_re, node.text)
    if gtin_match:
        # return so that we go no further.
        return click.echo(convert_gtin_to_urn(gtin_match, gtin_urn))
    sscc_match = re.match(sscc_re, node.text)
    if sscc_match:
        return click.echo(convert_sscc_to_urn(sscc_match, sscc_urn))


def convert_gtin_to_urn(gtin, gtin_urn):
    """
    Converts a GTIN.
    """
    formatter = {"urn_prefix": gtin_urn,
                 "company_prefix": gtin.group("company_prefix"),
                 "indicator": gtin.group("indicator"),
                 "product_id": gtin.group("product_id"),
                 "serial": gtin.group("serial")}
    return "%(urn_prefix)s%(company_prefix)s.%(indicator)s%(product_id)s.%(serial)s" % formatter


def convert_sscc_to_urn(sscc, sscc_urn):
    """
    Converts an SSCC.
    """
    formatter = {"urn_prefix": sscc_urn,
                 "company_prefix": sscc.group("company_prefix"),
                 "indicator": sscc.group("indicator"),
                 "serial": sscc.group("serial")}
    return "%(urn_prefix)s%(company_prefix)s.%(indicator)s%(serial)s" % formatter


if __name__ == "__main__":
    gs12urn_command()
