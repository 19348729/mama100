#!/usr/bin/python


def encrypt(key, s):
    b = bytearray(str(s).encode("gbk"))   
    n = len(b)
    c = bytearray(n*2)   
    j = 0   
    for i in range(0, n):   
        b1 = b[i]   
        b2 = b1 ^ key # b1 = b2^ key   
        c1 = b2 % 16   
        c2 = b2 // 16 # b2 = c2*16 + c1   
        c1 = c1 + 65   
        c2 = c2 + 65
        c[j] = c1   
        c[j+1] = c2   
        j = j+2   
    return c.decode("gbk")   
def decrypt(key, s):   
    c = bytearray(str(s).encode("gbk"))   
    n = len(c)
    if n % 2 != 0 :   
        return ""   
    n = n // 2   
    b = bytearray(n)   
    j = 0   
    for i in range(0, n):   
        c1 = c[j]   
        c2 = c[j+1]   
        j = j+2   
        c1 = c1 - 65   
        c2 = c2 - 65   
        b2 = c2*16 + c1   
        b1 = b2^ key   
        b[i]= b1   
    try:   
        return b.decode("gbk")   
    except:   
        return "failed"   
if __name__=='__main__':
	key = 138
	#s1 = encrypt(key, 'PPJPMPMKPPILGOEOIOHMNMKPBONPAOOPLOGOMLDP')   
	s2 = decrypt(key, 'PPJPMPMKPPILGOEOIOHMNMKPBONPAOOPLOGOMLDP')   
	#print s1,'\n',s2   	
	print s2
