# eventmaster
Here is REST API for simple application eventmaster. 
Its supports authorization by email, authentication by token, creating evens with remind, events statistic by day, 
by month and holidays statistic for users country by month.

You can clone the project and run it using SQLite or 
in Docker using PostgreSQL (needs adding docker-compose.yml and django_docker_file).
In manage.py you should set DJANGO_SETTINGS_MODULE with settings.py you would like use. 

### To test project site:

you can visit endpoins or put the code below into the jupyternotebook.

```Python
    from requests import get, post
    
    # registration
    # country examles: belarus, bonaire-st-eustatius-saba, central-african-republic, sao-tome-and-principe, ...
    # "offset":"3" or "0" (country and offset fiels do not required)
    data = {
        "email":"...@gmail.com", 
        "username":"...", 
        "password":"...", 
        "first_name":"...",
        "last_name":"...", 
        "country":"poland",
        "offset":"3"
    }
    response = get("https://blackdesert.ololosha.xyz/comrades/registration/",)
    print(response) # <Response [405]>
    response = post("https://blackdesert.ololosha.xyz/comrades/registration/", data=data)
    print(response) # <Response [201]>
    response.json()

    # activation
    # check email to get link
    activation_link = "https://blackdesert.ololosha.xyz/comrades/activation/xxxxxx-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    webtoken = "xxxxxx-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    response = get(activation_link, )
    print(response) # <Response [405]>
    # login: enter email or username
    data = {
        "login": "...@gmail.com"
    }
    response = post(f"https://blackdesert.ololosha.xyz/comrades/activation/{webtoken}", data=data)
    print(response) # <Response [202]>

    # login
    response = get("https://blackdesert.ololosha.xyz/comrades/login/",)
    print(response) # <Response [405]>
    # login: enter email or username to get token by email
    data = {
        'login': "...@gmail.com",
        'password': "...",
    }
    response = post("https://blackdesert.ololosha.xyz/comrades/login/", data=data)
    print(response) # <Response [200]>

    # test create event
    token = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    headers={"Authorization": "Token xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"}
    response = get("https://blackdesert.ololosha.xyz/events/list_create_event/", headers=headers)
    print(response) # <Response [200]>
    #         "0", 'Do not remind'
    #         "3600", '1 hour'
    #         "7200", '2 hours'
    #         "14400", '4 hours'
    #         "86400", '1 day'
    #         "604800", '1 week'
    data = {
        "event":"test ....",
        "date_event":"2021-02-16",
        "start_time":"20:59",
        "end_time":"23:30",
        "remind": "3600"
    }
    response = post("https://blackdesert.ololosha.xyz/events/list_create_event/", headers=headers, data=data)
    print(response) # <Response [201]>
    response.json()

    #statistic by user
    headers={"Authorization": "Token xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"}
    response = get("https://blackdesert.ololosha.xyz/events/statistic_by_user/", headers=headers)
    print(response) # <Response [200]>
    response.json()

    # statistic by day
    data = {
        "date_event":"2021-08-08",
    }
    headers={"Authorization": "Token xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"}
    response = get("https://blackdesert.ololosha.xyz/events/statistic_day/", headers=headers, data=data)
    print(response) # <Response [200]>
    response.json()

    # statistic by month
    data = {
        "month":"2021-02",
    }
    headers={"Authorization": "Token xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"}
    response = get("https://blackdesert.ololosha.xyz/events/statistic_month/", headers=headers, data=data)
    print(response) # <Response [200]>
    response.json()

    # holidays by month
    data = {
        "month":"2021-05",
    }
    headers={"Authorization": "Token 7912ede2bfa2066ddbc74e6a25b672160f111db7"}
    response = get("https://blackdesert.ololosha.xyz/events/holidays_month/", headers=headers, data=data)
    response.json()
```

