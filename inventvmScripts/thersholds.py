
def vbatTh(vbat):
    print('Vbat',hex(int(abs(3-vbat)/(0.5*10**(-3)))))

def ibatTh(ibat):
    print('ibat',hex(int(abs(100*10**(-3)-ibat)/(2*10**(-3)))))

def vbusTh(vbus):
    print('vbus',hex(int(abs(3.9-vbus)/(100*10**(-3)))))

def vbusThBoost(vbus):
    print('vbus Boost',hex(int(abs(5-vbus)/(100*10**(-3)))))

def ibusTh(ibus):
    print('ibus',hex(int(abs(90*10**(-3)-ibus)/(10*10**(-3)))))


vbat = 4
ibat = 1
vbus = 3.9
ibus = 3
vbatTh(vbat=vbat)
ibatTh(ibat)
vbusTh(vbus)
vbusThBoost(vbus)
ibusTh(ibus)