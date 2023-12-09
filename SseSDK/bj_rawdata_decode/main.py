import struct
import os
import binascii
from util.logTool import logger

file_path = '20231205_bj/Ldds-RawData-BJZQ.dat'
file_304000_path = '20231205_bj/304000.csv'
file_301000_path = '20231205_bj/301000.csv'
file_305000_path = '20231205_bj/305000.csv'
file_307011_path = '20231205_bj/307011.csv'
file_308011_path = '20231205_bj/308011.csv'
file_308012_path = '20231205_bj/308012.csv'
file_306001_path = '20231205_bj/306001.csv'

file = open(file_path, 'rb')
file_304000 = open(file_304000_path, 'w')
file_301000 = open(file_301000_path, 'w')
file_305000 = open(file_305000_path, 'w')
file_307011 = open(file_307011_path, 'w')
file_308011 = open(file_308011_path, 'w')
file_308012 = open(file_308012_path, 'w')
file_306001 = open(file_306001_path, 'w')

file_size = os.path.getsize(file_path)
read_len = 0
msgType = 0
uaType = 0

msg_total = set()

while True:
    # print(str(read_len) + "," + str(file_size))
    if read_len >= file_size:
        break
    step_head_start_pos = file.tell()
    step_head = file.read(13)
    read_len = read_len + 13
    while True:
        if read_len >= file_size:
            break

        old_pos = file.tell()
        tag_len = 0
        tag_data = ""
        while True:
            temp = file.read(1)
            if temp == b'\x01':
                file.seek(old_pos)
                tag_data = str(file.read(tag_len), encoding="utf-8")
                file.read(1)
                read_len = read_len + tag_len + 1
                break
            tag_len = tag_len + 1
        tag_detail = tag_data.split("=")

        # print("tag_detail:",tag_detail)
        if int(tag_detail[0]) == 35:
            uaType = int(tag_detail[1][-4:])

        if uaType != 6101:
            continue
        # print(uaType)

        if int(tag_detail[0]) == 95:
            step_in_data_len = int(tag_detail[1])
            file.read(3)
            in_data_len = 0
            msg_data = file.read(step_in_data_len)
            # {304000, 307011, 301000, 305000, 308011, 308012, 306001}

            while in_data_len < step_in_data_len:
                msgType = int.from_bytes(msg_data[in_data_len:in_data_len + 4], 'big')
                #print("msgType",msgType)
                msg_total.add(msgType)
                in_data_len += 4
                bodyLen = int.from_bytes(msg_data[in_data_len:in_data_len + 4], 'big')
                #print("bodyLen",bodyLen)
                in_data_len += 4
                #print("in_data_len",in_data_len)
                #print("msg_data:",msg_data)
                if msgType == 304000:
                    # Standard Header           uInt32
                    # OrigTime                  LocalTimestamp:Int64 #读取8个字节之后,需要跳过两个字节
                    # SecurityID                char[8]
                    # SecurityIDSource          char[4]
                    # SecuritySymbol            char[40]
                    # NoSwitch                  uInt32
                    # SecuritySwitchType        uInt16
                    # SecuritySwitchStatus      uInt16
                    msg = msg_data[in_data_len:in_data_len + 8]
                    OrigTime = struct.unpack(">q", msg)[0]
                    msg = msg_data[in_data_len+10:in_data_len + 10 + 56]
                    #print("OrigTime", OrigTime)
                    file_304000.write(str(OrigTime) + ",")
                    res = struct.unpack(">8s4s40sI", msg)
                    #print(res)
                    for i in range(0, len(res)):
                        if isinstance(res[i], bytes):
                            data = res[i].decode('gbk')
                            file_304000.write(str(data) + ",")
                        else:
                            file_304000.write(str(res[i]) + ",")

                    file_304000.write("\n")

                if msgType == 301000:
                    # Standard Header   uInt32
                    # ChannelNo         uInt16
                    # ApplLastSeqNum    Int64
                    # EndOfChannel      uInt16
                    msg = msg_data[in_data_len:in_data_len + 12]
                    res = struct.unpack(">HqH", msg)
                    #print(res)
                    for i in range(0, len(res)):
                        if isinstance(res[i], bytes):
                            data = res[i].decode('gbk')
                            #print("data",data)
                            file_301000.write(data + ",")
                        else:
                            file_301000.write(str(res[i]) + ",")
                    file_301000.write("\n")

                if msgType == 305000:
                    # Standard Header           uInt32
                    # OrigTime                  LocalTimestamp:Int64
                    # ChannelNo                 uInt16
                    # NewsID                    char[16]
                    # Headline                  char[128]
                    # RawDataFormat             char[8]
                    # NewsType                  uInt8
                    # RawDataLength             uInt32
                    # RawData                   char[n]
                    msg = msg_data[in_data_len:in_data_len + 167]
                    res = struct.unpack(">qH16s128s8sBI", msg)
                    for i in range(0, len(res)):
                        if isinstance(res[i], bytes):
                            data = res[i].decode('gbk')
                            file_305000.write(str(data) + ",")
                        else:
                            file_305000.write(str(res[i]) + ",")

                    raw_data_len = bodyLen - 167
                    if raw_data_len > 0:
                        fmt = "{}s".format(raw_data_len)
                        msg = msg_data[in_data_len+167:in_data_len + 167 + raw_data_len]
                        res = struct.unpack(fmt, msg)[0]
                        #print(res)
                        if isinstance(res, bytes):
                            data = res.decode('gbk')
                            data = data.replace('\n',' ')
                            file_305000.write(str(data) + ",")
                        else:
                            file_305000.write(str(res) + ",")

                    file_305000.write('\n')

                if msgType == 307011:
                    # MsgType
                    # ChannelNo         uInt16
                    # ApplSeqNum        Int64
                    # MDStreamID        char[3]
                    # SecurityID        char[8]
                    # SecurityIDSource  char[4]
                    # Price             Int64
                    # OrderQty          Int64
                    # Side              char
                    # TransactTime      Int64
                    # Extend Fields
                    msg = msg_data[in_data_len:in_data_len + 50]
                    res = struct.unpack(">Hq3s8s4sqq1sq", msg)
                    #print(res)
                    for i in range(0, len(res)):
                        if isinstance(res[i], bytes):
                            data = res[i].decode('gbk')
                            #print(data)
                            file_307011.write(str(data) + ",")
                        else:
                            file_307011.write(str(res[i]) + ",")
                    if bodyLen > 50: # 扩展字段
                        # OrdType           char
                        # SettlType         char
                        # SettlPeriod       char
                        msg = msg_data[in_data_len + 50:in_data_len + 50 + 3]
                        res = struct.unpack(">1s1s1s", msg)
                        for i in range(0, len(res)):
                            if isinstance(res[i], bytes):
                                data = res[i].decode('gbk')
                                #print(data)
                                file_307011.write(str(data) + ",")
                            else:
                                file_307011.write(str(res[i]) + ",")

                    file_307011.write('\n')

                if msgType == 308011 or msgType == 308012:
                # MsgType
                # ChannelNo                 uInt16
                # ApplSeqNum                Int64
                # MDStreamID                char[3]
                # SecurityID                char[8]
                # SecurityIDSource          char[4]
                # BidApplSeqNum             Int64
                # AskApplSeqNum             Int64
                # TradePrice                Int64
                # TradeQty                  Int64
                # TradeMoney                Int64
                # ExecType                  char
                # TransactTime              Int64
                # Extend Fields
                    if msgType == 308011:
                        write_file = file_308011
                    else:
                        write_file = file_308012

                    msg = msg_data[in_data_len:in_data_len + 74]
                    res = struct.unpack(">Hq3s8s4sqqqqq1sq", msg)
                    for i in range(0, len(res)):
                        if isinstance(res[i], bytes):
                            data = res[i].decode('gbk')
                            #print(data)
                            write_file.write(str(data) + ",")
                        else:
                            write_file.write(str(res[i]) + ",")

                    if bodyLen > 74:
                        # SettlPeriod       char
                        # SettlType         char
                        msg = msg_data[in_data_len + 74:in_data_len + 74 + 2]
                        res = struct.unpack(">1s1s", msg)
                        for i in range(0, len(res)):
                            if isinstance(res[i], bytes):
                                data = res[i].decode('gbk')
                                #print(data)
                                write_file.write(str(data) + ",")
                            else:
                                write_file.write(str(res[i]) + ",")
                    write_file.write('\n')

                if msgType == 306001:
                # Standard Header
                # OrigTime                  LocalTimestamp:Int64
                # ChannelNo                 uInt16
                # MDStreamID                char[3]
                # SecurityID                char[8]
                # SecurityIDSource          char[4]
                # TradingPhaseCode          char[8]
                # PreClosePx                Int64
                # NumTrades                 Int64
                # TotalVolumeTrade          Int64
                # TotalValueTrade           Int64
                # Extend Fields
                # NoMDEntries               uInt32
                    # MDEntryType           char[2]
                    # MDEntryPx             Int64
                    # MDEntrySize           Int64
                    # MDPriceLevel          uInt16
                    # NumberOfOrders        Int64
                    # NoOrders              uInt32
                        # OrderQty          Int64
                # NoSubTradingPhaseCodes    预留
                    # SubTradingPhaseCodes
                    # TradingType           uInt8
                # AuctionVolumeTrade        Int64
                # AuctionValueTrade         Int64
                # TradeTime                 Int64
                    index= in_data_len
                    msg = msg_data[index:index + 65]
                    index += 65
                    res = struct.unpack(">qH3s8s4s8sqqqq", msg)
                    for i in range(0, len(res)):
                        if isinstance(res[i], bytes):
                            data = res[i].decode('gbk')
                            #print(data)
                            file_306001.write(str(data) + ",")
                        else:
                            file_306001.write(str(res[i]) + ",")

                    if bodyLen > 65: # 有扩展数据
                        # NoMDEntries           uInt32
                            # MDEntryType           char[2]
                            # MDEntryPx             Int64
                            # MDEntrySize           Int64
                            # MDPriceLevel          uInt16
                            # NumberOfOrders        Int64
                            # NoOrders              uInt32
                                # OrderQty          Int64

                        msg = msg_data[index:index + 4]
                        index += 4
                        res = struct.unpack(">I", msg)[0]
                        file_306001.write(str(res) + ",")

                        NoMDEntries_Num = int(res)
                        #print("NoMDEntries_Num",NoMDEntries_Num)
                        for i in range(NoMDEntries_Num):
                            msg = msg_data[index:index + 32]
                            index += 32
                            res = struct.unpack(">2sqqHqI", msg)
                            for j in range(0, len(res)):
                                if isinstance(res[j], bytes):
                                    data = res[j].decode('gbk')
                                    file_306001.write(str(data) + ",")
                                else:
                                    file_306001.write(str(res[j]) + ",")

                            NoOrders_Num = res[len(res)-1]
                            if NoOrders_Num > 0:
                                for j in range(NoOrders_Num):
                                    msg = msg_data[index:index + 8]
                                    index += 8
                                    res = struct.unpack(">q", msg)
                                    if isinstance(res[j], bytes):
                                        data = res[j].decode('gbk')
                                        file_306001.write(str(data) + ",")
                                    else:
                                        file_306001.write(str(res[j]) + ",")

                        msg = msg_data[index:index + 4]
                        index +=4
                        NoSubTradingPhaseCodes_Num = struct.unpack(">I", msg)[0]
                        #print(NoSubTradingPhaseCodes_Num)
                        file_306001.write(str(NoSubTradingPhaseCodes_Num) + ",")
                        msg = msg_data[index:index + 24]
                        index += 24
                        res = struct.unpack(">qqq", msg)
                        for j in range(0, len(res)):
                            if isinstance(res[j], bytes):
                                data = res[j].decode('gbk')
                                file_306001.write(str(data) + ",")
                            else:
                                file_306001.write(str(res[j]) + ",")

                    file_306001.write('\n')

                in_data_len += bodyLen
                in_data_len += 4
            # 跳过校验和
            file.read(1)
            read_len = read_len + 3 + step_in_data_len + 1
logger.info(msg_total)