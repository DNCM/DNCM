from xml.etree.ElementTree import ElementTree
import xml.etree.ElementTree as ET
import os

files = ['index', 'About', 'Products', 'Photos', 'Contact', 'ForSale']
templateFile = 'page_template.html'
destDir = 'www'+os.sep


class CommentedTreeBuilder ( ET.XMLTreeBuilder ):
    def __init__ ( self, html = 0, target = None ):
        ET.XMLTreeBuilder.__init__( self, html, target )
        self._parser.CommentHandler = self.handle_comment
    
    def handle_comment ( self, data ):
        self._target.start( ET.Comment, {} )
        self._target.data( data )
        self._target.end( ET.Comment )

def findContentDiv(parentElem):
	for elem in list(parentElem):
		if elem.tag == 'div':
			idAttrib = elem.get('id')
			if idAttrib != None:
				if idAttrib == 'ContentDiv':
					return elem
		candidateElem = findContentDiv(elem)
		if candidateElem != None:
			return candidateElem
	return None

for srcFileRoot in files:
	srcFile = srcFileRoot+'.f'
	destFile = destDir+srcFileRoot+'.html' 
	print srcFile+' + '+templateFile+' => '+destFile
	
	try:
		os.remove(destFile)
	except WindowsError as (errno, strerror):
		#print "WindowsError({0}): {1}".format(errno, strerror)
		#print "Note: No "+destFile+" to remove."
		pass
	
	templateTree = ElementTree()
	templateRoot = templateTree.parse("page_template.html", parser = CommentedTreeBuilder())
	
	srcTree = ElementTree()
	srcRoot = srcTree.parse(srcFile, parser = CommentedTreeBuilder())
	
	contentDiv = findContentDiv(templateRoot)
	if contentDiv == None:
		print "ERROR: No Content Div found!"
		exit()
	#print "contentDiv.text='"+contentDiv.text+"'"
	#print "contentDiv.tail='"+contentDiv.tail+"'"
	
	for elem in srcRoot.getchildren():
		print elem, elem.tag, elem.text
		contentDiv.append(elem)
	
	dest = open(destFile, 'w')
	dest.write('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">\n')
	templateTree.write(dest)
	dest.close()

print "Done!"