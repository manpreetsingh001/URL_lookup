#URL_lookup

Write a small web service, using the technology of your choice, that responds to GET requests where the caller passes in a URL and the service responds with some information about that URL. 
 
The GET requests would look like this:
 
**GET /urlinfo/1/{hostname_and_port}/{original_path_and_query_string}**

- App is developed using python ,Web framework Flask and mysql  as an backend database
- URL_lookup.py  lookup for malicious URL in database and alert user accordingly
- database_update.py populate database with data from malicious_url.txt

**How to use:** 
   
  *Requirements*
   - mysql.connector for python
   - flask for python
   - Virtual env would be preferable for running app
   - mysql server
   - python

  
   *How to run*:
   - Clone the directory and move to directory
   - python database_update.py -This will going to populate the data
   - Then run python URL_lookup.py -This will going to start local web server
   - From your work station run **curl  http://127.0.0.1:5000/urlinfo/1/<<http://domain.com>>
      some of the acceptable formats are:
      
         *http://www.google.com*         #Valid
         
         *http://google.com*             #Invalid
          
         *www.google*                    #Invalid 
         
         *http://www.google.com/images*  #Valid
   
  *How to run unit test*:
   - move to test directory and make sure python mock and flask libraries are installed
   - Run it using python

   - [X] Version control plan:Going to use Tags for versoning and topic branches for adding features
   - [X] Going to write unittest for it using python mock library
   - [] Dockerize  app to remove dependencies 
   - [] Bonus Tasks    

**Security notes**
  -  Regex check is done on the URL input to prevent various injections and to also save time in querying the database if the URL is not a valid URL
  - Credentials are not hardcoded in the source code but put in a config file stored in a separate folder ( access to which should be protected )
   
**Change Log**

  - 0.1.0
  
  *Initial release version*

**Author**

 Urllookup service  created by Manpreet Singh





