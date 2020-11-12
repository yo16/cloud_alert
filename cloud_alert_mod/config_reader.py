# config_reader
# 諸々の設定情報を返す

import os
from typing import Dict, Union
import configparser

def get_config():
    """コンフィグ情報を得て、環境変数に突っ込む

    Args:
        None
    
    Returns:
        None
    """
    conf = configparser.ConfigParser()
    print(conf.read('./cloud_alert_mod/config.ini'))
    print(conf.sections())

    # 実行モード
    os.environ['run_mode'] = conf['Constant Values']['run_mode']
    print('run_mode:' + os.environ['run_mode'])

    # DB初期化フラグ
    os.environ['initialize_db'] = conf['Constant Values']['initialize_db']
    print('initialize_DB: ' + str(os.environ['initialize_db']))

    # DBファイル名
    os.environ['db_file'] = conf['Constant Values']['db_file']

    # APIキー
    os.environ['sendgrid_api_key'] = conf['Secret Keys']['sendgrid_api_key']

    return None
