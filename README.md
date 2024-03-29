# PYTHON-FLASK-REST-API-EXAMPLE

## DESCRIPTION
- Heroku free tier is used for deployment platform.
  
- MongoDB free tier is used for database connection.

- git & github is used for versioning

- Coded with Python

- tested with Postman and Jmeter


## DEPENDENCIES
```
atomicwrites==1.4.0
attrs==20.3.0
certifi==2020.12.5
chardet==4.0.0
click==7.1.2
colorama==0.4.4
dnspython==2.1.0
Flask==1.1.2
gunicorn==20.0.4
idna==2.10
iniconfig==1.1.1
itsdangerous==1.1.0
Jinja2==2.11.2
MarkupSafe==1.1.1
names==0.3.0
packaging==20.8
pluggy==0.13.1
py==1.10.0
pymongo==3.11.2
pyparsing==2.4.7
pytest==6.2.1
requests==2.25.1
toml==0.10.2
urllib3==1.26.2
Werkzeug==1.0.1
```

## python --version
```
python-3.8.6
```

## how to install dependencies?
```
>> pip install -r requirements.txt
```

## File Structure
```
│   app.py
│   Procfile
│   README.md
│   requirements.txt
│   runtime.txt
│
├───tests
│       test.py       
```

# SAMPLE USAGE
## listing the leaderboard [GET method]`https://host_url_here/leaderboard`
`sample response`
  ```json
    [
        {
            "country": "tr",
            "display_name": "Chasity_Deibel",
            "points": 999172,
            "rank": 1
        },
        {
            "country": "it",
            "display_name": "Frederick_Marquardt",
            "points": 999157,
            "rank": 2
        },
        {
            "country": "en",
            "display_name": "Walter_Rviz",
            "points": 999149,
            "rank": 3
        },
        {
            "country": "tr",
            "display_name": "Derrick_Switzer",
            "points": 998226,
            "rank": 4
        },
        {
            "country": "en",
            "display_name": "Beth_Acosta",
            "points": 997918,
            "rank": 5
        },
        {
            "country": "de",
            "display_name": "Jane_Baez",
            "points": 997908,
            "rank": 6
        },
        {
            "country": "es",
            "display_name": "Noel_Knapp",
            "points": 997488,
            "rank": 7
        },
        {
            "country": "es",
            "display_name": "Doris_Bergen",
            "points": 997331,
            "rank": 8
        },
        {
            "country": "de",
            "display_name": "Judith_Frank",
            "points": 996947,
            "rank": 9
        },
        {
            "country": "it",
            "display_name": "Randy_Amick",
            "points": 996876,
            "rank": 10
        }
    ]
```
        
## listing the leaderboard with country ISO code [GET method] `https://host_url_here/leaderboard/tr`
`sample response`
  ```json
[
    {
        "country": "tr",
        "display_name": "samet_kamgul",
        "points": 1023300,
        "rank": 1
    },
    {
        "country": "tr",
        "display_name": "Chasity_Deibel",
        "points": 999172,
        "rank": 3
    },
    {
        "country": "tr",
        "display_name": "Derrick_Switzer",
        "points": 998226,
        "rank": 7
    },
    {
        "country": "tr",
        "display_name": "Victoria_Rankin",
        "points": 995932,
        "rank": 16
    },
    {
        "country": "tr",
        "display_name": "Peter_Swihart",
        "points": 994600,
        "rank": 20
    },
    {
        "country": "tr",
        "display_name": "Salvador_Hunter",
        "points": 990471,
        "rank": 31
    },
    {
        "country": "tr",
        "display_name": "Thomas_Young",
        "points": 988804,
        "rank": 45
    },
    {
        "country": "tr",
        "display_name": "Claudia_Czarnecki",
        "points": 987721,
        "rank": 48
    },
    {
        "country": "tr",
        "display_name": "Carol_Donnelly",
        "points": 986183,
        "rank": 52
    },
    {
        "country": "tr",
        "display_name": "Erica_Lunstrum",
        "points": 985526,
        "rank": 54
    }
]
 ```

## get profile of a user with guid(wrong guid) [GET method] `https://host_url_here/4894b72a-8507-4d67-bf88-bfafa356814b`
  
`sample response`
```json
{
    "message": "user doesn't exists"
}
```
## get profile of a user with guid(correct guid) [GET method] `https://host_url_here/6d9d4bf3-dcfd-4137-9309-ae3cbc90b0c8`

`sample response`
```json
{
    "country": "it",
    "display_name": "June_Middleton",
    "points": 4892,
    "rank": 2989
}
```

## creating a user profile [POST method] `https://host_url_here/user/create`
`request json body`
```json
{
    "user_id" : "15453e8c-3db5-4dfb-9173-a11016c9b7d1111",
    "display_name" : "samet1111",
    "points" : 0,
    "country" : "tr"
}
```

`response json if user exists`
```json
{
    "message": "user exists",
    "success": false
}
```

`response json if user doesn't exist`
```json
{
    "country": "tr",
    "display_name": "samet_kamgul",
    "points": 1023300,
    "rank": 1
}
```
## submitting a user score [POST method] `https://host_url_here/score/submit`

`request body`
```json
{
    "score_worth" : 111,
    "user_id" : "4894b72a-8507-4d67-bf88-bfafa356814b"
}
```

`sample response if user doesn't exist`
```json
{
    "message": "user is not found"
}
```

`sample response if user exists`
```json
{
    "display_name": "June_Middleton",
    "points": 5003,
    "rank": 2988,
    "user_id": "6d9d4bf3-dcfd-4137-9309-ae3cbc90b0c8"
}
```

## requesting a invalid endpoint `https://host_url_here/xxx/yyy/15453e8c-3db5-4dfb-9173-a11016c9b7d9999`
`sample response`
````json
{
    "message": "The resource cannot be found"
}
````

## creating fake fields in the database endpoint [GET method] `https://host_url_here/createfields`
`Note: it creates 1000 fake data at once. and keep in mind it's response time is ~24 seconds.`

`sample response`
````json
{
    "message": "fake resources has been inserted"
}
````
