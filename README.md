**Simple Python URL Shortener**
--------------------------------

**URL Persistence** - data is stored in SqliteDict DB, which will persist short URL to long URL mapping between sessions.
**Capacity** - Short URL is a 7 character string in base62, so maximum capacity would be 62^7 ~= 3.5 trillion URLs. This should handle millions of URLs with minimal hash collisions easily.
**Uniqueness** - Encode endpoint will return two different short URLs if hit twice consecutively. These URLs are randomized so the probability of being discovered is low. Each short URL is also unique and will ever be generated once.

Instructions: To run the server, simply run main.py. Send requests to the port address followed with one of the 3 endpoints below:

**[POST] /encode** <br />
Enter a URL, receive a short URL string as a response. Short URL will be a 7 character long string in base62.

Sample request body: <br />
``{
    "longUrl": "https://en.wikipedia.org/wiki/Beaver"
}``


**[GET] /decode** <br />
Enter a short URL string. If short URL is valid, receive a long URL string as a response, and browser will navigate the URL.

Sample request body: <br />
``{
    "shortUrl": "gsKAEQe"
}``


**[GET] /stats** <br />
Enter a short URL string. If short URL is valid, receive a response with the number of total visits, visits in the past week, and visits in the past day of the short URL.

Sample request body: <br />
``{
    "shortUrl": "gsKAEQe"
}``
