# base.py

from abc import ABCMeta, abstractmethod
from typing import List, Dict, Union, Tuple
import requests
from bs4 import BeautifulSoup

CLOUD_INFOS = [
    {'id': 0, 'name':'AWS', 'url':'https://status.aws.amazon.com/'},
    {'id': 1, 'name':'GCP', 'url':'https://status.cloud.google.com/'},
]
CLOUD_STATUS = {'OK': 0, 'NG': 1}

class BaseStatusReader(metaclass=ABCMeta):
    def __init__(self):
        self.cloud_id = -1

        self.bs4_objs = {}
        return

    @abstractmethod
    def get_status(self, record_key: str) -> Tuple[int, str]:
        """ステータスを得る

        情報の取得の仕方や結果の値は、各クラウドサービスによって異なる。
        ここでは、各クラウドサービスによらず、OK/NGを取得し、配列に格納して返す。
        strは、ステータスの説明。

        Args:
            record_key (str): 検索に使用するキー情報。

        Returns:
            cloud_status (int): CLOUD_STATUSの値(int)のいずれか。
            message (str): 各クラウドのメッセージ。
        """
        pass

    
    @abstractmethod
    def align_status(self, cloud_status: int) -> Tuple[int, str]:
        """各クラウドのステータス値を、status_readerモジュールのステータスへ変換する

        Args:
            cloud_status (int): クラウドのステータス

        Returns:
            mod_status (int): モジュールとしてのステータス [0:正常 | 1:異常]
            mod_message (str): クラウドのメッセージ
        """
        pass


    def get_html(self) -> BeautifulSoup:
        """HTMLを読んでBeautifulSoupオブジェクトを取得する

        Args:
            None
        
        Returns:
            bs_obj (BeautifulSoup): 取得したBeautifulSoupオブジェクト
        """
        # まだ取得していない場合は取得
        if self.cloud_id not in self.bs4_objs:
            # HTMLを取得
            html_file = requests.get(CLOUD_INFOS[self.cloud_id]['url'])
            bs_obj = BeautifulSoup(html_file.content, "html.parser")

            # 登録
            self.bs4_objs[self.cloud_id] = bs_obj
        else:
            # 取得済みの場合は、そのobjを返す
            bs_obj = self.bs4_objs[self.cloud_id]

        return bs_obj
