"""
    juman ext api
"""
import os
import sys
import glob
from ctypes import CDLL, Structure, POINTER, byref, cast
from ctypes import c_int, c_char_p, c_size_t, c_byte, c_void_p
import re

def load_lib():
    """ Load shared library """
    libs = glob.glob(os.path.dirname(__file__) + '/libjuman.*so')
    if not libs:
        libs = glob.glob(os.path.dirname(__file__) + '/../dist/juman-*/lib/*.so')
        if not libs:
            print("Cannot find libjuman.so")
            sys.exit(-1)
    if len(libs) > 1: # To narrow down candidates
        if os.name == "nt":
            platform = "win64" if sys.maxsize > 2**32 else "win32"
            pl_libs = filter(lambda x: x.find(platform) >= 0, libs)
        else:   # POSIX
            pl_libs = filter(lambda x: x.find("win64") < 0 and x.find("win32") < 0, libs)
        if pl_libs:
            libs = list(pl_libs)
    return CDLL(libs[0])

LIBC = load_lib()

class MrphT(Structure):  # pylint: disable=R0903
    """ Type of morphese """
    _fields_ = [
        ("midasi1", c_char_p),
        ("yomi", c_char_p),
        ("midasi2", c_char_p),
        ("hinsi", c_int),
        ("bunrui", c_int),
        ("katuyou1", c_int),
        ("katuyou2", c_int)
    ]

#	EXT_RES_CODE
SUCCESS = 0
MRPH_BUFF_OVER = 1
WORD_BUFF_OVER = 2
ERROR = 100
RC_ERROR = 101
MALLOC_ERROR = 102
FILE_NOT_EXISTS = 103
ANA_ERROR = 104
PYMOD_ERROR = 200
TOO_LONG = 201

# void ext_set_encoding(const char *s_encoding);
LIBC.ext_init.restype = None
LIBC.ext_init.argtypes = (c_char_p,)

# EXT_RES_CODE ext_init(const char *s_rcfile, size_t word_buf_size, int max_mrphs);
LIBC.ext_init.restype = c_int
LIBC.ext_init.argtypes = (c_char_p, c_size_t, c_int)

# void ext_close();
LIBC.ext_close.restype = None
LIBC.ext_close.argtypes = ()

# char * ext_get_input_buff(size_t *psize);
LIBC.ext_get_input_buff.restype = POINTER(c_byte)
LIBC.ext_get_input_buff.argtypes = (POINTER(c_size_t),)

# EXT_MRPH_T * ext_get_mrph_buff();
LIBC.ext_get_mrph_buff.restype = POINTER(MrphT)
LIBC.ext_get_mrph_buff.argtypes = ()

# EXT_RES_CODE ext_analyze();
LIBC.ext_analyze.restype = c_int
LIBC.ext_analyze.argtypes = ()

# EXT_RES_CODE ext_get_result(int *pnum_mrphs);
LIBC.ext_get_result.restype = c_int
LIBC.ext_get_result.argtypes = (POINTER(c_int),)

# const char * ext_get_hinsi(int hinsi);
LIBC.ext_get_hinsi.restype = c_char_p
LIBC.ext_get_hinsi.argtypes = (c_int,)

# int ext_get_all_hinsi(const char ** list);
LIBC.ext_get_all_hinsi.restype = c_int
LIBC.ext_get_all_hinsi.argtypes = (POINTER(c_char_p),)

# const char * ext_get_bunrui(int hinsi, int bunrui);
LIBC.ext_get_bunrui.restype = c_char_p
LIBC.ext_get_bunrui.argtypes = (c_int, c_int)

# int ext_get_all_bunrui(int hinsi, const char ** list);
LIBC.ext_get_all_bunrui.restype = c_int
LIBC.ext_get_all_bunrui.argtypes = (c_int, POINTER(c_char_p))

# const char * ext_get_katuyou1(int katuyou1);
LIBC.ext_get_katuyou1.restype = c_char_p
LIBC.ext_get_katuyou1.argtypes = (c_int,)

# int ext_get_all_katuyou1(const char ** list);
LIBC.ext_get_all_katuyou1.restype = c_int
LIBC.ext_get_all_katuyou1.argtypes = (POINTER(c_char_p),)

# const char * ext_get_katuyou2(int katuyou1, int katuyou2);
LIBC.ext_get_katuyou2.restype = c_char_p
LIBC.ext_get_katuyou2.argtypes = (c_int, c_int)

# int ext_get_all_katuyou2(int katuyou1, const char ** list);
LIBC.ext_get_all_katuyou2.restype = c_int
LIBC.ext_get_all_katuyou2.argtypes = (c_int, POINTER(c_char_p))

# void ext_get_maxidx(int *pmax_hinsi, int *pmax_bunrui,
#	int *pmax_katuyou1, int *pmax_hatuyou2);
LIBC.ext_get_maxidx.restype = None
LIBC.ext_get_maxidx.argtypes = (POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int))

ERRORNO = SUCCESS

L_HINSI = []
L_BUNRUI = []
L_KATUYOU1 = []
L_KATUYOU2 = []

_JUMANRC = None
_WRITE_BUF = None
_BUF_SIZE = None
_READ_BUF = None
_ENCODING = "UTF-8"

_RE_EMPTY = re.compile(r"^[ \t\r\n]+$")

def get_error_msg()->str:
    """ Get last error message
    @return Error message. Or null string when no error.
    """
    msg = "Something wrong."
    if ERRORNO == SUCCESS:
        msg = ""
    elif ERRORNO == MRPH_BUFF_OVER:
        msg = "Morpheme buffer is not enough. Need to call several times."
    elif ERRORNO == WORD_BUFF_OVER:
        msg = "Word buffer is not enough. Need to call several times."
    elif ERRORNO == ERROR:
        msg = "Error in previous call."
    elif ERRORNO == RC_ERROR:
        msg = "Error in jumanrc."
    elif ERRORNO == MALLOC_ERROR:
        msg = "Fail to allocate buffer."
    elif ERRORNO == FILE_NOT_EXISTS:
        msg = "File does not exist."
    elif ERRORNO == ANA_ERROR:
        msg = "Error in analyze."
    elif ERRORNO == TOO_LONG:
        msg = "Input text is too long."
    return msg

def status(stream=None):
    """ Show status
    @param stream Stream to output
    @return String of status
    """
    stat_str = ""
    if _JUMANRC is None:
        stat_str += "Closed."
    else:
        stat_str += "Resource file: %s\n" % _JUMANRC
        ptr = cast(_WRITE_BUF, c_void_p)
        stat_str += "Write buffer : %s\n" % hex(ptr.value)
        stat_str += "Buffer size  : %d\n" % _BUF_SIZE
        ptr = cast(_READ_BUF, c_void_p)
        stat_str += "Read buffer  : %s\n" % hex(ptr.value)
        stat_str += "ERRORNO      : %d\n" % ERRORNO
        stat_str += "message : %s\n" % get_error_msg()
    if stream:
        stream.write(stat_str)
    return stat_str

def open_lib(rc_path: str = None)->bool:
    """ Open juman library
    @param rc_path Path to resource file. None is available to load default.
    @return True when success, otherwise False.
    """
    global _JUMANRC, ERRORNO, _WRITE_BUF, _BUF_SIZE, _READ_BUF
    global L_HINSI, L_BUNRUI, L_KATUYOU1, L_KATUYOU2
    ERRORNO = SUCCESS
    if _JUMANRC is not None:
        return True
    if rc_path is None:
        abspath = os.path.abspath(__file__)
        rc_path = os.path.join(os.path.dirname(abspath), 'jumanrc')
    if not os.path.exists(rc_path):
        ERRORNO = FILE_NOT_EXISTS
        return False
    res = LIBC.ext_init(rc_path.encode('UTF-8'), 0, 0)
    if SUCCESS != res:
        ERRORNO = res
        return False
    _JUMANRC = rc_path
    size = c_size_t()
    _WRITE_BUF = LIBC.ext_get_input_buff(byref(size))
    _BUF_SIZE = size.value
    _WRITE_BUF = cast(_WRITE_BUF, POINTER(c_byte * _BUF_SIZE))
    _READ_BUF = LIBC.ext_get_mrph_buff()
    # Get all word of grammar
    max_param = [c_int() for i in range(4)]
    LIBC.ext_get_maxidx(
        byref(max_param[0]), byref(max_param[1]),
        byref(max_param[2]), byref(max_param[3]))
    max_param = (x.value for x in max_param)
    max_num = max(max_param)
    alist = (c_char_p * max_num)()
    hinsi_num = LIBC.ext_get_all_hinsi(alist)
    for i in range(0, hinsi_num):
        L_HINSI.append(alist[i].decode("UTF-8"))
    for i in range(0, hinsi_num):
        sub_num = LIBC.ext_get_all_bunrui(i, alist)
        sublist = []
        for j in range(0, sub_num):
            sublist.append(alist[j].decode("UTF-8"))
        L_BUNRUI.append(sublist)
    k1_num = LIBC.ext_get_all_katuyou1(alist)
    for i in range(0, k1_num):
        L_KATUYOU1.append(alist[i].decode("UTF-8"))
    for i in range(0, k1_num):
        sub_num = LIBC.ext_get_all_katuyou2(i, alist)
        sublist = []
        for j in range(0, sub_num):
            sublist.append(alist[j].decode("UTF-8"))
        L_KATUYOU2.append(sublist)

    return True

def close_lib():
    """ Close juman library  """
    global _JUMANRC, ERRORNO, _WRITE_BUF, _BUF_SIZE, _READ_BUF
    global L_HINSI, L_BUNRUI, L_KATUYOU1, L_KATUYOU2
    if _JUMANRC is None:
        return
    LIBC.ext_close()
    # Clear
    _JUMANRC = None
    _WRITE_BUF = None
    _BUF_SIZE = None
    _READ_BUF = None
    _ENCODING = "UTF-8"
    L_HINSI = []
    L_BUNRUI = []
    L_KATUYOU1 = []
    L_KATUYOU2 = []

def set_encoding(encoding: str):
    """ Set encoding of input text
    @param encoding String of encoding
    @todo need to consider working with bytes data.
    """
    global _ENCODING
    _ENCODING = encoding

def analyze(text: str, remove_space: bool = False, just_word: bool = False)->[]:
    """ Analyze sentences
    @param text String to analyze
    @param remove_space If True, remove morpheme consist from only space, CR, LF, and tab.
    @param just_word If True, only word in text is set in list.
    Otherwise tuple of params is set.
    @return List of morpheme. If None, Error occured.
    If just_word is True, list likes [word:str, word:str, ... ].
    If just_word is False, list likes
    [ (midasi1:str, yimi:str, midasi2:str, hinsi:int,
        bunrui:int, katuyou1:int, katutou2:int), ... ]
    """
    global ERRORNO, _ENCODING
    if _do_analyze(text) is False:
        return None
    # Get result
    num = c_int()
    mrphs = []
    res = -1
    while res != SUCCESS:
        res = LIBC.ext_get_result(byref(num))
        if res >= ERROR:
            ERRORNO = res
            return None
        for i in range(0, num.value):
            word = _READ_BUF[i].midasi1.decode("UTF-8")
            if remove_space and re.match(_RE_EMPTY, word) is not None:
                continue
            if just_word:
                mrphs.append(word)
            else:
                mrph = _READ_BUF[i]
                mrphs.append((
                    word, mrph.yomi.decode("UTF-8"),
                    mrph.midasi2.decode("UTF-8"), mrph.hinsi,
                    mrph.bunrui, mrph.katuyou1, mrph.katuyou2
                ))
    return mrphs

def _do_analyze(text: str)->bool:
    """ Execute analyze part
    @param text String to analyze
    @return True when success, otherwise False.
    """
    global ERRORNO, _ENCODING
    data = text.encode(_ENCODING)
    data_len = len(data)
    if data_len >= _BUF_SIZE:
        ERRORNO = TOO_LONG
        return False
    _WRITE_BUF.contents[:data_len] = data[:]
    _WRITE_BUF.contents[data_len] = 0
    res = LIBC.ext_analyze()
    if res != SUCCESS:
        ERRORNO = res
        return False
    return True

def get_hinsi(hinsi: int)->str:
    """ Get honsi from code
    @param hinsi Hinsi code
    @reurn String of hinsi
    """
    global L_HINSI
    return L_HINSI[hinsi]

def get_bunrui(hinsi: int, bunrui: int)->str:
    """ Get bunrui from codes
    @param hinsi Hinsi code
    @param bunrui bunrui code
    @reurn String of bunrui
    """
    global L_BUNRUI
    return L_BUNRUI[hinsi][bunrui]

def get_katuyou1(katuyou1: int)->str:
    """ Get katuyou1 from code
    @param katuyou1 Katuyou1 code
    @reurn String of katuyou1
    """
    global L_KATUYOU1
    return L_KATUYOU1[katuyou1]

def get_katuyou2(katuyou1: int, katuyou2: int)->str:
    """ Get katuyou2 from codes
    @param katuyou1 Katuyou1 code
    @param katuyou2 Katuyou2 code
    @reurn String of katuyou2
    """
    global L_KATUYOU2
    return L_KATUYOU2[katuyou1][katuyou2]

if __name__ == '__main__':
    from test import get_jumanrc
    status(sys.stderr)
    if open_lib(get_jumanrc()) is False:
        print(get_error_msg())
        sys.exit(0)
    status(sys.stderr)
    Text = """吾輩は猫である。名前はまだ無い。\t
どこで生れたかとんと見当がつかぬ。何でも薄暗いじめじめした所でニャーニャー泣いていた事だけは記憶している。吾輩はここで始めて人間というものを見た。"""
    Mrphs = analyze(Text)
    if Mrphs is None:
        print(get_error_msg())
        sys.exit(0)
    print(repr(Mrphs))
    for (Midasi1, Yomi, Midasi2, Hinsi, Bunrui, Katuyou1, Katuyou2) in Mrphs:
        print("{} : {} : {} : {} : {} : {} : {}".format(
            Midasi1, Yomi, Midasi2, get_hinsi(Hinsi),
            get_bunrui(Hinsi, Bunrui), get_katuyou1(Katuyou1),
            get_katuyou2(Katuyou1, Katuyou2)
        ))
    print(analyze(Text, True, True))
    close_lib()
