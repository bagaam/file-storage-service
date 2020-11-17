from app.config import STORE_PATH
import os
import hashlib

def get_file_hash(file, blocksize=65536):
    '''
        возвращает хеш файла
    '''
    hasher = hashlib.md5()
    buf = file.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = file.read(blocksize)
    file.seek(0)
    return hasher.hexdigest()

def get_file_hash_dir(file_hash: str) -> str:
    '''
        возвращает имя директории, где должен храниться
        хеш файла
        имя директории - это первые 2 символа хеша файла
    '''
    return file_hash[:2]

def is_valid_file_hash(file_hash):
    '''
        проверят на валидность хеш файла
    '''
    if len(file_hash) != 32:
        return False
    return True

def get_hash_dir_path(file_hash):
    '''
        возвращает путь к директории, где должен
        храниться файл с именем file_hash
    '''
    return os.path.join(STORE_PATH, get_file_hash_dir(file_hash))

def make_hash_dir(file_hash):
    '''
        создает директорию для хранения хеша,
        если она не была создана ранее
        и возвращает  путь до директории
    '''
    hash_dir_name = get_file_hash_dir(file_hash)
    hash_dir_path = os.path.join(STORE_PATH, hash_dir_name)
    if not os.path.exists(hash_dir_path):
        os.makedirs(hash_dir_path, 0o770)
    return hash_dir_path

def save_file(file):
    '''
        сохраняет файл с именем его хеша (get_file_hash)
        в директорию /store/<file_hash_dir>/,
        где <file_hash_dir> - директория, которая создается
        при помощи get_file_hash_dir
    '''
    file_hash = get_file_hash(file)
    # file_hash = '0570caf9bb9823138615255710a1cb47'
    path = make_hash_dir(file_hash)
    file.save(os.path.join(path, file_hash))

def remove_file(file_hash):
    '''
        удаляет файл с именем file_hash
        возвращает True, если файл есть и удален
        False, если такого файла нет
    '''
    file_path = os.path.join(get_hash_dir_path(file_hash), file_hash)
    if os.path.isfile(file_path):
        os.remove(file_path)
        return True
    return False