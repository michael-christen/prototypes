import json

from cmsis_svd.parser import SVDParser

def main():
    parser = SVDParser.for_packaged_svd('STMicro', 'STM32F0xx.svd')
    address2peripheral = {}
    for peripheral in parser.get_device().peripherals:
        address2peripheral[peripheral.base_address] = peripheral
    for _, peripheral in sorted(address2peripheral.items()):
        print(f'{peripheral.name: <16} @ 0x{peripheral.base_address:08x}')
    svd_dict = parser.get_device().to_dict()
    print(json.dumps(svd_dict, sort_keys=True, indent=4))

if __name__ == '__main__':
    main()
