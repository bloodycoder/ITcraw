#coding:utf-8
import xlwt
import urllib2,urllib,re
import time
class getJuzi:
	def __init__(self):
		self.count = 0
		self.book = xlwt.Workbook(encoding='utf-8',style_compression=0)
		self.sheet=self.book.add_sheet('heihei',cell_overwrite_ok=True)
		title=['公司名称','轮次','类别','地区','成立时间','一句话简介','ceo姓名','ceo简介','融资信息']
		for i in range(len(title)):
			self.sheet.write(0,i,title[i])
		cookies = urllib2.HTTPCookieProcessor()
		self.opener = urllib2.build_opener(cookies)
		self.opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'),('Origin','https://github.com'),('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'),('Accept-Language','zh-CN,zh;q=0.8'),('Connection','keep-alive')]
	def login(self):
		self.formdata={'identity':'picardxie@foxmail.com','password':'992288','remember':'0'}
		data_encoded = urllib.urlencode(self.formdata)
		response = self.opener.open('https://www.itjuzi.com/user/login',data_encoded)
		print 'login'
	def logout(self):
		self.opener.open('https://www.itjuzi.com/user/login?exit=logout')
		print 'logout'
	def view_index(self):
		html = self.opener.open('https://www.itjuzi.com/').read()
		f = open('pig.html','w')
		f.write(html)
	def craw_onecom(self,url):
		self.count+=1
		html = self.opener.open(url).read()
		#f = open('pig.html')
		#html = f.read()
		re_name = re.compile('<title>[^>]+')
		re_lunci= re.compile('<span class="t-small c-green">[^>]+')
		re_type = re.compile('company\?scope=\d+" target="_blank">[^>]+')
		re_prov = re.compile('company\?prov=[^>]+')
		re_time = re.compile('成立时间[^>]+')
		re_des = re.compile('<div class="des">[^>]+')
		re_ceo = re.compile('<span class="c">[^>]+')
		re_ceoinfo = re.compile('<p class="mart10 person-des">[^>]+')
		re_rongzi_date = re.compile('<span class="date c-gray">[^>]+')
		re_rongzi_lun = re.compile('<span class="round round-afterdate"><a href="#" target="_blank">[^>]+')
		re_rongzi_money = re.compile('<span class="finades"><a href="http://www.itjuzi.com/investevents/\d+" target="_blank">[^>]+')
		re_company = re.compile('href="http://www.itjuzi.com/investfirm/\d+" target="_blank">[^>]+')
		try:
		    name = re_name.findall(html) [0][7:-17]
		except:
			name ='none'
		try:
		    lunci = re_lunci.findall(html)[0][65:-38]
		except:
			lunci = 'none'
		try:
		    type_name = re_type.findall(html)[0].split('>')[1][:-3]
		except:
			type_name = 'none'
		try:
		    prov = re_prov.findall(html)[0][13:-1]
		except:
			prov = 'none'
		try:
		    the_time = re_time.findall(html)[0][15:-6]
		except:
			the_time ='none'
		try:
			ceo_info = re_ceoinfo.findall(html)[0][41:-2]
		except:
			ceo_info ='none'
		describ = re_des.findall(html)[0][24:-5]
		try:
		    ceo = re_ceo.findall(html)[0].split('>')[1][:-6]
		except:
			ceo = 'none'
		info = [name,lunci,type_name,prov,the_time,describ,ceo,ceo_info]
		money = re_rongzi_money.findall(html)   #[89:-3]
		rongzi_date = re_rongzi_date.findall(html)#[26:-6]
		rongzi_lun = re_rongzi_lun.findall(html)#[64:-3]
		company = re_company.findall(html)#[60:-3]
		for i in range(len(money)):
			try:
			    rongzi_info = rongzi_date[i][26:-6]+' '+rongzi_lun[i][64:-3]+' '+ money[i][89:-3]+' '+company[i][60:-3]
			    info.append(rongzi_info)
			except:
				pass
		print name
		for i in range(len(info)):
			try:
			    self.sheet.write(self.count,i,info[i])
			except:
				pass
		self.book.save('pig.xlsx')
	def craw_onepage(self,n):
		page = self.opener.open('http://www.itjuzi.com/company?user_id=302199&page='+str(n)).read()
		re_link = re.compile('<a target="_blank" href="http://www.itjuzi.com/company/\d+')
		craw_list = re_link.findall(page)
		for i in range(1,11):
			 url = craw_list[i*2-1][25:]
			 self.craw_onecom(url)
A = getJuzi()
A.login()
for i in range(1,4203):
	try:
	    A.craw_onepage(i)
	    print '第'+str(i)+'页抓取完毕'
	    i+=1
	except:
		print '第'+str(i)+'页抓取失败,等待60秒后重新抓取'
		time.sleep(60)
	time.sleep(10)


"""
book = xlwt.Workbook(encoding='utf-8',style_compression=0)
sheet=book.add_sheet('heihei',cell_overwrite_ok=True)
#sheet.write()..
title=['公司名称','轮次','类别','地区','成立时间','一句话简介','ceo姓名','ceo简介','融资信息']
for i in range(len(title)):
	sheet.write(0,i,title[i])
companyId=0
book.save('pig.xlsx')

"""