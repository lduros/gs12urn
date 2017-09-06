# gs12urn
A conversion tool for GS1 inbound values (wrapped in typical XML) into EPC URI values for Python 3.6 or later.


    Run `pip3 install -r requirements.txt` to install packages.

    Usage: gs12urn.py [OPTIONS] INBOUND_FILE

      A GTIN/SSCC to URN conversion tool. Example typical usage:

          python3 gs12urn.py ./examples/inbound-sscc.xml

          python3 gs12urn.py ./examples/inbound.xml

      Options:
          --node-name TEXT  the XML nodename that contains the GTIN/SSCC values, with
                      namespace, default: cmn:SerialNumber
          --gtin-uri TEXT   The beginning of the URN for GTINs. Default:
                      urn:epc:tag:sgtin-198:0.
          --sscc-uri TEXT   The beginning of the URN for SSCCs. Default:
                      urn:epc:tag:sscc-96:0.
          -h, --help        Show this message and exit.
