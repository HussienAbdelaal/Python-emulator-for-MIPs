import re


class Emulator :
	
	def __init__(self):
		self.IR       = 0x0000
		self.PC       = 0x0000
		self.REG_FILE = [0x0,0x0,0x2,0x3,0x0,0x0,0xff,0x0]
		self.OUT      = 0x0000
		self.IN_PORT  = 0x0000
		self.OUT_PORT = 0x0000
		self.RESET_IN = 0
		self.RUN_OUT  = 0
		self.CLK      = 0
		self.memory   = [0] * 64000
		self.memory[10] = "test"
		self.re_line = re.compile(r'^(?:\S+\s+)?(?P<instr>[A-Za-z_\[\]+]+)\s+(?P<arga>[A-Za-z0-9_\[\]+]+)\s*(?:,\s*(?P<argb>[A-Za-z0-9_\[\]+]+))?\s*(?:,\s*(?P<argc>[A-Za-z0-9_\[\]+]+))?')
		self.reg_file_index = {'R0' : 0,'R1' : 1,'R2' : 2,'R3' : 3,'R4' : 4,'R5' : 5,'R6' : 6,'R7' : 7}


	def _eval_exp(self, exp):
		exp = exp.strip()
		result = self.re_line.search(exp)
		if result :
			data = result.groupdict()
			data['instr'] = data['instr'].upper()
			data['arga']  = data['arga'].upper()
			if data['argb']:
				data['argb']  = data['argb'].upper()
			if data['argc']:
				data['argc']  = data['argc'].upper()
		else :
			data = {}
		return data




	def excute(self, assembly_code):
		assembly_code = assembly_code.strip().split('\n')
		count = 0
		while count < len(assembly_code) :
			if len(assembly_code[count]):
				data = self._eval_exp(assembly_code[count])

				if(data['instr'] == 'ADD') :
					if (data['arga'] and data['argb'] and data['argc']):						
						self.REG_FILE[self.reg_file_index[data['arga']]] = self.REG_FILE[self.reg_file_index[data['argb']]] + self.REG_FILE[self.reg_file_index[data['argc']]]
						self.PC += 2 


				if(data['instr'] == 'SUB'):
					if (data['arga'] and data['argb'] and data['argc']):
						self.REG_FILE[self.reg_file_index[data['arga']]] = self.REG_FILE[self.reg_file_index[data['argb']]] - self.REG_FILE[self.reg_file_index[data['argc']]]
						self.PC += 2 
						

				if(data['instr'] == 'AND'):
					if (data['arga'] and data['argb'] and data['argc']):
						self.REG_FILE[self.reg_file_index[data['arga']]] = self.REG_FILE[self.reg_file_index[data['argb']]] & self.REG_FILE[self.reg_file_index[data['argc']]]
						self.PC += 2 
						

				if(data['instr'] == 'OR' ):
					if (data['arga'] and data['argb'] and data['argc']):
						self.REG_FILE[self.reg_file_index[data['arga']]] = self.REG_FILE[self.reg_file_index[data['argb']]] | self.REG_FILE[self.reg_file_index[data['argc']]]
						self.PC += 2 

						

				if(data['instr'] == 'NOR'):
					if (data['arga'] and data['argb'] and data['argc']):
						self.REG_FILE[self.reg_file_index[data['arga']]] = ~(self.REG_FILE[self.reg_file_index[data['argb']]] | self.REG_FILE[self.reg_file_index[data['argc']]])
						self.PC += 2 
						

				if(data['instr'] == 'XOR'):
					if (data['arga'] and data['argb'] and data['argc']):
						self.REG_FILE[self.reg_file_index[data['arga']]] = self.REG_FILE[self.reg_file_index[data['argb']]] ^ self.REG_FILE[self.reg_file_index[data['argc']]]
						self.PC += 2 
						

				if(data['instr'] == 'SLL'):
					if (data['arga'] and data['argb']):
						self.REG_FILE[self.reg_file_index[data['arga']]] = self.REG_FILE[self.reg_file_index[data['argb']]] << 1
						self.PC += 2 
						

				if(data['instr'] == 'SRL'):
					if (data['arga'] and data['argb']):
						self.REG_FILE[self.reg_file_index[data['arga']]] = self.REG_FILE[self.reg_file_index[data['argb']]]>> 1
						self.PC += 2 
						

				if(data['instr'] =='ADDI'):
					if (data['arga'] and data['argb'] and data['argc']):
						self.REG_FILE[self.reg_file_index[data['arga']]] = self.REG_FILE[self.reg_file_index[data['argb']]] + int(data['argc'])
						self.PC += 2 
						

				if(data['instr'] =='ANDI'):
					if (data['arga'] and data['argb'] and data['argc']):
						self.REG_FILE[self.reg_file_index[data['arga']]] = self.REG_FILE[self.reg_file_index[data['argb']]] & int(data['argc'])
						self.PC += 2 
						

				if(data['instr'] =='ORI'):
					if (data['arga'] and data['argb'] and data['argc']):
						self.REG_FILE[self.reg_file_index[data['arga']]] = self.REG_FILE[self.reg_file_index[data['argb']]] | int(data['argc'])
						self.PC += 2 
						

				if(data['instr'] == 'LW'):
					if (data['arga'] and data['argb'] and data['argc']):
						self.REG_FILE[self.reg_file_index[data['arga']]] = self.memory[int(data['argb']) + self.REG_FILE[self.reg_file_index[data['argc']]]]
						self.PC += 2 
						

				if(data['instr'] == 'SW'):
					if (data['arga'] and data['argb'] and data['argc']):
						self.memory[int(data['argb']) + self.REG_FILE[self.reg_file_index[data['argc']]]] = self.REG_FILE[self.reg_file_index[data['arga']]]
						self.PC += 2 
						
	
				if(data['instr'] == 'J'):
					if (data['arga']):
						self.PC = (int(data['arga']) | (self.PC & 0x000))
						count = ((self.PC)/2)-1


				if(data['instr'] == 'JAL') :
					if (data['arga']):
						self.PC = (int(data['arga']) | (self.PC & 0x000))
						count = ((self.PC)/2)-1
						self.REG_FILE[7] = self.PC + 2

		
				if(data['instr'] == 'JR')  :
					if (data['arga']):
						self.PC = self.REG_FILE[self.reg_file_index[data['arga']]]
						count = ((self.PC)/2)-1


				if(data['instr'] == 'NOP') :
					self.PC += 2


				if(data['instr'] == 'OUT') :
					if (data['arga']):
						self.OUT_PORT = self.REG_FILE[self.reg_file_index[data['arga']]]
						self.PC += 2

				if(data['instr'] == 'IN') :
					if (data['arga']):
						self.REG_FILE[self.reg_file_index[data['arga']]] = self.IN_PORT
						self.PC += 2


				if(data['instr'] == 'BEQ') :
					if (data['arga'] and data['argb'] and data['argc']):
						if (self.REG_FILE[self.reg_file_index[data['arga']]] == self.REG_FILE[self.reg_file_index[data['argb']]]):
							self.PC += 2 + int(data['argc'])
							count = ((self.PC)/2)-1

						else :
							self.PC += 2

				if(data['instr'] == 'BNE') :
					if (data['arga'] and data['argb'] and data['argc']):
						if (self.REG_FILE[self.reg_file_index[data['arga']]] != self.REG_FILE[self.reg_file_index[data['argb']]]):
							self.PC += 2 + int(data['argc'])
							count = ((self.PC)/2)-1
							
						else :
							self.PC += 2

				count += 1



code = """
	j 16
	add  r1, R2, r3
	sub  r0, r1, r3 
	and  r4, r3, r1
	or   r5, r3, r1
	sw r1, 8, r3
	or r5,r6,r5
	add r0, r1, r0
	add r0, r1, r3
	j 6
"""
test_code = Emulator()
print test_code.REG_FILE
print test_code.PC
test_code.excute(code)
print test_code.REG_FILE
print test_code.PC
