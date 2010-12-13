import random
import ImageDraw, Image

class antispamMath:
	"""
    Class that provide a simple math question to protect from rebot spam
        
        >>> antispam = antispamMath()
        >>> antispam.randomImg() #return a dict with 2 numbers and 1 math sign
        >>> antispam.validate(5) #5 is supposed to be a wrong answer
        False
        >>> antispam.validate(-2) #-2 is supposed to be the correct answer
        True
        >>> antispam.getNumberOfTry("all")
        2
        >>> antispam.getNumberOfTry("false")
        1
        >>> antispam.getNumberOfTry("true")
        1
    """
    
	def __init__(self):
		"""Mapping the numbers with their images name e.g. 2 = joje [.jpg]"""
		self.numbers = dict({1: "wahad", 
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
		self.mathSign = dict({"+": "zaide", #Mapping the signs with their images name e.g. '+' = zaide [.jpg]
							"-": "na9ise",
							})
		self.first = tuple()
		self.second = tuple()
		self.sign = tuple()

		self.nbrOfFalseTry = int(0)
		self.nbrOfTrueTry = int(0)
		
		
	def randomImg(self):
		"""Generate random numbers and sign"""
		
		width = 138
		height = 140
		
		self.first = random.choice(self.numbers.items())
		self.second = random.choice(self.numbers.items())
		self.sign = random.choice(self.mathSign.items())
		
		image = Image.new("RGBA", (width*3, height), (255,255,255, 0))
		draw = ImageDraw.Draw(image)
		
		img1 = Image.open("images/" + self.first[1] +".jpg").resize((width, height), Image.ANTIALIAS)
		img2 = Image.open("images/" + self.sign[1] +".jpg").resize((width, height), Image.ANTIALIAS)
		img3 = Image.open("images/" + self.second[1] +".jpg").resize((width, height), Image.ANTIALIAS)
		
		
		point1 = width*3 - (width)
		point2 = height - (height)
		point3 = width*3
		point4 = height
		image.paste(img1, (point1, point2, point3, point4))
		
		point1 = width*2 - (width)
		point2 = height - (height)
		point3 = width*2
		point4 = height
		image.paste(img2, (point1, point2, point3, point4))
		
		point1 = width - (width)
		point2 = height - (height)
		point3 = width
		point4 = height
		image.paste(img3, (point1, point2, point3, point4))
		
		image.save("captcha.jpg", "JPEG")
	
		## Uncomment to test ##
		#import webbrowser
		#webbrowser.open("captcha.jpg")
	
	def validate(self, answer):
		"""Validate the answer of the user"""
		
		try:
			answer = int(answer)
		except ValueError:
			self.nbrOfFalseTry += 1
			return False
		else:
			if self.sign[0] == '+':
				result = self.first[0] + self.second[0]
			else:
				result = self.first[0] - self.second[0]
			if answer == result:
				self.nbrOfTrueTry += 1
				return True
		
		self.nbrOfFalseTry += 1
		return False

	def getNumberOfTry(self, category):
		if category == 'all':
			return self.nbrOfFalseTry + self.nbrOfTrueTry
		elif category == 'false':
			return self.nbrOfFalseTry
		elif category == 'true':
			return self.nbrOfTrueTry
		else:
			return False
