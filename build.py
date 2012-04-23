from xml.etree.ElementTree import ElementTree
import xml.etree.ElementTree as ET
import os

doctype = '<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">\n'

#links = [['index', 'Home'], ['Products', 'Products'], ['Photos', 'Photos'], ['About', 'About Us'], ['Contact', 'Contact Us'], ['ForSale', 'For Sale']]
links = [['index', 'Home'], ['Products', 'Products'], ['Photos', 'Photos'], ['Videos', 'Videos'], ['Contact', 'Contact Us']]
pageTemplateFile = 'page_template.html'
photoTemplateFile = 'photo_template.html'
topDestDir = 'dncompositemasts.com_new'+os.sep
photoDestDir = topDestDir+'images'+os.sep

class CommentedTreeBuilder ( ET.XMLTreeBuilder ):
    def __init__ ( self, html = 0, target = None ):
        ET.XMLTreeBuilder.__init__( self, html, target )
        self._parser.CommentHandler = self.handle_comment
    
    def handle_comment ( self, data ):
        self._target.start( ET.Comment, {} )
        self._target.data( data )
        self._target.end( ET.Comment )

def findElemWithId(parentElem, tag, id):
	for elem in list(parentElem):
		if elem.tag == tag:
			idAttrib = elem.get('id')
			if idAttrib != None:
				if idAttrib == id:
					return elem
		candidateElem = findElemWithId(elem, tag, id)
		if candidateElem != None:
			return candidateElem
	return None

def findSidebar(parentElem):
	for elem in list(parentElem):
		if elem.tag == 'div':
			idAttrib = elem.get('id')
			if idAttrib != None:
				if idAttrib == 'sidebarLinks':
					return elem
		candidateElem = findSidebar(elem)
		if candidateElem != None:
			return candidateElem
	return None

def insertSidebarLinks(templateRoot, thisFile, links):
	sidebarElem = findSidebar(templateRoot)
	
	reversedLinks = list(links)
	reversedLinks.reverse()
	
	for linkTuple in reversedLinks:
		linkText = linkTuple[1]
		file = linkTuple[0]
		linkDest = file+'.html'
	
		if file == thisFile:
			linkTemplateTree = ElementTree()
			linkTemplateRoot = linkTemplateTree.parse('sidebarNoLink_template.f', parser = CommentedTreeBuilder())
			pElem = linkTemplateRoot.find('p')
			spanElem = pElem.find('span')
			spanElem.text=linkText
		else:
			linkTemplateTree = ElementTree()
			linkTemplateRoot = linkTemplateTree.parse('sidebarLink_template.f', parser = CommentedTreeBuilder())
			pElem = linkTemplateRoot.find('p')
			aElem = pElem.find('a')
			aElem.text=linkText
			aElem.set('href', linkDest)
		
		sidebarElem.insert(0, pElem)

print "Creating pages:"
for linkTuple in links:
	srcFileRoot = linkTuple[0]
	
	srcFile = srcFileRoot+'.f'
	destFile = topDestDir+srcFileRoot+'.html' 
	print "   "+srcFile+' + '+pageTemplateFile+' => '+destFile
	
	try:
		os.remove(destFile)
	except WindowsError as (errno, strerror):
		#print "WindowsError({0}): {1}".format(errno, strerror)
        #print "Note: No "+destFile+" to remove."
		pass
    
	templateTree = ElementTree()
	templateRoot = templateTree.parse(pageTemplateFile, parser = CommentedTreeBuilder())
	
	insertSidebarLinks(templateRoot, srcFileRoot, links)
	
	srcTree = ElementTree()
	srcRoot = srcTree.parse(srcFile, parser = CommentedTreeBuilder())
    
	
	contentDiv = findElemWithId(templateRoot, 'div', 'ContentDiv')
	if contentDiv == None:
		print "ERROR: No Content Div found!"
		exit()
	#print "contentDiv.text='"+contentDiv.text+"'"
	#print "contentDiv.tail='"+contentDiv.tail+"'"
	
	for elem in srcRoot.getchildren():
		contentDiv.append(elem)
	
	if srcFileRoot == 'index':
		metaTree = ElementTree()
		metaRoot = metaTree.parse('meta.f', parser = CommentedTreeBuilder())
		headElem = templateRoot.find('head')
		for elem in metaRoot.getchildren():
			headElem.append(elem)
	
	dest = open(destFile, 'w')
	dest.write(doctype)
	templateTree.write(dest)
	dest.close()

print "Creating photos:"
photosTree = ElementTree()
photosRoot = templateTree.parse("photos.xml")
for photoElem in photosRoot:
    srcFileRoot = photoElem.find('name').text
    srcFile = srcFileRoot+'.jpg'
    destFile = photoDestDir+srcFileRoot+'.html'
    print "   "+srcFile+' + '+photoDestDir+' => '+destFile
    
    height = photoElem.find('height').text
    width = photoElem.find('width').text
        
    try:
        os.remove(destFile)
    except WindowsError as (errno, strerror):
        #print "WindowsError({0}): {1}".format(errno, strerror)
        #print "Note: No "+destFile+" to remove."
        pass
    
    templateTree = ElementTree()
    templateRoot = templateTree.parse(photoTemplateFile, parser = CommentedTreeBuilder())
    
    photoPageElem = findElemWithId(templateRoot, 'div', 'photoDiv')
    style = 'height:'+str(int(height)+50)+'px; width:'+str(int(width)+50)+'px;'
    photoPageElem.set('style', style)
        
    imgElem = findElemWithId(templateRoot, 'img', 'imageTag')
    imgElem.set('src', srcFileRoot+'.jpg')
    imgElem.set('height', height)
    imgElem.set('width', width)
    
    creditSpanElem = findElemWithId(templateRoot, 'span', 'creditSpan')
    creditHrefElem = creditSpanElem.find('a')
    photographerTree = ElementTree()
    photographerRoot = photographerTree.parse(photoElem.find('photographer').text+'.xml')
    creditHrefElem.text = 'Photo: '+photographerRoot.find('name').text
    creditHrefElem.set('href', photographerRoot.find('url').text)
    
    captionDivElem = findElemWithId(templateRoot, 'div', 'caption')
    captionElem = photoElem.find('caption')
    captionDivElem.text = captionElem.text
    captionDivElem.extend(list(captionElem))
    captionDivElem.set('style', 'width:'+width+'px;')#    
    dest = open(destFile, 'w')
    dest.write(doctype)
    templateTree.write(dest)
    dest.close()

print "Done!"