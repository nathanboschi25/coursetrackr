DROP TABLE IF EXISTS
    subscribes,
    signatures,
    teachers,
    events,
    users,
    signature_list;

CREATE TABLE signature_list
(
    list_id     INT AUTO_INCREMENT,
    url_ical    VARCHAR(500) NOT NULL,
    designation VARCHAR(50),
    annee_univ  VARCHAR(50),
    CONSTRAINT PK_signature_list PRIMARY KEY (list_id)
);

CREATE TABLE events
(
    event_id       INT AUTO_INCREMENT,
    start_datetime DATETIME    NOT NULL,
    end_datetime   DATETIME    NOT NULL,
    title          VARCHAR(50) NOT NULL,
    content        VARCHAR(200),
    uid_ade        VARCHAR(50) NOT NULL,
    list_id        INT         NOT NULL,
    CONSTRAINT PK_events PRIMARY KEY (event_id),
    CONSTRAINT FK_events_signature_list FOREIGN KEY (list_id) REFERENCES signature_list (list_id)
);

CREATE TABLE teachers
(
    teacher_id   INT AUTO_INCREMENT,
    teacher_name VARCHAR(50) NOT NULL,
    CONSTRAINT PK_teachers PRIMARY KEY (teacher_id)
);

CREATE TABLE users
(
    user_id  INT AUTO_INCREMENT,
    password VARCHAR(50) NOT NULL,
    name     VARCHAR(50) NOT NULL,
    username VARCHAR(50) NOT NULL,
    list_id  INT,
    CONSTRAINT PK_users PRIMARY KEY (user_id),
    CONSTRAINT FK_users_signature_list FOREIGN KEY (list_id) REFERENCES signature_list (list_id)
);

CREATE TABLE signatures
(
    signature_id       INT AUTO_INCREMENT,
    signature_svg      TEXT,
    signature_datetime DATETIME NOT NULL,
    teacher_id         INT      NOT NULL,
    event_id           INT      NOT NULL,
    user_id            INT      NOT NULL,
    CONSTRAINT PK_signatures PRIMARY KEY (signature_id),
    CONSTRAINT FK_signatures_teachers FOREIGN KEY (teacher_id) REFERENCES teachers (teacher_id),
    CONSTRAINT FK_signatures_events FOREIGN KEY (event_id) REFERENCES events (event_id),
    CONSTRAINT FK_signatures_users FOREIGN KEY (user_id) REFERENCES users (user_id)
);
