import ctypes


HELLO_SO_PATH = '../c_package/libhello.so'
HELLO_SO_PATH = 'libhello.so'


def main():
    hello_lib = ctypes.cdll.LoadLibrary(HELLO_SO_PATH)
    hello_lib.hello()


if __name__ == '__main__':
    main()
