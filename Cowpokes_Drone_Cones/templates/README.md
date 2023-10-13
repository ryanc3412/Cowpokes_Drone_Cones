
NOTES ON DJANGO TEMPLATES

	Django templates work essentially as html files. However, usual html embedded elements such as:
		. links to other html files
		. images 
		. css file

		are managed by other elements of the Django project. 

	
	Django templates should follow general template:

	---------------------------------------------------------
	<!DOCTYPE html>
	<html lang="en">
		<head>
			<meta charset="utf-8"/>
			<title>title_text</title>
		</head>
		<body>

			--> Contents of the page goes here <--


		</body>
	</html>
	---------------------------------------------------------


HTML REVIEW

	    <a/>  -->  link tag
	 <body/>  -->  body tag
	  <nav/>  -->  navigation bar tag
	 <link/>  -->  connector to a css file, ex: 
			<link rel="stylesheet type="text/css" href="{file name}"/>

	<aside/>  -->  make a side tab



CSS REVIEW

	css file structure: 

	{element:specifier} {
		color: {choice};
		background-color: {choice};
		text-align: {choice};
		font-family: {choice};
		font-size: {choice};	

	}


TEMPLATE NAVIGATION ORDER
	. Landing page --> Login page
	. Login page --> (create account page / home page) --> (home page / admin page)
	. Order page --> Confirmation page
	. drones page --> register drones page --> drones page

	
	       Home Page Header: Home, Order, Drones, Login/Account --
	    Account Page Header: Home, Order, Drones --
	      Login Page Header: Home, Order, Drones --
     Create Account Page Header: Home, Order, Drones -- 
 	      Admin Page Header: Home, Order, Admin, Account --
 	      Order Page Header: Home, Order, Drones, Account --
       Confirmation Page Header: Home, Order, Drones, Account --
             Drones Page Header: Home, Order, Drones, Account
Drones Registration Page Header: Home, Order, Drones, Account







