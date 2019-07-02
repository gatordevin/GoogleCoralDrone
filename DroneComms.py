import socket
import time
class SBUSUDP:
    def __init__(self, ip=None):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.newChannels = [1024] * 16
        self.oldChannels = []
        self.ip = ""
        if(ip == None):
            hostname = socket.gethostname()
            IPAddr = socket.gethostbyname(hostname)
            splitted = IPAddr.split(".")
            ipSearch = ""
            for i in range(len(splitted) - 1):
                ipSearch += splitted[i] + "."
            for i in range(0, 101):
                ips = ipSearch + str(i)
                data = bytearray(4)
                data[0] = ord('H')
                data[1] = ord('A')
                data[2] = ord('N')
                data[3] = ord('D')
                self.client_socket.sendto(data, (ips, 6666))
                try:
                    self.client_socket.settimeout(0.01)
                    data = self.client_socket.recvfrom(256)
                    if (data != None):
                        self.ip = ips
                        break
                except:
                    None
        else:
            self.ip = ip
        print(self.ip)
        self.timeSent = time.time()

    def bit_not(self, n, numbits=8):
        return (1 << numbits) - 1 - n


    def create_SBUS(self, chan):
        data = bytearray(31)
        data[0] = ord('S')
        data[1] = ord('B')
        data[2] = ord('U')
        data[3] = ord('S')

        data[4] = 0x0f  # start byte

        current_byte = 5
        available_bits = 8

        for ch in chan:
            ch &= 0x7ff
            remaining_bits = 11
            while remaining_bits:
                mask = self.bit_not(0xffff >> available_bits << available_bits, 16)
                enc = (ch & mask) << (8 - available_bits)
                data[current_byte] |= enc

                encoded_bits = 0
                if remaining_bits < available_bits:
                    encoded_bits = remaining_bits
                else:
                    encoded_bits = available_bits

                remaining_bits -= encoded_bits
                available_bits -= encoded_bits
                ch >>= encoded_bits

                if available_bits == 0:
                    current_byte += 1
                    available_bits = 8

        data[27] = 0
        data[28] = 0
        checksum1 = 0
        for byte in data:
            checksum1 = checksum1 ^ byte
        checksum1 = checksum1 & 0xFE
        checksum2 = (~checksum1) & 0xFE
        data[29] = checksum1
        data[30] = checksum2
        return data

    def set_channel(self, chan, data):
        self.newChannels[chan] = data & 0x07ff
        #print(list(self.newChannels)[0])
    def update_channel(self, chan, value):
        self.set_channel(chan, self.mapData(value))

    def mapData(self, n):
        return int((819 * ((n - 1500) / 500)) + 992)

    def create_BEAT(self):
        data = bytearray(4)
        data[0] = ord('B')
        data[1] = ord('E')
        data[2] = ord('A')
        data[3] = ord('T')
        return (data)

    def findDevice(self):

        self.client_socket.sendto(self.create_BEAT(), (self.ip, 6666))
    def sendUDP(self, channels):
        for i in range(len(channels)):
            self.update_channel(i, channels[i])
        #print(list(self.newChannels))
        #print(list(self.oldChannels))
        if (list(self.newChannels) != list(self.oldChannels)):
            channels = bytearray(self.create_SBUS(self.newChannels))
            self.client_socket.sendto(channels, (self.ip, 6666))
            self.timeSent = time.time()
            #print(self.ip)
            #self.oldChannels = self.newChannels
            #print(list(self.newChannels))
        elif (time.time() - self.timeSent >= 0.5):
            self.client_socket.sendto(self.create_BEAT(), (self.ip, 6666))
            self.timeSent = time.time()
            #print(list(self.create_SBUS(self.newChannels)))

