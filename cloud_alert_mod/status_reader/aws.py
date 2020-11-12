# aws.py
# https://status.aws.amazon.com/

from typing import List, Dict, Union, Tuple
import re
from bs4 import BeautifulSoup

from .base import BaseStatusReader

class AwsStatusReader(BaseStatusReader):
    """AWSステータスリーダークラス

    AWSのステータスを取得する。
    """
    def __init__(self):
        super().__init__()
        self.cloud_id = 0   # 0:AWS
    

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
        bs_obj = self.get_html()

        # <td>のtextがrecord_keyであるDOMを探す
        target_dom = None
        for c in bs_obj.find_all(attrs={'class':'bb top pad8'}):
            if c.get_text()==record_key:
                target_dom = c
                break
        #print(target_dom)
        assert target_dom is not None, True

        # その１つ前の<td>の１つ目の要素が<image>
        image_dom = target_dom.previous_sibling.previous_sibling.contents[0]
        assert image_dom.name, 'image'

        # srcの解析
        img_src = image_dom['src']
        m = re.match(r'/images/status([0-9])\.gif', img_src)
        assert m is not None, True
        status_num = int(m.groups()[0])

        # AWSのステータスを、モジュールのステータスへ変換する
        mod_status, cloud_message = self.align_status(status_num)

        return (mod_status, cloud_message)


    def align_status(self, cloud_status: int) -> Tuple[int, str]:
        """各クラウドのステータス値を、status_readerモジュールのステータスへ変換する

        Args:
            cloud_status (int): クラウドのステータス

        Returns:
            mod_status (int): モジュールとしてのステータス [0:正常 | 1:異常]
            mod_message (str): クラウドのメッセージ
        """
        mod_status = 1
        mod_message = 'Default error'
        if cloud_status==0:
            mod_status = 0
            mod_message = 'Success!'
        return (mod_status, mod_message)
