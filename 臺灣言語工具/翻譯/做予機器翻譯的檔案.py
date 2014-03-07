"""
著作權所有 (C) 民國103年 意傳文化科技
開發者：薛丞宏
網址：http://意傳.台灣
語料來源：請看各資料庫內說明

本程式乃自由軟體，您必須遵照SocialCalc設計的通用公共授權（Common Public Attribution License, CPAL)來修改和重新發佈這一程式，詳情請參閱條文。授權大略如下，若有歧異，以授權原文為主：
	１．得使用、修改、複製並發佈此程式碼，且必須以通用公共授權發行；
	２．任何以程式碼衍生的執行檔或網路服務，必須公開該程式碼；
	３．將此程式的原始碼當函式庫引用入商業軟體，且不需公開非關此函式庫的任何程式碼

此開放原始碼、共享軟體或說明文件之使用或散佈不負擔保責任，並拒絕負擔因使用上述軟體或說明文件所致任何及一切賠償責任或損害。

臺灣言語工具緣起於本土文化推廣與傳承，非常歡迎各界用於商業軟體，但希望在使用之餘，能夠提供建議、錯誤回報或修補，回饋給這塊土地。

感謝您的使用與推廣～～勞力！承蒙！
"""
from 臺灣言語工具.資料庫.資料庫連線 import 資料庫連線
from 臺灣言語工具.資料佮語料匯入整合.教育部臺灣閩南語常用詞辭典.教育部閩南語辭典工具 import 教育部閩南語辭典工具
from 臺灣言語工具.資料庫.整合.教育部閩南語常用詞辭典 import 揣主條目
from 臺灣言語工具.斷詞.資料庫揣辭典條目 import 資料庫揣辭典條目
from 臺灣言語工具.資料庫.欄位資訊 import 偏漳優勢音腔口
from 臺灣言語工具.資料庫.整合.教育部閩南語常用詞辭典 import 教育部閩南語辭典空白符號
from 臺灣言語工具.字詞組集句章.解析整理工具.文章粗胚工具 import 文章粗胚工具
from 臺灣言語工具.字詞組集句章.音標系統.閩南語.臺灣閩南語羅馬字拼音 import 臺灣閩南語羅馬字拼音
from 臺灣言語工具.字詞組集句章.解析整理工具.拆文分析器 import 拆文分析器
from 臺灣言語工具.字詞組集句章.解析整理工具.物件譀鏡 import 物件譀鏡
from 臺灣言語工具.字詞組集句章.解析整理工具.轉物件音家私 import 轉物件音家私
from 臺灣言語工具.斷詞.中研院工具.官方斷詞工具 import 官方斷詞工具
from 臺灣言語工具.斷詞.中研院工具.斷詞結構化工具 import 斷詞結構化工具

class 做予機器翻譯的檔案:
	揣例句 = lambda self :資料庫連線.prepare('SELECT "釋義編號","例句","標音","例句翻譯" ' + 
		'FROM "教育部臺灣閩南語常用詞辭典"."例句" ORDER BY "流水號" ASC ')()
	條目 = 資料庫揣辭典條目()
	揣華語對應 = lambda self, 主編號 :資料庫連線.prepare('SELECT "對照表"."華語" '
		+ 'FROM "教育部臺灣閩南語常用詞辭典"."華語對照表" AS "對照表", '
		+ '"言語來源"."教育部臺灣閩南語常用詞辭典來源" AS "辭典來源"'
		+ 'WHERE "辭典來源"."流水號"=$1 '
		+ 'AND "辭典來源"."主編號"="對照表"."主編號"'
		+ 'ORDER BY "對照表"."流水號" ASC ')(主編號)
	def 產生標音(self):
		臺語字 = open('/dev/shm/翻.臺語字.txt', 'w')
		臺語音 = open('/dev/shm/翻.臺語音.txt', 'w')
		臺語斷詞 = open('/dev/shm/翻.臺語斷詞.txt', 'w')
		國語字 = open('/dev/shm/翻.國語字.txt', 'w')
		辭典工具 = 教育部閩南語辭典工具()
		粗胚工具 = 文章粗胚工具()
		分析器 = 拆文分析器()
		家私 = 轉物件音家私()
		譀鏡 = 物件譀鏡()
		for 釋義編號, 例句, 標音, 例句翻譯 in self.揣例句():
# 			 print(釋義編號,例句,標音,例句翻譯)
			try:
				if 標音[0].isupper():
					例句 = 辭典工具.共造字換做統一碼表示法(例句)
					標音 = 粗胚工具.建立物件語句前處理減號(臺灣閩南語羅馬字拼音, 標音)
					句物件 = 分析器.產生對齊句(例句, 標音)
					標準句物件 = 家私.轉做標準音標(臺灣閩南語羅馬字拼音, 句物件)
					例句翻譯 = 例句翻譯.strip()
					if 例句翻譯 == '':
						例句翻譯 = 例句
# 						print(釋義編號, 例句, 標音, '無翻譯')
	# 				 print(例句,標音,例句翻譯)
					print(譀鏡.看型(標準句物件, 物件分詞符號=' '), file=臺語字)
					print(譀鏡.看音(標準句物件), file=臺語音)
					print(譀鏡.看斷詞(標準句物件, '｜'), file=臺語斷詞)
					print(例句翻譯, file=國語字)
			except:
				pass
		腔口 = 偏漳優勢音腔口
		for 流水號, 型體, 音標 in self.條目.揣腔口字詞資料(腔口):
			for 華語 in self.揣華語對應(流水號):
# 				print(型體, 音標, 華語[0].strip(教育部閩南語辭典空白符號))
#  				print(型體, file = 臺語字)
#  				print(音標, file = 臺語音)
				句物件 = 分析器.產生對齊句(型體, 音標)
				標準句物件 = 家私.轉做標準音標(臺灣閩南語羅馬字拼音, 句物件)
				print(譀鏡.看型(標準句物件, 物件分詞符號=' '), file=臺語字)
				print(譀鏡.看音(標準句物件), file=臺語音)
				print(譀鏡.看斷詞(標準句物件, '｜'), file=臺語斷詞)
				print(華語[0].strip(教育部閩南語辭典空白符號), file=國語字)
		臺語字.close()
		臺語音.close()
		國語字.close()
	def 斷國語字(self):
		國語字 = open('/dev/shm/翻.國語字.txt')
		國語字斷詞 = open('/dev/shm/翻.國語字斷詞.txt', 'w')
		斷詞工具 = 官方斷詞工具()
		結構化工具 = 斷詞結構化工具()
		譀鏡=物件譀鏡()
# 		印到斷詞 = lambda 詞:結構化工具.印出(詞, 國語字斷詞)
		for 一逝 in 國語字:
			try:
				章物件 = 結構化工具.斷詞轉章物件(斷詞工具.斷詞(一逝.strip()))
# 				for 一句 in 剖析了:
# 					結構化結果 = 結構化工具.結構化剖析結果(一句.strip())
# 					結構化工具.處理結構化結果(結構化結果, 印到斷詞)
				
				print(譀鏡.看型(章物件,物件分詞符號=' '),file=國語字斷詞)
			except Exception as 錯誤:
				print(' '.join(一逝), file=國語字斷詞)
				print(錯誤, 一逝.strip())
		國語字斷詞.close()

if __name__ == '__main__':
	機器翻譯的檔案 = 做予機器翻譯的檔案()
# 	機器翻譯的檔案.產生標音()
	機器翻譯的檔案.斷國語字()
