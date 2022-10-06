class Torrent:
    def __init__(self):
        self.data={}
    def load(self,filename):
        self.stream=Stream(filename,"rb")
        if self.stream.next()==b'd':
            self.data=build_dic(self.stream)
        else:
            raise Exception("invalid torrent file")
    def dump(self,filename):
        self.stream=Stream(filename,"wb")
        dump_dic(self.stream,self.data)
        self.stream.close()
        
def build_dic(stream):#call after symbol 'd' found
    list=[]
    proxy_build(stream,list)
    dic={}
    for i in range(0,len(list)-1,2):   #convert a list[k1,v1,k2,v2...] to a dic
        dic[list[i]]=list[i+1]
    return dic
def build_list(stream):#call after symbol 'l' found
    list=[]
    proxy_build(stream,list)
    return list
def build_str(stream,str_len):#call after num found
    values=[]
    for i in range(str_len):
        values.append(stream.next())
    return b''.join(values)
def build_num(stream):#call after symbol 'i' found
    num=0
    minus=False
    while True:
        ch=stream.next()
        if ch>=b'0' and ch<=b'9':
            num=num*10+int(ch)
        elif ch==b'-':
            minus=True
        elif ch==b'e':
            break
        else:
            raise Exception("invalid torrent file")
    num=-num if minus else num
    return num
def proxy_build(stream,list): #because build_dic and build_list is simaliar,so I def a proxy-function  
    while True:
        ch=stream.next()
        if ch>=b'0' and ch<=b'9':#I think ch==0 is not very valid,but just do this.
            str_len=int(ch)
            while True:
                ch=stream.next()
                if ch==b':':
                    break
                elif ch>=b'0' and ch<=b'9':
                    str_len=str_len*10+int(ch)
                else:
                    raise Exception("invalid torrent file")
            list.append(build_str(stream,str_len))
        elif ch==b'l':
            list.append(build_list(stream))
        elif ch==b'i':
            list.append(build_num(stream))
        elif ch==b'd':
            list.append(build_dic(stream))
        elif ch==b'e':
            break
        else:
            raise Exception("invalid torrent file")

def str2bytes(s):
    return s.encode("utf-8")

def bytes2str(s):
    return s.decode("utf-8")
"""
for dumpfile
"""
import types
def dump_dic(stream,dic):
    stream.put(str2bytes("d"))
    for k,v in dic.items():
        dump_str(stream,k)
        proxy_dump(stream,v)
    stream.put(str2bytes("e"))
def dump_list(stream,list):
    stream.put(str2bytes("l"))
    for item in list:
        proxy_dump(stream,item)
    stream.put(str2bytes("e"))
def dump_str(stream,mystr):
    stream.put(str2bytes(str(len(mystr))+":"))
    stream.put(mystr)
def dump_num(stream,num):
    stream.put(str2bytes("i"))
    stream.put(str2bytes(str(num)))
    stream.put(str2bytes("e"))

def proxy_dump_python2(stream,item):
    if isinstance(item,types.DictionaryType):
        dump_dic(stream,item)
    elif isinstance(item,types.ListType):
        dump_list(stream,item)
    elif isinstance(item,types.StringType):
        dump_str(stream,item)
    elif isinstance(item,types.IntType) or isinstance(item,types.LongType):
        dump_num(stream,item)
    else:
        raise Exception("dump info error")
def proxy_dump(stream,item):
    if isinstance(item,dict):
        dump_dic(stream,item)
    elif isinstance(item,list):
        dump_list(stream,item)
    elif isinstance(item,bytes):
        dump_str(stream,item)
    elif isinstance(item,int):
        dump_num(stream,item)
    else:
        raise Exception("dump info error")
"""
byte stream
"""
class Stream:       
    def __init__(self,filename,mode):
        self.file=open(filename,mode)
    def next(self): #for mode r
        return self.file.read(1)
    def put(self,byte): #for mode w
        self.file.write(byte)
    def close(self):
        self.file.close()
    def __del__(self):
        self.file.close()
