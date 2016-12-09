CS4920 Management and Ethics

Supervisor: 	Bruno Gaeta

Team members: 	Pu Lin(Edward) 	 Yixuan Li(Egbert)	Yuan Ren(Martin)
					John Wang		Qianrui Zhao(Cherry)


***************************************************

Web Application Structure

Home page ->

	•	Signin Signup ->
		o	Our system will send user an email after sign up. User can click the link provided in that email to complete their registration. 
		o	User can retrieve their password by email address.

	•	User profile ->
		o	Account information page
			♣	User can change username, avatar and current location in account information page, and daily sign up in this page.
			♣	User can view nearby people in this page, group with others to activate themselves.

		o	Personal information page
			♣	User can adjust their personal information here.

		o	Fitness recommendation page
			♣	Recommendation is based on machine learning algorithm, will recommend the videos based on similarity of users’ personal information.

		o	User account security page
			♣	User can change password here.

		o	Logout

	•	Chat channel ->
		o	User can enter chat channel, and send message in the Chat Channel, and also can click the user’s photo to link to user’s profile, then they can friend each other.

	•	Food main page ->
		o	Food main page allows user view nutrition detail of a food under a particular food group.

	•	Fitness main page ->
		o	Fitness page offers user to select particular fitness videos which are grouped by body parts. User can get professional training based on those videos. 

	•	Search ->
		o	User can enter any word in search input box, and the search results would include foods, fitness videos, and user name. 
	
	(Also from the drop-down menu, user can quickly enter the Fitness Category Page, Food List Page and Home Page. If user currently login, then he/she also can quickly)



***************************************************

Technical details

1.	Django based project, MVP model.
2.	Basic interface - Bootstrap.
3.	Machine Learning - scikit-learn, pandas
4.	Database - Mysql
5.	User Location - Google Maps APIs
6.	Food database - USDA Food Composition Databases API, handle Json Data
7.	Communication - Json, Ajax
8.	Sending Email - Security Token, SMTP provided by Gmail



***************************************************

Prerequisites

1.	Python == 3.5
2.	Django==1.11.dev20160923021937
3.	MySQL==5.7.15
4.	scikit-learn=0.18.0
5.	pandas=0.19.0


