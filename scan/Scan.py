import nmap
import os
from export.Export import *

"""
    nmap scan mapper
"""

class Scan(object):
    """
        Scan manager class, configure and do scans
    """

    def __init__(self):
        """
            Constructor, no param
            New scan contexts can be added here
            Default or fullscan command can be changed here
        """
        self.ps = nmap.PortScanner()
        self.colors = {
            "W": "\033[0m",  # white (normal)
            "R": "\033[41m",
            "fR": "\033[31m",  # red
            "G": "\033[42m",  # green
            "Y": "\033[33m"
        }
        self.scan_context = {
            "contexts": "nas,web,current",
            "ports_context_web": "80,8080,8000,8128,443",
            "ports_context_nas": "21,22,139,445",
            "ports_context_current": "20,21,22,23,80,139,443,445,3306"
        }
        self.opt = {
            "bool": {
                "scan_udp": False,
                "scan_tcp": True,
                "raw_mode": False
            },
            "string": {
                "target": "",
                "ports": "",
                "args": "",
                "export_format": "txt",
                "exp_basename":"nmshell_"
            },
            "int": {
                'tempo': 3
            },

        }
        self.generated_args = ""
        self.json_res = {}
        self.hport = []
        self.hostlist = []
        self.allscan = []
        self.last_scan_type = ""
        self.base_cmd = "nmap -oX -"
        self.targeted_opts = "-sV -sS -sU -O"
        self.fullscan_cmd = "nmap -sS "#-sU -A "


    def reset(self):

        for option,value in [ ("scan_udp",False), ("scan_tcp",True), ("raw_mode",False)] :
            self.opt["bool"][option] = value

        for option in ["target","ports","args"] :
            self.opt["string"][option] = ""


        self.opt["int"]["tempo"] = 3


    def getcli(self):
        """
            Build the command line from args
        """
        self.generate_args()
        cli = []
        cli.append(self.base_cmd)
        cli.append(self.generated_args)
        cli.append(self.opt['string']['target'])
        cli.append("-T" + str(self.opt['int']['tempo']))
        if(self.opt['string']['ports'] != ""):
            cli.append("-p " + self.opt['string']['ports'])
        return " ".join(cli)

    def getopt(self):
        """
            Fetch an option value
        """
        for stype in self.opt:
            if (stype == "bool"):
                print("\t===  Boolean  ===")
                for key, val in self.opt[stype].items():
                    print(key, ": ", val)
            if (stype == "int"):
                print("\t===  Integer  ===")
                for key, val in self.opt[stype].items():
                    print(key, ": ", str(val))
            elif (stype == "string"):
                print("\t===  String  ===")
                for key, val in self.opt[stype].items():
                    print(key, ': "' + val + '"')

    def showvar(self, varname):
        """
            Display a specified option value
        """
        for t in self.opt:
            for key, var in self.opt[t].items():
                if(key == varname):
                    print(key, " => ", var)
                    return True
        return False

    def checkprescan(self, stype):
        """
            Check validity of needed options
        """
        if(self.opt['string']['target'] == ""):
            print("Choose a target before scan with 'set' ('help set')")
            return False

        if stype in self.scan_context['contexts'].split(','):
            self.opt['string']['ports'] = self.scan_context['ports_context_' + stype]
            return True

        if(stype != "default"):
            print("Specified scan type doesn't exist, using default")

        if(self.opt['string']['ports'] == ""):
            print("No ports specified, using defaults")

        return True

    def generate_args(self):
        """
            Generate command line args from options
        """
        args_str = []
        args_str.append(self.opt['string']['args'])

        if(self.opt['bool']['scan_tcp']):
            args_str.append("-sS")
        if(self.opt['bool']['scan_udp']):
            args_str.append("-sU")

        self.generated_args = " ".join(args_str)

    def scan(self, stype="default"):
        """
            Do scan, and save result
        """
        if(not self.checkprescan(stype)):
            return

        self.generate_args()

        if(self.opt["bool"]["raw_mode"]):
            ret = os.popen(self.getcli().replace("-oX -",""))
            print(ret.read())
            return

        print("Start ...", self.opt['string']['target'] + ':' + self.opt['string']['ports'])
        self.json_res = self.ps.scan(self.opt['string']['target'],
              self.opt['string']['ports'],
              arguments=self.generated_args)

        self.last_scan_type = "udp" if self.opt["bool"]["scan_udp"] else "tcp"
        self.printres()


    def printres(self):
        """
            Print scan result
        """
        if not self.last_scan_type:
            print("No result found, did you scan ?")
            return

        disp_lines = []
        self.hport = []
        i = 1
        port_w = False
        hline_format = '#{:^3} {:^15}'
        cell_f = '{:^7}'
        port_line_format = '|' + cell_f

        for host in self.json_res['scan']:
            self.hostlist.append(host)
            s_result = hline_format.format(i, host)
            try:
                
                for port in self.json_res['scan'][host][self.last_scan_type]:
                    if not port_w:
                        self.hport.append(port)
                    state = self.json_res['scan'][host][self.last_scan_type][port]['state']
                    state = state.replace('filtered', 'filt.')
                    if (state == "closed"):
                        s_result += '|' + self.colors['R'] + cell_f.format(state) + self.colors['W']
                    elif (state == "open"):
                        s_result += '|' + self.colors['G'] + cell_f.format(state) + self.colors['W']
                    else:
                        s_result += '|' + self.colors['Y'] + cell_f.format(state) + self.colors['W']
                port_w = True
            except KeyError:
                pass
                #print(self.json_res['scan'][host])
            i += 1
            disp_lines.append(s_result)


        disp_ports = " " * (len("255.255.255.255") +5) 
        
        for portnum in self.hport:    
            disp_ports += port_line_format.format(portnum)
        
        print(disp_ports)
        print(len(self.hport) * '==========' + 13 * "=")

        for line in disp_lines:
            print(line)

        str_stats = "\n\tDone: " + self.json_res['nmap']['scanstats']['timestr']
        str_stats += "(" + self.json_res['nmap']['scanstats']['elapsed'] + "s)"
        str_stats += "\n\tHost(s) up: " + self.json_res['nmap']['scanstats']['uphosts'] + " "
        str_stats += "/" + self.json_res['nmap']['scanstats']['totalhosts']
        
        print(str_stats)

    def targetedscan(self, target_id):
        """
            Do a fullscan for a specified target
        """
        if(target_id > len(self.hostlist) or (target_id <= 0)):
            print("Unknow target, see 'show result'")
            return
        print("Full scan (-sS -sU -A), it can take a while ...")
        targ = self.hostlist[target_id-1]
        ret = os.popen(self.fullscan_cmd + targ)
        print(ret.read())

    def export_result(self):
        
        if not self.last_scan_type:
            print("No result found, did you scan ?")
            return

        xporter = Export(self.opt['string']['exp_basename'])

        if(self.opt['string']['export_format'] == "txt"):
            xporter.export_txt(self.json_res, self.last_scan_type)
        elif(self.opt['string']['export_format'] == "json"):
            xporter.export_json(self.json_res)
        else:
            print("Unknow export format")
            print("Available formats : txt, json")

    def test(self):
        self.opt["string"]["target"] = "192.168.0.1-10"
        self.opt["string"]["ports"] = "20,21,22,80,8080"
       