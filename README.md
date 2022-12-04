This web application is based on a compilation of hate crimes in the United States reported to the FBI during the year 2013.
Information on the different types of reported hate crimes can be found in the Crime Ranking tab, where states are ordered from the highest
crimes reported per capita to lowest. On the Political Affiliation tab we subset each state by their political affiliation according to data
collected from the 2012 political election and compute summary statistics of crimes reported.

To run the application perform the following steps:

1. From /crimes folder, set FLASK_APP environment variable: $export FLASK_APP='main.py'

2. From /crimes folder, execute the application by running the following command:
  - $python3 -m flask  run --host=0.0.0.0 --port=500X (where 500X is your assigned port number)

3. Open a browser (e.g. Chrome) and type: localhost:500X

4. If the application is not opened in your browser, create a tunnel to Flask. For so:
   - Being Loged out of Flask server, execute the line: ssh -4 -N -L 500X:localhost:500x user@flask01.network.ncf.edu

5. Open again your browser and enjoy the application!

Note: You might be asked to install additional packages when trying to access some features from the web application


This application was created by Paul Cummins, Marina Sanchez-Millan, and Conor Welch for the final project of the 2022 Databases class of NCF's Master of Science in Data Science program.
