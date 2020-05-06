# 下载telegram内容

###依赖
```sbtshell
pip/pip3 install telethon  
pip/pip3 install PySocks  
pip/pip3 install PyMySQL  
```

####local
```sbtshell
python download.py -c ./config.json  
```

```json
{
  "job": {
    "path": "", //存储路径
    "use_proxy": 1, //是否使用代理 0:否，1:是
    "entity": "", //entity_like
    "type_video": 1, //视频
    "type_photo": 0, //图片
    "type_message": 0, //信息
    "type_document": 0, //文档
    "type_round_video": 0 //round video
  },
  "user": {
    "my_session": "", //session id
    "api_id": 0, //api_id
    "api_hash": "" //api_hash
  },
  "proxy": {
    "protocol": 2, //协议 1:socks4, 2:socks5, 3:http
    "address": "", //地址
    "port": 1080 //端口
  }
}
```

####database
```sbtshell
python download.py -i [id] -d ./datasource.json  
```

```json
{
  "host": "",
  "port": 3306,
  "user": "",
  "password": "",
  "db": "",
  "charset": "utf8"
}
```

see create.sql