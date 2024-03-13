create table tasks
(
    task_id          INTEGER not null
        primary key,
    task_title       TEXT    not null,
    task_description TEXT    not null,
    task_deadline    INTEGER not null
);
