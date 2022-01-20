## URL Shortener


URL Shortener made with Python Flask, MongoDB for storage and Docker for deployment.

The application has 2 methods:
    
    1.POST: Shortening a URL -> returns the shortened URL
    2.GET: Looking up a URL -> returns the original URL

To run application, clone the repository and execute following commands

1. `docker compose build`
2. `docker compose up`

Once the application is up and running,to test it execute:
    
    1. To Shorten a URL:
    curl --location --request POST 'http://127.0.0.1:5000/api/v1/shorten/' \
         --form 'link="https://en.wikipedia.org/wiki/Reality#Perception"'

    It will return a response like:
        {
          "url": "https://tinyurl.com/ykkld2zk"
        }
    
    Please note in the shortened URL: "https://tinyurl.com/ykkld2zk" ,this "ykkld2zk" is the url_id(indentifier)

    2. To lookup original URL from shortened URL's identifier:
    curl --location --request GET 'http://localhost:5000/api/v1/lookup/<url_id>'

    With respect to above eg. the curl request for looking up a shortened URL would look like:
    curl --location --request GET 'http://localhost:5000/api/v1/lookup/ykkld2zk'
    It will return a response like:
        {
          "lookup": {
            "added": "20-01-2022- 11:25:10",
            "id": "61e946969fdb0451be7fe55a",
            "added": "23-08-2012- 13:44:23",
            "link": "https://en.wikipedia.org/wiki/Reality#Perception",
            "url_id": "y3uaxp32"
          }
        }

