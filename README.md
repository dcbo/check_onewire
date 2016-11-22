# check_onewire
nagios check plugin which connects to owserver (from owfs) to check temperature sensors


# usage
usage: check_onewire.py [-h] [-cl <critical low>] [-ch <critical high>]
                        [-wl <warning low>] [-wh <warning high>] [-s <server>]
                        [-p <port>] [-v]
                        <sensor_id>

connects to onewire-server and retrieves temperature from
onewire sensor and check, if temperature exceeds the
defined warning oder critical levels.

positional arguments:
  <sensor_id>           ID of 1-wire sensor

optional arguments:
  -h, --help            show this help message and exit
  -cl <critical low>, --critical_low <critical low>
                        critical low value (default -50)
  -ch <critical high>, --critical_high <critical high>
                        critical high value (default 120)
  -wl <warning low>, --warning_low <warning low>
                        warning low value (default -50)
  -wh <warning high>, -warning_high <warning high>
                        warning high value (default 120)
  -s <server>, --server <server>
                        owserver address (::1)
  -p <port>, --port <port>
                        owserver port (default 4304)
  -v, --verbose         increase output verbosity

exit status:
  0 - OK:       sensor value is between defined ranges.
  1 - WARNING:  sensor value exceeds warning limits
                but not critical limits.
  2 - CRITICAL: sensor value exceeds critical limits,
                or sensor was not found.

