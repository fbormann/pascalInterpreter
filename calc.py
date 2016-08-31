INTEGER, PLUS, EOF = 'INTEGER', 'PLUS', 'EOF'

class Token(object):
	def __init__(self, type, value):
		# token type: Integer, plus, eof
		self.type = type
		# token value : 1,2,3,4...'+'
		self.value = value

	def __str__(self):
		return 'Token {type} {value}'.format(type=self.type,
			value=repr(self.value))

	def repr(self):
		return self.__str__()


class Interpreter(object):
	def __init__(self, text):
		self.text = text
		self.pos = 0
		self.current_token = None

	def error(self):
		raise Exception('Error parsing input')

	def get_next_token(self):

		text = self.text
		if self.pos > len(text) - 1:
			return Token(EOF, None)

		current_char = text[self.pos]
		if current_char.isdigit():
			digit = int(current_char)
			
			number = digit
			if self.pos < len(text) - 1:
				self.pos += 1
				current_char = text[self.pos]
				while current_char.isdigit(): #this add support for multiple digit integers
					number *= 10
					digit = int(current_char)
					number += digit
					self.pos += 1
					if self.pos > len(text) - 1:
						break
					current_char = text[self.pos]
			token = Token(INTEGER, number)
			print(token.repr())
			return token

		if current_char == '+':
			token = Token(PLUS, current_char)
			self.pos += 1
			return token

		self.error()
	
	def eat(self, token_type):
	# compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
		if self.current_token.type == token_type:
			self.current_token = self.get_next_token()
		else:
            		self.error()
	def expr(self):
		"""expr -> INTEGER PLUS INTEGER"""
		# set current token to the first token taken from the input
		self.current_token = self.get_next_token()
		# we expect the current token to be a single-digit integer
		left = self.current_token
		self.eat(INTEGER)

        # we expect the current token to be a '+' token
		op = self.current_token
		self.eat(PLUS)

        # we expect the current token to be a single-digit integer
		right = self.current_token
		self.eat(INTEGER)
        # after the above call the self.current_token is set to
        # EOF token

        # at this point INTEGER PLUS INTEGER sequence of tokens
        # has been successfully found and the method can just
        # return the result of adding two integers, thus
        # effectively interpreting client input
		result = left.value + right.value
		return result


def main():
    while True:
        try:
            # To run under Python3 replace 'raw_input' call
            # with 'input'
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)


if __name__ == '__main__':
    main()