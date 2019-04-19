import click

from cmsis_svd.parser import SVDParser

MCU_OPTIONS = [
    'STM32F0xx',
]

MCU2VENDOR_FILE = {
    'STM32F0xx': ('STMicro', 'STM32F0xx.svd'),
}

ALL = 'show_all'


def show_register(register):
    fields = []
    for field in register.fields:
        upper_index = field.bit_offset + field.bit_width - 1
        lower_index = field.bit_offset
        if upper_index == lower_index:
            index_s = str(upper_index)
        else:
            index_s = f'{upper_index}:{lower_index}'
        fields.append(f'{field.name}[{index_s}]')
    print(f'{register.name: <5} 0x{register.address_offset:04x}: {",".join(fields)}')


def show_peripheral(peripheral):
    print(peripheral.name)
    for register in peripheral.registers:
        show_register(register)
    print()


@click.command()
@click.option('--mcu', type=click.Choice(MCU_OPTIONS), required=True,
              help='MCU Name')
@click.option('--mcu-peripheral', help='Peripheral Specified')
def main(mcu, mcu_peripheral=None):
    """Given a chip and peripheral, prints the registers.
    """
    parser = SVDParser.for_packaged_svd(*MCU2VENDOR_FILE[mcu])
    address2peripheral = {}
    for peripheral in parser.get_device().peripherals:
        address2peripheral[peripheral.base_address] = peripheral
    for _, peripheral in sorted(address2peripheral.items()):
        print(f'{peripheral.name: <16} @ 0x{peripheral.base_address:08x} ({peripheral.address_block.size: >4})')
    if mcu_peripheral:
        for peripheral in parser.get_device().peripherals:
            if peripheral.name == mcu_peripheral or mcu_peripheral == ALL:
                show_peripheral(peripheral)


if __name__ == '__main__':
    main()
