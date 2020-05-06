from telethon import TelegramClient, sync
from pathlib import Path
from telethon.tl.types import InputMessagesFilterVideo, \
    InputMessagesFilterPhotos, \
    MessageMediaPhoto, \
    MessageMediaDocument
import socks
import time
import datetime
import argparse
import json
from datasource import Datasource
from read_config import ReadDatabaseConfig, ReadJsonConfig
from log import DatasourceLog, LocalLog

# 获取参数
parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument("-i", type=int, default=-1)
parser.add_argument("-d", type=str)
parser.add_argument("-c", type=str)
args = parser.parse_args()

if args.d is not None and args.c is not None:
    raise Exception("数据库及json配置不能共存")

config = None
log = None

if args.d is not None:
    if args.i < 0:
        raise Exception("输入任务id，[-i]")

    with open(args.d, encoding='utf-8') as datasource_context:
        contents = datasource_context.read()
        content = json.loads(contents)
        my_source = Datasource(content['host'],
                               content['port'],
                               content['user'],
                               content['password'],
                               content['db'],
                               content['charset'])
        config = ReadDatabaseConfig(my_source, args.i)
        exec_id = my_source.insert('insert into job_exec (start_time, job_id) values (sysdate(), ' + str(args.i) + ')')
        log = DatasourceLog(config, exec_id)

elif args.c is not None:
    with open(args.c, encoding='utf-8') as json_context:
        contents = json_context.read()
        content = json.loads(contents)
        config = ReadJsonConfig(content)
        log = LocalLog('./log-' + str(int(time.time())) + '.log')

proxy = None
client = None
api_id = config.user['api_id']
api_hash = config.user['api_hash']
my_session = config.user['my_session']
picture_storage_path = config.job['path']

if config.job['use_proxy'] == 1:
    proxy = (config.proxy['protocol'], config.proxy['address'], config.proxy['port'])
    client = TelegramClient(my_session, api_id=api_id, api_hash=api_hash, proxy=proxy).start()
else:
    client = TelegramClient(my_session, api_id=api_id, api_hash=api_hash).start()

log.info('已连接')
client.get_dialogs()


def download(_filter):
    _type = _filter.__name__
    log.info('开始下载' + _type + '类型文件')
    entity_like = config.job['entity']
    if entity_like.isdigit():
        entity_like = int(entity_like)
    entitys = client.get_messages(entity_like, None, filter=_filter)

    total = len(entitys)
    log.info('共有' + str(total) + '条' + _type + '数据等待下载')

    index = 0
    for entity in entitys:
        try:
            start_time = datetime.datetime.now()
            index = index + 1
            # 视频
            if isinstance(entity.media, MessageMediaDocument):
                if len(entity.media.document.attributes) > 1:
                    filename = picture_storage_path + "/" + str(entity.media.document.attributes[1].file_name) + ""
                else:
                    filename = picture_storage_path + "/" + str(entity.id) + ".mp4"
            # 图片
            elif isinstance(entity.media, MessageMediaPhoto):
                filename = picture_storage_path + "/" + str(entity.id) + ".jpg"
            else:
                raise Exception('类型' + str(type(entity.media)) + '无法识别')

            cur_file = Path(filename)
            if cur_file.exists():
                log.info('文件已存在' + str(filename))
            else:
                log.info('开始下载[' + str(filename) + '], 当前进度' + str(index) + "/" + str(total))
                client.download_media(entity, filename)
                end_time = datetime.datetime.now()
                log.info('下载完成[' + str(filename) + '], 耗时' + str(end_time - start_time))

        except BaseException as e:
            try:
                log.info('下载失败,尝试删除文件[' + filename + ']')
                cur_file.unlink()
            except IsADirectoryError as ie:
                log.error('删除文件[' + filename + ']失败' + ie)
            log.error('Exception:' + str(index) + ':' + str(e))
    log.info(_type + '类型文件下载结束')


if config.job['type_video'] == 1:
    download(InputMessagesFilterVideo)

if config.job['type_photo'] == 1:
    download(InputMessagesFilterPhotos)

client.disconnect()
if args.d is not None:
    exec_id = my_source.update('update job_exec set end_time = sysdate() where id = ' + str(exec_id))
