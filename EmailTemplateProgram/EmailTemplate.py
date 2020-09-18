# 
# 	Address OUTLOOK rendering issue
# 		- https://www.contactmonkey.com/blog/outlook-rendering-issues
# 

# imports
import os
import codecs
import math
import drawBot

# Email Template Builder Class
class EmailTemplate:

	# constructor
	def __init__( self,
			# CONTENT INFORMATION
			extImgUrl='', contentPath='./contents/', docTitle='', docDesc='',
			# GENERAL STYLES
			width=600, tableClass='', bodyStyles=''' ''', divStyleDefault=''' ''', imgStyleDefault=''' ''',
			# EXPORT OPTIONS
			saveAs='default-out.html', showMsgs=False, minifyHtmlOut=False, exportFile=False
		):
		self.externalImgUrl = extImgUrl
		self.width = width
		self.PATH_TO_CONTENT = contentPath
		self.contents = None
		self.c_types = {
			'img': ['png', 'jpg', 'gif'],
			'html': ['html', 'txt']
		}
		self.docTitle = docTitle
		self.docDesc = docDesc
		self.bodyStyles = self.minifyHtml( bodyStyles )
		self.divStyleDefault = self.minifyHtml( divStyleDefault )
		self.imgStyleDefault = self.minifyHtml( imgStyleDefault )
		self.tableClass = tableClass
		self.emailHtml = ''
		self.notify = showMsgs
		self.minify = minifyHtmlOut
		self.exportFile = exportFile
		self.saveAs = saveAs
		# BEGIN
		if self.notify:
			print('\n*** Welcome to GC Email Template Builder ***\n')
			print('Running Initializer... . .  .   .     .        .')
		# get all content from path
		self.getContentItemsFromPath(contentPath)
		# now caluculate layout information
		self.spanMax = self.calulateColSpanMax()
		# begin build
		self.isBuilding = False
		if not self.isBuilding:
			self.build()

	# --------------------------------------------------
	# 	CLASS FUNCTIONS
	# --------------------------------------------------

	# generate a dictionary of email content/items
	def getContentItemsFromPath(self, FPATH):
		contentItems = {}
		# build email content list by file type
		for fileName in os.listdir(FPATH):
			if not fileName[0] == '.':
				# split and check ext
				# HTML/TXT
				if fileName.split('.',1)[1] in self.c_types["html"]:
					htmlStr = codecs.open(FPATH+fileName, 'r').read()
					htmlStr = self.minifyHtml(htmlStr)
					contentItems[fileName] = ( 'html', htmlStr )
				# IMAGES
				else:
					# linked img
					if not fileName.find('-link-') == -1:
						contentItems[fileName] = ( 'link', drawBot.imageSize(FPATH+fileName) )
					# plain img
					else:
						contentItems[fileName] = ( 'img', drawBot.imageSize(FPATH+fileName) )
		# set contents to use
		self.contents = contentItems

	# build the output string
	def build(self):
		self.isBuilding = True
		if self.notify:
			print('Building...')
		output = ''
		output += self.GenerateHeader()
		output += self.GenerateBody()
		currentSpan = self.spanMax
		internalSpan = 0
		fullSpan = True # assume full colspan
		# loop through each content item and build HTML output
		for c_index, (fileName, (f_type, item_content) ) in enumerate(sorted(self.contents.items())):
			#print(c_index, fileName, f_type, item_content )
			# only close row if reached start of a span line
			if fullSpan or internalSpan == 0:
				# open row
				output += self.openRow()
			# do something with html
			if f_type == 'html':
				output += self.openColumn(span=currentSpan)
				output += self.contentHtmlTxt(item_content, self.divStyleDefault)
				output += self.closeColumn()
			# do something with plain img
			if f_type == 'img':
				# check img width to span td elm
				# not full width
				if not item_content[0] == self.width:
					# get the actual span for this element
					fullSpan = False
					actualColSpan = self.calulateColSpan(cIndex=c_index, item=item_content)
					internalSpan += actualColSpan
					output += self.openColumn(span=actualColSpan)
				# full width elm
				else:
					output += self.openColumn(span=currentSpan)
				# close out column
				output += self.contentPlainImg(fileName, item_content, self.imgStyleDefault)
				output += self.closeColumn()
			# do something with linked img
			if f_type == 'link':
				# check img link width to span td elm
				# not full width
				if not item_content[0] == self.width:
					# get the actual span for this element
					fullSpan = False
					actualColSpan = self.calulateColSpan(cIndex=c_index, item=item_content)
					internalSpan += actualColSpan
					output += self.openColumn(span=actualColSpan)
				# full width elm
				else:
					output += self.openColumn(span=currentSpan)
				# close out column
				output += self.contentLinkedImg(fileName, item_content, self.imgStyleDefault)
				output += self.closeColumn()
			# if the current colspan is less than the maximum allowed
			if currentSpan < self.spanMax:
				# subtract colspan from max until reach end of row
				currentSpan -= currentSpan
			# if reached end of span line
			if internalSpan == currentSpan:
				# resent row span counts
				currentSpan = self.spanMax
				internalSpan = 0
				# set close row marker
				fullSpan = True
			# only close row if row is full
			if fullSpan:
				# close row
				output += self.closeRow()
				# reset full span ref
				fullSpan = False
		# close last row/table/body/html elms
		output += self.closeRow()
		output += self.closeBody()
		# minify html
		if self.minify:
			output = self.minifyHtml(output)
		# set emailHTML
		self.emailHtml = output
		# notify build completed
		if self.notify:
			print('...Build DONE!')
		self.isBuilding = False

	# ---------------------------------------------------------------------------
	# 	MODEL FUNCTIONS (returns something)
	# ---------------------------------------------------------------------------
	
	# get link from image path 
	def getLinkFromImagePath(self, fName):
		return fName.split('-link-',1)[1]

	# loop items and determine the total colspans available
	def calulateColSpan(self, cIndex, item):
		# calc percent
		itemSpanPerc = math.floor(item[0] / self.width * 100)
		# get value from range within span max
		colspan = math.floor ( (itemSpanPerc * (self.spanMax - 1) / 100) + 1 )
		# SPECIAL CASES
		if itemSpanPerc in [15, 16, 25, 26]:
			colspan = 1
		if itemSpanPerc in [68]:
			colspan = 3
		# return colspan
		return colspan

	# loop items and determine the total colspans available
	def calulateColSpanMax(self):
		# count vars
		numCols = 1
		currentMaxSpan = 1
		# loop through each content item and update the count
		for c_index, (fileName, (f_type, item_content) ) in enumerate(sorted(self.contents.items())):
			# imgs only atm — IMPROVE FEATURES TO ALLOW MULTI COL TEXT
			if f_type == 'img':
				# get width
				itemWidth = item_content[0]
				# calc perceny
				itemSpanPerc = math.floor(itemWidth / self.width * 100)
				# not at 100% yet
				if itemSpanPerc < 100:
					# add to numCol count
					numCols += 1
				# reached 100%
				else:
					# reset col loop
					numCols = 0
				# numCols 
				if not numCols == 0 and numCols > currentMaxSpan:
					# set new max
					currentMaxSpan = numCols
		# reutrn span max
		return currentMaxSpan

	# takes a template string with \n \t \r
	# condenses format in to single string
	def minifyHtml(self, htmlStr):
		return htmlStr.replace('\n', '').replace('\t', '').replace('\r', '')

	# exports HTML
	def exportHtml(self, htmlStr=''):
		# Write HTML String to file.html
		with open(self.saveAs, 'w') as htmlFile:
			return htmlFile.write(htmlStr)

	# generate header string
	def GenerateHeader(self):
		hstr = '''
			<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
			<html xmlns="http://www.www.w3.org/1999/xhtml">
			<head>
				<title>%s</title>
				<meta name="description" content="%s">
				<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
			</head>
			''' % (self.docTitle, self.docDesc)
		return hstr

	# generate body string
	def GenerateBody(self):
		bstr = '''
			<body bgcolor="#FFFFFF" leftmargin="0" topmargin="0" marginwidth="0" marginheight="0" style="%s">
				<table id="%s" width="%d" align="center" border="0" cellpadding="0" cellspacing="0">
			''' % (self.bodyStyles, self.tableClass, self.width)
		return bstr

	# open a new row
	def openRow(self):
		srStr = '<tr>'
		return srStr

	# open table row element + TD column span
	def openColumn(self, span=1):
		ocStr = '<td colspan="%d">\n' % span
		return ocStr

	# content - html
	def contentHtmlTxt(self, cObj, styleStr):
		htmlStr = '<div style="%s">\n%s\n</div>\n' % (styleStr, cObj)
		return htmlStr

	# content - plain img
	def contentPlainImg(self, fName, cObj, styleStr):
		imgId = fName.split('.',1)[0]
		imgSrc = 'http://'+self.externalImgUrl+fName
		imgStyles = styleStr
		pImgStr = '<img id="%s" src="%s" width="%d" height="%d" border="0" style="%s" alt="" />\n' % (imgId, imgSrc, cObj[0], cObj[1], imgStyles)
		return pImgStr

	# content - linked img
	def contentLinkedImg(self, fName, cObj, styleStr):
		linkTo = 'http://'+self.getLinkFromImagePath(fName).replace(':','/')
		imgId = fName.split('.',1)[0]
		imgSrc = self.externalImgUrl+fName
		imgStyles = styleStr
		lImgStr = '''
			<a href="%s" target="_blank">
				<img id="%s" src="%s" width="%d" height="%d" border="0" style="%s" alt="" />
			</a>
		''' % (linkTo, imgId, imgSrc, cObj[0], cObj[1], imgStyles)
		return lImgStr

	# close table row element + TD column span
	def closeColumn(self):
		ccStr = '</td>\n'
		return ccStr

	# close table row
	def closeRow(self):
		crStr = '</tr>\n'
		return crStr

	# close out table and body elements
	def closeBody(self):
		bstr = '''
					</table>
				</body>
			</html>
			'''
		return bstr

	# ---------------------------------------------------------------------------
	# 	USER FUNCTIONS
	# ---------------------------------------------------------------------------
	# close out table and body elements
	def getContents(self):
		# save html email file
		if self.exportFile:
			self.exportHtml(self.emailHtml)
		else:
			print(self.emailHtml)
