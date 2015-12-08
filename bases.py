# bases.py
# python port for https://github.com/aseemk/bases.js
# Utility for converting numbers to/from different bases/alphabets.
# See README.md for details.

import math
import re
import string

class Bases(object):

	# init
	def __init__(self):

		# Known alphabets:
		self.numerals = string.digits
		self.lettersLowercase = string.ascii_lowercase
		self.lettersUppercase = string.ascii_uppercase
		self.knownAlphabets = {}

		# Each of the number ones, starting from base-2 (base-1 doesn't make sense?):
		i = 2
		while i <= 10:
			self.knownAlphabets[i] = self.numerals[:i]
			i += 1

		# python's native hex is 0-9 followed by *lowercase* a-f, so we'll take that
		# approach for everything from base-11 to base-16:
		i = 11
		while i <= 16:
			self.knownAlphabets[i] = self.numerals + self.lettersLowercase[:i - 10]
			i += 1

		# We also model base-36 off of that, just using the full letter alphabet:
		self.knownAlphabets[36] = self.numerals + self.lettersLowercase

		# And base-62 will be the uppercase letters added:
		self.knownAlphabets[62] = self.numerals + self.lettersLowercase + self.lettersUppercase

		# For base-26, we'll assume the user wants just the letter alphabet:
		self.knownAlphabets[26] = self.lettersLowercase

		# We'll also add a similar base-52, just letters, lowercase then uppercase:
		self.knownAlphabets[52] = self.lettersLowercase + self.lettersUppercase

		# Base-64 is a formally-specified alphabet that has a particular order:
		# http://en.wikipedia.org/wiki/Base64 (and Python follows this too)
		# TODO FIXME But our code above doesn't add padding! Don't use this yet...
		self.knownAlphabets[64] = self.lettersUppercase + self.lettersLowercase + self.numerals + '+/'

		# Flickr and others also have a base-58 that removes confusing characters, but
		# there isn't consensus on the order of lowercase vs. uppercase... =/
		# http://www.flickr.com/groups/api/discuss/72157616713786392/
		# https://en.bitcoin.it/wiki/Base58Check_encoding#Base58_symbol_chart
		# https://github.com/dougal/base58/blob/master/lib/base58.rb
		# http://icoloma.blogspot.com/2010/03/create-your-own-bitly-using-base58.html
		# We'll arbitrarily stay consistent with the above and using lowercase first:
		self.knownAlphabets[58] = re.sub(r'[0OlI]', '', self.knownAlphabets[62])

		# And Douglas Crockford shared a similar base-32 from base-36:
		# http://www.crockford.com/wrmg/base32.html
		# Unlike our base-36, he explicitly specifies uppercase letters
		self.knownAlphabets[32] = self.numerals + re.sub(r'[ILOU]', '', self.lettersUppercase)

		# Do this for all known alphabets:
		for base in self.knownAlphabets:
			if base in self.knownAlphabets:
				self.makeAlias(base, self.knownAlphabets[base])

	# Returns a stringing representation of the given number for the given alphabet:
	def toAlphabet(self, num, alphabet):
		base = len(alphabet)
	  
		digits = []# these will be in reverse order since arrays are stacks
		# execute at least once, even if num is 0, since we should return the '0':
		while num >= 0:
			digits.append(num % base)# TODO handle negatives properly?
			num = math.floor(num / base)
			if num == 0:
				break
		chars = [];
		while len(digits):
			chars.append(alphabet[int(digits.pop())])
		return ''.join(chars)

	# Returns an integer representation of the given stringing for the given alphabet:
	def fromAlphabet(self, strRep, alphabet):
		base = len(alphabet)
		pos = 0
		num = 0
		c = False
		while len(strRep):
			c = strRep[len(strRep) - 1]
			strRep = strRep[:len(strRep) - 1]
			num += math.pow(base, pos) * alphabet.index(c)
			pos += 1
		return int(num)

	# And a generic alias too:
	def toBase(self, num, base):
		return self.toAlphabet(num, self.knownAlphabets[base])

	def fromBase(self, strRep, base):
		return self.fromAlphabet(strRep, self.knownAlphabets[base])

	# Closure helper for convenience aliases like bases.toBase36():
	def makeAlias(self, base, alphabet):
		setattr(self, 'toBase' + str(base), lambda num: self.toAlphabet(num, alphabet))
		setattr(self, 'fromBase' + str(base), lambda strRep: self.fromAlphabet(strRep, alphabet))
