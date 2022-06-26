
def checkFsAlign(fd):
    buf = bytearray(4)
    try:
        fcntl.ioctl(fd, FS_IOCNUM_CHECK_FS_ALIGN, buf)
    except:
        return False

    fsAlign = struct.unpack("i", buf)
    return fsAlign[0] == 1

