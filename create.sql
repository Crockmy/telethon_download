create table telegram.job
(
    id int auto_increment
        primary key,
    user_id int null,
    proxy_id int null,
    path varchar(100) CHARACTER SET utf8 DEFAULT NULL,
    use_proxy int null,
    entity varchar(40) CHARACTER SET utf8 DEFAULT NULL,
    type_video int null,
    type_photo int null,
    type_message int null,
    type_document int null,
    type_round_video int null
)
comment '任务表' charset=utf8;

create table telegram.job_exec
(
    id int auto_increment
        primary key,
    job_id int null,
    start_time timestamp null,
    end_time timestamp null,
    content varchar(2000) CHARACTER SET utf8 DEFAULT NULL
)
comment '运行任务表' charset=utf8;

create table telegram.job_log
(
    id int auto_increment
        primary key,
    create_time timestamp null,
    content varchar(1000) CHARACTER SET utf8 DEFAULT NULL,
    type varchar(10) CHARACTER SET utf8 DEFAULT NULL,
    job_exec_id int null
)
comment '任务日志' charset=utf8;

create table telegram.proxy
(
    id int auto_increment
        primary key,
    protocol int null comment 'socks4=1,socks5=2,http=3',
    address varchar(100) CHARACTER SET utf8 DEFAULT NULL,
    port int null
)
comment '代理表' charset=utf8;

create table telegram.user
(
    id int auto_increment
        primary key,
    my_session varchar(40) CHARACTER SET utf8 DEFAULT NULL,
    api_id int null,
    api_hash varchar(40) CHARACTER SET utf8 DEFAULT NULL
)
comment '用户信息' charset=utf8;

