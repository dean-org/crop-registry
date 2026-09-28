from enum import Enum
class G2PRegistryErrorCodes(Enum):
    REQUEST_VALIDATION_ERROR=("x","REQ-VAL")
class G2PRegistryException(Exception):
    def __init__(self, code, message): super().__init__(message); self.code=code; self.message=message
