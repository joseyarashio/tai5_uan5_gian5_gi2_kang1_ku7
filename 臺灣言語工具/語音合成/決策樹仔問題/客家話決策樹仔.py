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
from 臺灣言語工具.語音合成.決策樹仔問題.公家決策樹仔 import 公家決策樹仔
from 臺灣言語工具.語音合成.生決策樹仔問題 import 生決策樹仔問題
from 臺灣言語工具.音標系統.客話.臺灣客家話拼音 import 臺灣客家話拼音調類對照表
import itertools
from 臺灣言語工具.音標系統.客話.臺灣客家話拼音轉音值模組 import 臺灣客家話拼音聲母實際音值表
from 臺灣言語工具.音標系統.客話.臺灣客家話拼音轉音值模組 import 臺灣客家話拼音對照音值韻母表

class 客家話決策樹仔(公家決策樹仔):
	_生問題 = 生決策樹仔問題()
	聲韻符號 = ('', '-', '+', '/調:')
	調符號 = ('/調:', '<', '>', '/詞:')
	詞符號 = ('/詞:', '!', '@', '/句:')
	句符號 = ('/句:', '^', '_', '')
	def 生(self):
		問題 = set()
		問題 |= self.孤聲韻()
		print(len(問題))
		問題 |= self.元音分韻()
		print(len(問題))
		問題 |= self.孤元音()
		print(len(問題))
		問題 |= self.陰聲韻()
		print(len(問題))
		問題 |= self.鼻化韻佮聲化韻()
		print(len(問題))
		問題 |= self.韻尾()
		print(len(問題))
		問題 |= self.輔音()
		print(len(問題))
		問題 |= self.全部調()
		print(len(問題))
		問題 |= self.詞句長度(10, 20)
		print(len(問題))

		self._生問題.檢查(問題)
		return 問題
	def 孤聲韻(self):
		聲韻 = []
		for 實際音 in itertools.chain(
				['sil', 'sp', ],
				臺灣客家話拼音聲母實際音值表.values(),
				臺灣客家話拼音對照音值韻母表.values()):
			聲韻.append(('{0}'.format(實際音), [實際音]))
		return self._生問題.問題集(聲韻, self.聲韻符號, '孤條')
	def 元音分韻(self):
		全部元音題目 = [('全部韻', ['*i*', '*ï*', '*u*', '*e*', '*ə*', '*o*', '*ɛ*', '*ɔ*', '*a*', ])]
		元音 = self._生問題.問題集(全部元音題目, self.聲韻符號, '孤條')
		懸低元音題目 = [
			('懸元音韻', ['*i*', '*ï*', '*u*']),
			('中懸元音韻', ['*e*', '*ə*', '*o*', ]),
			('中低元音韻', ['*ɛ*', '*ɔ*', ]),
			('低元音韻', ['*a*', ])
			]
		元音 |= self._生問題.問題集(懸低元音題目, self.聲韻符號, '孤條')
		前後元音題目 = [
			('前元音韻', ['*i*', '*e*', '*ɛ*', ]),
			('央元音韻', ['*ï*', '*ə*', '*a*', ]),
			('後元音韻', ['*ɔ*', '*o*', '*u*'])
			]
		元音 |= self._生問題.問題集(前後元音題目, self.聲韻符號, '孤條')
		孤元音題目 = [	]
		for 元音韻種類 in 全部元音題目[0][1]:
			孤元音題目.append(
				('{}元音韻'.format(元音韻種類[1:-1]), [元音韻種類]))
		元音 |= self._生問題.問題集(孤元音題目, self.聲韻符號, '孤條')
		return 元音
	def 孤元音(self):
		全部元音題目 = [('全部孤元音', ['i', 'ï', 'u', 'e', 'ə', 'o', 'ɛ', 'ɔ', 'a', ])]
		元音 = self._生問題.問題集(全部元音題目, self.聲韻符號, '孤條')
		懸低元音題目 = [
			('懸孤元音', ['i', 'ï', 'u']),
			('中懸孤元音', ['e', 'ə', 'o', ]),
			('中低孤元音', ['ɛ', 'ɔ', ]),
			('低孤元音', ['a', ])
			]
		元音 |= self._生問題.問題集(懸低元音題目, self.聲韻符號, '孤條')
		前後元音題目 = [
			('前孤元音', ['i', 'e', 'ɛ', ]),
			('央孤元音', ['ï', 'ə', 'a', ]),
			('後孤元音', ['ɔ', 'o', 'u'])
			]
		元音 |= self._生問題.問題集(前後元音題目, self.聲韻符號, '孤條')
		孤元音題目 = [	]
		for 元音韻種類 in 全部元音題目[0][1]:
			孤元音題目.append(
				('孤{}元音'.format(元音韻種類), [元音韻種類]))
		元音 |= self._生問題.問題集(孤元音題目, self.聲韻符號, '孤條')
		return 元音
	def 陰聲韻(self):
		全部元音題目 = [('全部陰聲韻', ['*i', '*ï', '*u', '*e', '*ə', '*o', '*ɛ', '*ɔ', '*a', ])]
		陰聲韻 = self._生問題.問題集(全部元音題目, self.聲韻符號, '孤條')
		尾懸低元音題目 = [
			('尾懸陰聲韻', ['*i', '*ï', '*u']),
			('尾中懸陰聲韻', ['*e', '*ə', '*o', ]),
			('尾中低陰聲韻', ['*ɛ', '*ɔ', ]),
			('尾低陰聲韻', ['*a', ])
			]
		陰聲韻 |= self._生問題.問題集(尾懸低元音題目, self.聲韻符號, '孤條')
		尾前後元音題目 = [
			('尾前陰聲韻', ['*i', '*e', '*ɛ', ]),
			('尾央陰聲韻', ['*ï', '*ə', '*a', ]),
			('尾後陰聲韻', ['*o', '*ɔ', '*u'])
			]
		陰聲韻 |= self._生問題.問題集(尾前後元音題目, self.聲韻符號, '孤條')
		孤元音題目 = [	]
		for 元音韻種類 in 全部元音題目[0][1]:
			孤元音題目.append(
				('尾{}陰聲韻'.format(元音韻種類[1:]), [元音韻種類]))
		陰聲韻 |= self._生問題.問題集(孤元音題目, self.聲韻符號, '孤條')

		頭懸低元音題目 = [
			('頭懸陰聲韻', ['i*', 'ï*', 'u*']),
			('頭中懸陰聲韻', ['e*', 'ə*', 'o*', ]),
			('頭中低陰聲韻', ['ɛ*', 'ɔ*', ]),
			('頭低陰聲韻', ['a*', ])
			]
		陰聲韻 |= self._生問題.問題集(頭懸低元音題目, self.聲韻符號, '孤條')
		頭前後元音題目 = [
			('頭前陰聲韻', ['i*', 'e*', 'ɛ*', ]),
			('頭央陰聲韻', ['ï*', 'ə*', 'a*', ]),
			('頭後陰聲韻', ['o*', 'ɔ*', 'u*'])
			]
		陰聲韻 |= self._生問題.問題集(頭前後元音題目, self.聲韻符號, '孤條')
		孤元音題目 = [	]
		for 元音韻種類 in 全部元音題目[0][1]:
			孤元音題目.append(
				('頭{}陰聲韻'.format(元音韻種類[1:]), [元音韻種類]))
		陰聲韻 |= self._生問題.問題集(孤元音題目, self.聲韻符號, '孤條')
		return 陰聲韻
	def 鼻化韻佮聲化韻(self):
		懸低鼻化音題目 = [
			('懸鼻化韻', ['iⁿ', 'ïⁿ', 'n̩', 'ŋ̩', ]),
			('中懸鼻化韻', ['eⁿ', 'oⁿ', ]),
			('中低鼻化韻', ['ɛⁿ', 'ɔⁿ', ]),
			('低鼻化韻', ['m̩', 'aⁿ', ])
			]
		前後鼻化音題目 = [
			('唇鼻化韻', ['m̩', ]),
			('前鼻化韻', ['iⁿ', 'eⁿ', 'ɛⁿ', 'n̩', ]),
			('央鼻化韻', ['ïⁿ', 'aⁿ', ]),
			('後鼻化韻', ['ɔⁿ', 'oⁿ', 'ŋ̩', ])
			]
		佇頭題目 = []
		佇尾題目 = []
		喉塞題目 = []
		for 原本題目 in [懸低鼻化音題目, 前後鼻化音題目]:
			for 名, 內容 in 原本題目:
				佇頭題目.append(('韻頭' + 名, list(map((lambda 內容:內容 + '*'), 內容))))
				佇尾題目.append(('韻尾' + 名, list(map((lambda 內容:'*' + 內容), 內容))))
				喉塞題目.append(('喉塞' + 名, list(map((lambda 內容:'*' + 內容 + 'ʔ'), 內容))))
		鼻化韻 = set()
		for 改好題目 in [佇頭題目, 佇尾題目, 喉塞題目]:
			鼻化韻 |= self._生問題.問題集(改好題目, self.聲韻符號, '孤條')
		return 鼻化韻
	def 韻尾(self):
		韻尾題目 = [
			('陽聲韻', ['*?m', '*?n', '*?ŋ']),
			('入聲韻', ['*?p', '*?t', '*?k', '*?ʔ']),
			]
		韻尾 = self._生問題.問題集(韻尾題目, self.聲韻符號, '孤條')
		孤韻 = []
		for 非陰聲 in 韻尾題目[0][1] + 韻尾題目[1][1]:
			孤韻.append(('是{}韻尾'.format(非陰聲[2:]), [非陰聲]))
		韻尾 |= self._生問題.問題集(孤韻, self.聲韻符號, '孤條')
		return 韻尾
	def 輔音(self):
		塞擦題目 = [
			('塞音', ['p', 'pʰ', 'b', 't', 'tʰ', 'k', 'kʰ', 'g', 'ʔ', ]),
			('塞擦音', ['ts', 'tsʰ', 'dz', 'tɕ', 'tɕʰ', 'tʃ', 'tʃʰ', ]),
			('擦音', ['f', 'v', 's', 'ɕ', 'ʃ', 'ʒ', 'j', 'h', ]),
			]
		發音方法 = [
			('鼻音', ['m', 'n', 'ȵ', 'ŋ']),
			('清塞音', ['p', 't', 'k', 'ts', 'tɕ', 'tʃ', 'ʔ', ]),
			('送氣音', ['pʰ', 'tʰ', 'kʰ', 'tsʰ', 'tɕʰ', 'tʃʰ', ]),
			('濁塞音', ['b', ]),
			('清擦音', ['f', 's', 'ɕ', 'ʃ', 'h', ]),
			('濁擦音', ['v', 'ʒ', 'j', ]),  # 愛查j的特性
			('濁輔音', ['b', 'l', 'v', 'j', ]),
			('濁非元音', ['m', 'n', 'ȵ', 'ŋ', 'b', 'l', 'v', 'j', ]),
			]
		發音所在 = [
			('唇輔音', ['p', 'pʰ', 'b', 'm', 'f', 'v', ]),
			('齒輔音', ['t', 'tʰ', 'n', 'l',
					'ts', 'tsʰ', 's', 'tɕ', 'tɕʰ', 'ɕ', 'tʃ', 'tʃʰ', 'ʃ',
					'ȵ', 'ʒ', 'j', ]),
			('根輔音', ['k', 'kʰ', 'ŋ', ]),
			('喉輔音', ['h', 'ʔ', ]),
			]
		return self._生問題.問題集(塞擦題目, self.聲韻符號, '連紲') | \
			self._生問題.問題集(發音方法, self.聲韻符號, '孤條') | \
			self._生問題.問題集(發音所在, self.聲韻符號, '孤條')
	def 全部調(self):
		'''孤，組合'''
		題目 = []
		for 調號 in 臺灣客家話拼音調類對照表:
# 		for 調號 in range(0, 11):  # 有輕聲到第十調
			題目.append(('{}調'.format(調號), ['{}'.format(調號)]))
		return self._生問題.問題集(題目, self.調符號, '組合')
if __name__ == '__main__':
	問題 = 客家話決策樹仔().生()
	檔案 = open('questions_qst001.hed', 'w')
	print('\n'.join(問題), file=檔案)
	檔案.close()
