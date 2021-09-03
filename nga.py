import requests
from bs4 import BeautifulSoup
import re


url = 'https://bbs.nga.cn/read.php?tid=28158704' 
headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
	'cookie':"guestJs=1629536481; UM_distinctid=17b67f179d1201-02a3862dadc7ce-7868786b-384000-17b67f179d22ac; PHPSESSID=b348a2f7c1134dbf5a3cd5a08f99e5d7; ngacn0comUserInfo=tamiyaaaa%09tamiyaaaa%0939%0939%09%0910%090%094%090%090%09; ngacn0comUserInfoCheck=1061edfeda8fd53bac5e921c9332ee14; ngacn0comInfoCheckTime=1629536731; ngaPassportUid=61098867; ngaPassportUrlencodedUname=tamiyaaaa; ngaPassportCid=X8ruo40u4saos03lql4unt9kunrtju5md15nrpqd; CNZZDATA30043604=cnzz_eid%3D1261991273-1629531664-https%253A%252F%252Fbbs.nga.cn%252F%26ntime%3D1629537064; lastvisit=1629537340; lastpath=/read.php?tid=28158704; bbsmisccookies=%7B%22pv_count_for_insad%22%3A%7B0%3A-39%2C1%3A1629565264%7D%2C%22insad_views%22%3A%7B0%3A1%2C1%3A1629565264%7D%2C%22uisetting%22%3A%7B0%3A%22d%22%2C1%3A1629537635%7D%7D; _cnzz_CV30043604=forum%7Cfid-7202235%7C0"
}                                                

r = requests.get(url, headers=headers,verify=False)    
soup = BeautifulSoup(r.content,'lxml')       
                  
file=open('nga带路.txt','w',encoding='utf-8')
file.write(str(soup))

content=open('nga带路.txt','r+',encoding='utf-8')
l=content.read()

pattern=re.compile('带路条件(.+?)\[table\](.+?)\[\/table\]')# ~ 定位带路条件下的表格
rs=pattern.findall(l)
file=open('nga带路.txt','w',encoding='utf-8')

# ~ print(len(rs))查看数量是否符合预期

NumOfPara=2#选取第几个表格
content=rs[NumOfPara][1]#正则表达式中需要选取第二个匹配字符段
pattern=re.compile('\[(.+?)\]')#将bbcode中所有的[]转换为html5的<>
tag=pattern.findall(content)

def getTable(tag,content):
	for i in tag:
		var1="["+i+"]"
		var2='<'+i+'>'
		content=str(content).replace(var1,var2)
	#替换[]完成
	content=content.replace('list','ul')#替换list为ul
	content=content.replace('<*>','<li>')#替换<*>为<li>
	
	temp="<table style='text-align: left' class='wikitable'  >"+str(content)
	content=str(temp)+'</table>'#前后增加table标签
	content=content.replace('<br/><br/>','')
	return content
	
content=getTable(tag,content)

def chColor(content):#更换color标签格式
	pattern=re.compile('\<color(.+?)\>(.+?)\<\/color\>')
	color=pattern.findall(content)
	# ~ print(color)
	for i in range(len(color)):
		var1='<color'+color[i][0]+'>'
		rcolor=(color[i][0])[1:]
		var2='<span style="color:'+rcolor+'">'
		
		content=content.replace(var1,var2)
		content=content.replace('</color>','</span>')
	return content
		
content=chColor(str(content))

def removeTdBr(content):#去除多余的换行符
	content=content.replace('<br/>','<br/>')
	content=content.replace('</td><br/>','</td>')
	content=content.replace('</ul><br/>','</ul>')
	return content
	
content=removeTdBr(content)

print(content)
file.write(content)


