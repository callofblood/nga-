import requests
from bs4 import BeautifulSoup
import re
def run():
	url = 'https://bbs.nga.cn/read.php?tid=23451223&rand=110' 
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
		'cookie':"guestJs=1629536481; UM_distinctid=17b67f179d1201-02a3862dadc7ce-7868786b-384000-17b67f179d22ac; PHPSESSID=b348a2f7c1134dbf5a3cd5a08f99e5d7; ngacn0comUserInfo=tamiyaaaa%09tamiyaaaa%0939%0939%09%0910%090%094%090%090%09; ngacn0comUserInfoCheck=1061edfeda8fd53bac5e921c9332ee14; ngacn0comInfoCheckTime=1629536731; ngaPassportUid=61098867; ngaPassportUrlencodedUname=tamiyaaaa; ngaPassportCid=X8ruo40u4saos03lql4unt9kunrtju5md15nrpqd; CNZZDATA30043604=cnzz_eid%3D1261991273-1629531664-https%253A%252F%252Fbbs.nga.cn%252F%26ntime%3D1629537064; lastvisit=1629537340; lastpath=/read.php?tid=28158704; bbsmisccookies=%7B%22pv_count_for_insad%22%3A%7B0%3A-39%2C1%3A1629565264%7D%2C%22insad_views%22%3A%7B0%3A1%2C1%3A1629565264%7D%2C%22uisetting%22%3A%7B0%3A%22d%22%2C1%3A1629537635%7D%7D; _cnzz_CV30043604=forum%7Cfid-7202235%7C0"
	}                                                
	r = requests.get(url, headers=headers,verify=False)    
	soup = BeautifulSoup(r.content,'lxml')       
	headTable=soup.find_all('table')
	headTable=headTable[0] 
	headTbody=headTable.findAll('p')
	patternMap=re.compile('\[pid=(\d+)\](\d-\d)(.+?)\[/pid\]')
	maps=patternMap.findall(str(headTbody))
	tempUrl='https://bbs.nga.cn/read.php?pid=xxxx' 
	for i in range(len(maps)):
		curUrl=maps[i][0]
		url = tempUrl.replace('xxxx',curUrl)
		r = requests.get(url, headers=headers,verify=False)    
		curMap = BeautifulSoup(r.content,'lxml')     
		# ~ print(curMap)//获取了某张图的html
		patternRoutes=re.compile('\[pid=(\d+)\]带路条件\(新窗口\)\[/pid\]')
		routesUrl=patternRoutes.findall(str(curMap))
		curTableUrl=tempUrl.replace('xxxx',routesUrl[0])
		# ~ print(curTable)//获取了某张图的带路html
		r = requests.get(curTableUrl, headers=headers,verify=False)    
		curTableHTML=BeautifulSoup(r.content,'lxml')
		if(1):
			
			# ~ patternTable=re.compile('\[table\].+?\[/table\]')
			# ~ rs=patternTable.findall(str(curTableHTML))
			
			patternList=re.compile('\[table\](.+)\[/table\]')
			rs=patternList.search(str(curTableHTML))	
			temp="<table style='text-align: left' class='wikitable'  >"
			
			newrs=temp+str(rs.group(1))+'</table>'
			newrs=newrs.replace('[','<')
			newrs=newrs.replace(']','>')
			newrs=newrs.replace('<*>','<li>')
			newrs=newrs.replace('<b><b>','<b>')
			newrs=newrs.replace('</b></b>','</b>')
			newrs=newrs.replace('<align=center>','')
			newrs=newrs.replace('</align>','')
			newrs=newrs.replace('list','ul')
			newrs=newrs.replace('<collapse=舰种缩写>','')
			newrs=newrs.replace('</collapse>','')
			newrs=removeTdBr(newrs)
			newrs=chColor(newrs)
			
			patternRemoveHead=re.compile('<tr>.+?<\/tr>')
			head=patternRemoveHead.findall(newrs)[0]
			newrs=newrs.replace(head,'')
			
			# ~ print(newrs)
			
			
			print(curTableUrl)
			addHead=open('header.txt','r+',encoding='utf-8')
			newrs=str(addHead.read())+newrs
			addHead.close()
			newrs+='<div>'+'转自nga梦美:'+curTableUrl+'</div>'
			f=open(maps[i][1]+'.txt','w',encoding='utf-8')
			f.write(newrs)
			f.close()
			# ~ exit()

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
		

def removeTdBr(content):#去除多余的换行符
	content=content.replace('<br/><br/>','')
	content=re.sub('</td>\s*<br/>','</td>',content)
	content=re.sub('</tr>\s*<br/>','</tr>',content)
	# ~ content=re.sub('<td colspan=(\d)+>\s*<br/>','<td colspan=$1>',content)

	content=re.sub('</ul>\s*<br/>','</ul>',content)
	pattern=re.compile('<td colspan=(\d)+>\s*<br/>')
	tdbr=pattern.findall(content)
	for i in range(len(tdbr)):
		content=re.sub('<td colspan='+tdbr[i]+'>\s*<br/>','<td colspan='+tdbr[i]+'>',content)
	return content
	
def align(content):#<align=center>出发点</align>
	pattern=re.compile('\<align(.+?)\>(.+?)\<\/align\>')
	alignStyle=pattern.findall(content)
	for i in range(len(alignStyle)):
		var1='<align'+alignStyle[i][0]+'>'
		where=(alignStyle[i][0])[1:]
		var2='<span style="text-align:'+where+'">'
		
		content=content.replace(var1,var2)
		content=content.replace('</align>','</span>')
	return content
# ~ print(content)
# ~ file.write(content)
if __name__=='__main__':
	run()

