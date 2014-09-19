"""
Useful constants culled lovingly from the loam/plasma header files.
"""

# (c) 2014 MCT

import sys

PYPLASMA_VERSION                      = '2.0.0'
DEFAULT_POOLS_DIR                     = '/var/ob/pools'
SLAW_VERSION_CURRENT                  = 2
PLASMA_BINARY_FILE_TYPE_SLAW          = 1
PLASMA_BINARY_FILE_TYPE_POOL          = 2
POOL_TCP_VERSION_CURRENT              = 3

## libLoam/ob-retorts.h
OB_RETORTS_COMMON_FIRST               = 0
OB_RETORTS_COMMON_LAST                = 99999
OB_RETORTS_APP_FIRST                  = 100000
OB_RETORTS_APP_LAST                   = 199999
OB_RETORTS_PLASMA_FIRST               = 200000
OB_RETORTS_PLASMA_LAST                = 299999
OB_RETORTS_VIDEO_FIRST                = 300000
OB_RETORTS_VIDEO_LAST                 = 399999
OB_RETORTS_BASEMENT_FIRST             = 400000
OB_RETORTS_BASEMENT_LAST              = 499999
OB_RETORTS_IMPETUS_FIRST              = 500000
OB_RETORTS_IMPETUS_LAST               = 599999
OB_RETORTS_NOODOO_FIRST               = 600000
OB_RETORTS_NOODOO_LAST                = 699999
OB_RETORTS_AFFERENT_FIRST             = 700000
OB_RETORTS_AFFERENT_LAST              = 799999
OB_RETORTS_PROTIST_FIRST              = 800000
OB_RETORTS_PROTIST_LAST               = 899999
OB_RETORTS_LOAMXX_FIRST               = 900000
OB_RETORTS_LOAMXX_LAST                = 999999
OB_RETORTS_GANGLIA_FIRST              = 1000000
OB_RETORTS_GANGLIA_LAST               = 1099999
OB_RETORTS_PLASMAXX_FIRST             = 1100000
OB_RETORTS_PLASMAXX_LAST              = 1199999
OB_RETORTS_WIN32_FIRST                = 0x7fffffff00000000
OB_RETORTS_WIN32_LAST                 = 0x7fffffffffffffff
OB_OK                                 = 0
OB_NO_MEM                             = -201
OB_BAD_INDEX                          = -202
OB_ARGUMENT_WAS_NULL                  = -203
OB_NOT_FOUND                          = -204
OB_INVALID_ARGUMENT                   = -205
OB_UNKNOWN_ERR                        = -220
OB_INADEQUATE_CLASS                   = -221
OB_ALREADY_PRESENT                    = -222
OB_EMPTY                              = -223
OB_INVALID_OPERATION                  = -224
OB_DISCONNECTED                       = -260
OB_VERSION_MISMATCH                   = -261
OB_STOP                               = 300
OB_NOTHING_TO_DO                      = 301
OB_YES                                = 302
OB_NO                                 = 303
OB_MIN_ERRNO                          = 1
OB_MAX_ERRNO                          = 999
OB_SHARED_ERRNOS                      = 0x7fbff77fe
OB_RETORTS_ERRNO_SHARED               = 90000 # thru 90999
OB_RETORTS_ERRNO_LINUX                = 91000 # thru 91999
OB_RETORTS_ERRNO_MACOSX               = 92000 # thru 92999
OB_RETORTS_ERRNO_WINDOWS              = 93000 # thru 93999

OB_RETORTS_PLASMA_SLAW                = (OB_RETORTS_PLASMA_FIRST + 10000)
OB_RETORTS_PLASMA_IO                  = (OB_RETORTS_PLASMA_FIRST + 20000)
SLAW_CORRUPT_PROTEIN                  = -(OB_RETORTS_PLASMA_SLAW + 0)
SLAW_CORRUPT_SLAW                     = -(OB_RETORTS_PLASMA_SLAW + 1)
SLAW_FABRICATOR_BADNESS               = -(OB_RETORTS_PLASMA_SLAW + 2)
SLAW_NOT_NUMERIC                      = -(OB_RETORTS_PLASMA_SLAW + 3)
SLAW_RANGE_ERR                        = -(OB_RETORTS_PLASMA_SLAW + 4)
SLAW_UNIDENTIFIED_SLAW                = -(OB_RETORTS_PLASMA_SLAW + 5)
SLAW_WRONG_LENGTH                     = -(OB_RETORTS_PLASMA_SLAW + 6)
SLAW_NOT_FOUND                        = -(OB_RETORTS_PLASMA_SLAW + 7)
SLAW_ALIAS_NOT_SUPPORTED              = -(OB_RETORTS_PLASMA_IO + 0)
SLAW_BAD_TAG                          = -(OB_RETORTS_PLASMA_IO + 1)
SLAW_END_OF_FILE                      = -(OB_RETORTS_PLASMA_IO + 2)
SLAW_PARSING_BADNESS                  = -(OB_RETORTS_PLASMA_IO + 3)
SLAW_WRONG_FORMAT                     = -(OB_RETORTS_PLASMA_IO + 4)
SLAW_WRONG_VERSION                    = -(OB_RETORTS_PLASMA_IO + 5)
SLAW_YAML_ERR                         = -(OB_RETORTS_PLASMA_IO + 6)
SLAW_NO_YAML                          = -(OB_RETORTS_PLASMA_IO + 7)

SEARCH_GAP                            = 0
SEARCH_CONTIG                         = 1

## libPlasma / plasma-retorts.h
OB_RETORTS_PLASMA_POOLS               = (OB_RETORTS_PLASMA_FIRST)
POOL_NO_POOLS_DIR                     = -(OB_RETORTS_PLASMA_POOLS +  400)
POOL_FILE_BADTH                       = -(OB_RETORTS_PLASMA_POOLS +  500)
POOL_NULL_HOSE                        = -(OB_RETORTS_PLASMA_POOLS +  505)
POOL_SEMAPHORES_BADTH                 = -(OB_RETORTS_PLASMA_POOLS +  510)
POOL_MMAP_BADTH                       = -(OB_RETORTS_PLASMA_POOLS +  520)
POOL_INAPPROPRIATE_FILESYSTEM         = -(OB_RETORTS_PLASMA_POOLS +  525)
POOL_IN_USE                           = -(OB_RETORTS_PLASMA_POOLS +  530)
POOL_TYPE_BADTH                       = -(OB_RETORTS_PLASMA_POOLS +  540)
POOL_CONFIG_BADTH                     = -(OB_RETORTS_PLASMA_POOLS +  545)
POOL_WRONG_VERSION                    = -(OB_RETORTS_PLASMA_POOLS +  547)
POOL_CORRUPT                          = -(OB_RETORTS_PLASMA_POOLS +  548)
POOL_POOLNAME_BADTH                   = -(OB_RETORTS_PLASMA_POOLS +  550)
POOL_IMPOSSIBLE_RENAME                = -(OB_RETORTS_PLASMA_POOLS +  551)
POOL_FIFO_BADTH                       = -(OB_RETORTS_PLASMA_POOLS +  555)
POOL_INVALID_SIZE                     = -(OB_RETORTS_PLASMA_POOLS +  560)
POOL_NO_SUCH_POOL                     = -(OB_RETORTS_PLASMA_POOLS +  570)
POOL_EXISTS                           = -(OB_RETORTS_PLASMA_POOLS +  575)
POOL_ILLEGAL_NESTING                  = -(OB_RETORTS_PLASMA_POOLS +  576)
POOL_PROTOCOL_ERROR                   = -(OB_RETORTS_PLASMA_POOLS +  580)
POOL_NO_SUCH_PROTEIN                  = -(OB_RETORTS_PLASMA_POOLS +  635)
POOL_AWAIT_TIMEDOUT                   = -(OB_RETORTS_PLASMA_POOLS +  640)
POOL_AWAIT_WOKEN                      = -(OB_RETORTS_PLASMA_POOLS +  650)
POOL_WAKEUP_NOT_ENABLED               = -(OB_RETORTS_PLASMA_POOLS +  660)
POOL_PROTEIN_BIGGER_THAN_POOL         = -(OB_RETORTS_PLASMA_POOLS +  700)
POOL_FROZEN                           = -(OB_RETORTS_PLASMA_POOLS +  710)
POOL_FULL                             = -(OB_RETORTS_PLASMA_POOLS +  720)
POOL_NOT_A_PROTEIN                    = -(OB_RETORTS_PLASMA_POOLS +  800)
POOL_NOT_A_PROTEIN_OR_MAP             = -(OB_RETORTS_PLASMA_POOLS +  810)
POOL_CONF_WRITE_BADTH                 = -(OB_RETORTS_PLASMA_POOLS +  900)
POOL_CONF_READ_BADTH                  = -(OB_RETORTS_PLASMA_POOLS +  910)
POOL_SEND_BADTH                       = -(OB_RETORTS_PLASMA_POOLS + 1000)
POOL_RECV_BADTH                       = -(OB_RETORTS_PLASMA_POOLS + 1010)
POOL_SOCK_BADTH                       = -(OB_RETORTS_PLASMA_POOLS + 1020)
POOL_SERVER_BUSY                      = -(OB_RETORTS_PLASMA_POOLS + 1030)
POOL_SERVER_UNREACH                   = -(OB_RETORTS_PLASMA_POOLS + 1040)
POOL_ALREADY_GANG_MEMBER              = -(OB_RETORTS_PLASMA_POOLS + 1050)
POOL_NOT_A_GANG_MEMBER                = -(OB_RETORTS_PLASMA_POOLS + 1055)
POOL_EMPTY_GANG                       = -(OB_RETORTS_PLASMA_POOLS + 1060)
POOL_NULL_GANG                        = -(OB_RETORTS_PLASMA_POOLS + 1070)
POOL_UNSUPPORTED_OPERATION            = -(OB_RETORTS_PLASMA_POOLS + 1100)
POOL_INVALIDATED_BY_FORK              = -(OB_RETORTS_PLASMA_POOLS + 1110)
POOL_NO_TLS                           = -(OB_RETORTS_PLASMA_POOLS + 1500)
POOL_TLS_REQUIRED                     = -(OB_RETORTS_PLASMA_POOLS + 1505)
POOL_TLS_ERROR                        = -(OB_RETORTS_PLASMA_POOLS + 1510)
POOL_CREATED                          =  (OB_RETORTS_PLASMA_POOLS + 10)

DEFAULT_AWAIT_TIMEOUT                 = 3600

POOL_WAIT_FOREVER                     = -1.0
POOL_NO_WAIT                          =  0.0
POOL_WAIT_FOREVER_OLD                 =  0.0
POOL_NO_WAIT_OLD                      = -1.0
TIMESTAMP_ABSOLUTE                    = -1
TIMESTAMP_RELATIVE                    =  0
DIRECTION_ABSOLUTE                    =  0
DIRECTION_LOWER                       =  1
DIRECTION_HIGHER                      =  2

BUFSIZE                               = 4096
DEFAULT_PORT                          = 65456

POOL_DIRECTORY_VERSION_CONFIG_IN_FILE = 4
POOL_DIRECTORY_VERSION_CONFIG_IN_MMAP = 5
POOL_DIRECTORY_VERSION_SINGLE_FILE    = 6

POOL_FLAG_STOP_WHEN_FULL              = 1 << 0
POOL_FLAG_FROZEN                      = 1 << 1
POOL_FLAG_AUTO_DISPOSE                = 1 << 2
POOL_FLAG_CHECKSUM                    = 1 << 3
POOL_FLAG_SYNC                        = 1 << 32

KILOBYTE                              = 2**10
MEGABYTE                              = 2**20
GIGABYTE                              = 2**30
TERABYTE                              = 2**40
POOL_SIZE_TINY                        = 10 * KILOBYTE
POOL_SIZE_SMALL                       = 1 * MEGABYTE
POOL_SIZE_MEDIUM                      = 10 * MEGABYTE
POOL_SIZE_LARGE                       = 100 * MEGABYTE
POOL_SIZE_OBSCENE                     = 2 * GIGABYTE
if sys.maxsize > 2**32:
    POOL_SIZE_MAX                     = 8 * TERABYTE
else:
    POOL_SIZE_MAX                     = 2 * GIGABYTE

HOSE_STATE_INITIAL                    = 0
HOSE_STATE_PARTICIPATE                = 1
HOSE_STATE_FINAL                      = 2
