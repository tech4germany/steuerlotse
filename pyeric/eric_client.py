import argparse
import time

import os
import sys

curr_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(curr_dir)
sys.path.insert(0, parent_dir)
from app.utils import pretty_xml
from pyeric import EricApi


if __name__ == "__main__":
    start_time = time.time()

    parser = argparse.ArgumentParser(description='PyERiC client')
    parser.add_argument('--work-dir', type=str,
                        help='The working directory with the input files (input.xml, cert.pfx). Will also be used for the output files (eric_response.xml, server_response.xml, print.pdf, eric.log)')
    parser.add_argument('--cert-pin', type=str, help='The PIN for the certificate.')
    parser.add_argument('--verfahren', type=str, help='The "Verfahren" that is to be used. E.g. ESt_2011')
    parser.add_argument('--verbose', dest='verbose', action='store_const', const=True,
                        default=False, help='Only validate, but do not actually send')
    parser.add_argument('--only-validate', dest='only_validate', action='store_const', const=True,
                        default=False, help='Enable debug output of pyeric')

    args = parser.parse_args()
    work_dir, cert_pin = os.path.abspath(args.work_dir), args.cert_pin
    verfahren, only_validate, verbose = args.verfahren, args.only_validate, args.verbose

    eric = EricApi(debug=verbose)
    try:
        eric.initialise(log_path=work_dir)
        with open(os.path.join(work_dir, 'input.xml'), 'r') as f:
            input_xml = f.read()

        # Clean-up if neccessary
        output_files = ('eric.log', 'eric_response.xml', 'server_response.xml', 'print.pdf',)
        for output_file_name in output_files:
            path = os.path.join(work_dir, output_file_name)
            if os.path.isfile(path):
                os.remove(path)

        if only_validate:
            response = eric.validate(input_xml, verfahren)
        else:
            # Send it over into ELSTER land \o/
            response = eric.validate_and_send(
                input_xml, verfahren,
                cert_path=os.path.join(work_dir, "cert.pfx"),
                cert_pin=cert_pin,
                print_path=os.path.join(work_dir, "print.pdf"))

        with open(os.path.join(work_dir, 'eric_response.xml'), 'w') as f:
            xml = pretty_xml(response.eric_response.decode())
            f.write(xml)

        if not only_validate:
            with open(os.path.join(work_dir, 'server_response.xml'), 'w') as f:
                xml = pretty_xml(response.server_response.decode())
                f.write(xml)

    finally:
        eric.shutdown()

        delta_time = time.time() - start_time
        if verbose:
            print("TIME: %0.2fs" % delta_time)
