# Nmshell - Interactive port scanner

![alt text](https://raw.githubusercontent.com/masterccc/nmshell/master/img/screenshot.png)

# Dependancies

This programm runs under python3, you need python-nmap for python3 (https://pypi.python.org/pypi/python-nmap)

# Basic usage

## Simple scan
Simple scan on a port range :
```
set port 80,81
set target 192.168.1-50
```

The target can be an IP address or a range ( from-to.from-to.from-to.from-to)

## Scan with pre-defined ports

Scan all web-related ports :

```
set target 192.168.1-50
scan web
```

You can use ```nas``` or ```current``` instead of "web" for the scan option.

"Web","nas" and "current" ports are defined in scan/Scan.py :

```
"ports_context_web": "80,8080,8000,8128,443"
"ports_context_nas": "21,22,139,445",
"ports_context_current": "20,21,22,23,80,139,443,445,3306"
```

Feel free to add your own contexts and pull them.


# Change options

You can see options by typing "show options", and change them with "set opt_name value" :

![alt text](https://raw.githubusercontent.com/masterccc/nmshell/master/img/options.png)

Boolean option can be set with True,False,1,0.


# Export

"export" command exports your scan in a file in the specified format ("export_format" option) with the prefix specified in the "exp_basename" option.

# History

You can see your history with :

```history```

You can replay history commands with

```history n``` (where n is the history line index)

# Detailed scan

Once a mass scan is done, you can target a specific ip for a detailed scan.

```details n``` (where n is the line number of the target, you can find this number in the scan table)

# Manual

You can access manual pages with "man" or "help" command.

For more information about a command, type ```help the_command```


# Other options

You can see the last scan result with "show result"
The raw_scan option allows you to scan without the nmshell layout. It performs an ordinary scan with native nmap.

# Powered by nmap

![alt text](https://raw.githubusercontent.com/masterccc/nmshell/master/img/nmap_prop.jpg)

More details at https://nmap.org/