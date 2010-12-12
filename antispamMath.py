import random

class antispamMath:
	"""
    Class that provide a simple math question to protect from rebot spam
        
        >>> antispam = antispamMath()
        >>> antispam.randomImg() #return a dict with 2 number and 1 math sign
        >>> antispam.validate(5) #5 is supposed to be a wrong answer
        False
        >>> antispam.validate(-2) #-2 is supposed to be the correct answer
        True
    """

	def __init__(self):
		self.numbers = dict({1: "wahad", #Mapping the numbers with their image name e.g. 2 = joje.jpg
				2: "joje",
				3: "talata",
				4: "rab3a",
				5: "khamsa",
				6: "sata",
				7: "sab3a",
				8: "tamanya",
				9: "tas3od",
				10: "3achra",
				11: "hadach"
				})
		self.mathSign = dict({"+": "zaide", #Mapping the signs with their image name e.g. '+' = zaide.jpg
						"-": "na9ise",
						})
		self.first = tuple()
		self.second = tuple()
		self.sign = tuple()
	
	def randomImg(self):
		"""Generate random number and sign"""
		
		self.first = random.choice(self.numbers.items())
		self.second = random.choice(self.numbers.items())
		self.sign = random.choice(self.mathSign.items())

		return dict({"first": self.first[1], "second": self.second[1],"sign": self.sign[1]})
	
	def validate(self, answer):
		"""Validate the answer of the user"""
		if self.sign[0] == '+':
			result = int(self.first[0]) + int(self.second[0])
		else:
			result = int(self.first[0]) - int(self.second[0])
		if answer == result:
			return True
		
		return False
