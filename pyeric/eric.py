from ctypes import *
from collections import namedtuple
import os

EricResponse = namedtuple(
    'EricResponse',
    ['result_code', 'eric_response',  'server_response']
)


# As explained in the original ERiC documentation
class eric_druck_parameter_t(Structure):
    _fields_ = [("version", c_int),
                ("vorschau", c_int),
                ("ersteSeite", c_int),
                ("duplexDruck", c_int),
                ("pdfName", c_char_p),
                ("fussText", c_char_p)]


# As explained in the original ERiC documentation
class eric_verschluesselungs_parameter_t(Structure):
    _fields_ = [("version", c_int),
                ("zertifikatHandle", c_int),
                ("pin", c_char_p),
                ("abrufCode", c_char_p)]


class EricApi(object):
    """A Python wrapper for the native ERiC library. It uses `ctypes` for calling
    the respective functions of the `.so` file.
    """

    ERIC_VALIDIERE = 1 << 1
    ERIC_SENDE = 1 << 2
    ERIC_DRUCKE = 1 << 5

    def __init__(self, debug=True):
        """Creates a new instance of the pyeric wrapper. If `debug==True` (default)
        debug messages are printed to `sys.std.out`. The output function can
        be overwritten under `EricApi.print`.
        """
        self.print = print if debug else self._nop

        self.eric = CDLL("pyeric/lib/libericapi.so")
        self.print("eric:", self.eric)

    def _nop(self, *args):
        pass  # Used for outputting nothing if debug==False

    def initialise(self, log_path=None):
        """Initialises ERiC and a successful return from this method shall indicate
        that the .so file was found and loaded successfully. Where `initialise` is called,
        `shutdown` shall be called when done.
        """
        fun_init = self.eric.EricInitialisiere
        fun_init.argtypes = [c_char_p, c_char_p]
        fun_init.restype = c_int

        curr_dir = os.path.dirname(os.path.realpath(__file__))
        plugin_path = c_char_p(os.path.join(curr_dir, "lib/plugins2").encode())

        log_path = c_char_p(log_path.encode() if log_path else None)

        res = fun_init(plugin_path, log_path)
        self.print("fun_init res:", res)

    def shutdown(self):
        """Shutsdown ERiC and releases resources. One must not use the object afterwards."""
        fun_shutdown = self.eric.EricBeende
        fun_shutdown.argtypes = []
        fun_shutdown.restype = c_int
        res = fun_shutdown()
        self.print("fun_shutdown res:", res)

    def validate(self, xml, data_type_version):
        """Validate the given XML using the built-in plausibility checks."""
        return self.process(xml, data_type_version, EricApi.ERIC_VALIDIERE)

    def validate_and_send(self, xml, data_type_version, cert_path, cert_pin, print_path):
        """Validate and (more importantly) send the given XML using the built-in 
        plausibility checks. For this a test certificate and pin must be provided and the
        `data_type_version` shall match the XML data. When a `print_path` is given, a PDF
        will be created under that path."""

        print_params = self.alloc_eric_druck_parameter_t(print_path)

        cert_handle = self.get_cert_handle(cert_path.encode())

        try:
            cert_params = self.alloc_eric_verschluesselungs_parameter_t(cert_handle, cert_pin)
            flags = EricApi.ERIC_SENDE | (EricApi.ERIC_DRUCKE if print_path else 0)

            return self.process(
                xml, data_type_version,
                flags,
                cert_params=pointer(cert_params),
                print_params=pointer(print_params))
        finally:
            self.close_cert_handle(cert_handle)

    def alloc_eric_druck_parameter_t(self, print_path):
        return eric_druck_parameter_t(
            version=2,
            vorschau=0,
            ersteSeite=0,
            duplexDruck=0,
            pdfName=c_char_p(print_path.encode()) if print_path else None,
            fussText=None,
        )

    def alloc_eric_verschluesselungs_parameter_t(self, zertifikatHandle, pin):
        return eric_verschluesselungs_parameter_t(
            version=2,
            zertifikatHandle=zertifikatHandle,
            pin=pin.encode(),
            abrufCode=None,
        )

    def get_cert_handle(self, cert_path):
        fun_get_cert_handle = self.eric.EricGetHandleToCertificate
        fun_get_cert_handle.argtypes = [c_void_p, c_void_p, c_char_p]
        fun_get_cert_handle.restype = c_int

        cert_handle_out = c_int()
        res = fun_get_cert_handle(pointer(cert_handle_out), None, cert_path)
        self.print("fun_get_cert_handle res:", res)
        return cert_handle_out

    def close_cert_handle(self, cert_handle):
        fun_close_cert_handle = self.eric.EricCloseHandleToCertificate
        fun_close_cert_handle.argtypes = [c_int]
        fun_close_cert_handle.restype = c_int

        res = fun_close_cert_handle(cert_handle)
        self.print("fun_close_cert_handle res:", res)

    def process(self,
                xml, data_type_version, flags,
                transfer_handle=None, cert_params=None, print_params=None):
        xml = xml.encode('utf-8')
        data_type_version = data_type_version.encode('utf-8')

        try:
            eric_response_buffer = self.create_buffer()
            server_response_buffer = self.create_buffer()

            fun_process = self.eric.EricBearbeiteVorgang
            fun_process.argtypes = [c_char_p, c_char_p, c_uint32,
                                    c_void_p, c_void_p, c_void_p,
                                    c_void_p, c_void_p]
            fun_process.restype = c_int

            res = fun_process(xml, data_type_version, flags,
                              print_params, cert_params, transfer_handle,
                              eric_response_buffer, server_response_buffer)
            self.print("fun_process res:", res)

            eric_response = self.read_buffer(eric_response_buffer)
            server_response = self.read_buffer(server_response_buffer)
            self.print("eric_response:", eric_response.decode())
            self.print("server_response:", server_response.decode())

            return EricResponse(res, eric_response, server_response)
        finally:
            self.close_buffer(eric_response_buffer)
            self.close_buffer(server_response_buffer)

    def create_buffer(self):
        fun_create_buffer = self.eric.EricRueckgabepufferErzeugen
        fun_create_buffer.argtypes = []
        fun_create_buffer.restype = c_void_p

        res = fun_create_buffer()
        self.print("fun_create_buffer res:", res)
        return res

    def read_buffer(self, buffer):
        fun_read_buffer = self.eric.EricRueckgabepufferInhalt
        fun_read_buffer.argtypes = [c_void_p]
        fun_read_buffer.restype = c_char_p

        return fun_read_buffer(buffer)

    def close_buffer(self, buffer):
        fun_close_buffer = self.eric.EricRueckgabepufferFreigeben
        fun_close_buffer.argtypes = [c_void_p]
        fun_close_buffer.restype = int

        res = fun_close_buffer(buffer)
        self.print("fun_close_buffer res:", res)
        return res

    def create_th(self,
                  xml, datenart='ESt', verfahren='ElsterErklaerung', vorgang='send-Auth',
                  testmerker='700000004', herstellerId='74931', datenLieferant='Softwaretester ERiC', versionClient='1'):
        fun_create_th = self.eric.EricCreateTH
        fun_create_th.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p,
                                  c_char_p, c_char_p, c_char_p, c_char_p,
                                  c_char_p, c_void_p]
        fun_create_th.restype = int

        buf = self.create_buffer()
        try:
            res = fun_create_th(
                xml.encode(), verfahren.encode(), datenart.encode(), vorgang.encode(),
                testmerker.encode(), herstellerId.encode(), datenLieferant.encode(), versionClient.encode(),
                None, buf)
            self.print("fun_create_th res", res)

            return self.read_buffer(buf)
        finally:
            self.close_buffer(buf)
