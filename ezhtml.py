'''
	EZHTML by diablo.

	EZHTML is an easy to use python module to code HTML without actually coding any HTML.
	For practical uses.... can't really think of any actual real world uses, unless you needed
	help understanding how HTML works I guess.
'''

import sys

class TEXT_ORDER:
	'''
		Used for declaring whether the HTML element will require the innerText
		to be before any other child HTML elements, or after the children.
	'''
	FIRST = True
	LAST  = False


class Element:
	'''
		An HTML element. Can be any type of HTML element. From "html" to "body", from "div" to "img".
	'''
	def __init__(self, tag_: str, attr=dict(), text=str()):
		'''
			tag_ : the HTML tag for the element
			attr : a dictionary containing any attributes required for the element (can be added later)
			text : the innerText for the HTML element
		'''
		self.__tag = tag_
		self.__Attributes = attr
		self.__children = {}
		self.__text_order = True
		self.__text = text

		# make the Attributes for the html tag be an actual part of the element, rather than "myElement.attribute['id'] = blahblahblah"
		for key in self.__Attributes.keys():
			setattr(self, key, self.__Attributes[key])

	def appendChild(self, child):
		'''
			Append a child Element object to this element
		'''
		self.__children[child.tag] = child # store the data of all the elements
		setattr(self, child.tag, child) #make the child a part of the parent

	def childrenCount(self):
		'''
			Gather the count of all the children in this html document, and all the other nested children
		'''
		ctr = 0
		for child in self.__children.values():
			ctr += 1 + child.childrenCount()
		return ctr

	@property
	def head(self):
		'''
			The HTML tag head; i.e. '<div id="bruh">'
		'''
		r = f'<{self.tag}'
		for attr in self.__Attributes.items():
			r += ' ' + attr[0] + '="' + attr[1] + '"'
		return r + '>'

	@property
	def foot(self):
		'''
			The HTML tag foot; i.e. '</div>'
		'''
		return f'</{self.tag}>'

	@property
	def children(self):
		'''
			See the children this element has. (Non-recursive)
		'''
		return self.__children

	@property
	def tag(self):
		'''
			The element's tag; i.e. "head", "div", "id"
		'''
		return self.__tag

	@tag.setter
	def tag(self, val: str):
		self.__tag = val

	@property
	def text(self):
		return self.__text

	@text.setter
	def text(self, val: str):
		self.__text = val

	@property
	def text_order(self):
		'''
			The order which the text should be in.
			The text should be BEFORE any children, or AFTER any child elements.
		'''
		return self.__text_order

	@text_order.setter
	def text_order(self, val: bool):
		self.__text_order = val

	@property
	def attributes(self):
		'''
			Returns the dictionary containing all the attributes to this element.
		'''
		return self.__Attributes

	@attributes.setter
	def attributes(self, val):
		if type(val) != dict:
			print("Cannot set attributes to a non-dict object")
			sys.exit(1)
		else:
			self.__Attributes = val
	
	def add_attr(self, attr: str, val: str)->None:
		self.__Attributes[attr]=val
		setattr(self, attr, val)
	
	def rem_attr(self, attr: str)-> bool:
		#should an error occur (maybe because that attribute does not exist), will return False
		try:
			del self.__Attributes[attr]
			delattr(self, attr)
			return True
		except KeyError:
			return False

	def __str__(self):
		return prettify(self)

	def __repr__(self):
		return f'element: {self.tag}; {self.childrenCount()} child(ren)'	

def _r_html_blocks_to_str(child: dict)-> str:
	'''
		Outputs the text of the children elements and the parent element.
	'''
	ret = str()
	tag = child['tag']
	text = child['text']
	head = child['head']
	tabsize = child['tabsize']
	textorder = child['textorder']

	ret += '\n' + ('\t' * tabsize) + head
	if textorder:
		if len(text) > 1:
			ret += child['text']
	
	if len(child['children']) >= 1:
		for c in child['children']:
			ret += _r_html_blocks_to_str(c)
	if not textorder:
		if len(text) > 1:
			ret += '\n' + ('\t' * (tabsize+1)) + f'{text}'

	if not len(child['children']) >= 1:
		ret +=  f'</{tag}>'
	else:
		ret += '\n' + ('\t' * tabsize) + f'</{tag}>'
	return ret

def _r_html_child_tabs_text(element: Element, ctr: int)-> dict:
	# get the formatted information for each html element and child
	ret = { 'tag': element.tag, 'head': element.head, 'tabsize': ctr, 'children': [], 'text': element.text, 'textorder': element.text_order }
	
	# if there are any children, append any other children objects
	if element.childrenCount() >= 1:
		for child in element.children.values():
			ret['children'].append(_r_html_child_tabs_text(child, ctr + 1))
	return ret



def prettify(html_element: Element, type_ = 'html')-> str:
	'''
		Returns pretty formatted HTML code.
	'''
	res = str()

	#if the document is to be in HTML5
	if type_ == 'html5':
		res += '<!DOCTYPE html>\n'

	res += f'{html_element.head}'
	if html_element.childrenCount() >= 1:
		children = []
		for child in html_element.children.items():
			children.append(_r_html_child_tabs_text(child[1], 1))

		for child in children:
			res += _r_html_blocks_to_str(child)
	res += f'\n{html_element.foot}'
	return res

def save_html(path: str, html: Element, html5 = True, verbose= False):
	'''
		Save the HTML element object to a file.

		path    : path to file
		html    : the Element to write
		html5   : Is the document HTML5, or not
		verbose : Let you know if the file saved properly
	'''
	with open(path, 'w') as file:
		res = None
		if html5:
			res = prettify(html, 'html5')
		else:
			res = prettify(html)

		file.write(res)
		file.close()
		if verbose:
			print("Saved html file")