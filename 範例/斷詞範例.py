from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語工具.表單.型音辭典 import 型音辭典
from 臺灣言語工具.斷詞.辭典揣詞 import 辭典揣詞
from 臺灣言語工具.表單.實際語句連詞 import 實際語句連詞
from 臺灣言語工具.斷詞.連詞揀集內組 import 連詞揀集內組
import os
import gzip
import pickle
_分析器=拆文分析器()

閩南語辭典連詞檔名='閩南語辭典連詞.pickle.gz'
if os.path.isfile(閩南語辭典連詞檔名):
    閩南語辭典連詞檔案 = gzip.open(閩南語辭典連詞檔名, 'rb')
    辭典, 連詞 = pickle.load(閩南語辭典連詞檔案)
    閩南語辭典連詞檔案.close()

火車火車頭 =_分析器.建立句物件('hue1 tshia1 hue1 tshia1 thau5')

斷詞 = 辭典揣詞()
斷詞結果, 分數, 詞數 =斷詞.斷詞(辭典,火車火車頭 )
print(斷詞結果, 分數, 詞數)

_連詞揀集內組 = 連詞揀集內組()
標好, 分數, 詞數 = _連詞揀集內組.揀(連詞, 斷詞結果)
print(標好)
