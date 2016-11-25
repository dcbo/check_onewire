# check_onewire.py

check_onewire.py is a [nagios](http://nagios.org) nagios plugin which connects to [owserver](http://owfs.org/index.php?page=owserver) (from [owfs](http://owfs.org) to check **DS18x20** onewire temperature sensors.
It returns the status by setting the exit state and the value of the sensor formatted as performance data.

A running owserver is required to use this plugin.

## Usage

There is no configuration, all parameters set by command line arguments:

```
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
```

## Example

```
 ./check_onewire.py 10.CD5B54020800 -wl 55 -wh 70 -cl 45 -ch 80

OK - 61.12 C|temp=61.12;55:70;45:80
```

```
 ./check_onewire.py 10.CD5B54020800 -wh 60 -ch 70

WARNING - 61.94 C|temp=61.94;-50:60;-50:70
```


## Nagios Configuration
### command definition
```
define command{
        command_name    check_temp
        command_line    $USER1$/check_owserver.py '$ARG1$' -cl '$ARG2$' -wl '$ARG3$' -wh '$ARG4$' -ch '$ARG5$'
        }
```

### service definition
```
define service {
        use                      local-service
        host_name                localhost
        service_description      Kesseltemperatur
        check_command            check_temp!10.CD5B5402080024!1!3!85!90        
        }
```

## Libs required 
python-ow is required by check_onewire.py (tested with version: 2.9p8-6)

install with
```
apt-get install python-ow
```

test which version is installed
```
# dpkg -s python-ow
Package: python-ow
Status: install ok installed
Priority: extra
Section: python
Installed-Size: 144
Maintainer: Vincent Danjean <vdanjean@debian.org>
Architecture: amd64
Source: owfs
Version: 2.9p8-6
Provides: python2.7-ow
Depends: libc6 (>= 2.14), libow-2.9-8 (>= 2.8p4), python (>= 2.7), python (<< 2.8)
Description: Dallas 1-wire support: Python bindings
 The 1-Wire bus is a cheap low-speed bus for devices like weather
 sensors, access control, etc. It can be attached to your system via
 serial, USB, I2C, and other interfaces.
 .
 Python bindings for the OWFS 1-Wire support library have been produced
 with SWIG and allow access to libow functions from Python code.
Homepage: http://owfs.org/
Python-Version: 2.7
```

## References 
- http://nagios.org
- http://owfs.org
- http://owfs.org/index.php?page=owserver
