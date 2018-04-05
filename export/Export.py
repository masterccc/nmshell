"""
Export result to a file
"""

import datetime

class Export(object):
	"""
	Export Class
	"""
	def __init__(self, file_basename):
		"""
		Constructor
		"""
		self.file_basename = file_basename


	def get_filename(self, ext):
		now = datetime.datetime.now()
		fname = self.file_basename
		fname += str(now.year)
		fname += str(now.month)
		fname += str(now.day)
		fname += str(now.minute)
		fname += str(now.second)
		fname += "." + ext
		return fname

	def export_json(self, json):

		file_name = self.get_filename("json")
		file = open(file_name, "w")
		file.write(str(json))
		file.close()
		print("Saved as '" + file_name + "'")

	def export_txt(self, json_result, last_scan_type):
		
		file_name = self.get_filename("txt")
		file = open(file_name, "w")
		
		txt = ""
		disp_lines = []
		self.hport = []
		i = 1
		port_w = False
		hline_format = '#{:^3} {:^15}'
		cell_f = '{:^7}'
		port_line_format = '|' + cell_f

		for host in json_result['scan']:
			s_result = hline_format.format(i, host)
			try:
				
				for port in json_result['scan'][host][last_scan_type]:
					if not port_w:
						self.hport.append(port)
					state = json_result['scan'][host][last_scan_type][port]['state']
					state = state.replace('filtered', 'filt.')
					if (state == "closed"):
						s_result += '|' + cell_f.format(state)
					elif (state == "open"):
						s_result += '|' + cell_f.format(state) 
					else:
						s_result += '|' + cell_f.format(state) 
				port_w = True
			except KeyError:
				pass
				#print(json_result['scan'][host])
			i += 1
			txt += s_result + "\n"

		disp_ports = " " * (len("255.255.255.255") +5) 
		
		for portnum in self.hport:	
			disp_ports += port_line_format.format(portnum)
		
		txt = disp_ports + '\n' + txt + "\n"
		txt += len(self.hport) * '==========' + 13 * "="
		txt += "\n"

		for line in disp_lines:
			txt += line + "\n"

		txt += "\nDone: " + json_result['nmap']['scanstats']['timestr']
		txt += "(" + json_result['nmap']['scanstats']['elapsed'] + "s)"
		txt += "\nHost(s) up: " + json_result['nmap']['scanstats']['uphosts'] + " "
		txt += "/" + json_result['nmap']['scanstats']['totalhosts'] + "\n"
		

		txt = "Scan type : " + last_scan_type.upper()+ '\n' + txt
		txt = "Generated : " + str(datetime.datetime.now()) + '\n\n' + txt
		txt = "Nmshell Report\n" + txt 

		file.write(txt)
		file.close()
		print("Saved as '" + file_name + "'")

