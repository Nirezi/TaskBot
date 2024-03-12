create table tasks
(
    task_id          INTEGER default 0                not null
        primary key,
    task_title       TEXT    default task_title       not null,
    task_description TEXT    default task_description not null,
    task_status      TEXT    default YET              not null,
    task_deadline    TEXT    default 19700101         not null
);
