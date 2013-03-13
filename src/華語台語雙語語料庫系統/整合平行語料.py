'''
Created on 2013/3/5

@author: Ihc
'''
from 教育部臺灣閩南語常用詞辭典.資料庫連線 import 資料庫連線
from 文章音標解析器 import 文章音標解析器
from 華語台語雙語語料庫系統.文章標點處理工具 import 文章標點處理工具
from 華語台語雙語語料庫系統.何澤政教會羅馬字音標 import 何澤政教會羅馬字音標
from 言語資料庫.公用資料 import 加文字佮版本
from 言語資料庫.公用資料 import 國語腔口
from 言語資料庫.公用資料 import 臺員
from 言語資料庫.公用資料 import 版本音標有問題
from 教育部臺灣閩南語常用詞辭典.資料庫連線 import 加關係
from 教育部臺灣閩南語常用詞辭典.資料庫連線 import 義近
from 言語資料庫.公用資料 import 加文字佮組合佮版本
from 言語資料庫.公用資料 import 語句
from 言語資料庫.公用資料 import 章表冊
from 言語資料庫.公用資料 import 版本正常
from 言語資料庫.公用資料 import 臺語腔口

揣攏總資料 = 資料庫連線.prepare('SELECT "aid","year", ' +
	'"title","title_translation","content","TaiLuo","JiaoLuo" ' +
	'FROM "華語台語雙語語料庫系統"."article_frank" WHERE "整合遏袂"=false AND ("TaiLuo"!=\'\' OR "JiaoLuo"!=\'\') ' +
	'ORDER BY "aid" DESC LIMIT 1')
整合過矣 = lambda aid: 資料庫連線.prepare('UPDATE "華語台語雙語語料庫系統"."article_frank" ' +
	'SET "整合遏袂"=true WHERE "aid"=$1')(aid)

標點符號 = {' ', '-', ',', '。', '、', '，','?',
	'；', '？', '！', '：', '"', '．',
	'「', '」', '(', ')', '『', '』', '【', '】', '《', '》', '（', '）', '＊', '…', '～', '—', '＜', '＞'}
# 臺羅解析器 = 文章音標解析器(教會羅馬字音標)
# 臺羅解析器.合法字元 = {'-', ' '}
無合法的符號 = '!!!!!!!!!!'

教羅解析器 = 文章音標解析器(何澤政教會羅馬字音標)
教羅解析器.標點符號 = 標點符號
標點處理工具 = 文章標點處理工具()
標點處理工具.標點符號 = 標點符號
# 通用解析器 = 文章音標解析器(通用拼音音標)
# 通用解析器.合法字元 = {'-', ' '}
# 「 Toa7-tiau5-hang7 」
代換字串 = [(' ', ' '), ('　', ' '), ('  ', ' '), ('  ', ' '), ('  ', ' ')]
英文詞 = {'DNA'}
空白符號 = ' '
# print(揣攏總資料.first())
# return None
for 文章編號, 西元年, 標題國語, 標題音標, 國語, 臺羅, 教羅 in 揣攏總資料():
	print(文章編號)
	if 臺羅 == '':
		內文音標 = 教羅
	else:
		內文音標 = 臺羅
	for 錯誤, 正確 in 代換字串:
		標題國語 = 標題國語.replace(錯誤, 正確)
		標題音標 = 標題音標.replace(錯誤, 正確)
		國語 = 國語.replace(錯誤, 正確)
		內文音標 = 內文音標.replace(錯誤, 正確)
	標題國語 = 標題國語.strip()
	標題音標 = 標題音標.strip()
	國語文章 = [標點處理工具.切開語句(標題國語)]
	音標文章 = [標點處理工具.切開語句(標題音標)]
# 	print(標題音標)
# 	print(標點處理工具.切開語句(標題音標))
# 	break
	標題翻譯解析結果, 標題翻譯合法無 = 教羅解析器.解析語句佮顯示毋著字元(標題音標)
	for 處理一半的國語 in 國語.split('\r\n'):
		for 一逝國語 in 處理一半的國語.split('\n'):
			一个句語的詞 = 標點處理工具.切開語句(一逝國語.strip())
			國語文章.append(一个句語的詞)
# 			for 一个詞 in 一个句語的詞:
# 				國語文章.append(一个詞)
# 				print(一个詞, end = '')
# 			print(一个句語的詞)
	for 處理一半的內文音標 in 內文音標.split('\r\n'):
		for 一逝內文音標 in 處理一半的內文音標.split('\n'):
			一个句語的詞 = 標點處理工具.切開語句(一逝內文音標.strip())
			新語句 = []
			for 一个詞 in 一个句語的詞:
				if 一个詞 in 英文詞:
					新語句.append(一个詞)
				else:
					內文翻譯解析結果, 內文翻譯合法無 = 教羅解析器.解析語句佮顯示毋著字元(一个詞, True)
					if not 內文翻譯合法無:
						print('「' + 一个詞 + '」是英文諾？')
						新語句.append(內文翻譯解析結果 + 無合法的符號)
					else:
						新語句.append(內文翻譯解析結果)
			if 一个句語的詞 != [] or len(音標文章) != len(國語文章):
				音標文章.append(新語句)
# 				print(內文翻譯解析結果, end = '')
# 			print(一个句語的詞)
# 			print(音標文章[-1])
# 			print()
# 	print(len(國語文章))
# 	print(len(音標文章))
	長度 = (len(國語文章), len(音標文章))
	print('語句數量=' + str(長度))
	if min(長度) != max(長度):
# 		print(國語文章)
# 		print(音標文章)
		綜合文章 = []
		for i in range(min(長度)):
			綜合文章.append((國語文章[i], 音標文章[i]))
		print(綜合文章)
		# 無愛輸入到資料庫
	else:
		臺語規篇版本 = 版本正常
		國語流水號組合 = '#,'
		音標流水號組合 = '#,'
		國語文 = []
		音標文 = []
		for i in range(長度[0]):
			舊國語語句 = 國語文章[i]
			舊音標語句 = 音標文章[i]
			國語長度 = len(舊國語語句)
			音標長度 = len(舊音標語句)
			語句長度 = (國語長度, 音標長度)
			有對齊無 = True
			if min(語句長度) != max(語句長度):
		# 		print(國語文章)
		# 		print(音標文章)
# 				綜合文章 = []
# 				for j in range(min(語句長度)):
# 					綜合文章.append((舊國語語句[j], 舊音標語句[j]))
# 				print(綜合文章)
				國語位置 = 0
				音標位置 = 0
				綜合文章 = []
				while  國語位置 < 國語長度 and 音標位置 < 音標長度:
					國語詞長度 = 標點處理工具.計算漢字語句漢字數量(舊國語語句[國語位置])
					音標詞長度 = 標點處理工具.計算音標語句音標數量(舊音標語句[音標位置])
# 					print((國語詞長度,音標詞長度))
# 					print(標點處理工具.計算音標語句音標數量(舊音標語句[音標位置 + 2]))
					if 舊國語語句[國語位置] == '的' and not 舊音標語句[音標位置].startswith('e5'):
						綜合文章.append((舊國語語句[國語位置], ''))
						國語位置 += 1
						音標位置 -= 1
					elif 國語詞長度 <= 音標詞長度:
						綜合文章.append((舊國語語句[國語位置], 舊音標語句[音標位置]))
					else:
						新音標詞 = 舊音標語句[音標位置]
						while 音標位置 + 2 < 音標長度 and 舊音標語句[音標位置 + 1] == ' ' and 國語詞長度 >= 音標詞長度 + \
							標點處理工具.計算音標語句音標數量(舊音標語句[音標位置 + 2]) and \
							舊音標語句[音標位置 + 2] != '':
							新音標詞 += 舊音標語句[音標位置 + 1]
							新音標詞 += 舊音標語句[音標位置 + 2]
							音標詞長度 += 標點處理工具.計算音標語句音標數量(舊音標語句[音標位置 + 2])
							音標位置 += 2
						綜合文章.append((舊國語語句[國語位置], 新音標詞))
					國語位置 += 1
					音標位置 += 1
				if 國語位置 < 國語長度 or 音標位置 < 音標長度:
					print(綜合文章)
					print((舊國語語句[國語位置:], 舊音標語句[音標位置:]))
					有對齊無 = False
				else:
					國語文章[i] = [國語 for 國語, 臺語音標 in 綜合文章]
					音標文章[i] = [臺語音標 for 國語, 臺語音標 in 綜合文章]
# 			print((國語文章[i], 音標文章[i]))
			if 有對齊無:
				國語句流水號組合 = '#,'
				臺語句流水號組合 = '#,'
				臺語規句版本 = 版本正常
				國語句 = ''
				臺語句 = ''
				綜合文章 = [ (國語文章[i][j], 音標文章[i][j]) for j in range(len(國語文章[i]))]
				for 國語, 臺語音標 in 綜合文章:
					if 國語 == 空白符號 and 臺語音標 == 空白符號:
						臺語句 += 臺語音標
						continue
					國語流水號 = 加文字佮版本('華語台語雙語語料庫系統', '字詞', 國語腔口, 臺員, 西元年 - 1911,
							國語, '', 版本正常)
# 					國語流水號 = 揣文字上大流水號()
					臺語版本 = 版本正常
					if 臺語音標.endswith(無合法的符號):
						臺語音標 = 臺語音標[:-len(無合法的符號)]
						臺語版本 = 版本音標有問題
						臺語規句版本 = 版本音標有問題
						臺語規篇版本 = 版本音標有問題
					臺語流水號 = 加文字佮版本('華語台語雙語語料庫系統', '字詞', 臺語腔口, 臺員, 西元年 - 1911,
						國語, 臺語音標, 臺語版本)
# 					臺語流水號 = 揣文字上大流水號()
					國語關係流水號 = 加關係(國語流水號, 臺語流水號, 義近, '')
					臺語關係流水號 = 加關係(臺語流水號, 國語流水號, 義近, '')
					國語句流水號組合 += str(國語關係流水號) + ','
					臺語句流水號組合 += str(臺語關係流水號) + ','
# 					國語句流水號組合 += str(國語流水號) + ','
# 					臺語句流水號組合 += str(臺語流水號) + ','
					國語句 += 國語
					臺語句 += 臺語音標
				國語句流水號組合 += '#'
				臺語句流水號組合 += '#'
				國語句 = 國語句.replace(' ', '')

				國語流水號 = 加文字佮組合佮版本('華語台語雙語語料庫系統', 語句, 國語腔口, 臺員, 西元年 - 1911,
					國語句, '', 國語句流水號組合, 版本正常)
# 				國語流水號 = 揣文字上大流水號()
				臺語版本 = 版本正常
				臺語流水號 = 加文字佮組合佮版本('華語台語雙語語料庫系統', 語句, 臺語腔口, 臺員, 西元年 - 1911,
					國語句, 臺語句, 臺語句流水號組合, 臺語規句版本)
# 				臺語流水號 = 揣文字上大流水號()
				國語關係流水號 = 加關係(國語流水號, 臺語流水號, 義近, '')
				臺語關係流水號 = 加關係(臺語流水號, 國語流水號, 義近, '')
				國語流水號組合 += str(國語關係流水號) + ','
				音標流水號組合 += str(臺語關係流水號) + ','
# 				國語流水號組合 += str(國語流水號) + ','
# 				音標流水號組合 += str(臺語流水號) + ','
			else:
				臺語規句版本 = 版本正常
				國語句 = ''
				臺語句 = ''
				綜合文章 = [ (國語文章[i][j], 音標文章[i][j]) for j in range(len(國語文章[i]))]
				for 國語, 臺語音標 in 綜合文章:
					if 國語 == 空白符號 and 臺語音標 == 空白符號:
						臺語句 += 臺語音標
						continue
					if 臺語音標.endswith(無合法的符號):
						臺語音標 = 臺語音標[:-len(無合法的符號)]
						臺語規句版本 = 版本音標有問題
						臺語規篇版本 = 版本音標有問題
					國語句 += 國語
					臺語句 += 臺語音標
				國語句 = 國語句.replace(' ', '')

				國語流水號 = 加文字佮版本('華語台語雙語語料庫系統', 語句, 國語腔口, 臺員, 西元年 - 1911,
					國語句, '', 版本正常)
# 				國語流水號 = 揣文字上大流水號()
				臺語版本 = 版本正常
				臺語流水號 = 加文字佮版本('華語台語雙語語料庫系統', 語句, 臺語腔口, 臺員, 西元年 - 1911, 國語句, 臺語句, 臺語規句版本)
# 				臺語流水號 = 揣文字上大流水號()
				國語關係流水號 = 加關係(國語流水號, 臺語流水號, 義近, '')
				臺語關係流水號 = 加關係(臺語流水號, 國語流水號, 義近, '')
				國語流水號組合 += str(國語關係流水號) + ','
				音標流水號組合 += str(臺語關係流水號) + ','
# 				國語流水號組合 += str(國語流水號) + ','
# 				音標流水號組合 += str(臺語流水號) + ','
			國語文.append(國語句)
			音標文.append(臺語句)
		國語文章 = ''.join(國語文)
		音標文章 = ' '.join(音標文)
		國語流水號組合 += '#'
		音標流水號組合 += '#'
		國語流水號 = 加文字佮組合佮版本('華語台語雙語語料庫系統', 章表冊, 國語腔口, 臺員, 西元年 - 1911,
			國語文章, '', 國語流水號組合, 版本正常)
# 		國語流水號 = 揣文字上大流水號()
		臺語版本 = 版本正常
		臺語流水號 = 加文字佮組合佮版本('華語台語雙語語料庫系統', 章表冊, 臺語腔口, 臺員, 西元年 - 1911,
			國語文章, 音標文章, 音標流水號組合, 臺語規篇版本)
# 		臺語流水號 = 揣文字上大流水號()
		加關係(國語流水號, 臺語流水號, 義近, '')
		加關係(臺語流水號, 國語流水號, 義近, '')

		整合過矣(文章編號)



