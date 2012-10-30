files = ['index', 'About', 'Products', 'Photos', 'Contact', 'ForSale']

import os

templateFile = 'page_template.html'
destDir = 'www'+os.sep

for srcFileRoot in files:
	srcFile = srcFileRoot+'.f'
	destFile = destDir+srcFileRoot+'.html' 
	print srcFile+' + '+templateFile+' => '+destFile
	
	os.remove(destFile)

	template = open(templateFile, 'r')
	src = open(srcFile, 'r')
	dest = open(destFile, 'w')
	for tline in template:
		dest.write(tline)
		if '      <!-- Main Block Content Starts Here -->\n' == tline:
			print "   Inserting ..."
			for sline in src:
				dest.write('        '+sline)
			dest.write('\n')
	template.close()
	src.close()
	dest.close()
print "Done!"