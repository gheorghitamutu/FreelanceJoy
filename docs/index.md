# Welcome
This is the documentation page for Cloud Computing final project.

# Getting started
Clone the project's repository and create a virtual python environment with all the packages from requirements.txt.

# Project layout
    docs/                                   # The mkdocs docs files.
        index.md                            # The documentation homepage.
    site/                                   # The mkdocs auto-generated site.
        ...                                 # The mkdocs site's files and folders.
    web/                                    # Flask website of the project.
        static/                             # Site's static files (.css, images, .js).
            css/                            # Site's .css files.
                stylesheet.css              # Custom css for project .html pages.
            images/                         # Site's images.
                favicon.ico                 # Project site's favicon.
            js/                             # Custom made .js scripts.     
                scripts.js                  # Authentication handling script.       
        templates/                          # Project's Flask site's files.
            public/                         # Site's structure accessible to users.
                dashboard.html              # Landing page for authenticated users.
                landing.html                # Landing page for guests/login page.
                index.html                  # Base layout for pages.
        uploads/                            # Configurations files (.json) uploaded by user.
    .cloudignore                            # Ignore file for Google Cloud build.
    .gitignore                              # Ignore file for repository.
    app.yaml                                # Configuration file for container deployment on Google Cloud.
    cloud_build.yaml                        # Configuration file for Google Cloud Build.
    main.py                                 # Flask initialization and routes (the Flask app class).
    mkdocs.yml                              # The configuration file.
    piece.py                                # Piece class & default pieces.
    README.md                               # Project's Readme file.
    requirements.txt                        # Project's python dependencies.

# Project Guidelines
    Two components:
    	1. Posting announcements with deadline (number of days, months), tags and possible attachments
    		- every freelancer bids for any project 
    		- the client contacts the freelancer through the email posted on the website (may add some other form of contact)
    		- the freelancer adds a project version for each iteration established between him and the employer
    		- an iteration has a fee due to file storage
    		
    	2. Putting projects up for sale
    		- a project can be put up for sale on the platform by any account type (you can sell or bid for a project)
    		- each party receives a percentage of the price (40% employee, 60% employer) - a passive income would be generated
    		- the project can be sold once or several times (from the employee point of view)
        
    All files that are uploaded are scanned with VirusTotal.
    
    APIs: 
    	1. Ad management (addition, deletion, etc.).
    	2. Project management :
    	    - file storage for each project version iteration by the freelancer
    		- helper files storage (diagrams, plans, etc)
    	3. Parties involved management:
    		- used for profile creation
    	4. The managent of the projects that are up for sale.

