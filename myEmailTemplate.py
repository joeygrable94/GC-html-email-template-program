#	
#	1) import EmailTemplate Class
#	
from EmailTemplateProgram.EmailTemplate import EmailTemplate



#	
#	2) generate custom email template
#	
template = EmailTemplate(
	# CONTENT INFORMATION
	extImgUrl='www.getcommunityinc.com/mycommunityapps/eblasts/wr/wr_sept_2020/',
	contentPath='./EmailContent/',
	docTitle='Whitney Ranch Prominence | A new-home community in Rocklin, CA',
	docDesc='Are you ready to live boldly? Prominence by JMC Homes is now open! Each spacious floorplan is designed to add a flair of luxury into every space.',
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
	saveAs='2020-09-wr-eblast-prominence-go.html',
	showMsgs=False,
	minifyHtmlOut=False,
	exportFile=True
)



#	
#	3) Show or Export Generated Html Email
#	
template.getContents()


