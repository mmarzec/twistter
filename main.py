import config
from helper import rest_api_json, get_json_arg
from error import Unauthorized

import uuid
from datetime import datetime
from klein import run, route
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from twisted.python import log


db_path = 'mysql://{}:{}@{}/{}'.format(config.db_user, config.db_pass,
    config.db_host, config.db_name)
engine = create_engine(db_path, execution_options={'autocommit': True})
db_connection = engine.connect()


@route('/v1/messages', methods=['POST'])
@rest_api_json
def messages(json):
    user_id = get_json_arg(json, 'user_id')
    message = get_json_arg(json, 'message')

    log.msg('Inserting message for user '+user_id)

    # check for message length
    if len(message) > config.message_size_limit:
        raise MethodNotAllowed('Message size bigger than limit '+config.message_size_limit)

    # extract tags
    tags = {tag.strip("#") for tag in message.split() if tag.startswith("#")}
    log.msg('Found tags: '+str(tags))


    with db_connection.begin() as db_trans:

        # check if user exist
        if db_connection.execute(text('SELECT id FROM users WHERE id = :id'),id=user_id).fetchone() is None:
            raise Unauthorized('User not authorized')

        # insert message
        message_id = uuid.uuid4()
        db_connection.execute(text('INSERT INTO messages (id, user_id, message_text, message_time) '\
            'VALUES (:message_id, :user_id, :message, CURRENT_TIMESTAMP(6))'),
            message_id=str(message_id), user_id=user_id, message=message)

        # insert tags
        for tag in tags:
            tag_id = uuid.uuid4()
            db_connection.execute(text('INSERT INTO tags (id, tag_name) '\
                'VALUES (:tag_id, :tag_name)'),
                tag_id=str(tag_id), tag_name=tag)

            db_connection.execute(text('INSERT INTO message_tag (message_id, tag_id) '\
                'VALUES (:message_id, :tag_id)'),
                message_id=str(message_id), tag_id=str(tag_id))


    return { 'status': 'ok', 'id': str(message_id) }


@route('/v1/messages/tags', methods=['GET'])
@rest_api_json
def tag(json):
    tag_name = get_json_arg(json, 'tag_name')

    if 'start_time' in json:
        start_time = get_json_arg(json, 'start_time')
    else:
        start_time = str(datetime.today())

    if 'offset' in json:
        offset = get_json_arg(json, 'offset')
    else:
        offset = 0

    if 'limit' in json:
        limit = get_json_arg(json, 'limit')
    else:
        limit = 20

    log.msg(start_time)
    log.msg(offset)
    log.msg(limit)

    result = db_connection.execute(text('SELECT users.user_name, messages.message_text, messages.message_time FROM messages '\
        'INNER JOIN message_tag ON message_tag.message_id = messages.id '\
        'INNER JOIN tags ON message_tag.tag_id = tags.id '\
        'INNER JOIN users ON messages.user_id = users.id '\
        'WHERE tags.tag_name = :tag_name '\
        'AND messages.message_time < :start_time '\
        'ORDER BY messages.message_time DESC '\
        'LIMIT :limit OFFSET :offset'),
        tag_name=tag_name, start_time=start_time, limit=limit, offset=offset).fetchall()

    log.msg(result)

    return [dict(r) for r in result]



if __name__ == '__main__':
    run(config.bind_address, config.bind_port)
