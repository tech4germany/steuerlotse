from dataclasses import dataclass
from typing import ByteString


@dataclass
class PyericResponse:
    eric_response: str
    server_response: str
    pdf: ByteString = None
