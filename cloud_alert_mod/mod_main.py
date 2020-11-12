# mod_main

from typing import List, Tuple, Dict, Union
import sqlite3
#import smtplib
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from status_reader.aws import AwsStatusReader

def main() -> None:
    """ メイン関数

    全体で唯一のメイン処理。

    Args:
        None
    
    Returns:
        None
    """
    print('main')

    # DB接続
    """
    conn = sqlite3.connect(cfg['db_file'])

    # 初期化
    if cfg['initialize_db']:
        initialize_db(cfg, conn)
    
    # 抽出
    tbl = conn.execute('select * from m_targets;')
    recs = tbl.fetchall()
    if cfg['run_mode']=='DEBUG':
        print(recs)

    conn.close()
    
    # ステータスのチェック
    sts = check_all_statuses(cfg, recs)
    """

    # メールを送る
    alert_cloud_status([])



def initialize_db(
    cfg: Dict[str, Union[str, int, bool]],
    conn: sqlite3.Connection
) -> None:
    """DB初期化

    DB自体を作り直す。

    Args:
        cfg (Dict[str, Union[str, int, bool]]): コンフィグ情報
        conn (sqlite3.Connection): DBコネクション
    
    Returns:
        None
    """
    print('initialize db!')

    cur = conn.cursor()

    # テーブル作成
    cur.execute(
        'DROP TABLE IF EXISTS m_targets;'
    )
    cur.execute(
        'CREATE TABLE IF NOT EXISTS m_targets ' +
        '( ' +
            'target_id INT NOT NULL PRIMARY KEY, ' +
            'cloud_id INT NOT NULL, ' +
            'search_hint str STR NOT NULL'
        ');')
    
    # レコード作成
    m_targets_initialize_recs = [
        (0, 0, 'Amazon Elastic Compute Cloud (Tokyo)'),
        #(1, 0, 'Amazon Elastic Compute Cloud (Tokyo)')
    ]
    cur.executemany(
        'INSERT INTO m_targets values (?, ?, ?);',
        m_targets_initialize_recs
    )

    # commit
    conn.commit()


def check_all_statuses(
    cfg: Dict[str, Union[str, int, bool]], 
    recs: List[Tuple]
) -> List[Tuple[int,int]]:
    """登録されているすべてのクラウド情報を確認し、エラーの場合は警告を出す

    Args:
        recs (List[tuple]): m_targetsから読み込んだデータ
    
    Returns:
        check_results (List[Tuple[int,int]]):
            target_id, statusのtupleのリスト
    """
    print('check_all_statuses')
    
    statuses = []

    # 全行１行ずつ取り出して処理する
    for rec in recs:
        (target_id, cloud_id, search_hint) = rec

        if cloud_id==0: # AWS
            r = AwsStatusReader()
            stat, msg = r.get_status(search_hint)

            if cfg['run_mode']=='DEBUG':
                print(f'STATUS --- id:{target_id}, stat:{stat}, msg:{msg}')

        else:
            print(f'[E] Illegular colud_id: {target_id}')
        
        # 結果へ追加
        # ここのstatは、cloud_alert_modのステータス(CLOUD_STATUSの値)
        statuses.append((target_id, stat))

    return statuses


def alert_cloud_status(statuses: List[Tuple[int,int]]):
    """異常ステータスがある場合は警告を出す
    """
    message = Mail(
        from_email = 'yoichiro.ikeda@mioana.com',
        to_emails = 'xxyo1xx@gmail.com',
        subject = 'Sending with Twilio SendGrid is Fun',
        html_content = '<strong>and easy to do anywhere, even with Python</strong>日本語はおｋ？'
    )
    try:
        sg = SendGridAPIClient(os.environ.get('sendgrid_api_key'))
        response = sg.send(message)
        print(f'status_code:{response.status_code}')
        print(f'body:{response.body}')
        print(f'header:{response.headers}')

    except Exception as e:
        print(type(e))
        print(e.message)

    return None
