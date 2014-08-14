# -*- coding: utf-8 -*-
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
# 竺家寧(1992)《聲韻學》p.76-8
官話注音符號對照音值聲母表 = {
	'ㄅ':'p', 'ㄆ':'pʰ', 'ㄇ':'m', 'ㄈ':'f',
	'ㄉ':'t', 'ㄊ':'tʰ', 'ㄋ':'n', 'ㄌ':'l',
	'ㄍ':'k', 'ㄎ':'kʰ', 'ㄏ':'h',
	'ㄐ':'tɕ', 'ㄑ':'tɕʰ', 'ㄒ':'ɕ',
	'ㄓ':'tʂ', 'ㄔ':'tʂʰ', 'ㄕ':'ʂ', 'ㄖ':'ʐ',
	'ㄗ':'ts', 'ㄘ':'tsʰ', 'ㄙ':'s', '':'ʔ',
}

官話注音符號對照音值韻母表 = {
	'':'ï', 'ㄧ':'i', 'ㄨ':'u', 'ㄩ':'y',
	'ㄚ':'a', 'ㄛ':'o', 'ㄜ':'ɤ', 'ㄝ':'e',
	'ㄞ':'ai', 'ㄟ':'ei', 'ㄠ':'au', 'ㄡ':'ou',
	'ㄢ':'an', 'ㄣ':'ən', 'ㄤ':'aŋ', 'ㄥ':'əŋ', 'ㄦ':'ɚ',
	'ㄧㄚ':'ia', 'ㄧㄛ':'io', 'ㄧㄝ':'ie', 'ㄧㄞ':'iai',
	'ㄧㄠ':'iau', 'ㄧㄡ':'iou',
	'ㄧㄢ':'ien', 'ㄧㄣ':'in', 'ㄧㄤ':'iaŋ', 'ㄧㄥ':'iŋ',
	'ㄨㄚ':'ua', 'ㄨㄛ':'uo', 'ㄨㄞ':'uai', 'ㄨㄟ':'uei',
	'ㄨㄢ':'uan', 'ㄨㄣ':'uən', 'ㄨㄤ':'uaŋ', 'ㄨㄥ':'uŋ',
	'ㄩㄝ':'ye', 'ㄩㄢ':'yen', 'ㄩㄣ':'yn', 'ㄩㄥ':'yuŋ',
	}

官話韻母實際音值表 = {'sï':'ɿ', 'ʂï' : 'ʅ', 'tuŋ' : 'oŋ'}
官話韻母實際音值表.update(官話注音符號對照音值韻母表)

class 官話注音符號轉音值模組():
	聲母表 = 官話注音符號對照音值聲母表
	韻母表 = 官話注音符號對照音值韻母表
	唇音 = {'p', 'pʰ', 'm', 'f', }
	def 轉(self, 聲, 韻, 調):
		if 聲 == None or 韻 == None or 調 == None:
			return
		音值聲 = self.聲母表[聲]
		音值韻 = self.韻母表[韻]
		if 音值韻 == 'ï':
			if 's' in 音值聲:  # 舌尖前音
				音值韻 = 'ɿ'
			elif 'ʂ' in 音值聲:  # 舌尖前音
				音值韻 = 'ʅ'
			else:
				raise RuntimeError('函式庫有問題！！')
		elif 音值韻 == 'o':
			if 音值聲 in self.唇音:
				音值韻 = 'uo'
		elif 音值韻 == 'uŋ':
			if 音值聲 != 'ʔ':
				音值韻 = 'oŋ'
		音值調 = 調
		return (音值聲, 音值韻, 音值調)
