import math

base93_map = [None] * 150
base93_map[33] = 0
base93_map[35] = 1
base93_map[36] = 2
base93_map[37] = 3
base93_map[38] = 4
base93_map[39] = 5
base93_map[40] = 6
base93_map[41] = 7
base93_map[42] = 8
base93_map[43] = 9
base93_map[45] = 10
base93_map[46] = 11
base93_map[47] = 12
base93_map[48] = 13
base93_map[49] = 14
base93_map[50] = 15
base93_map[51] = 16
base93_map[52] = 17
base93_map[53] = 18
base93_map[54] = 19
base93_map[55] = 20
base93_map[56] = 21
base93_map[57] = 22
base93_map[58] = 23
base93_map[59] = 24
base93_map[60] = 25
base93_map[61] = 26
base93_map[62] = 27
base93_map[63] = 28
base93_map[64] = 29
base93_map[65] = 30
base93_map[66] = 31
base93_map[67] = 32
base93_map[68] = 33
base93_map[69] = 34
base93_map[70] = 35
base93_map[71] = 36
base93_map[72] = 37
base93_map[73] = 38
base93_map[74] = 39
base93_map[75] = 40
base93_map[76] = 41
base93_map[77] = 42
base93_map[78] = 43
base93_map[79] = 44
base93_map[80] = 45
base93_map[81] = 46
base93_map[82] = 47
base93_map[83] = 48
base93_map[84] = 49
base93_map[85] = 50
base93_map[86] = 51
base93_map[87] = 52
base93_map[88] = 53
base93_map[89] = 54
base93_map[90] = 55
base93_map[92] = 56
base93_map[94] = 57
base93_map[95] = 58
base93_map[96] = 59
base93_map[97] = 60
base93_map[98] = 61
base93_map[99] = 62
base93_map[100] = 63
base93_map[101] = 64
base93_map[102] = 65
base93_map[103] = 66
base93_map[104] = 67
base93_map[105] = 68
base93_map[106] = 69
base93_map[107] = 70
base93_map[108] = 71
base93_map[109] = 72
base93_map[110] = 73
base93_map[111] = 74
base93_map[112] = 75
base93_map[113] = 76
base93_map[114] = 77
base93_map[115] = 78
base93_map[116] = 79
base93_map[117] = 80
base93_map[118] = 81
base93_map[119] = 82
base93_map[120] = 83
base93_map[121] = 84
base93_map[122] = 85
base93_map[126] = 86


def decode(encodeString: str) -> int:
	decodeVal = 0
	if encodeString is not None and len(encodeString) > 0:
		for index in range(len(encodeString), 0, -1):
			index -= 1
			c = encodeString[index]
			mypow = math.pow(87, len(encodeString)-index-1)
			magic_chr = base93_map[ord(c)]
			if magic_chr is None:
				# maybe handle err
				continue
			decodeVal += (magic_chr*mypow)
	return int(decodeVal)
