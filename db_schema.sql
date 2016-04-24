-- requires Mysql 5.6

DROP TABLE IF EXISTS `message_tag`;
DROP TABLE IF EXISTS `messages`;
DROP TABLE IF EXISTS `users`;
DROP TABLE IF EXISTS `tags`;


CREATE TABLE `users` (
    `id` CHAR(36) NOT NULL,
    `user_name` VARCHAR(255) NOT NULL,
     PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


CREATE TABLE `messages` (
    `id` CHAR(36) NOT NULL,
    `user_id` CHAR(36) NOT NULL,
    `message_text` VARCHAR(140) NOT NULL,
    `message_time` TIMESTAMP(6) NOT NULL,
     PRIMARY KEY (`id`),
     KEY `messages_fk1` (`user_id`),
     KEY `message_time_idx` (`message_time`),
     CONSTRAINT `messages_fk1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


CREATE TABLE `tags` (
    `id` CHAR(36) NOT NULL,
    `tag_name` VARCHAR(140) NOT NULL,
     PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


CREATE TABLE `message_tag` (
    `message_id` CHAR(36) NOT NULL,
    `tag_id` CHAR(36) NOT NULL,
    PRIMARY KEY (`message_id`, `tag_id`),
    KEY `message_tag_fk1` (`message_id`),
    KEY `message_tag_fk2` (`tag_id`),
    CONSTRAINT `message_tag_fk1` FOREIGN KEY (`message_id`) REFERENCES `messages` (`id`),
    CONSTRAINT `message_tag_fk2` FOREIGN KEY (`tag_id`) REFERENCES `tags` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


-- Initial sample data
INSERT INTO users VALUES ('ba8bf220-62bc-472c-94a1-418503e88708', 'Test user 1');
INSERT INTO users VALUES ('9f3b9431-55c7-4ad6-860a-bc39341ea2ad', 'Test user 2');
INSERT INTO users VALUES ('7b3d359a-f33c-4a02-8a02-1ed4ecf1c9e3', 'Test user 3');


INSERT INTO messages VALUES ('46849f25-bfa1-4bdd-b9e3-4985cf64b5f6', 'ba8bf220-62bc-472c-94a1-418503e88708','Some test message 1', '2016-04-01 17:03:40');
INSERT INTO messages VALUES ('d7df4678-0544-4210-9a73-6abaf16b002c', 'ba8bf220-62bc-472c-94a1-418503e88708','Some test message 2 with some #testtag1', '2016-04-02 17:03:40');
INSERT INTO messages VALUES ('fda1df01-c329-4397-9be8-ae118ff0d19a', 'ba8bf220-62bc-472c-94a1-418503e88708','Some test message 3', '2016-04-03 17:03:40');
INSERT INTO messages VALUES ('0230b825-aafe-44b0-8204-60ff1b5ddf59', 'ba8bf220-62bc-472c-94a1-418503e88708','#testtag2 Some test message 4 with some #testtag1', '2016-04-04 17:03:40');
INSERT INTO messages VALUES ('6f215300-df0f-4cf9-8fcd-47154cbd1d91', 'ba8bf220-62bc-472c-94a1-418503e88708','Some test message 5', '2016-04-05 17:03:40');
INSERT INTO messages VALUES ('5fa27bab-f18a-4ad8-ae1a-d56c39f522a6', '9f3b9431-55c7-4ad6-860a-bc39341ea2ad','Some test message 6', '2016-04-06 17:03:40');
INSERT INTO messages VALUES ('b489abc3-9d04-4ea4-8a29-a579b2f50ff7', '9f3b9431-55c7-4ad6-860a-bc39341ea2ad','Some test message 7', '2016-04-07 17:03:40');
INSERT INTO messages VALUES ('c68629b4-c0b9-4a39-af23-a86159b24145', '9f3b9431-55c7-4ad6-860a-bc39341ea2ad','Some test message 8 with some #testtag1', '2016-04-08 17:03:40');
INSERT INTO messages VALUES ('d15310d5-93ba-4fb1-8852-3423c11a753e', '9f3b9431-55c7-4ad6-860a-bc39341ea2ad','Some test message 9', '2016-04-09 17:03:40');
INSERT INTO messages VALUES ('3e438743-e950-4ba7-b013-fc405bc117be', '9f3b9431-55c7-4ad6-860a-bc39341ea2ad','#testtag2 Some test message 10', '2016-04-10 17:03:40');
INSERT INTO messages VALUES ('434e5ac5-0d01-414b-a78d-eb7c850c81ad', '7b3d359a-f33c-4a02-8a02-1ed4ecf1c9e3','Some test message 11', '2016-04-11 17:03:40');
INSERT INTO messages VALUES ('0865f53a-ddd4-467e-8e19-1fe3e3c09070', '7b3d359a-f33c-4a02-8a02-1ed4ecf1c9e3','Some test message 12', '2016-04-12 17:03:40');
INSERT INTO messages VALUES ('41bb0904-b5fb-4f17-8c4b-bd84dbd9d6c2', '7b3d359a-f33c-4a02-8a02-1ed4ecf1c9e3','Some test #testtag3 message 13', '2016-04-14 17:03:40');
INSERT INTO messages VALUES ('b935ac76-d83e-49d4-8d76-a88c128a539b', '7b3d359a-f33c-4a02-8a02-1ed4ecf1c9e3','#testtag2 Some test message 14', '2016-04-15 17:03:40');


INSERT INTO tags VALUES ('ee91ca09-2465-434e-902a-b68332ae2f42', 'testtag1');
INSERT INTO tags VALUES ('0a1a56da-34a5-459b-a03e-bde3d45e9db4', 'testtag2');
INSERT INTO tags VALUES ('baf75b86-98ad-4aa2-a2c3-40a4279e8fa8', 'testtag3');

INSERT INTO message_tag VALUES ('d7df4678-0544-4210-9a73-6abaf16b002c', 'ee91ca09-2465-434e-902a-b68332ae2f42');
INSERT INTO message_tag VALUES ('0230b825-aafe-44b0-8204-60ff1b5ddf59', 'ee91ca09-2465-434e-902a-b68332ae2f42');
INSERT INTO message_tag VALUES ('0230b825-aafe-44b0-8204-60ff1b5ddf59', '0a1a56da-34a5-459b-a03e-bde3d45e9db4');
INSERT INTO message_tag VALUES ('c68629b4-c0b9-4a39-af23-a86159b24145', 'ee91ca09-2465-434e-902a-b68332ae2f42');
INSERT INTO message_tag VALUES ('3e438743-e950-4ba7-b013-fc405bc117be', '0a1a56da-34a5-459b-a03e-bde3d45e9db4');
INSERT INTO message_tag VALUES ('41bb0904-b5fb-4f17-8c4b-bd84dbd9d6c2', 'baf75b86-98ad-4aa2-a2c3-40a4279e8fa8');
INSERT INTO message_tag VALUES ('b935ac76-d83e-49d4-8d76-a88c128a539b', '0a1a56da-34a5-459b-a03e-bde3d45e9db4');

