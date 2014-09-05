import re
import platform

#
#from loam.const import *
#

## libLoam / ob-retorts.h
OB_RETORTS_COMMON_FIRST        = 0
OB_RETORTS_COMMON_LAST     = 99999
OB_RETORTS_APP_FIRST      = 100000
OB_RETORTS_APP_LAST       = 199999
OB_RETORTS_PLASMA_FIRST   = 200000
OB_RETORTS_PLASMA_LAST    = 299999
OB_RETORTS_VIDEO_FIRST    = 300000
OB_RETORTS_VIDEO_LAST     = 399999
OB_RETORTS_BASEMENT_FIRST = 400000
OB_RETORTS_BASEMENT_LAST  = 499999
OB_RETORTS_IMPETUS_FIRST  = 500000
OB_RETORTS_IMPETUS_LAST   = 599999
OB_RETORTS_NOODOO_FIRST   = 600000
OB_RETORTS_NOODOO_LAST    = 699999
OB_RETORTS_AFFERENT_FIRST = 700000
OB_RETORTS_AFFERENT_LAST  = 799999
OB_RETORTS_PROTIST_FIRST  = 800000
OB_RETORTS_PROTIST_LAST   = 899999
OB_RETORTS_LOAMXX_FIRST   = 900000
OB_RETORTS_LOAMXX_LAST    = 999999
OB_RETORTS_GANGLIA_FIRST   = 1000000
OB_RETORTS_GANGLIA_LAST    = 1099999
OB_RETORTS_PLASMAXX_FIRST  = 1100000
OB_RETORTS_PLASMAXX_LAST   = 1199999
OB_RETORTS_WIN32_FIRST = 0x7fffffff00000000
OB_RETORTS_WIN32_LAST  = 0x7fffffffffffffff
OB_OK                   = 0
OB_NO_MEM               = -201
OB_BAD_INDEX            = -202
OB_ARGUMENT_WAS_NULL    = -203
OB_NOT_FOUND            = -204
OB_INVALID_ARGUMENT     = -205
OB_UNKNOWN_ERR          = -220
OB_INADEQUATE_CLASS     = -221
OB_ALREADY_PRESENT      = -222
OB_EMPTY                = -223
OB_INVALID_OPERATION    = -224
OB_DISCONNECTED         = -260
OB_VERSION_MISMATCH     = -261
OB_STOP                  = 300
OB_NOTHING_TO_DO         = 301
OB_NO                    = 303
OB_MIN_ERRNO = 1
OB_MAX_ERRNO = 999
OB_SHARED_ERRNOS = 0x7fbff77fe
OB_RETORTS_ERRNO_SHARED  = 90000 # thru 90999
OB_RETORTS_ERRNO_LINUX   = 91000 # thru 91999
OB_RETORTS_ERRNO_MACOSX  = 92000 # thru 92999
OB_RETORTS_ERRNO_WINDOWS = 93000 # thru 93999

OB_RETORTS_PLASMA_SLAW  = (OB_RETORTS_PLASMA_FIRST + 10000)
OB_RETORTS_PLASMA_IO    = (OB_RETORTS_PLASMA_FIRST + 20000)
SLAW_CORRUPT_PROTEIN     = -(OB_RETORTS_PLASMA_SLAW + 0)
SLAW_CORRUPT_SLAW        = -(OB_RETORTS_PLASMA_SLAW + 1)
SLAW_FABRICATOR_BADNESS  = -(OB_RETORTS_PLASMA_SLAW + 2)
SLAW_NOT_NUMERIC         = -(OB_RETORTS_PLASMA_SLAW + 3)
SLAW_RANGE_ERR           = -(OB_RETORTS_PLASMA_SLAW + 4)
SLAW_UNIDENTIFIED_SLAW   = -(OB_RETORTS_PLASMA_SLAW + 5)
SLAW_WRONG_LENGTH        = -(OB_RETORTS_PLASMA_SLAW + 6)
SLAW_NOT_FOUND           = -(OB_RETORTS_PLASMA_SLAW + 7)
SLAW_ALIAS_NOT_SUPPORTED = -(OB_RETORTS_PLASMA_IO + 0)
SLAW_BAD_TAG             = -(OB_RETORTS_PLASMA_IO + 1)
SLAW_END_OF_FILE         = -(OB_RETORTS_PLASMA_IO + 2)
SLAW_PARSING_BADNESS     = -(OB_RETORTS_PLASMA_IO + 3)
SLAW_WRONG_FORMAT        = -(OB_RETORTS_PLASMA_IO + 4)
SLAW_WRONG_VERSION       = -(OB_RETORTS_PLASMA_IO + 5)
SLAW_YAML_ERR            = -(OB_RETORTS_PLASMA_IO + 6)
SLAW_NO_YAML             = -(OB_RETORTS_PLASMA_IO + 7)



#
#from loam.exceptions import *
#
class ObException(Exception):
    """
    Base exception class for loam and plasma.  In the C versions of these
    libraries, exceptions are indicated by numeric (int64) return values
    from functions, but we have the luxury of raising exceptions.  These
    exceptions should corespond one to one with the libLoam and libPlasma
    "retorts".  If you are already familiar with those implementations,
    the exception names we define here should merely be StudlyCap translations
    of the C constants, with the word "Exception" tacked onto the end.
    """

    def __init__(self, msg=None, retort=None):
        self.msg = msg
        self._retort = retort

    def __str__(self):
        try:
            return '%s(%d): %s' % (type(self).__name__, self.retort(), self.msg)
        except:
            return self.msg

    def __repr__(self):
        return self.__str__()

    def name(self):
        ex = re.sub('([A-Z])', '_\\1', type(self).__name__)[1:].upper()
        return ex.replace('_EXCEPTION', '')

class ObErrnoException(ObException):
    """
    Wrapper exception for system defined errno-style exceptions.
    """
    def __init__(self, msg='', errno=None, retort=None):
        self.msg = msg
        self.errno = errno
        self._retort = retort

    def retort(self):
        """
        Returns the numeric retort associated with this exception
        """
        if self._retort is not None:
            return self._retort
        if self.errno is None:
            return OB_UNKNOWN_ERR
        if self.errno < OB_MIN_ERRNO or self.errno > OB_MAX_ERRNO:
            return OB_UNKNOWN_ERR
        if self.errno < 64 and (OB_SHARED_ERRNOS & (1 << self.errno)):
            return -1 * (OB_RETORTS_ERRNO_SHARED + self.errno)
        system = platform.system()
        if system == 'Linux':
            return -1 * (OB_RETORTS_ERRNO_LINUX + self.errno)
        if system == 'Darwin':
            return -1 * (OB_RETORTS_ERRNO_MACOSX + self.errno)
        if system == 'Windows':
            return -1 * (OB_RETORTS_ERRNO_WINDOWS + self.errno)
        return OB_UNKNOWN_ERR

class LoamException(ObException):
    def retort(self):
        """
        Returns the numeric retort associated with this exception
        """
        if self._retort is not None:
            return self._retort
        const = re.sub('([A-Za-z])([A-Z])', '\\1_\\2', type(self).__name__[:-9]).upper()
        return globals()[const]

#---------------------------------------------------
class DataPackingException(LoamException):
    pass

class AlarmException(LoamException):
    pass

class HoseCommandException(LoamException):
    pass

class HoseStateException(LoamException):
    pass

class PackingException(LoamException):
    pass

class PoolCommandException(LoamException):
    pass

class PoolInvalidName(LoamException):
    pass

class SlawError(LoamException):
    pass

class StompledException(LoamException):
    pass

class UnsupportedPoolType(LoamException):
    pass

class VersionError(LoamException):
    pass

class WakeUpException(LoamException):
    pass

#----------------------

class ObNoMemException(LoamException):
    """
    malloc failed, or similar
    """
    pass

class ObBadIndexException(LoamException):
    """
    out-of-bounds access
    """
    pass

class ObArgumentWasNullException(LoamException):
    """
    function was not expecting a NULL argument, but it was nice enough to
    tell you instead of segfaulting.
    """
    pass

class ObNotFoundException(LoamException):
    """
    not the droids you're looking for
    """
    pass

class ObInvalidArgumentException(LoamException):
    """
    argument badness other than NULL or out-of-bounds
    """
    pass

class ObUnknownErrException(LoamException):
    """
    There was no way to determine what the error was, or the error is
    so esoteric that nobody has bothered allocating a code for it yet.
    """
    pass

class ObInadequateClassException(LoamException):
    """
    wrong parentage
    """
    pass

class ObAlreadyPresentException(LoamException):
    """
    You tried to add something that was already there.
    """
    pass

class ObEmptyException(LoamException):
    """
    There was nothing there.  (e. g. popping from an empty stack)
    """
    pass

class ObInvalidOperationException(LoamException):
    """
    You tried to do something that was not allowed.
    """
    pass

class ObDisconnectedException(LoamException):
    """
    The link to whatever-you-were-talking-to has been severed
    """
    pass

class ObVersionMismatchException(LoamException):
    """
    Illegal mixing of different versions of g-speak headers and shared libs.
    """
    pass

class SlawCorruptProteinException(LoamException):
    """
    """
    def __str__(self):
        return '%s: %s' % (type(self).__name__, self.msg)

class SlawCorruptSlawException(LoamException):
    """
    """
    pass

class SlawFabricatorBadnessException(LoamException):
    """
    """
    pass

class SlawNotNumericException(LoamException):
    """
    """
    pass

class SlawRangeErrException(LoamException):
    """
    """
    pass

class SlawUnidentifiedSlawException(LoamException):
    """
    """
    pass

class SlawWrongLengthException(LoamException):
    """
    """
    pass

class SlawNotFoundException(LoamException):
    """
    """
    pass

class SlawAliasNotSupportedException(LoamException):
    """
    """
    pass

class SlawBadTagException(LoamException):
    """
    """
    pass

class SlawEndOfFileException(LoamException):
    """
    """
    pass

class SlawParsingBadnessException(LoamException):
    """
    """
    pass

class SlawWrongFormatException(LoamException):
    """
    """
    pass

class SlawWrongVersionException(LoamException):
    """
    """
    pass

class SlawYamlErrException(LoamException):
    """
    """
    pass

class SlawNoYamlException(LoamException):
    """
    """
    pass


LOAM_RETORT_EXCEPTIONS = {
    OB_NO_MEM:            ObNoMemException,
    OB_BAD_INDEX:         ObBadIndexException,
    OB_ARGUMENT_WAS_NULL: ObArgumentWasNullException,
    OB_NOT_FOUND:         ObNotFoundException,
    OB_INVALID_ARGUMENT:  ObInvalidArgumentException,
    OB_UNKNOWN_ERR:       ObUnknownErrException,
    OB_INADEQUATE_CLASS:  ObInadequateClassException,
    OB_ALREADY_PRESENT:   ObAlreadyPresentException,
    OB_EMPTY:             ObEmptyException,
    OB_INVALID_OPERATION: ObInvalidOperationException,
    OB_DISCONNECTED:      ObDisconnectedException,
    OB_VERSION_MISMATCH:  ObVersionMismatchException,

    SLAW_CORRUPT_PROTEIN:          SlawCorruptProteinException,
    SLAW_CORRUPT_SLAW:             SlawCorruptSlawException,
    SLAW_FABRICATOR_BADNESS:       SlawFabricatorBadnessException,
    SLAW_NOT_NUMERIC:              SlawNotNumericException,
    SLAW_RANGE_ERR:                SlawRangeErrException,
    SLAW_UNIDENTIFIED_SLAW:        SlawUnidentifiedSlawException,
    SLAW_WRONG_LENGTH:             SlawWrongLengthException,
    SLAW_NOT_FOUND:                SlawNotFoundException,
    SLAW_ALIAS_NOT_SUPPORTED:      SlawAliasNotSupportedException,
    SLAW_BAD_TAG:                  SlawBadTagException,
    SLAW_END_OF_FILE:              SlawEndOfFileException,
    SLAW_PARSING_BADNESS:          SlawParsingBadnessException,
    SLAW_WRONG_FORMAT:             SlawWrongFormatException,
    SLAW_WRONG_VERSION:            SlawWrongVersionException,
    SLAW_YAML_ERR:                 SlawYamlErrException,
    SLAW_NO_YAML:                  SlawNoYamlException,
}




#
# plasma const
#

## libPlasma / plasma-retorts.h
OB_RETORTS_PLASMA_POOLS = (OB_RETORTS_PLASMA_FIRST)
POOL_NO_POOLS_DIR             = -(OB_RETORTS_PLASMA_POOLS +  400)
POOL_FILE_BADTH               = -(OB_RETORTS_PLASMA_POOLS +  500)
POOL_NULL_HOSE                = -(OB_RETORTS_PLASMA_POOLS +  505)
POOL_SEMAPHORES_BADTH         = -(OB_RETORTS_PLASMA_POOLS +  510)
POOL_MMAP_BADTH               = -(OB_RETORTS_PLASMA_POOLS +  520)
POOL_INAPPROPRIATE_FILESYSTEM = -(OB_RETORTS_PLASMA_POOLS +  525)
POOL_IN_USE                   = -(OB_RETORTS_PLASMA_POOLS +  530)
POOL_TYPE_BADTH               = -(OB_RETORTS_PLASMA_POOLS +  540)
POOL_CONFIG_BADTH             = -(OB_RETORTS_PLASMA_POOLS +  545)
POOL_WRONG_VERSION            = -(OB_RETORTS_PLASMA_POOLS +  547)
POOL_CORRUPT                  = -(OB_RETORTS_PLASMA_POOLS +  548)
POOL_POOLNAME_BADTH           = -(OB_RETORTS_PLASMA_POOLS +  550)
POOL_IMPOSSIBLE_RENAME        = -(OB_RETORTS_PLASMA_POOLS +  551)
POOL_FIFO_BADTH               = -(OB_RETORTS_PLASMA_POOLS +  555)
POOL_INVALID_SIZE             = -(OB_RETORTS_PLASMA_POOLS +  560)
POOL_NO_SUCH_POOL             = -(OB_RETORTS_PLASMA_POOLS +  570)
POOL_EXISTS                   = -(OB_RETORTS_PLASMA_POOLS +  575)
POOL_ILLEGAL_NESTING          = -(OB_RETORTS_PLASMA_POOLS +  576)
POOL_PROTOCOL_ERROR           = -(OB_RETORTS_PLASMA_POOLS +  580)
POOL_NO_SUCH_PROTEIN          = -(OB_RETORTS_PLASMA_POOLS +  635)
POOL_AWAIT_TIMEDOUT           = -(OB_RETORTS_PLASMA_POOLS +  640)
POOL_AWAIT_WOKEN              = -(OB_RETORTS_PLASMA_POOLS +  650)
POOL_WAKEUP_NOT_ENABLED       = -(OB_RETORTS_PLASMA_POOLS +  660)
POOL_PROTEIN_BIGGER_THAN_POOL = -(OB_RETORTS_PLASMA_POOLS +  700)
POOL_FROZEN                   = -(OB_RETORTS_PLASMA_POOLS +  710)
POOL_FULL                     = -(OB_RETORTS_PLASMA_POOLS +  720)
POOL_NOT_A_PROTEIN            = -(OB_RETORTS_PLASMA_POOLS +  800)
POOL_NOT_A_PROTEIN_OR_MAP     = -(OB_RETORTS_PLASMA_POOLS +  810)
POOL_CONF_WRITE_BADTH         = -(OB_RETORTS_PLASMA_POOLS +  900)
POOL_CONF_READ_BADTH          = -(OB_RETORTS_PLASMA_POOLS +  910)
POOL_SEND_BADTH               = -(OB_RETORTS_PLASMA_POOLS + 1000)
POOL_RECV_BADTH               = -(OB_RETORTS_PLASMA_POOLS + 1010)
POOL_SOCK_BADTH               = -(OB_RETORTS_PLASMA_POOLS + 1020)
POOL_SERVER_BUSY              = -(OB_RETORTS_PLASMA_POOLS + 1030)
POOL_SERVER_UNREACH           = -(OB_RETORTS_PLASMA_POOLS + 1040)
POOL_ALREADY_GANG_MEMBER      = -(OB_RETORTS_PLASMA_POOLS + 1050)
POOL_NOT_A_GANG_MEMBER        = -(OB_RETORTS_PLASMA_POOLS + 1055)
POOL_EMPTY_GANG               = -(OB_RETORTS_PLASMA_POOLS + 1060)
POOL_NULL_GANG                = -(OB_RETORTS_PLASMA_POOLS + 1070)
POOL_UNSUPPORTED_OPERATION    = -(OB_RETORTS_PLASMA_POOLS + 1100)
POOL_INVALIDATED_BY_FORK      = -(OB_RETORTS_PLASMA_POOLS + 1110)
POOL_NO_TLS                   = -(OB_RETORTS_PLASMA_POOLS + 1500)
POOL_TLS_REQUIRED             = -(OB_RETORTS_PLASMA_POOLS + 1505)
POOL_TLS_ERROR                = -(OB_RETORTS_PLASMA_POOLS + 1510)
POOL_CREATED                  =  (OB_RETORTS_PLASMA_POOLS + 10)







class AbstractClassError(Exception):
    def __init__(self, msg=None):
        self.msg = msg

    def __str__(self):
        return '%s: %s' % (type(self).__name__, self.msg)

    def __repr__(self):
        return self.__str__()

class HoseStateException(Exception):
    """
    Not a libPlasma-defined exception.  This exception is raised by hose
    methods when a given method is called in an invalid sequence.  For
    example, we cannot await on a hose that is not participating in a pool.
    """
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return '%s(%s)' % (type(self).__name__, self.msg)

    def __repr__(self):
        return self.__str__()

class PlasmaException(ObException):
    def retort(self):
        """
        Returns the numeric retort associated with this exception
        """
        if self._retort is not None:
            return self._retort
        const = re.sub('([A-Za-z])([A-Z])', '\\1_\\2', type(self).__name__[:-9]).upper()
        return globals()[const]

class PoolNoPoolsDirException(PlasmaException):
    """
    Couldn't find a directory to put pools in
    """
    pass

class PoolFileBadthException(PlasmaException):
    """
    Some file-related op failed
    """
    pass

class PoolNullHoseException(PlasmaException):
    """
    pool_hose passed was NULL
    """
    pass

class PoolSemaphoresBadthException(PlasmaException, ObErrnoException):
    """
    Problem with semaphores
    """

    def __init__(self, msg='', errno=None, cmd=None, *args):
        self.msg = msg
        self.errno = errno
        self.command = cmd
        self.args = args

    def __str__(self):
        if self.command is not None:
            return '%s(%d/%s): %s [%s(%s)]' % (type(self).__name__, self.retort(), self.errno, self.msg, self.command, ', '.join('%s' % x for x in self.args))
        return '%s(%d/%s): %s' % (type(self).__name__, self.retort(), self.errno, self.msg)

    def __repr__(self):
        return self.__str__()

    def retort(self):
        if self.errno is None:
            return POOL_SEMAPHORES_BADTH
        if self.errno < OB_MIN_ERRNO or self.errno > OB_MAX_ERRNO:
            return POOL_SEMAPHORES_BADTH
        if self.errno < 64 and (OB_SHARED_ERRNOS & (1 << self.errno)):
            return -1 * (OB_RETORTS_ERRNO_SHARED + self.errno)
        system = platform.system()
        if system == 'Linux':
            return -1 * (OB_RETORTS_ERRNO_LINUX + self.errno)
        if system == 'Darwin':
            return -1 * (OB_RETORTS_ERRNO_MACOSX + self.errno)
        if system == 'Windows':
            return -1 * (OB_RETORTS_ERRNO_WINDOWS + self.errno)
        return POOL_SEMAPHORES_BADTH

class PoolMmapBadthException(PlasmaException):
    """
    mmap didn't work
    """
    pass

class PoolInappropriateFilesystemException(PlasmaException):
    """
    User tried to create an mmap pool on NFS
    """
    pass

class PoolInUseException(PlasmaException):
    """
    Tried to delete (or rename) a pool that was still in use
    """
    pass

class PoolTypeBadthException(PlasmaException):
    """
    Unknown pool type
    """
    pass

class PoolConfigBadthException(PlasmaException):
    """
    Pool config file problem
    """
    pass

class PoolWrongVersionException(PlasmaException):
    """
    Unexpected pool-version in config file
    """
    pass

class PoolCorruptException(PlasmaException):
    """
    Something about the pool itself is bad/invalid
    """
    pass

class PoolPoolnameBadthException(PlasmaException):
    """
    Invalid pool name
    """
    pass

class PoolImpossibleRenameException(PlasmaException):
    """
    Trying to rename a local pool to a network pool, or similar nonsense.
    """
    pass

class PoolFifoBadthException(PlasmaException):
    """
    Problem with fifos
    """
    pass

class PoolInvalidSizeException(PlasmaException):
    """
    The size specified for a pool was not a number or beyond bounds
    """
    pass

class PoolNoSuchPoolException(PlasmaException):
    """
    No pool with this name
    """
    pass

class PoolExistsException(PlasmaException):
    """
    Attempted to create existing pool.
    """
    pass

class PoolIllegalNestingException(PlasmaException):
    """
    Attempted to create pool "foo/bar" when pool "foo" exists, or vice versa.
    """
    pass

class PoolProtocolErrorException(PlasmaException):
    """
    Something unexpected happened in the network pool protocol.
    """
    pass

class PoolNoSuchProteinException(PlasmaException):
    """
    The requested protein was not available
    """
    pass

class PoolAwaitTimedoutException(PlasmaException):
    """
    Await period expired
    """
    pass

class PoolAwaitWokenException(PlasmaException):
    """
    Await cancelled by wake()
    """
    pass

class PoolWakeupNotEnabledException(PlasmaException):
    """
    Attempted to wake a hose without having previously enabled wakeup.
    """
    pass

class PoolProteinBiggerThanPoolException(PlasmaException):
    """
    Protein bigger than pool
    """
    pass

class PoolFrozenException(PlasmaException):
    """
    Tried to deposit to a "frozen" pool
    """
    pass

class PoolFullException(PlasmaException):
    """
    Tried to deposit to full pool that does not allow wrapping
    """
    pass

class PoolNotAProteinException(PlasmaException):
    """
    Tried to deposit a non-protein slaw
    """
    pass

class PoolNotAProteinOrMapException(PlasmaException):
    """
    The options slaw was not a protein or map
    """
    pass

class PoolConfWriteBadthException(PlasmaException):
    """
    Writing config file failed
    """
    pass

class PoolConfReadBadthException(PlasmaException):
    """
    Reading config file failed
    """
    pass

class PoolSendBadthException(PlasmaException):
    """
    Problem sending over network
    """
    pass

class PoolRecvBadthException(PlasmaException):
    """
    Problem reading over network
    """
    pass

class PoolSockBadthException(PlasmaException):
    """
    Problem making network socket
    """
    pass

class PoolServerBusyException(PlasmaException):
    """
    Network pool server busy
    """
    pass

class PoolServerUnreachException(PlasmaException):
    """
    Network pool server unreachable
    """
    pass

class PoolAlreadyGangMemberException(PlasmaException):
    """
    Pool hose already part of a gang
    """
    pass

class PoolNotAGangMemberException(PlasmaException):
    """
    Pool hose is not a member of a given gang
    """
    pass

class PoolEmptyGangException(PlasmaException):
    """
    pool_next_multi() called on an empty gang
    """
    pass

class PoolNullGangException(PlasmaException):
    """
    A NULL gang was passed to any of the gang functions
    """
    pass

class PoolUnsupportedOperationException(PlasmaException):
    """
    The pool type does not support what you want to do to it.
    """
    pass

class PoolInvalidatedByForkException(PlasmaException):
    """
    A hose created before a fork is no longer valid in the child.
    """
    pass

class PoolNoTlsException(PlasmaException):
    """
    Server does not support TLS
    """

class PoolTlsRequiredException(PlasmaException):
    """
    Client does not want to use TLS, but server requires it
    """

class PoolTlsErrorException(PlasmaException):
    """
    Something went wrong with TLS... not very specific
    """

class SemPermissionException(PoolSemaphoresBadthException):
    pass

class SemExistsException(PoolSemaphoresBadthException):
    pass

class SemInvalidException(PoolSemaphoresBadthException):
    pass

class SemDoesNotExistException(PoolSemaphoresBadthException):
    pass

class SemNoSpaceException(PoolSemaphoresBadthException):
    pass

class SemInterruptException(PoolSemaphoresBadthException):
    pass

class SemRangeException(PoolSemaphoresBadthException):
    pass

class SemWaitException(PoolSemaphoresBadthException):
    pass

class SemUndoException(PoolSemaphoresBadthException):
    pass

class SemTooBigException(PoolSemaphoresBadthException):
    pass


POOL_RETORT_EXCEPTIONS = {

    POOL_NO_POOLS_DIR:             PoolNoPoolsDirException,
    POOL_FILE_BADTH:               PoolFileBadthException,
    POOL_NULL_HOSE:                PoolNullHoseException,
    POOL_SEMAPHORES_BADTH:         PoolSemaphoresBadthException,
    POOL_MMAP_BADTH:               PoolMmapBadthException,
    POOL_INAPPROPRIATE_FILESYSTEM: PoolInappropriateFilesystemException,
    POOL_IN_USE:                   PoolInUseException,
    POOL_TYPE_BADTH:               PoolTypeBadthException,
    POOL_CONFIG_BADTH:             PoolConfigBadthException,
    POOL_WRONG_VERSION:            PoolWrongVersionException,
    POOL_CORRUPT:                  PoolCorruptException,
    POOL_POOLNAME_BADTH:           PoolPoolnameBadthException,
    POOL_IMPOSSIBLE_RENAME:        PoolImpossibleRenameException,
    POOL_FIFO_BADTH:               PoolFifoBadthException,
    POOL_INVALID_SIZE:             PoolInvalidSizeException,
    POOL_NO_SUCH_POOL:             PoolNoSuchPoolException,
    POOL_EXISTS:                   PoolExistsException,
    POOL_ILLEGAL_NESTING:          PoolIllegalNestingException,
    POOL_PROTOCOL_ERROR:           PoolProtocolErrorException,
    POOL_NO_SUCH_PROTEIN:          PoolNoSuchProteinException,
    POOL_AWAIT_TIMEDOUT:           PoolAwaitTimedoutException,
    POOL_AWAIT_WOKEN:              PoolAwaitWokenException,
    POOL_WAKEUP_NOT_ENABLED:       PoolWakeupNotEnabledException,
    POOL_PROTEIN_BIGGER_THAN_POOL: PoolProteinBiggerThanPoolException,
    POOL_FROZEN:                   PoolFrozenException,
    POOL_FULL:                     PoolFullException,
    POOL_NOT_A_PROTEIN:            PoolNotAProteinException,
    POOL_NOT_A_PROTEIN_OR_MAP:     PoolNotAProteinOrMapException,
    POOL_CONF_WRITE_BADTH:         PoolConfWriteBadthException,
    POOL_CONF_READ_BADTH:          PoolConfReadBadthException,
    POOL_SEND_BADTH:               PoolSendBadthException,
    POOL_RECV_BADTH:               PoolRecvBadthException,
    POOL_SOCK_BADTH:               PoolSockBadthException,
    POOL_SERVER_BUSY:              PoolServerBusyException,
    POOL_SERVER_UNREACH:           PoolServerUnreachException,
    POOL_ALREADY_GANG_MEMBER:      PoolAlreadyGangMemberException,
    POOL_NOT_A_GANG_MEMBER:        PoolNotAGangMemberException,
    POOL_EMPTY_GANG:               PoolEmptyGangException,
    POOL_NULL_GANG:                PoolNullGangException,
    POOL_UNSUPPORTED_OPERATION:    PoolUnsupportedOperationException,
    POOL_INVALIDATED_BY_FORK:      PoolInvalidatedByForkException,
    POOL_NO_TLS:                   PoolNoTlsException,
    POOL_TLS_REQUIRED:             PoolTlsRequiredException,
    POOL_TLS_ERROR:                PoolTlsErrorException,
}

#Merge the 2 exception types
PLASMA_RETORT_EXCEPTIONS = LOAM_RETORT_EXCEPTIONS
PLASMA_RETORT_EXCEPTIONS.update(POOL_RETORT_EXCEPTIONS)

