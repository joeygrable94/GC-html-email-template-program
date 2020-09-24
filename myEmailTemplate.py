#	
#	1) import EmailTemplate Class
#	
from EmailTemplateProgram.EmailTemplate import EmailTemplate



#	
#	2) generate custom email template
#	
template = EmailTemplate(
	# CONTENT INFORMATION
	extImgUrl='www.getcommunityinc.com/mycommunityapps/eblasts/millville/sept_retiree_2020/',
	contentPath='./EmailContent/',
	docTitle='Millville By The Sea | September Newsletter 2020',
	docDesc='4 miles from Bethany Beach, DE, Millville by the Sea is a new home master-planned community with amenities including pools, lakes, parks, trails and more.',
	# GENERAL STYLES
	width=600,
	tableClass='gc-table--email',
	bodyStyles='''
		font-family: 'Helvetica', 'Arial', sans-serif;
		font-weight: 100; font-size: 16px;
		line-height: 32px; background-color: #ffffff;
	''',
	divStyleDefault='''
		font-size: 16px;
		line-height: 1.5em;
		font-weight: lighter;
		font-family: Helvetica, Arial, sans-serif;
		margin: 20px 24px 20px 24px;
		color: #000000;
		text-align: center;
	''',
	imgStyleDefault='''
		display: block;
	''',
	# EXPORT OPTIONS
	saveAs='2020-09-mbts-eblast-retiree.html',
	showMsgs=False,
	minifyHtmlOut=False,
	exportFile=True
)



#	
#	3) Show or Export Generated Html Email
#	
template.getContents()


