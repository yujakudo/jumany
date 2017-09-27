"""
jumany
Python interface for JUMAN
"""
from .juman_ext import SUCCESS, MRPH_BUFF_OVER, WORD_BUFF_OVER
from .juman_ext import ERROR, RC_ERROR, MALLOC_ERROR, FILE_NOT_EXISTS
from .juman_ext import ANA_ERROR, PYMOD_ERROR, TOO_LONG

from .juman_ext import ERRORNO, L_HINSI, L_BUNRUI, L_KATUYOU1, L_KATUYOU2

from .juman_ext import get_error_msg, open_lib, close_lib, analyze
from .juman_ext import get_hinsi, get_bunrui, get_katuyou1, get_katuyou2
# from .juman_ext import set_encoding
