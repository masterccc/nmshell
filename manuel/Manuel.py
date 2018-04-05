"""
    Display help for specific command
    or in case of misuse
"""

class Manuel(object):
    """
        Help management class
    """
    def __init__(self):
        """
            Constructor, no param
        """
        self.header = "That's not working, read the friendly manual: "
        self.man = {
            "set": """
Assign value to a variable.

Syntax : set variable value

Examples :
set target 192.169.1.1-50
Boolean values can be "true","false","0","1".
All non-true value is considered as false.""",
            "export":"""
Export result to a file

Syntax : export
            """,

            "show":
            """
Show options or variables

Syntax : show item

item can be a variable (ports, target,...)or "options"

Examples :

    show target
    show options

            """,
            "help": "help objet (eg: help show)",
            "history": "display and replay history",
            
            "scan":
            """
Perform scan

scan [scan_type]

no option : scan with specified ports, if no port specified, scan with defaults ports (1000 most used ports see nmap manual).
scan_type scans with preset ports. scan_type can take the following values:

web : 80,8080,8000,8128,443
nas : 21,22,139,445
current 20,21,22,23,80,139,443,445,3306
            """
        }
        self.not_found = "Command doen't exist"

    def get_man(self, search, doomy=True):
        """
            Display help when user provided invalid input
        """
        msg = self.man.get(search, self.not_found)
        if(doomy):
            msg = self.header + msg
        print(msg)


    def help(self, cmd="nop"):
        """
            Fetch help for a specified command
        """
        if(cmd != "nop"):
            for entry in self.man:
                if(entry == cmd):
                    self.get_man(cmd, False)
                    return

        print("""
Commands:
    scan     Do scan
    set      Set value for selected var
    help     Get some help
    show     Display object
    history  Get and replay commands
    reset    Reset params to default
    quit     Exit programm
    exit     see 'quit'
    bye      see 'exit'

Examples :

1. Scan web/nas/current ports for range 192.168.0.1 to 192.168.0.20

    > set target 192.168.0.1-20
    > scan web
    or
    > scan nas
    or
    > scan current

2. Scan specified ports for 192.168.0.1

    > set target 192.168.0.1
    > set ports 21,22,8000-9000
    > scan

3. Scan without nmapshell layout (print nmap output directly)

    > set raw_mode true
    > set target 192.168.0.1
    > set ports 80,8080,3306
    > scan

4. Export (Text is default format)

    (optional) > set export_format json
    > export
""")
