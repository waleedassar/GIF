import os,sys,time,struct

def StringToList(StrX):
    ListX = []
    if StrX == 0:
        return ListX
    lenXXYY = len(StrX)
    if lenXXYY == 0:
        return ListX
    for iy in range(0,lenXXYY):
        ListX.append(StrX[iy])
    return ListX
#-------------------- Start Of rosettacode.org ---------------------
def compress(uncompressed):
    """Compress a string to a list of output symbols."""
 
    # Build the dictionary.
    dict_size = 256
    dictionary = dict((chr(i), chr(i)) for i in xrange(dict_size))
    # in Python 3: dictionary = {chr(i): chr(i) for i in range(dict_size)}
 
    w = ""
    result = []
    for c in uncompressed:
        wc = w + c
        if wc in dictionary:
            w = wc
        else:
            result.append(dictionary[w])
            # Add wc to the dictionary.
            dictionary[wc] = dict_size
            dict_size += 1
            w = c
 
    # Output the code for w.
    if w:
        result.append(dictionary[w])
    return result
 
 
def decompress(compressed):
    """Decompress a list of output ks to a string."""
    from cStringIO import StringIO
 
    # Build the dictionary.
    dict_size = 256
    dictionary = dict((chr(i), chr(i)) for i in xrange(dict_size))
    # in Python 3: dictionary = {chr(i): chr(i) for i in range(dict_size)}
 
    # use StringIO, otherwise this becomes O(N^2)
    # due to string concatenation in a loop
    result = StringIO()
    w = compressed.pop(0)
    result.write(w)
    for k in compressed:
        if k in dictionary:
            entry = dictionary[k]
        elif k == dict_size:
            entry = w + w[0]
        else:
            raise ValueError('Bad compressed k: %s' % k)
        result.write(entry)
 
        # Add w+entry[0] to the dictionary.
        dictionary[dict_size] = w + entry[0]
        dict_size += 1
 
        w = entry
    return result.getvalue()
#---------------- End of rosettacode.org code --------------------

 
if len(sys.argv)!=2:
    print "Usage: GifParser.py input.gif\r\n"
    sys.exit(-1)


inF = sys.argv[1]
if os.path.exists(inF)==False or os.path.getsize(inF)==0:
    print "File does not exist or empty\r\n"
    sys.exit(-2)


fIn = open(inF,"rb")
fCon = fIn.read()
fIn.close()

inFSize = len(fCon)

if inFSize <= 6:
    print "Input file is too small to be GIF image\r\n"
    sys.exit(-3)

Magic = fCon[0:6]

if Magic != "GIF87a" and Magic != "GIF89a":
    print "Invalid GIF Magic\r\n"
    sys.exit(-4)

print "Magic: " + str(Magic)

if inFSize < 13:
    print "Input file is too small to be GIF image\r\n"
    sys.exit(-3)
    
logScreenWidth = fCon[6:8]
logScreenWidth_i = struct.unpack("H",logScreenWidth)[0]
print "Logical Screen Width (pixels): " + str(logScreenWidth_i)

logScreenHeight = fCon[8:10]
logScreenHeight_i = struct.unpack("H",logScreenHeight)[0]
print "Logical Screen Height (pixels): " + str(logScreenHeight_i)

ColorTableFlags = ord(fCon[0xA])
print "ColorFlags: " + str(ColorTableFlags )
NumberOfColors = 0
if ColorTableFlags & 0x80 == 0:
    print "Has Color Map: No"
else:
    print "Has color map: Yes"
    NumberOfColors = (((ColorTableFlags & 0x7)+1))*2
    print "Number of colors: " + str(NumberOfColors)

BackgroundColor = ord(fCon[0xB])
print "Background Color: " + str(BackgroundColor)

DefPixelAspectRatio = ord(fCon[0xC])
print "Default Pixel Aspect Ratio: " + str(DefPixelAspectRatio)


print "Skipping Color Table.."
AfterGCT = 0xD + (NumberOfColors * 3)
#print "Start: " + str(hex(AfterGCT))
if AfterGCT >= inFSize:
    print "Input file is too small to be GIF image\r\n"
    sys.exit(-3)

i = AfterGCT
gOff = 0
while i < inFSize:
    ix = i
    Ctrl = fCon[ix]
    ix += 1
    if Ctrl == "\x21":
        Code = ""
        if ix < inFSize:
            Code = fCon[ix]
            ix += 1
            LenXX = 0
            if ix < inFSize:
                LenXX = struct.unpack("B",fCon[ix:ix+1])[0]
                ix += 1
                gData = ""
                if Code == "\xFF":
                    print "Start of Application Extension block"
                    while LenXX != 0:
                        print "ff --- " + str(hex(LenXX))
                        gData = fCon[ix:ix+LenXX]
                        print gData
                        ix += LenXX
                        LenXX = ord(fCon[ix])
                        ix += 1
                    print "End of Application Extension block"
                elif Code == "\xF9":
                    print "Start of Graphic Control Extension"
                    while LenXX != 0:
                        print "f9 --- " + str(hex(LenXX))
                        gData = fCon[ix:ix+LenXX]
                        ix += LenXX
                        LenXX = ord(fCon[ix])
                        ix += 1
                    print "End of Graphic Control Extension"
                else:
                    print "Uknown function code: " + str(hex(Code))
                    sys.exit(-5)
    elif Ctrl == "\x2C":
        print "Start of Image Descriptor"
        NWCornerFrame = fCon[ix:ix+4]
        ix += 4
        WidthHeightFrame = fCon[ix:ix+4]
        ix += 4
        ColorTableX = ord(fCon[ix])
        ix += 1
        if ColorTableX != 0:
            ColorFlags__x = ColorTableX
            print "Color Flags: " + str(hex(ColorFlags__x))
            if ColorFlags__x & 0x80 != 0:
                ColorAreaSize = 256 * 3
                ix += ColorAreaSize
            #sys.exit(-7)
        LZWMinSize = ord(fCon[ix])
        print "LZW Minimum Length: " + str(LZWMinSize)
        ix += 1
        #Loop here
        while ix < inFSize:
            LenLZW = struct.unpack("B",fCon[ix:ix+1])[0]
            if LenLZW == 0:
                print "End of Image Descriptor"
                ix += 1
                gOff = ix
                break
            ix += 1
            Comp_LZW_Data = fCon[ix:ix+LenLZW]
            Comp_LZW_Data_l = StringToList(Comp_LZW_Data)
            print Comp_LZW_Data_l
            print decompress(Comp_LZW_Data_l)
            ix += LenLZW
    elif Ctrl == "\x3B":
        print "End Of GIF"
        sys.exit(0)
    else:
        print "Uknown Control code: " + str(hex(ord(Ctrl)))
        sys.exit(-5)
    i = ix



