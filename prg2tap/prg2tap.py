"""
Convert .prg file to Oric .tap file
"""

def sync_bytes():
    """
    Sync Bytes for start of Oric tape header
    """
    return bytearray(b'\x10\x10\x10\x10\x24')

def code_type():
    """
    Declare program as executable machine code
    """
    return bytearray(b'\x80\xc7')

def address_range(prg):
    result = bytearray()
    result_end = (prg[1] * 255) + prg[0] + (len(prg) - 2)
    result.append(int(result_end / 255))
    result.append(int(result_end % 255))
    result.append(prg[1])
    result.append(prg[0])

    return result

def reserved(num):
    return bytearray(num)

def filename(name):
    result = bytearray()
    result.extend(map(ord, name))
    result.append(0)
    return result

def body(prg):
    return prg[2:]

def header(prg, name):
    result = sync_bytes()
    result.extend(reserved(2))
    result.extend(code_type())
    result.extend(address_range(prg))
    result.extend(reserved(1))
    result.extend(filename(name))
    result.extend(body(prg))
    return result
