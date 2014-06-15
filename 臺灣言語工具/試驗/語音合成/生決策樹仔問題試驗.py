# -*- coding, utf-8 -*-
"""
著作權所有 (C) 民國102年 意傳文化科技
開發者：薛丞宏
網址：http,//意傳.台灣
語料來源：請看各資料庫內說明

本程式乃自由軟體，您必須遵照SocialCalc設計的通用公共授權（Common Public Attribution License, CPAL)來修改和重新發佈這一程式，詳情請參閱條文。授權大略如下，若有歧異，以授權原文為主：
	１．得使用、修改、複製並發佈此程式碼，且必須以通用公共授權發行；
	２．任何以程式碼衍生的執行檔或網路服務，必須公開該程式碼；
	３．將此程式的原始碼當函式庫引用入商業軟體，且不需公開非關此函式庫的任何程式碼

此開放原始碼、共享軟體或說明文件之使用或散佈不負擔保責任，並拒絕負擔因使用上述軟體或說明文件所致任何及一切賠償責任或損害。

臺灣言語工具緣起於本土文化推廣與傳承，非常歡迎各界用於商業軟體，但希望在使用之餘，能夠提供建議、錯誤回報或修補，回饋給這塊土地。

感謝您的使用與推廣～～勞力！承蒙！
"""
import unittest
from 臺灣言語工具.語音合成.生決策樹仔問題 import 生決策樹仔問題
from 臺灣言語工具.解析整理.解析錯誤 import 解析錯誤

class 生決策樹仔問題試驗(unittest.TestCase):
	def setUp(self):
		self.生問題 = 生決策樹仔問題()
	def tearDown(self):
		pass

	def test_頭前空(self):
		資料 = [('i', ['i']), ('e', ['e']), ]
		答案 = {
			'QS "中央是i" { "*-i+*" }',
			'QS "中央是e" { "*-e+*" }',
			'QS "頭前是i" { "i-*" }',
			'QS "頭前是i、e" { "i-*","e-*" }',
			'QS "後壁是i" { "*+i/*" }',
			'QS "後壁是e" { "*+e/*" }',
		}
	def test_後壁空(self):
		資料 = [('i', ['i']), ('e', ['e']), ]
		答案 = {
			'QS "中央是i" { "*-i+*" }',
			'QS "中央是e" { "*-e+*" }',
			'QS "頭前是i" { "*音：i-*" }',
			'QS "頭前是e" { "*音：e-*" }',
			'QS "後壁是i" { "*+i" }',
			'QS "後壁是e" { "*+e" }',
		}
		self.assertEqual(
			self.生問題.問題集(
				資料, ('音：', '-', '+', ''), '孤條',),
			答案)
	def test_頭前有物件(self):
		資料 = [('i', ['i']), ('e', ['e']), ]
		答案 = {
			'QS "中央是i" { "*Xi+*" }',
			'QS "中央是e" { "*Xe+*" }',
			'QS "頭前是i" { "*ZZiX*" }',
			'QS "頭前是e" { "*ZZeX*" }',
			'QS "後壁是i" { "*+i＠＠*" }',
			'QS "後壁是e" { "*+e＠＠*" }',
		}
		self.assertEqual(
			self.生問題.問題集(
				資料, ('ZZ', 'X', '+', '＠＠'), '孤條',),
			答案)
	def test_一類兩个物件(self):
		資料 = [('i類', ['i', 'ii', 'iii']), ('e類', ['e']), ('a類', ['*a*']) ]
		答案 = {
			'QS "頭前是i類" { "*$i-*","*$ii-*","*$iii-*" }',
			'QS "頭前是e類" { "*$e-*" }',
			'QS "頭前是a類" { "*$*a*-*" }',
			'QS "中央是i類" { "*-i+*","*-ii+*","*-iii+*" }',
			'QS "中央是e類" { "*-e+*" }',
			'QS "中央是a類" { "*-*a*+*" }',
			'QS "後壁是i類" { "*+i/*","*+ii/*","*+iii/*" }',
			'QS "後壁是e類" { "*+e/*" }',
			'QS "後壁是a類" { "*+*a*/*" }',
		}
		self.assertEqual(
			self.生問題.問題集(
				資料, ('$', '-', '+', '/'), '孤條',),
			答案)
		
	def test_種類毋著(self):
		'''1 2 3'''
		self.assertRaises(解析錯誤,self.生問題.問題集,
				self.看排法資料, ('', '-', '+', '/'), '攏愛',)
		
	def test_孤條(self):
		'''1 2 3'''
		self.assertEqual(
			self.生問題.問題集(
				self.看排法資料, ('', '-', '+', '/'), '孤條',),
			self.孤條答案)

	def test_連紲(self):
		'''1 12 123 123 2 23 3'''
		self.assertEqual(
			self.生問題.問題集(
				self.看排法資料, ('', '-', '+', '/'), '連紲',),
			self.連紲答案)

	def test_組合(self):
		''' 1 12 123 13 2 23 3'''
		self.assertEqual(
			self.生問題.問題集(
				self.看排法資料, ('', '-', '+', '/'), '組合',),
			self.組合答案)

	看排法資料 = [('i', ['i']), ('e', ['e']), ('a', ['a']), ('o', ['o', 'ə']), ('u', ['u']), ]
	孤條答案 = {
		'QS "中央是i" { "*-i+*" }',
		'QS "中央是e" { "*-e+*" }',
		'QS "中央是a" { "*-a+*" }',
		'QS "中央是o" { "*-o+*","*-ə+*" }',
		'QS "中央是u" { "*-u+*" }',
		'QS "頭前是i" { "i-*" }',
		'QS "頭前是e" { "e-*" }',
		'QS "頭前是a" { "a-*" }',
		'QS "頭前是o" { "o-*","ə-*" }',
		'QS "頭前是u" { "u-*" }',
		'QS "後壁是i" { "*+i/*" }',
		'QS "後壁是e" { "*+e/*" }',
		'QS "後壁是a" { "*+a/*" }',
		'QS "後壁是o" { "*+o/*","*+ə/*" }',
		'QS "後壁是u" { "*+u/*" }',
		}
	連紲答案 = {
		'QS "中央是i" { "*-i+*" }',
		'QS "中央是i、e" { "*-i+*","*-e+*" }',
		'QS "中央是i、e、a" { "*-i+*","*-e+*","*-a+*" }',
		'QS "中央是i、e、a、o" { "*-i+*","*-e+*","*-a+*","*-o+*","*-ə+*" }',
		'QS "中央是i、e、a、o、u" { "*-i+*","*-e+*","*-a+*","*-o+*","*-ə+*","*-u+*" }',
		'QS "中央是e" { "*-e+*" }',
		'QS "中央是e、a" { "*-e+*","*-a+*" }',
		'QS "中央是e、a、o" { "*-e+*","*-a+*","*-o+*","*-ə+*" }',
		'QS "中央是e、a、o、u" { "*-e+*","*-a+*","*-o+*","*-ə+*","*-u+*" }',
		'QS "中央是a" { "*-a+*" }',
		'QS "中央是a、o" { "*-a+*","*-o+*","*-ə+*" }',
		'QS "中央是a、o、u" { "*-a+*","*-o+*","*-ə+*","*-u+*" }',
		'QS "中央是o" { "*-o+*","*-ə+*" }',
		'QS "中央是o、u" { "*-o+*","*-ə+*","*-u+*" }',
		'QS "中央是u" { "*-u+*" }',
		'QS "頭前是i" { "i-*" }',
		'QS "頭前是i、e" { "i-*","e-*" }',
		'QS "頭前是i、e、a" { "i-*","e-*","a-*" }',
		'QS "頭前是i、e、a、o" { "i-*","e-*","a-*","o-*","ə-*" }',
		'QS "頭前是i、e、a、o、u" { "i-*","e-*","a-*","o-*","ə-*","u-*" }',
		'QS "頭前是e" { "e-*" }',
		'QS "頭前是e、a" { "e-*","a-*" }',
		'QS "頭前是e、a、o" { "e-*","a-*","o-*","ə-*" }',
		'QS "頭前是e、a、o、u" { "e-*","a-*","o-*","ə-*","u-*" }',
		'QS "頭前是a" { "a-*" }',
		'QS "頭前是a、o" { "a-*","o-*","ə-*" }',
		'QS "頭前是a、o、u" { "a-*","o-*","ə-*","u-*" }',
		'QS "頭前是o" { "o-*","ə-*" }',
		'QS "頭前是o、u" { "o-*","ə-*","u-*" }',
		'QS "頭前是u" { "u-*" }',
		'QS "後壁是i" { "*+i/*" }',
		'QS "後壁是i、e" { "*+i/*","*+e/*" }',
		'QS "後壁是i、e、a" { "*+i/*","*+e/*","*+a/*" }',
		'QS "後壁是i、e、a、o" { "*+i/*","*+e/*","*+a/*","*+o/*","*+ə/*" }',
		'QS "後壁是i、e、a、o、u" { "*+i/*","*+e/*","*+a/*","*+o/*","*+ə/*","*+u/*" }',
		'QS "後壁是e" { "*+e/*" }',
		'QS "後壁是e、a" { "*+e/*","*+a/*" }',
		'QS "後壁是e、a、o" { "*+e/*","*+a/*","*+o/*","*+ə/*" }',
		'QS "後壁是e、a、o、u" { "*+e/*","*+a/*","*+o/*","*+ə/*","*+u/*" }',
		'QS "後壁是a" { "*+a/*" }',
		'QS "後壁是a、o" { "*+a/*","*+o/*","*+ə/*" }',
		'QS "後壁是a、o、u" { "*+a/*","*+o/*","*+ə/*","*+u/*" }',
		'QS "後壁是o" { "*+o/*","*+ə/*" }',
		'QS "後壁是o、u" { "*+o/*","*+ə/*","*+u/*" }',
		'QS "後壁是u" { "*+u/*" }',
		}
	組合答案 = {
		'QS "中央是i" { "*-i+*" }',
		'QS "中央是i、e" { "*-i+*","*-e+*" }',
		'QS "中央是i、e、a" { "*-i+*","*-e+*","*-a+*" }',
		'QS "中央是i、e、a、o" { "*-i+*","*-e+*","*-a+*","*-o+*","*-ə+*" }',
		'QS "中央是i、e、a、o、u" { "*-i+*","*-e+*","*-a+*","*-o+*","*-ə+*","*-u+*" }',
		'QS "中央是i、e、a、u" { "*-i+*","*-e+*","*-a+*","*-u+*" }',
		'QS "中央是i、e、o" { "*-i+*","*-e+*","*-o+*","*-ə+*" }',
		'QS "中央是i、e、o、u" { "*-i+*","*-e+*","*-o+*","*-ə+*","*-u+*" }',
		'QS "中央是i、e、u" { "*-i+*","*-e+*","*-u+*" }',
		'QS "中央是i、a" { "*-i+*","*-a+*" }',
		'QS "中央是i、a、o" { "*-i+*","*-a+*","*-o+*","*-ə+*" }',
		'QS "中央是i、a、o、u" { "*-i+*","*-a+*","*-o+*","*-ə+*","*-u+*" }',
		'QS "中央是i、a、u" { "*-i+*","*-a+*","*-u+*" }',
		'QS "中央是i、o" { "*-i+*","*-o+*","*-ə+*" }',
		'QS "中央是i、o、u" { "*-i+*","*-o+*","*-ə+*","*-u+*" }',
		'QS "中央是i、u" { "*-i+*","*-o+*","*-ə+*","*-u+*" }',
		'QS "中央是e" { "*-e+*" }',
		'QS "中央是e、a" { "*-e+*","*-a+*" }',
		'QS "中央是e、a、o" { "*-e+*","*-a+*","*-o+*","*-ə+*" }',
		'QS "中央是e、a、o、u" { "*-e+*","*-a+*","*-o+*","*-ə+*","*-u+*" }',
		'QS "中央是e、a、u" { "*-e+*","*-a+*","*-o+*","*-ə+*","*-u+*" }',
		'QS "中央是e、o" { "*-e+*","*-o+*","*-ə+*" }',
		'QS "中央是e、o、u" { "*-e+*","*-o+*","*-ə+*","*-u+*" }',
		'QS "中央是e、u" { "*-e+*","*-u+*" }',
		'QS "中央是a" { "*-a+*" }',
		'QS "中央是a、o" { "*-a+*","*-o+*","*-ə+*" }',
		'QS "中央是a、o、u" { "*-a+*","*-o+*","*-ə+*","*-u+*" }',
		'QS "中央是a、u" { "*-a+*","*-u+*" }',
		'QS "中央是o" { "*-o+*","*-ə+*" }',
		'QS "中央是o、u" { "*-o+*","*-ə+*","*-u+*" }',
		'QS "中央是u" { "*-o+*","*-ə+*","*-u+*" }',
		'QS "頭前是i" { "i-*" }',
		'QS "頭前是i、e" { "i-*","e-*" }',
		'QS "頭前是i、e、a" { "i-*","e-*","a-*" }',
		'QS "頭前是i、e、a、o" { "i-*","e-*","a-*","o-*","ə-*" }',
		'QS "頭前是i、e、a、o、u" { "i-*","e-*","a-*","o-*","ə-*","u-*" }',
		'QS "頭前是i、e、a、u" { "i-*","e-*","a-*","u-*" }',
		'QS "頭前是i、e、o" { "i-*","e-*","o-*","ə-*" }',
		'QS "頭前是i、e、o、u" { "i-*","e-*","o-*","ə-*","u-*" }',
		'QS "頭前是i、e、u" { "i-*","e-*","u-*" }',
		'QS "頭前是i、a" { "i-*","a-*" }',
		'QS "頭前是i、a、o" { "i-*","a-*","o-*","ə-*" }',
		'QS "頭前是i、a、o、u" { "i-*","a-*","o-*","ə-*","u-*" }',
		'QS "頭前是i、a、u" { "i-*","a-*","u-*" }',
		'QS "頭前是i、o" { "i-*","o-*","ə-*" }',
		'QS "頭前是i、o、u" { "i-*","o-*","ə-*","u-*" }',
		'QS "頭前是i、u" { "i-*","o-*","ə-*","u-*" }',
		'QS "頭前是e" { "e-*" }',
		'QS "頭前是e、a" { "e-*","a-*" }',
		'QS "頭前是e、a、o" { "e-*","a-*","o-*","ə-*" }',
		'QS "頭前是e、a、o、u" { "e-*","a-*","o-*","ə-*","u-*" }',
		'QS "頭前是e、a、u" { "e-*","a-*","o-*","ə-*","u-*" }',
		'QS "頭前是e、o" { "e-*","o-*","ə-*" }',
		'QS "頭前是e、o、u" { "e-*","o-*","ə-*","u-*" }',
		'QS "頭前是e、u" { "e-*","u-*" }',
		'QS "頭前是a" { "a-*" }',
		'QS "頭前是a、o" { "a-*","o-*","ə-*" }',
		'QS "頭前是a、o、u" { "a-*","o-*","ə-*","u-*" }',
		'QS "頭前是a、u" { "a-*","u-*" }',
		'QS "頭前是o" { "o-*","ə-*" }',
		'QS "頭前是o、u" { "o-*","ə-*","u-*" }',
		'QS "頭前是u" { "o-*","ə-*","u-*" }',
		'QS "後壁是i" { "*+i/*" }',
		'QS "後壁是i、e" { "*+i/*","*+e/*" }',
		'QS "後壁是i、e、a" { "*+i/*","*+e/*","*+a/*" }',
		'QS "後壁是i、e、a、o" { "*+i/*","*+e/*","*+a/*","*+o/*","*+ə/*" }',
		'QS "後壁是i、e、a、o、u" { "*+i/*","*+e/*","*+a/*","*+o/*","*+ə/*","*+u/*" }',
		'QS "後壁是i、e、a、u" { "*+i/*","*+e/*","*+a/*","*+u/*" }',
		'QS "後壁是i、e、o" { "*+i/*","*+e/*","*+o/*","*+ə/*" }',
		'QS "後壁是i、e、o、u" { "*+i/*","*+e/*","*+o/*","*+ə/*","*+u/*" }',
		'QS "後壁是i、e、u" { "*+i/*","*+e/*","*+u/*" }',
		'QS "後壁是i、a" { "*+i/*","*+a/*" }',
		'QS "後壁是i、a、o" { "*+i/*","*+a/*","*+o/*","*+ə/*" }',
		'QS "後壁是i、a、o、u" { "*+i/*","*+a/*","*+o/*","*+ə/*","*+u/*" }',
		'QS "後壁是i、a、u" { "*+i/*","*+a/*","*+u/*" }',
		'QS "後壁是i、o" { "*+i/*","*+o/*","*+ə/*" }',
		'QS "後壁是i、o、u" { "*+i/*","*+o/*","*+ə/*","*+u/*" }',
		'QS "後壁是i、u" { "*+i/*","*+o/*","*+ə/*","*+u/*" }',
		'QS "後壁是e" { "*+e/*" }',
		'QS "後壁是e、a" { "*+e/*","*+a/*" }',
		'QS "後壁是e、a、o" { "*+e/*","*+a/*","*+o/*","*+ə/*" }',
		'QS "後壁是e、a、o、u" { "*+e/*","*+a/*","*+o/*","*+ə/*","*+u/*" }',
		'QS "後壁是e、a、u" { "*+e/*","*+a/*","*+o/*","*+ə/*","*+u/*" }',
		'QS "後壁是e、o" { "*+e/*","*+o/*","*+ə/*" }',
		'QS "後壁是e、o、u" { "*+e/*","*+o/*","*+ə/*","*+u/*" }',
		'QS "後壁是e、u" { "*+e/*","*+u/*" }',
		'QS "後壁是a" { "*+a/*" }',
		'QS "後壁是a、o" { "*+a/*","*+o/*","*+ə/*" }',
		'QS "後壁是a、o、u" { "*+a/*","*+o/*","*+ə/*","*+u/*" }',
		'QS "後壁是a、u" { "*+a/*","*+u/*" }',
		'QS "後壁是o" { "*+o/*","*+ə/*" }',
		'QS "後壁是o、u" { "*+o/*","*+ə/*","*+u/*" }',
		'QS "後壁是u" { "*+o/*","*+ə/*","*+u/*" }',
		}
