import os
import re

class TEXT_ORDER:
	FIRST = True
	LAST  = False


class Element:
	def __init__(self, type_: str, attr=dict(), text=str()):
		self.Type = type_
		self.Attributes = attr
		self.__sauce = { 'children': [], 'text-order': (True, text)}

	def appendChild(self, child):
		self.__sauce['children'].append(child)

	def childrenCount(self):
		ctr = 0
		for child in self.__sauce['children']:
			ctr += 1 + child.childrenCount()
		return ctr

	@property
	def head(self):
		r = f'<{self.Type}'
		for attr in self.Attributes:
			r += ' ' + attr[0] + '="' + attr[1]
		return r + '>'

	@property
	def foot(self):
		return f'</{self.Type}>'

	@property
	def children(self):
		return self.__sauce['children']

	@property
	def text(self):
		return self.__sauce['text-order'][1]

	@text.setter
	def text(self, val: str):
		self.__sauce['text-order'] = (self.__sauce['text-order'][0], val)

	@property
	def text_order(self):
		return self.__sauce['text-order'][0]

	@text_order.setter
	def text_order(self, val: bool):
		self.__sauce['text-order'] = (val, self.__sauce['text-order'][1])

	def __str__(self):
		html_code = f'<{self.Type}'
		for attr in self.Attributes.items():
			html_code += f' {attr[0]}="{attr[1]}"'
		html_code += '>'
		# inner text is before any of the elements ahead
		if self.__sauce['text-order'][0]:
			html_code += self.__sauce['text-order'][1]
		for child in self.__sauce['children']:
			html_code += f'\n\t{child.__str__()}'
		if not self.__sauce['text-order'][0]:
			html_code += self.__sauce['text-order'][1]
		if len(self.__sauce['children']) >= 1:
			html_code += f'\n</{self.Type}>'
		else:
			html_code += f'</{self.Type}>'
		return html_code

	def __repr__(self):
		return f'element: {self.Type}; {self.childrenCount()} child(ren)'	

def _r_html_blocks_to_str(child: dict)-> str:
	ret = str()
	tag = child['tag']
	head = child['head']
	tabsize = child['tabsize']
	textorder = child['textorder']



	ret += '\n' + ('\t' * tabsize) + head
	if textorder:
		if len(child['text']) > 1:
			ret += child['text']
	
	if len(child['children']) >= 1:
		for c in child['children']:
			ret += _r_html_blocks_to_str(c)
	if not textorder:
		if len(child['text']) > 1:
			ret += '\n' + ('\t' * (tabsize+1)) + f'{child["text"]}'
	ret += '\n' + ('\t' * tabsize) + f'</{tag}>'
	return ret

def _r_html_child_tabs_text(element: Element, ctr: int)-> dict:
	# get the formatted information for each html element and child
	ret = { 'tag': element.Type, 'head': element.head, 'tabsize': ctr, 'children': [], 'text': element.text, 'textorder': TEXT_ORDER.LAST }
	if element.childrenCount() >= 1:
		for child in element.children:
			ret['children'].append(_r_html_child_tabs_text(child, ctr + 1))
	return ret



def prettify(html_element: Element, type_ = 'html')-> str:
	res = str()
	if type_ == 'html5':
		res += '<!DOCTYPE html>\n'
	res += f'{html_element.head}'
	if html_element.childrenCount() >= 1:
		children = []
		for child in html_element.children:
			children.append(_r_html_child_tabs_text(child, 1))

		for child in children:
			res += _r_html_blocks_to_str(child)
	res += f'\n{html_element.foot}'
	return res
	


	return res


def save_html(path: str, html: Element, html5 = True, verbose= False):
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