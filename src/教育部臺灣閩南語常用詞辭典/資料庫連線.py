import postgresql
from 言語資料庫.公用資料 import 國語腔口
from 言語資料庫.公用資料 import 臺語腔口

空白符號 = '\u3000 \t'
隔開符號 = '\u3000'
俗音記號 = '??????'
合音記號 = '------'
會當替換 = '會當替換'
袂當替換 = '袂當替換'
義近 = '義近'
義倒 = '義倒'

資料庫連線 = postgresql.open(host = "localhost", port = 5432, user = "Ihc", password = "983781", database = "言語系統")

揣主條目 = 資料庫連線.prepare('SELECT "主編號","屬性","詞目","音讀","方言差" ' +
	'FROM "教育部臺灣閩南語常用詞辭典"."詞目總檔" ORDER BY "主編號" ASC')
揣義倒詞的詞音 = 資料庫連線.prepare('SELECT "另注音讀" ' +
	'FROM "教育部臺灣閩南語常用詞辭典"."反義詞對應" WHERE "反義詞" = $1 ORDER BY "流水號"')
揣義近詞的詞音 = 資料庫連線.prepare('SELECT "另注音讀" ' +
	'FROM "教育部臺灣閩南語常用詞辭典"."近義詞對應" WHERE "近義詞對應" = $1 ORDER BY "流水號"')
揣詞別音 = 資料庫連線.prepare('SELECT "又音" ' +
	'FROM "教育部臺灣閩南語常用詞辭典"."又音" WHERE "主編號"=$1 AND "屬性" = \'又唸作\' ' +
	' ORDER BY "流水號"')
揣詞俗音 = 資料庫連線.prepare('SELECT "又音" ' +
	'FROM "教育部臺灣閩南語常用詞辭典"."又音" WHERE "主編號"=$1 AND "屬性" = \'俗唸作\' ' +
	' ORDER BY "流水號"')
揣詞合音 = 資料庫連線.prepare('SELECT "又音" ' +
	'FROM "教育部臺灣閩南語常用詞辭典"."又音" WHERE "主編號"=$1 AND "屬性" = \'合音唸作\' ' +
	' ORDER BY "流水號"')

揣字方言差 = 資料庫連線.prepare('SELECT * ' +
	'FROM "教育部臺灣閩南語常用詞辭典"."語音方言差" WHERE "字號"=$1 ')
揣詞方言差 = 資料庫連線.prepare('SELECT * ' +
	'FROM "教育部臺灣閩南語常用詞辭典"."詞彙方言差" WHERE "詞彙編號"=$1 ')
偏漳優勢音腔口 = 臺語腔口 + '偏漳優勢音'
偏泉優勢音腔口 = 臺語腔口 + '偏泉優勢音'
字方言差欄位 = ['閩南語' + 地區 + '腔' for 地區 in 揣字方言差.column_names[3:]]
詞方言差欄位 = ['閩南語' + 地區 + '腔' for 地區 in 揣詞方言差.column_names[3:]]
國語臺員腔 = 國語腔口

設定來源 = 資料庫連線.prepare('INSERT INTO "言語來源"."教育部臺灣閩南語常用詞辭典來源" ' +
	'("流水號","主編號") ' + 'VALUES ($1,$2)')
設定合音遏袂處理 = 資料庫連線.prepare('INSERT INTO "言語來源"."教育部臺灣閩南語常用詞辭典合音遏袂處理" ' +
	'("流水號") ' + 'VALUES ($1)')

揣文字上大流水號資料 = 資料庫連線.prepare('SELECT MAX("流水號") ' +
	'FROM "言語"."文字"')
揣文字上大流水號 = lambda:揣文字上大流水號資料.first()
揣關係上大流水號資料 = 資料庫連線.prepare('SELECT MAX("流水號") ' +
	'FROM "言語"."關係"')
揣關係上大流水號 = lambda:揣關係上大流水號資料.first()
揣演化上大流水號資料 = 資料庫連線.prepare('SELECT MAX("流水號") ' +
	'FROM "言語"."演化"')
揣演化上大流水號 = lambda:揣演化上大流水號資料.first()


資料庫加文字 = 資料庫連線.prepare('INSERT INTO "言語"."文字" ' +
	'("來源","種類","腔口","地區","年代","型體","音標") ' +
	'VALUES (\'教育部臺灣閩南語常用詞辭典\',$1,$2,\'臺員\',\'97\',$3,$4) ')
資料庫加關係 = 資料庫連線.prepare('INSERT INTO "言語"."關係" ' +
	'("甲流水號","乙流水號","乙對甲的關係類型","關係性質") ' + 'VALUES ($1,$2,$3,$4)')
資料庫加關係無性質 = 資料庫連線.prepare('INSERT INTO "言語"."關係" ' +
	'("甲流水號","乙流水號","乙對甲的關係類型") ' + 'VALUES ($1,$2,$3)')
資料庫加演化 = 資料庫連線.prepare('INSERT INTO "言語"."演化" ' +
	'("甲流水號","乙流水號","乙對甲的演化類型") ' + 'VALUES ($1,$2,$3)')
加編修狀況 = 資料庫連線.prepare('INSERT INTO "言語"."編修" ' +
	'("流水號","資料種類") ' + 'VALUES ($1,$2)')
def 加文字(種類, 腔口, 型體, 音標):
	資料庫加文字(種類, 腔口, 型體, 音標)
	流水號 = 揣文字上大流水號()
	加編修狀況(流水號, '文字')
	
def 加關係(甲流水號, 乙流水號, 乙對甲的關係類型, 關係性質):
	if 關係性質 == '':
		資料庫加關係無性質(甲流水號, 乙流水號, 乙對甲的關係類型)
	else:
		資料庫加關係(甲流水號, 乙流水號, 乙對甲的關係類型, 關係性質)
	流水號 = 揣關係上大流水號()
	加編修狀況(流水號, '關係')
	return 流水號

def 加演化(種類, 腔口, 型體, 音標):
	資料庫加演化(種類, 腔口, 型體, 音標)
	流水號 = 揣演化上大流水號()
	加編修狀況(流水號, '演化')
	return 流水號
設定編修狀況 = 資料庫連線.prepare('UPDATE "言語"."編修" ' +
	'SET "版本"=$2 ' + ' WHERE "流水號"=$1')

揣義倒詞組合 = 資料庫連線.prepare('SELECT "主編號","反義詞" ' +
	'FROM "教育部臺灣閩南語常用詞辭典"."反義詞對應" ORDER BY "流水號"')
揣義近詞組合 = 資料庫連線.prepare('SELECT "主編號","近義詞對應" ' +
	'FROM "教育部臺灣閩南語常用詞辭典"."近義詞對應" ORDER BY "流水號"')
用主碼號揣流水號 = 資料庫連線.prepare('SELECT "流水號" FROM "言語來源"."教育部臺灣閩南語常用詞辭典來源" ' +
	'WHERE "主編號"=$1')
揣文白流水號 = 資料庫連線.prepare('SELECT "主編號","詞目","文白俗替" FROM "教育部臺灣閩南語常用詞辭典"."詞目總檔" ' +
	'WHERE "文白俗替" = \'文\' OR "文白俗替" = \'白\' ORDER BY "詞目" ASC, "文白俗替" ASC')

揣釋義 = 資料庫連線.prepare('SELECT "流水號","主編號","義項順序","詞性","釋義" ' +
	'FROM "教育部臺灣閩南語常用詞辭典"."釋義" WHERE "流水號">8016 ORDER BY "流水號"')

用釋義揣例句 = 資料庫連線.prepare('SELECT "例句","標音","例句翻譯" ' +
	'FROM "教育部臺灣閩南語常用詞辭典"."例句" WHERE "釋義編號"=$1 ORDER BY "流水號" ASC ')
用流水號揣腔口 = lambda 流水號:資料庫連線.prepare('SELECT "腔口" ' +
	'FROM "言語"."文字" WHERE "流水號"=$1').first(流水號)
設定文字組合 = 資料庫連線.prepare('UPDATE "言語"."文字" ' +
	'SET "組合"=$2 WHERE "流水號"=$1')

設定無音文字 = 資料庫連線.prepare('UPDATE "言語"."文字" ' +
	'SET "音標"=NULL WHERE "音標"=\'\'')

查詞性對照 = 資料庫連線.prepare('SELECT "詞性","詞性內容" ' +
	'FROM "教育部臺灣閩南語常用詞辭典"."詞性對照" ORDER BY "詞性" ASC ')
詞性對照表 = {詞性:詞性內容 for 詞性, 詞性內容 in 查詞性對照()}
設定詞性 = 資料庫連線.prepare('UPDATE "言語"."關係" ' +
	'SET "詞性"=$2 WHERE "流水號"=$1')
