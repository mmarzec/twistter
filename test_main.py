import json
import requests
from sqlalchemy import create_engine
from sqlalchemy.sql import text

base_url = 'http://127.0.0.1:6060/'
test_user_id_1 = 'ba8bf220-62bc-472c-94a1-418503e88708'
test_user_id_2 = '9f3b9431-55c7-4ad6-860a-bc39341ea2ad'
test_user_id_3 = '7b3d359a-f33c-4a02-8a02-1ed4ecf1c9e3'


db_user = 'twistter'
db_pass = 'twistter'
db_name = 'twistter'
db_host = '127.0.0.1'
db_path = 'mysql://{}:{}@{}/{}'.format(db_user, db_pass, db_host, db_name)
engine = create_engine(db_path, execution_options={'autocommit': True}, echo=False)
db_connection = engine.connect()


# Test setup
def setup():
# clean db
    db_connection.execute('DELETE FROM message_tag')
    db_connection.execute('DELETE FROM tags')
    db_connection.execute('DELETE FROM messages')
    db_connection.execute('DELETE FROM users')

    # initial data
    db_connection.execute("INSERT INTO users VALUES ('"+test_user_id_1+"', 'Test user 1')")
    db_connection.execute("INSERT INTO users VALUES ('"+test_user_id_2+"', 'Test user 2')")
    db_connection.execute("INSERT INTO users VALUES ('"+test_user_id_3+"', 'Test user 3')")


# Input functions
def post_message(user_id, message):
    data = {'user_id': user_id,
            'message': message}
    response = requests.post(base_url+'v1/messages', data=json.dumps(data))
    return response

def get_messages_tag(tag_name):
    data = {'tag_name': tag_name}
    response = requests.get(base_url+'v1/messages/tags', data=json.dumps(data))
    return response



# Verify functions

def verify_message(id, expected_message, expected_user_id):
    result = db_connection.execute(text(
        'SELECT message_text, user_id FROM messages '\
        'WHERE id = :id'), id=id).fetchone()
    assert result['message_text'] == expected_message
    assert result['user_id'] == expected_user_id

def verify_tags_in_messsage(message_id, expected_tags):
    result = db_connection.execute(text(
        'SELECT tags.tag_name FROM messages '\
        'INNER JOIN message_tag ON message_tag.message_id = messages.id '\
        'INNER JOIN tags ON message_tag.tag_id = tags.id '\
        'WHERE messages.id = :message_id '),
        message_id=message_id).fetchall()
    result = [r['tag_name'] for r in result]
    for tag in expected_tags:
        assert tag in result
    assert len(expected_tags) == len(result)

def verify_messages_in_tag(received_messages, expected_messages):
    for i in xrange(0, len(received_messages)):
        assert received_messages[i]['user_name'] == expected_messages[i][0]
        assert received_messages[i]['message_text'] == expected_messages[i][1]



# Testcases

def test_post_message():
    setup()
    message = 'Some test message'
    response = post_message(test_user_id_1, message)
    response_data = response.json()
    assert response.status_code == 200
    assert response_data['status'] == 'ok'
    verify_message(response_data['id'], message, test_user_id_1)

def test_post_message_with_tags():
    setup()
    message = 'Some test message with #tag1 and #tag2 and #tag3'
    response = post_message(test_user_id_1, message)
    response_data = response.json()
    assert response.status_code == 200
    assert response_data['status'] == 'ok'
    verify_message(response_data['id'], message, test_user_id_1)
    verify_tags_in_messsage(response_data['id'], ['tag1', 'tag2', 'tag3'])

def test_get_messages_for_tag():
    setup()
    message1 = 'Some test message with #tag1 and #tag2 and #tag3'
    message2 = 'Some test message with #tag1'
    message3 = '#tag1 some text1'
    message4 = '#tag1 some text2'
    message5 = '#tag2 some text'

    response1 = post_message(test_user_id_1, message1)
    response2 = post_message(test_user_id_2, message2)
    response3 = post_message(test_user_id_3, message3)
    response4 = post_message(test_user_id_1, message4)
    response5 = post_message(test_user_id_2, message5)


    received_messages = get_messages_tag('tag1').json()
    expected_messages = [
            ('Test user 1', '#tag1 some text2'),
            ('Test user 3', '#tag1 some text1'),
            ('Test user 2', 'Some test message with #tag1'),
            ('Test user 1', 'Some test message with #tag1 and #tag2 and #tag3')
        ]
    verify_messages_in_tag(received_messages, expected_messages)


    received_messages = get_messages_tag('tag2').json()
    expected_messages = [
            ('Test user 2', '#tag2 some text'),
            ('Test user 1', 'Some test message with #tag1 and #tag2 and #tag3')
        ]
    verify_messages_in_tag(received_messages, expected_messages)

    received_messages = get_messages_tag('tag3').json()
    expected_messages = [
            ('Test user 1', 'Some test message with #tag1 and #tag2 and #tag3')
        ]
    verify_messages_in_tag(received_messages, expected_messages)

def test_wrong_user():
    setup()
    message = 'Some test message'
    response = post_message('00000000-62bc-472c-94a1-418503e88708', message)
    response_data = response.json()
    assert response.status_code == 401
    assert response_data['status'] == 'error'
