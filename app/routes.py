
from os import path
from .config import STORE_PATH
import os
from . import app
from flask import (
    render_template,
    request,
    redirect,
    send_from_directory,
    abort,
    url_for,
)
from .utils import (
    get_hash_dir_path,
    is_valid_file_hash,
    save_file,
    remove_file,
)

@app.route('/files', methods=['GET', 'POST'])
def upload_file():
    '''
        GET: отправляет на страницу с формой отправки файлов
        POST: сохраняет отправленный пользователем файл
    '''
    if request.method == 'POST':
        if request.files:
            file = request.files['file'] # FileStorage object
            save_file(file)
            return redirect(request.url)
    return render_template('upload_file.html')

@app.route('/files/<file_hash>', methods=['GET', 'DELETE'])
def download_file(file_hash):
    '''
        GET: отправляет файл,если он существует, с именем file_hash
        DELETE: удаляет файл,если он существует, с именем file_hash

    '''
    path = get_hash_dir_path(file_hash)
    if request.method == 'GET':
        if not is_valid_file_hash(file_hash):
            abort(404)
        try:
            return send_from_directory(
                path, filename=file_hash, as_attachment=False
            )
        except FileNotFoundError:
            abort(404)
    if request.method == 'DELETE':
        is_removed = remove_file(file_hash)
        if is_removed:
            return redirect(url_for('upload_file'))
        abort(404)

