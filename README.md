# check_onewire.py

check_onewire.py is a [nagios](http://nagios.org) nagios plugin which connects to [owserver](http://owfs.org/index.php?page=owserver) (from [owfs](http://owfs.org) to check onewire temperature sensors.
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

## references 
- http://nagios.org
- http://owfs.org
- http://owfs.org/index.php?page=owserver
