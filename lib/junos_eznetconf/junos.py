
from lxml import etree
from ncclient import manager as netconf_ssh

class JunosEzNetconf(object):

  ##### -------------------------------------------------------------------------
  ##### PROPERTIES
  ##### -------------------------------------------------------------------------

  ### ---------------------------------------------------------------------------
  ### property: hostname
  ### ---------------------------------------------------------------------------

  @property
  def hostname(self):
    """
      The hostname/ip-addr of the Junos device
    """
    return self._hostname

  ### ---------------------------------------------------------------------------
  ### property: user
  ### ---------------------------------------------------------------------------
  
  @property
  def user(self):
    """
      The login user accessing the Junos device
    """
    return self._user

  ### ---------------------------------------------------------------------------
  ### property: password
  ### ---------------------------------------------------------------------------

  @property
  def password(self):
    """
      The login password to access the Junos deviec
    """
    return None  # read-only      

  @password.setter
  def password(self, value):
    self._password = value
  
  ### ---------------------------------------------------------------------------
  ### property: logfile
  ### ---------------------------------------------------------------------------

  @property
  def logfile(self):
    """
      simply returns the log file object
    """
    return self._logfile

  @logfile.setter
  def logfile(self, value):
    """
      assigns an opened file object to the device for logging
      If there is an open logfile, and 'value' is None/False
      then close the existing file
    """
    # got an existing file that we need to close
    if (not value) and (None != self._logfile):
      rc = self._logfile.close()
      self._logfile = False
      return rc

    if not isinstance(value, file):
      raise ValueError("value must be a file object")  

    self._logfile = value
    return self._logfile

  ##### -----------------------------------------------------------------------
  ##### CONSTRUCTOR
  ##### -----------------------------------------------------------------------

  def __init__(self, *vargs, **kvargs):
    """
      Required args:
        user: login user name
        host: host-name or ip-addr

      Optional args:
        password: login user password; if not provided, assumes ssh-keys
    """

    # private attributes

    self._hostname = kvargs['host']
    self._auth_user = kvargs['user']
    self._auth_password = kvargs['password']
    self._conn = None

    # accessable attributes

    self.connected = False
    self.rpc = True

  ##### -----------------------------------------------------------------------
  ##### Basic device methods
  ##### -----------------------------------------------------------------------

  def open( self, *vargs, **kvargs ):
    """
      opens a connection to the device using existing login/auth 
      information.  No additional options are supported; at this time
    """
    # open connection using ncclient transport
    self._conn =  netconf_ssh.connect( host=self.hostname,
      username=self._auth_user, password=self._auth_password,
      hostkey_verify=False )

    self.connected = True

  def close( self ):
    """
      closes the connection to the device
    """
    self._conn.close_session()
    self.connected = False

  def execute( self, rpc_cmd ):
    """
      executes the :rpc_cmd: and returns the result as an lxml Element

      :rpc_cmd: can either be an Element or xml-as-string.  In either case
      the command starts with the specific command element, i.e., not the
      <rpc> element itself
    """

    if isinstance(rpc_cmd, str):
      rpc_cmd_e = etree.XML( rpc_cmd )
    elif isinstance(rpc_cmd, etree._Element):
      rpc_cmd_e = rpc_cmd
    else:
      raise ValueError("Dont know what to do with rpc of type %s" % rpc_cmd.__class__.__name__)

    rpc_rsp_e = self._conn.rpc( rpc_cmd_e )._NCElement__doc

    return rpc_rsp_e

  ##### -------------------------------------------------------------
  ##### Constructor buddies ...
  ##### -------------------------------------------------------------

  def Template( self, filename ):
    return True

