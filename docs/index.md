# Welcome
This is the documentation page for Artificial Intelligence Final Project.

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
