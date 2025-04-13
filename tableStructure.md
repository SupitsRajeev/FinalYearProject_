<!-- create table user
(
    id           int          null,
    name         varchar(50)  null,
    email        varchar(120) null,
    password     varchar(120) null,
    isHr         int          null,
    isIt         int          null,
    created_date datetime     null,
    created_by   varchar(120) null,
    updated_by   varchar(120) null,
    updated_date datetime     null
);

create index user_id
    on user (id);

create table user_priviledge_groups
(
    Id           int auto_increment
        primary key,
    name         varchar(120) null,
    role_level   int          null,
    created_date datetime     null,
    created_by   varchar(120) null,
    updated_date datetime     null,
    updated_by   varchar(120) null
);

create index user_priviledge_groups_role
    on user_priviledge_groups (role_level);


create table user_priviledge
(
    id                     int auto_increment
        primary key,
    userId                 int          null,
    priviledge_groups_role int          null,
    created_by             varchar(120) null,
    created_at             datetime     null,
    updated_by             varchar(120) null,
    updated_at             datetime     null,
    constraint user_priviledge_user_priviledge_groups_role_level_fk
        foreign key (priviledge_groups_role) references user_priviledge_groups (role_level),
    constraint userid
        foreign key (userId) references user (id)
); -->