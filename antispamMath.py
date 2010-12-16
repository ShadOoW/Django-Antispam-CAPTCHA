import random, glob
import ImageDraw, Image
from datetime import datetime

path_to_numbers = "m/images/captcha/numbers/" #Path to the folders with numbers images
path_to_signs = "m/images/captcha/signs/" #Path to the folders with signs images
path_to_save = "m/images/captcha/"
#The two path should be different!

class antispamMath:
	"""
    Class that provide a simple math question to protect from rebot spam
        
        >>> antispam = antispamMath()
        >>> antispam.randomImg()
        
    For a complet how to use visit : www.icode.co/en/code/
    """
    
	def __init__(self):
		self.numbers = glob.glob(path_to_numbers + "*.jpg")
		self.signs = glob.glob(path_to_signs + "*.jpg")
		
		self.first = tuple()
		self.second = tuple()
		self.sign = tuple()
		
	def randomImg(self):
		"""Generate random numbers and sign"""
		
		#Size of the images
		width = 138
		height = 140
		
		#Choose randomly 2 numbers and 1 sign from the dicts
		self.first = random.choice(self.numbers)
		self.second = random.choice(self.numbers)
		self.sign = random.choice(self.signs)
		
		#Create a new image that can contain the 3 other - width*3
		image = Image.new("RGBA", (width*3, height), (255,255,255, 0))
		draw = ImageDraw.Draw(image)
		
		#Open the 3 images randomly chosen and resize them in case their are bigger.
		img1 = Image.open(self.first).resize((width, height), Image.ANTIALIAS)
		img2 = Image.open(self.sign).resize((width, height), Image.ANTIALIAS)
		img3 = Image.open(self.second).resize((width, height), Image.ANTIALIAS)
		
		#Paste each of the 3 images into the final captcha image
		point1 = width*3 - (width)
		point2 = height - (height)
		point3 = width*3
		point4 = height
		image.paste(img3, (point1, point2, point3, point4))
		
		point1 = width*2 - (width)
		point2 = height - (height)
		point3 = width*2
		point4 = height
		image.paste(img2, (point1, point2, point3, point4))
		
		point1 = 0
		point2 = 0
		point3 = width
		point4 = height
		image.paste(img1, (point1, point2, point3, point4))
		
		#Finally save the captcha image as jpeg.
		image.save(path_to_save + "captcha.jpg", "JPEG")
	
		## Uncomment to test ##
		#import webbrowser
		#webbrowser.open(path_to_save + "captcha.jpg")
		
	def validate(self, request ,answer):
		"""Validate the answer of the user"""
		
		try:
			answer = int(answer)
		except ValueError:
			request.session['nbrOfFalseTry'] += 1
			return False
		else:
			if self.getSign(self.sign) == '+':
				result = self.getNumber(self.first) + self.getNumber(self.second)
			else:
				result = self.getNumber(self.first) - self.getNumber(self.second)
			if answer == result:
				return True
		request.session['nbrOfFalseTry'] += 1
		return False
		
	def numberOfTry(self, request ,limit=5):
		"""Should be used in a If statement. return True until the limit of try is by passed
		
		if the number of false try is bigger than the limit set, some session var are created:
		time_out: the exact time when the limit of  authorized try is by passed.
		reason: is a text message that explain to the user what happening.
		message: is the name of the form field that we want to save and display in the next page
		
		"""
		if 'nbrOfFalseTry' not in request.session:
			request.session['nbrOfFalseTry'] = 0
		
		if request.session['nbrOfFalseTry'] <= limit:
			return True
		else:
			if 'time_out' not in request.session:
				request.session['time_out'] = datetime.now() 
			if 'reason' not in request.session:
				request.session['reason'] = "You have tried 5 time to answer the CAPTCHA without succes."
			try:
				if 'message' not in request.session:
					request.session['message'] = request.POST['message']
			except NameError:
				pass
			return False
			
	def restart(self, request):
		request.session['nbrOfFalseTry'] = 0
		
		if 'time_out' in request.session:
			del request.session['time_out']
		if 'reason' in request.session:
			del request.session['reason']
		if 'message' in request.session:
			del request.session['message']

	def getNumber(self, number):
		"""Get the integer version of the images from their name."""
		result = str()
		for i in range(len(number)):
			try:
				int(number[i])
				result += number[i]
			except ValueError:
				continue
		return int(result)

	def getSign(self, sign):
		"""Get the sign version of the image from the name."""
		if '+' in sign:
			return '+'
		else:
			return '-'   
