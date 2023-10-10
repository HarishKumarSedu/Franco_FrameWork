msb=19
lsb=14
number = 0x4000

mask = ~(((1<<(msb-lsb+1)) -1)<<lsb)
# mask = ~(((1<<msb+1) -1 ) & ((1<<lsb) -1))
value = 2

modifiednumber = (number & mask) | (value << lsb)

print(f'Original number {hex(number)} MSB {msb} LSB {lsb} mask {hex(mask)} modfiednumber {hex(modifiednumber)}')