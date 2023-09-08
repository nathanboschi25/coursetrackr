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
    PRIMARY KEY (list_id)
);

CREATE TABLE users
(
    user_id  INT AUTO_INCREMENT,
    username VARCHAR(50)  NOT NULL,
    password VARCHAR(200) NOT NULL,
    name     VARCHAR(50)  NOT NULL,
    list_id  INT,
    PRIMARY KEY (user_id),
    FOREIGN KEY (list_id) REFERENCES signature_list (list_id)
);

CREATE TABLE events
(
    event_id       INT AUTO_INCREMENT,
    start_datetime DATETIME    NOT NULL,
    end_datetime   DATETIME    NOT NULL,
    title          VARCHAR(50) NOT NULL,
    content        VARCHAR(200),
    uid_ade        VARCHAR(50),
    list_id        INT         NOT NULL,
    PRIMARY KEY (event_id),
    FOREIGN KEY (list_id) REFERENCES signature_list (list_id)
);

CREATE TABLE teachers
(
    teacher_id   INT AUTO_INCREMENT,
    teacher_name VARCHAR(50) NOT NULL,
    PRIMARY KEY (teacher_id)
);

CREATE TABLE signatures
(
    sinature_id        INT AUTO_INCREMENT,
    signature_svg      TEXT     NOT NULL,
    signature_datetime DATETIME NOT NULL,
    teacher_id         INT      NOT NULL,
    event_id           INT      NOT NULL,
    user_id            INT      NOT NULL,
    PRIMARY KEY (sinature_id),
    FOREIGN KEY (teacher_id) REFERENCES teachers (teacher_id),
    FOREIGN KEY (event_id) REFERENCES events (event_id),
    FOREIGN KEY (user_id) REFERENCES users (user_id)
);

# CREATE TABLE subscribes
# (
#     user_id INT,
#     list_id INT,
#     PRIMARY KEY (user_id, list_id),
#     FOREIGN KEY (user_id) REFERENCES users (user_id),
#     FOREIGN KEY (list_id) REFERENCES signature_list (list_id)
# );