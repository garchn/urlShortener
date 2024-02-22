**Simple Python URL Shortener**

Instructions: To run the server, simply run main.py. Send requests to the following 3 endpoints below:


**[POST] /encode**
Enter a URL, receive a short URL string as a response. Short URL will be a 7 character long string in base62.

Sample request body:
{
    "longUrl": "https://en.wikipedia.org/wiki/Beaver"
}


**[GET] /decode**
Enter a short URL string. If short URL is valid, receive a long URL string as a response, and browser will navigate the URL.

Sample request body:
{
    "shortUrl": "gsKAEQe"
}


**[GET] /stats**
Enter a short URL string. If short URL is valid, receive a response with the number of total visits, visits in the past week, and visits in the past day of the short URL.

Sample request body:
{
    "shortUrl": "gsKAEQe"
}
