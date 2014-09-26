'''
C Plasma
'''

# (c) 2014 MCT

import native
import numpy
from cplasma._pyplasma_api import RProtein
from cplasma import exceptions

POOL_WAIT_FOREVER = -1.0

class slaw(object):
    @staticmethod
    def from_json(data):
        return Slaw(data)

import time
def _interruptable_await(hose_or_gang, stop):
    if stop == POOL_WAIT_FOREVER:
        stop = None
    else:
        stop = time.time() + stop
    curr = time.time()
    while stop is None or curr < stop:
        result = hose_or_gang.awaitNext(0.1)
        if result is not None:
            return result
        curr = time.time()
    #Time ran out, nothing received
    return None

def Slaw(x):
    'Turn an object in to a Slaw that you can send over a hose'
    # x = compat.loam_conv(x)

    if x is None:
        return native.Slaw.nil()
    elif isinstance(x, native.Slaw):
        return x
    elif hasattr(x, 'toSlaw'):
        # Here's our recipe for dealing with user-defined classes.
        # It's expected that their `toSlaw` will use this Slaw
        # function under the hood to produce results of type
        # `native.Slaw`.
        return x.toSlaw()
    elif isinstance(x, numpy.ndarray):
        return native.Slaw.makeArray(x)
    elif isinstance(x, dict):
        bu = native.SlawBuilder()
        for k, v in x.iteritems():
            bu.mapPut(Slaw (k), Slaw (v))
        return bu.takeMap()
    elif isinstance(x, tuple) and len(x) == 2:
        return native.Slaw.makeCons(Slaw(x[0]), Slaw(x[1]))
    elif isinstance(x, list) or isinstance(x, tuple):
        #TODO: Should we reject tuples here since they can also mean cons?
        it = iter(x)
        bu = native.SlawBuilder()
        for y in it:
            sy = Slaw(y)
            bu.listAppend(sy)
        return bu.takeList()
    elif isinstance(x, numpy.uint8):
        return native.Slaw.make_unt8(int(x))
    elif isinstance(x, numpy.int8):
        return native.Slaw.make_int8(int(x))
    # numpy's scalar types will describe our underlying oblong types
    elif isinstance(x, numpy.uint16):
        return native.Slaw.make_unt16(int(x))
    elif isinstance(x, numpy.int16):
        return native.Slaw.make_int16(int(x))
    elif isinstance(x, numpy.uint32):
        return native.Slaw.make_unt32(long(x))
    elif isinstance(x, numpy.int32):
        return native.Slaw.make_int32(long(x))
    elif isinstance(x, numpy.uint64):
        return native.Slaw.make_unt64(long(x))
    elif isinstance(x, numpy.int64):
        return native.Slaw.make_int64(long(x))
    elif isinstance(x, numpy.float32):
        return native.Slaw.make_float32(float(x))
    elif isinstance(x, numpy.float64):
        return native.Slaw.make_float64(float(x))
    elif isinstance(x, (int, long)):
        return native.Slaw.make_int64(x)
    elif isinstance(x, float):
        return native.Slaw.make_float64(x)
    elif isinstance(x, basestring):
        return native.Slaw.make(str(x))
    else:
        # native.Slaw.make knows how to deal with Python's builtin
        # types. We currently don't have a way to deal with arbitrary
        # classes and whatnot
        return native.Slaw.make(x)

def Protein(descrips, ingests):
    'Create a write-only protein for depositing purposes'
    return native.Slaw.makeProtein(Slaw(descrips), Slaw(ingests))

def QID(qid):
    'Create the magic, mythical SlawQID.  Bizarrely a cons.'
    bytez = numpy.array([qid[i] for i in xrange(16)], numpy.uint8)
    return native.Slaw.makeCons(native.Slaw.make('SlawQID'),
                                native.Slaw.makeArray(bytez))

class Hose(object):
    def __init__(self, pool, options = None):
        self.__hose = native.Hose(str(pool))

    def _native_hose(self):
        "You probably don't want to."
        return self.__hose

    ## --------------------- ##
    ## Creation and Disposal ##
    ## --------------------- ##

    @staticmethod
    def create(name, pool_type, options):
        """
        Create a new pool.

        The pool_type string specifies what kind of pool you want to create,
        e.g., "mmap". This refers to the type of the pool on the host
        machine, _not_ the transport (e.g., "tcp"). Currently, the transport
        is specified by the pool hose.

        The options argument may be either an obmap or a protein, and
        describes any parameters needed to create the pool, which will vary
        by the type of pool. The option format is a protein containing
        multiple ingests, where the ingest key is the parameter to set and
        the ingest value is (unsurprisingly) the value of the parameter.
        (Or just an obmap or dict with similar key/value pairs.) For
        example, mmap pools need to know what size of pool to create, so to
        create a pool of size 1048576, you'd pass it an option protein with
        the ingest "size:1048576". If no parameters are needed, the options
        argument is None.

        Possible options are:
            +----------------+-----------------------------------+----------+
            | key            | type                              | default  |
            +================+===================================+==========+
            | resizable      | obbool                            | True     |
            +----------------+-----------------------------------+----------+
            | single-file    | obbool                            | False    |
            +----------------+-----------------------------------+----------+
            | size           | unt64 (bytes)                     | required |
            +----------------+-----------------------------------+----------+
            | index-capacity | unt64 (proteins)                  | 0        |
            +----------------+-----------------------------------+----------+
            | stop-when-full | obbool                            | False    |
            +----------------+-----------------------------------+----------+
            | frozen         | obbool                            | False    |
            +----------------+-----------------------------------+----------+
            | auto-dispose   | obbool                            | False    |
            +----------------+-----------------------------------+----------+
            | sync           | obbool                            | False    |
            +----------------+-----------------------------------+----------+
            | mode           | string (octal) or int32           | -1       |
            +----------------+-----------------------------------+----------+
            | owner          | string (username) or int32 (uid)  | -1       |
            +----------------+-----------------------------------+----------+
            | group          | string (groupname) or int32 (gid) | -1       |
            +----------------+-----------------------------------+----------+

        On success, this method returns None.  On error, it raises the
        following exceptions, contained in a PlasmaException's tort:

        * OB_NO_MEM
          (memory allocation errors)
        * POOL_INVALID_SIZE
          (the size specified in options is below or above limits,
          or is not coercible to an integer)
        * POOL_NAME_BADTH
          (name is ill-formed)
        * POOL_TYPE_BADTH
          (type does not name a known pool type)
        * POOL_EXISTS
          (a pool with this name already exists)
        * OB_ERRNO...
          (system error such as a failure to acquire an OS lock)
        """
        native.Hose.create(name, pool_type, Slaw(options))

    @staticmethod
    def dispose(name):
        """
        Destroy a pool utterly.

        Possible exceptions by way of PlasmaException's retort:

        * POOL_NO_SUCH_POOL
          (a pool by that name pool doesn't exist)
        * POOL_IN_USE
          (there is still a hose open to this pool)
        """
        native.Hose.dispose(str(name))

    @staticmethod
    def rename(old_name, new_name):
        """
        Rename a pool.

        Like dispose(), raises PlasmaException if you call it while there
        are any open hoses to old_name.
        """
        native.Hose.rename(str(old_name), str(new_name))

    @staticmethod
    def exists(name):
        """
        Returns True if name exists, and returns False if name does not exist.

        (And, of course, raises an exception if an error occurs.) Beware of
        TOCTOU! In most cases, it would be more robust to just use
        participate(), because then if it does exist, you'll have a hose to
        it. With exists(), it might go away between now and when you
        participate in it.
        """
        return native.Hose.exists(str(name))

    def set_hose_index(self, index):
        #+1 because otherwise the hose returns the index we just set
        native.Hose.seekto(self.__hose, index+1)

    @staticmethod
    def validate_name(name):
        """
        Check that a pool name is valid.  Returns True if the name is just
        fine, and raises an PoolPoolnameBadthException if the name is no good.

        Pool names may contain most printable characters, including '/',
        although '/' is special since it indicates a subdirectory, just
        like on the filesystem. Some other restrictions on pool name:

        * The total pool name must be between 1 and 100 characters in length
        * A pool name consists of one or more components, separated by
          slashes
        * A component may not be the empty string
        * A component may only contain the characters:
          "!#$%&'()+,-.0123456789;=@ ABCDEFGHIJKLMNOPQRSTUVWXYZ"
          "[]^_`abcdefghijklmnopqrstuvwxyz{}~"
          (the double quotes are not part of the legal character set)
        * A component may not begin with '.', and may not end with '.',
          ' ', or '$'
        * A component may not be any of the following names,
          case-insensitively, nor may it begin with one of these
          immediately followed by a dot: CON, PRN, AUX, NUL, COM1, COM2,
          COM3, COM4, COM5, COM6, COM7, COM8, COM9, LPT1, LPT2, LPT3,
          LPT4, LPT5, LPT6, LPT7, LPT8, and LPT9
        """
        return native.Hose.validateName(str(name))

    @staticmethod
    def sleep(name):
        """
        Put a pool "to sleep", which means allowing the pool implementation
        to free certain resources used by the pool, in the expectation that
        it won't be used in a while.

        A pool can only be put to sleep if there are no open hoses to it;
        a PoolInUseException will be raised if this condition is not met.
        The pool will automatically "wake up" (reacquire the resources it
        needs) the next time it is in participated in.

        In practice, in the current implementation, "resources" means
        "semaphores". This function is only useful/necessary if you intend
        to have a large number (more than 32768) of pools.
        """
        native.Hose.sleep(str(name))

    @staticmethod
    def check_in_use(name):
        """
        If the named pool exists and there are currently no hoses open to it,
        returns True.

        If the named pool currently has one or more hoses open to it, raises
        a PoolInUseException.  Can also raise other exceptions, such as
        PoolNoSuchPoolException if the pool does not exist.

        Note:
          Beware of TOCTOU issues, though:
          http://cwe.mitre.org/data/definitions/367.html
        """
        return native.Hose.checkInUse(str(name))

    ## ---------------------------- ##
    ## Connecting and Disconnecting ##
    ## ---------------------------- ##

    @staticmethod
    def participate(name, options = None):
        """
        Create a connection to a pool - a pool hose.

        The pool hose can only be used by one thread at a time, very similar
        to a file descriptor. The options slaw, which can be either an
        obmap or a protein (or can be None) describes any parameters needed
        to connect to the pool. At present, nothing is required, but in the
        future it may have uses, e.g., for authentication.

        If the connection is successful, the associated index will be set to
        its newest value, and a Hose is returned. Possible exceptions,
        by way of a PlasmaException's tort, include:

        * OB_NO_MEM
          (memory allocation errors)
        * POOL_POOLNAME_BADTH
          (name is not a legal pool name)
        * OB_ERRNO...
          (system error such as a failure to acquire an OS lock or a network
          resource)
        * POOL_NO_SUCH_POOL
          (a pool with this name does not exist)
        * POOL_CORRUPT, POOL_WRONG_VERSION, SLAW_WRONG_VERSION
          (the pool data does not have the expected format)

        For local pools we have also:

        * POOL_INVALID_SIZE
          (the size in an mmap pool's configuration is incorrect)
        * POOL_INAPPROPRIATE_FILESYSTEM
          (the pool is backed by a filesystem not supported by plasma, eg. NFS)
        * POOL_MMAP_BADTH
          (errors accessing mapped memory in mmap pools)

        And, for remote ones:

        * POOL_SOCK_BADTH, POOL_SERVER_UNREACH
          (connectivity problems)
        * POOL_PROTOCOL_ERROR
          (unexpected responses from the pool server)
        """
        return Hose(name)

    @staticmethod
    def participate_creatingly(name, pool_type, create_options, participate_options = None):
        """
        Combines create() and participate() in a single call, returning a hose
        to the newly created pool.
        """
        name = str(name)
        if not native.Hose.exists(name):
            native.Hose.create(name, pool_type, create_options)
        return Hose.participate(name, participate_options)

    def withdraw(self):
        '''
        Noop. This will happen automagically when the hose is destroyed.
        Want to make it happen sooner? del(self).
        '''
        pass

    ## ------------------------- ##
    ## Pool and Hose Information ##
    ## ------------------------- ##

    @staticmethod
    def list_pools():
        """
        List all the pools on the local system, returning their names as an
        list of strings.
        """
        return native.Hose.listPools()

    @staticmethod
    def list_ex(prefix):
        """
        List all the pools under a specified URI.

        If uri is NULL, then lists all local pools under OB_POOLS_DIR
        (behaves like list()). A subset of those pools, underneath a
        specified subdirectory of OB_POOLS_DIR, can be requested with a
        uri of the form "some/dir". Pools underneath an arbitrary local
        directory can be listed with "local:/an/absolute/dir". uri should
        be a string like "tcp://chives.la923.oblong.net:1234/" if you want
        to list pools on a remote server.

        Returns an list of strings, one for each pool name.
        """
        return native.Hose.listPoolsEx(prefix)

    def name(self):
        """
        Get the name of the pool this hose is connected to.
        This is also the name used by the user to connect to the pool.
        """
        return self.__hose.name

    def get_hose_name(self):
        'Get the name of this hose. Note: this is *not* necessairly the name of the pool'
        return self.__hose.hoseName()

    def set_hose_name(self, name):
        """
        Set the name of this hose.

        Hose names have no effect on the functioning of libPlasma, and
        exist only as a debugging aid. Hose names may be used in various
        messages, so you should set it to something that's meaningful to
        a human. Besides OB_OK on success, this method can raise an
        OB_NO_MEM PlasmaException in out of memory conditions.
        """
        self.__hose.setHoseName(str(name))

    def get_info(self, hops = 0):
        """
        Returns a protein with information about a pool.

        Should always include an ingest "type", which is a string naming the
        pool type, and "terminal", which is a boolean which is true if this
        is a terminal pool type like "mmap", or false if this is a transport
        pool type like "tcp". For mmap pools, should include an ingest
        "size", which is an integer giving the size of the pool in bytes.
        For tcp pools, should include an ingest "host", which is a string
        naming the host the pool is on, and "port" which is an integer
        giving the port. For other pool types, ingests with other relevant
        info can be included. If "hops" is 0, means return information
        about this pool hose. If "hops" is 1, means return information
        about the pool beyond this hose (assuming this hose is a nonterminal
        type like TCP). And higher values of "hops" mean go further down
        the line, if multiple nonterminal types are chained together. If
        "hops" is -1, means return information about the terminal pool, no
        matter how far it is.
        """
        return self.__hose.getInfo(hops)

    def newest_index(self):
        """
        Get the index of the newest protein in this pool.

        Raises POOL_NO_SUCH_PROTEIN if no proteins are in the pool.
        """
        return self.__hose.newestIndex

    def oldest_index(self):
        """
        Get the index of the oldest protein in this pool.

        Raises POOL_NO_SUCH_PROTEIN if no proteins are in the pool.
        """
        return self.__hose.oldestIndex


    ## ----------------------------- ##
    ## Depositing (Writing) to Pools ##
    ## ----------------------------- ##

    def deposit(self, protein):
        """
        Deposit (write) a protein into this pool.

        Returns the index of the deposited protein.

        Possible exceptions, via PlasmaException:

        * POOL_NOT_A_PROTEIN
          (argument is not a protein)
        * OB_ERRNO...
          (system error such as a failure to acquire an OS lock)
        * POOL_SEMAPHORES_BADTH
          (the required locks couldn't be acquired)
        * POOL_PROTEIN_BIGGER_THAN_POOL
          (the protein won't fit in the pool)
        * POOL_CORRUPT
          (the pool data does not have the expected format)

        And for remote pools:

        * POOL_SOCK_BADTH, POOL_SERVER_UNREACH
          (connectivity problems)
        * POOL_PROTOCOL_ERROR
          (unexpected responses from the pool server)
        """
        if not isinstance(protein, native.Slaw):
            protein = Slaw(protein)
        return self.__hose.deposit(protein)

    def deposit_ex(self, protein):
        """
        For compatibility purposes this exists, yet it is simply deposit().
        """
        return self.deposit(protein)

    ## ------------------ ##
    ## Reading from Pools ##
    ## ------------------ ##

    def curr(self):
        """
        Retrieve the protein at the pool hose's index.  The returned
        protein will have its timestamp and index properties set.

        This method may raise the same exceptions as next().
        """
        return self.__hose.nth(self.__hose.index)

    def next(self):
        """
        Retrieve the next available protein at or following the pool hose's
        index and advance the index to position following.

        May skip proteins since the protein immediately following the last
        read protein may have been discarded.  The protein will have its
        timestamp and index properties set.

        Returns none of there is no available protein.  Otherwise returns
        a tuple containing the protein, its index and its timestamp.

        Possible exceptions:

        * OB_ERRNO...
          (system error such as a failure to acquire an OS lock)
        * POOL_CORRUPT
          (the pool data does not have the expected format)

        And for remote pools:

        * POOL_SOCK_BADTH, POOL_SERVER_UNREACH
          (connectivity problems)
        * POOL_PROTOCOL_ERROR
          (unexpected responses from the pool server)
        """
        return self.__hose.next()

    def prev(self):
        """
        Retrieve the protein just previous to the pool hose's current index,
        and move the pool hose's index to this position.  The returnd
        protein will have its timetamp and index properties set.

        This method may raise the same exceptions as next().  It definitely
        returns the same things as next().
        """
        return self.__hose.prev()

    def fetch(self, ops, clamp = False):
        """
        This isn't implemented. In all of my years working with Plasma,
        I've never once used this facility.  I'm sure it's good fun.
        """
        raise RuntimeError('Unimplemented method: Hose.fetch')

    def nth_protein(self, idx):
        """
        Retrieve the protein with the given index.

        The protein will have its timestamp and index properties set.

        Possible exceptions:

        * POOL_NO_SUCH_PROTEIN
          (the index is previous to that of the oldest index, or it is
          after the newest index)
        * OB_ERRNO...
          (system error such as a failure to acquire an OS lock)
        * POOL_CORRUPT
          (the pool data does not have the expected format)

        And for remote pools:

        * POOL_SOCK_BADTH, POOL_SERVER_UNREACH
          (connectivity problems)
        * POOL_PROTOCOL_ERROR
          (unexpected responses from the pool server)
        """
        ret = self.__hose.nth(idx)
        protein, index, timestamp = ret
        return RProtein(protein, self, index, timestamp)

    def index_lookup(self, *args, **kwargs):
        """
        This isn't implemented. In all of my years working with Plasma,
        I've never once used this facility.  I'm sure it's good fun.
        """
        raise RuntimeError('Unimplemented method: Hose.index_lookup')


    def probe_back(self, search):
        """
        Search backward in the pool for a protein with a descrip matching
        that of the search argument.  The returned protein will have its
        timestamp and index properties set.

        If the beginning of the pool is reached without finding a match,
        a POOL_NO_SUCH_PROTEIN will be raised.  On success, the
        hose's current index will be set to that of the matched protein.
        """
        return self.__hose.probeBack(search)

    def probe_frwd(self, search):
        """
        Search forward in the pool for a protein with a descrip matching
        that of the search argument.

        If the end of the pool is reached without finding a match, a
        POOL_NO_SUCH_PROTEIN will be raised.  On success, the hose's
        currnet index will be set to one more than that of the matched
        protein.
        """
        return self.__hose.probeForward(search)

    def await_next(self, timeout=POOL_WAIT_FOREVER):
        """
        The same as next(), but wait for the next protein if none are
        available now.

        The timeout argument specifies how long to wait for a protein:
            * timeout == POOL_WAIT_FOREVER (-1): Wait forever
            * timeout == POOL_NO_WAIT (0): Don't wait at all
            * timeout > 0: only wait this many seconds.

        In addition to the exceptions raised by next(), this method may
        also raise:

        * PoolAwaitTimedoutException
          (no protein arrived before the timeout expired)
        """
        await_result = _interruptable_await(self.__hose, timeout)
        if await_result is None:
            return None
        protein, index, timestamp = await_result
        return RProtein(protein, self, index, timestamp)

    def await_probe_frwd(self, search, timeout=POOL_WAIT_FOREVER):
        """
        The same as probe_frwd(), but wait if necessary.  See await_next()
        comments for the meaning of the timeout argument,

        Note:
            timeout is overall, and does not restart when a non-matching
            protein is found.
        """
        search = Slaw(search)
        r = self.__hose.probeForwardAwait(search, timeout)
        if r is None:
            raise exceptions.PoolAwaitTimedoutException
        return RProtein(r[0], self, r[1], r[2])

    def enable_wakeup(self):
        """
        Enable wake_up() for this hose.

        Calling this function multiple times on a hose is the same as
        calling it once on a hose. Wakeup is mediated by a system-dependent
        IPC mechanism: a failure on acquiring the necessary system resources
        is signalled by raising an OB_ERRNO....
        """
        self.__hose.enableWakeup()

    def wake_up(self):
        """
        A signal-safe and thread-safe function to interrupt any call to
        await_next() on this hose.

        For each time that this function is called, one call to await() will
        raise a PoolAwaitWokenException. (XXX That's not really true if
        enough wakeup requests pile up -- they will eventually be eaten if
        no one looks at them. See bug 771.)

        It is an error to call this function without previously having
        called enable_wakeup() on this hose: in that case, this function
        will raise a PoolWakeupNotEnabledException.
        """
        self.__hose.wakeup()

    def join_gang(self, gang):
        """
        Convenience method for HoseGang.add_hose
        """
        gang.add_hose(self)

    def leave_gang(self, gang):
        """
        Convenience method for HoseGang.remove_hose
        """
        gang.remove_hose(self)

class HoseGang(object):
    """
    HoseGangs allow you to await on multiple hoses simultaneously, without
    having to poll.
    """
    def __init__(self):
        self.__gang = native.Gang()
        self.__hoses = []

    def find_hose_index(self, name):
        hose_i = -1
        name = str(name)
        for i, hose in enumerate(self.__hoses):
            if name in hose.get_hose_name():
                hose_i = i
                break
        return hose_i

    def add_hose(self, hose):
        """
        Add a hose to the gang.  If the argument is a string, create a new
        hose to participate in the named pool.
        """
        if isinstance(hose, (str, unicode)):
            hose = Hose.participate(hose)
        self.__hoses.append(hose)
        self.__gang.join(hose._native_hose())

    def remote_hose(self, hose):
        """
        Remove a hose from the gang.  If the argument is a string, remove
        the hose connected to the named pool.
        """
        if isinstance(hose, (str, unicode)):
            candidates = [h for h in self.__hoses if h.name == hose]
            if 1 != len(candidates):
                raise LookupError('No hose named %s in this gang' % hose)
            hose = candidates[0]
        self.__gang.leave(hose._native_hose())
        self.__hoses.remove(hose)

    def cancel_awaiter(self):
        """
        A signal-safe and thread-safe function to interrupt any call to
        pool_await_next_multi() on this gang. For each time that this
        function is called, one call to await_next_multi() will return with a
        pool_retort of POOL_AWAIT_WOKEN.
        """
        self.__gang.wakeup()

    def withdraw(self):
        '''
        Noop. This will happen automagically when the hose is destroyed.
        Want to make it happen sooner? del(self).
        '''
        pass

    def hose_count(self):
        """
        Return the number (int64) of hoses participating in the gang.
        """
        return self.__gang.count()

    def nth_hose(self):
        '''
        Noop. I get that Oblong really likes to be able to access everything
        by name and by order. I really do. I never understood it, and I'm
        just too lazy to make the native Hose class capably contend with
        multiple objects holding references to it.
        '''
        pass

    def next(self):
        '''
        Returns the protein, its index, its timestamp, and the name of the pool
        it came from.  Or `None` if we time out.
        '''
        return self.__gang.next()

    def await_next(self, timeout = POOL_WAIT_FOREVER):
        '''
        Returns the protein, its index, its timestamp, and the name of the pool
        it came from.  Or `None` if we time out.
        '''
        await_result = _interruptable_await(self.__gang, timeout)
        if await_result is None:
            return None
        protein, index, timestamp, pool_name = await_result
        #This is very ugly
        my_hose = None
        for h in self.__hoses:
            if h.get_hose_name() in pool_name:
                my_hose = h
                break
        return RProtein(protein, my_hose, index, timestamp)

