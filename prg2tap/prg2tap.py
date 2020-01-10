"""
Convert .prg file to Oric .tap file
"""

import sys

FILENAME = 'OSDK'

def sync_bytes():
    """
    Sync Bytes for start of Oric tape header
    """
    return bytearray(b'\x16\x16\x16\x16\x24')

def code_type():
    """
    Declare program as executable machine code
    """
    return bytearray(b'\x80\xc7')

def address_range(prg):
    """
    Get address range of code
    """
    result = bytearray()
    result_end = (prg[1] * 255) + prg[0] + (len(prg) - 2)
    result.append(int(result_end / 255))
    result.append(int(result_end % 255))
    result.append(prg[1])
    result.append(prg[0])

    return result

def reserved(num):
    """
    Return reserved bytes - zeros
    """
    return bytearray(num)

def filename(name):
    """
    Encode filename
    """
    result = bytearray()
    result.extend(map(ord, name))
    result.append(0)
    return result

def body(prg):
    """
    Code body
    """
    return prg[2:]

def process(prg, name):
    """
    Transform prg into tap
    """
    result = sync_bytes()
    result.extend(reserved(2))
    result.extend(code_type())
    result.extend(address_range(prg))
    result.extend(reserved(1))
    result.extend(filename(name))
    result.extend(body(prg))
    return result

def convert():
    """Convert stdin .prg to stdout .tap"""
    try:
        data = sys.stdin.buffer.read()
    except AttributeError:
        sys.exit('error reading from stdin')
    output = process(data, FILENAME)
    sys.stdout.buffer.write(output)

if __name__ == '__main__':

    convert()
