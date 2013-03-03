from 音標介面 import 音標介面
from 臺灣語言音標 import 臺灣語言音標
from 通用拼音佮臺灣語言音標調類對照表 import 通用拼音佮臺灣語言音標聲韻對照表, 通用拼音佮臺灣語言音標調類對照表

class 通用拼音音標(音標介面):
	聲韻 = None
	調類 = None
	音標 = None
	def __init__(self, 音標):
		self.聲韻對照表 = 通用拼音佮臺灣語言音標聲韻對照表
		self.調類對照表 = 通用拼音佮臺灣語言音標調類對照表
		if 音標[:-1] in self.聲韻對照表 and 音標[-1:] in self.調類對照表:
			self.聲韻 = 音標[:-1]
			self.調類 = 音標[-1:]
			self.音標 = 音標
		else:
			self.音標 = None

	def 轉換到臺灣閩南語羅馬字拼音(self):
		if self.音標 == None:
			return None
		聲韻 = self.聲韻對照表[self.聲韻]
		調類 = self.調類對照表[self.調類]
		return 臺灣語言音標(聲韻 + str(調類)).轉換到臺灣閩南語羅馬字拼音()

if __name__ == '__main__':
	字音對照 = 通用拼音音標('bai5')
	print(字音對照.音標)
	print(字音對照.轉換到臺灣閩南語羅馬字拼音())
	print(通用拼音音標('zit3').轉換到臺灣閩南語羅馬字拼音())
	print(通用拼音音標('zit3').轉換到臺灣閩南語羅馬字拼音())
	print('gior4')
	print(通用拼音音標('gior4').轉換到臺灣閩南語羅馬字拼音())
	print('gier3')
	print(通用拼音音標('gier3').轉換到臺灣閩南語羅馬字拼音())
