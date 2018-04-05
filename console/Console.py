"""
    Console module for nmshell,
    allow the script to be run interactively
"""

from scan.Scan import *
from manuel.Manuel import *

class Console(object):
    """
        Console class, get input from user, parse and dispatch
    """
    def __init__(self):
        """
            Constructor, no params
        """
        self.scanner = Scan()
        self.man = Manuel()
        self.prompt = "nmapshell > "
        self.hist = []
        self.start()


    def start(self):
        """
            Starts the shell
        """
        while True:
            self.prompt = self.scanner.colors['fR']
            self.prompt += "nmapshell (" + self.scanner.getcli()

            if(self.scanner.opt["bool"]["raw_mode"]):
                self.prompt += self.scanner.colors['Y'] + " (raw_mode)"

            self.prompt += self.scanner.colors['fR'] + ")\n"
            self.prompt += self.scanner.colors['W'] +"~>"
            raw_cmd = input(self.prompt)
            if raw_cmd in ['exit', 'bye', 'quit']:
                print("Exit")
                break
            elif(raw_cmd != ""):
                self.dispatch(raw_cmd)

    def dispatch(self, raw_cmd):
        """
            Parse input and call the related func
        """
        cmd = raw_cmd.split()

        if(cmd[0] == "set"):
            self.setvar(cmd)
        elif(cmd[0] == "show" or cmd[0] == "sh"):
            self.show(cmd)
        elif(cmd[0] == "scan" or cmd[0] == "s"):
            self.generic_oneparam(cmd, self.scanner.scan)
        elif(cmd[0] == "export" or cmd[0] == "e"):
            self.generic_oneparam(cmd, self.scanner.export_result)
        elif(cmd[0] == "history" or cmd[0] == "h"):
            self.history(cmd)
        elif(cmd[0] == "details"):
            self.tscan(cmd)
        elif(cmd[0] == "test"):
            self.scanner.test()
        elif(cmd[0] == "reset" or cmd[0] == "r"):
            self.scanner.reset()
        elif(cmd[0] == "help" or cmd[0] == "man"):
            self.generic_oneparam(cmd, self.man.help)
        if(cmd[0] != "history" and cmd[0] != "h"):
            self.hist.append(raw_cmd)


    def tscan(self, cmd):
        """
            Check params to launch a full scan
        """

        if (len(cmd) < 2):
            self.man.get_man("details")
            return
        target = -1
        try:
            target = int(cmd[1])
        except:
            print('Error, <' + cmd[1] + '> is not a number, try again')
            return
        self.scanner.targetedscan(target)


    def generic_oneparam(self, cmd, func):
        """
            Check params for 1-param functions
        """
        if(len(cmd) < 2):
            func()
        else:
            func(cmd[1])

    def history(self, cmd):
        """
            Fetch history and replay if a "hist number"
            is specified
        """
        if( len(cmd) > 1 and len(self.hist) > 0):
            wanted = cmd[1]
            try:
                replaycmd = int(cmd[1])
                if((replaycmd) <= len(self.hist)):
                    print('replay', self.hist[replaycmd - 1])
                    self.dispatch(self.hist[replaycmd - 1])

            except:
                print("Wrong history number, check 'history'", cmd[1])

        else:
            index = 1
            for line in self.hist:
                print(str(index) + ' - ' + line)
                index += 1

    def show(self, cmd):
        """
            show command allows to view scan options 
            or previous scan results
        """
        if (len(cmd) < 2):
            self.man.get_man("show")
            return
        target = cmd[1]

        if(target == "options"):
            self.scanner.getopt()
        if (target == "result"):
            self.scanner.printres()
        else:
            self.scanner.showvar(cmd[1])

    def setvar(self, cmd):
        """
            Change an option value
        """

        if(len(cmd) < 3):
            self.man.get_man("set")
            return

        var = cmd[1]
        arg = cmd[2]

        success = True

        for vartype in self.scanner.opt:
            if var in self.scanner.opt[vartype]:
                success = True
                if(vartype == "bool"):
                    self.scanner.opt[vartype][var] = False if arg in ['0', 'null', 'false'] else True
                    if(var == "scan_udp"):
                        self.scanner.opt[vartype]["scan_tcp"] = (not self.scanner.opt[vartype][var])
                    elif(var == "scan_tcp"):
                        self.scanner.opt[vartype]["scan_udp"] = (not self.scanner.opt[vartype][var])
                    break
                if(vartype == "int"):
                    try:
                        self.scanner.opt[vartype][var] = int(arg)
                    except:
                        print('<' + arg + '> needs to be an integer')
                    break
                elif (vartype == "string"):
                    self.scanner.opt[vartype][var] = arg
                    break
            else:
                success = False

        if(success):
            print(var, ' = ', arg)
        else:
            print('Unknown variable', var)
