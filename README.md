# Twistter

Twitter like application made with python Twisted



#### Dependencies

* Python 2.7
* Mysql 5.6
* Python modules: twisted klein sqlalchemy MySQL-python requests pytest

To install python modules run:
```
pip install twisted klein sqlalchemy MySQL-python requests pytest
```


#### Setup:

You need to prepare database. Import schema from `db_schema.sql`


#### Running app:
```
python main.py
```

#### Runnin tests:
* Start the app
* Run `py.test`


#### API doc:

* `POST` `/v1/messages`
Posts a message by user
Request data:
```json
{
  "user_id": "2581c0bc-6693-4e69-bbcc-b15a6cdea04e", // id of a user
  "message": "Message text, can have #tags , limited to 140 characters"
}
```

Response data:
```json
{
  "status": "ok",
  "id": "fb780bc2-fdb5-43b5-9502-f59e4cb88b0c" //id of saved message
}
```

* `GET` `/v1/messages/tags`
Retrieves messages with specific tag
Request data:
```json
{
  "tag_name": "sometagname",
  "start_time": "", // returns messages older than this date, optional
  "offset": 10,     // offset for pagination, default 0, optional
  "limit": 100      // limit for pagination, default 20, optional
}
```

Response data:
```json
[
    {
        "message_text": "Message text that have #tag",
        "user_name": "User name",
        "message_time": {
            "$date": 1461510941609
        }
    },
    ...
]
```