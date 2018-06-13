import sys
from urllib import request as HttpAgent
from urllib import error as Error_handler
from bs4 import BeautifulSoup
import re

class subscene:
	"""Subscene API, ver: 1.0
		That use's Beautiful Soup to web scrap the www.subscene.com search page to get the movies and thair subtitles.
		Created by: Mohammed NaderShah, a beginner of python programming.

	"""

	def Clear_Class_String(String):
		return str(String).strip("]").strip("[").strip("'")

	def Strip_newlines(String):
		return "".join(str(String).split())

	class Movies:
		"""

		Movies class handle's things about getting the movies

		"""

		def __init__(self,url,headers):
			"""

			Use's the URL that pass as arugment and the Header to web scrap www.subscene.com/subtitles/title?q= [Movie name].
			set the [self.Movie_Search_Result] var = web page div that has the search-result class attached to it,
			and call the [self.Movie_type()] method to set [self.Mv_type] list which is the all h2 tags(exact, popular, ...etc) that in the [self.Movie_Search_Result]

			"""
			request_url = HttpAgent.Request(url=url,headers=headers)
			try:
				content = HttpAgent.urlopen(request_url).read()
				soup = BeautifulSoup(content, 'html.parser')
				self.Movie_Search_Result = soup.find("div",{"class": "search-result"})
				self.Mv_type = self.Movie_type()
			except Error_handler.URLError as e:
				print("Page request has failed")
				sys.exit()

		def Strip_newlines(self,String):
			""" Method that take a String and return it without the [/n] , [/t], [/r] """
			return "".join(str(String).split())

		def Clear_Class_String(self,String):
			""" Method that take a String and return it without ( [ ), ( ] ), ( ' ) """
			return str(String).strip("]").strip("[").strip("'")

		def Movie_type(self):
			"""  

				Method that return a list that have all [h2 tags class] which is the search result type that is related to the search of the moive name that was entered

			"""
			Movie_h2 = self.Movie_Search_Result.find_all("h2")
			Movie_type = []
			for _Mv_type in Movie_h2:
				if str(_Mv_type.get('class')) != "None":
					Movie_type.append(self.Clear_Class_String(String= str(_Mv_type.get('class'))))
				elif _Mv_type.text != "":
					Movie_type.append(self.Clear_Class_String(String= str(_Mv_type.text)))
			return Movie_type

		def Movies(self):
			"""

			Method that retuen a dict, the dict keys are the elements in the list which is the return of the method: [Movie_type].
			Each dict key has valuse that represent a list of movies that is related to the search result 

			dict[Movie_type] -> list( dict( ["title"], [link], ["num.sub"] ) )
			num.sub: How many subtitles are in this movie

			"""
			All_Movies_ul = self.Movie_Search_Result.find_all("ul")
			Movies = {} #initilzing the dict for the Movies
			for _Mv_type in self.Mv_type:
				Movies[str(_Mv_type)] = list([])
			for key,ul in enumerate(All_Movies_ul):
				_type = self.Mv_type[key]
				ul_li = ul.find_all("li")
				for li in ul_li:
					li_div_title = li.find_all("div",{"class": "title"})[0]
					_link = li_div_title.a.get("href")
					_title = li_div_title.a.text
					li_div_subtle = li.find_all("div",{"class": "subtle"})
					li_span_subtle = li.find_all("span",{"class": "subtle"})
					if len(li_div_subtle) != 0:
						_num_sub = re.findall(r'\d+',self.Strip_newlines(str(li_div_subtle[0].text)))[0]
					if len(li_span_subtle) != 0:
						_num_sub = re.findall(r'\d+',self.Strip_newlines(str(li_span_subtle[0].text)))[0]
					sub = dict({"title": str(_title),"link": str(_link),"num.sub": str(_num_sub)})
					Movies[str(_type)].append(sub)
			return Movies

	class Subtitles:
		"""

		Subtitle class handle's things about getting the movies' subtitles

		"""
		#initilzing filters
		filter_lang = [] 
		filter_sub_type = []

		def __init__(self,url,headers):
			"""

			Use's the URL that pass as arugment and the Header to web scrap www.subscene.com/subtitles/[Movie name].
			set the [self.Subtitles_Search_Result] var = web page div that has the content id attached to it and navigate to the table and table.tbody,
			and call the [self.Get_languages()] method to set [self.languages] list which is the all languages available(arabic, english, ...etc)

			"""
			request_url = HttpAgent.Request(url=url,headers=headers)
			try:
				content = HttpAgent.urlopen(request_url).read()
				soup = BeautifulSoup(content, 'html.parser')
				self.Subtitles_Search_Result = soup.find("div",{"id": "content"}).table.tbody
				self.Get_languages()
			except Error_handler.URLError as e:
				print("Page request has failed")
				sys.exit()

		def Strip_newlines(self,String):
			return "".join(str(String).split())

		def Clear_Class_String(self,String):
			return str(String).strip("]").strip("[").strip("'")

		def Get_languages(self):
			languages = []
			language_td = self.Subtitles_Search_Result.find_all("td",{"class": "language-start"})
			for language in language_td:
				languages.append(str(language.get("id")))
			self.languages = languages

		def Add_filter(self,filter_type,_filter):
			"""

			Method to set filters for filtering the subtitles

			"""
			# [Lang] Language filter = by language name
			# [Sub] Subtitle type filter = [1]: positive [2]: not rated [3]: bad
			if str(filter_type) == "Lang" or str(filter_type) == "lang":
				self.filter_lang.append(str(_filter).lower())
			elif str(filter_type) == "Sub" or str(filter_type) == "sub":
				if str(_filter) == "1":
					self.filter_sub_type.append("positive-icon")
				elif str(_filter) == "2":
					self.filter_sub_type.append("neutral-icon")
				elif str(_filter) == "3":
					self.filter_sub_type.append("bad-icon")

		def Subtitles(self):
			"""

			Method that retuen a dict, the dict keys are the elements in the list which is the return of the method: [Get_languages()].
			Each dict key has valuse that represent a list of subtitles that is related to the languages

			dict[Language] -> list( dict(["name"], ["Type"], ["Link"]) )
			Type: positive-icon, neutral-icon (not rated), bad-icon (negative)

			"""
			languages = {}
			for lang in self.languages:
				if len(self.filter_lang) == 0:
					languages[str(lang)] = list([])
				elif len(self.filter_lang) > 0:
					for lang_filter in self.filter_lang:
						if str(lang_filter) == lang:
							languages[str(lang)] = list([])

			tr_subtitle = self.Subtitles_Search_Result.find_all("tr")

			for tr in tr_subtitle:
				if self.Clear_Class_String(String= str(tr.td.get("class"))) == "language-start":
					Current_language = str(tr.td.get("id"))
				elif self.Clear_Class_String(String = str(tr.td.get("class"))) == "banner-inlist":
					continue
				else:
					if len(self.filter_lang) == 0:
						_link = tr.find("td",{"class": "a1"}).a.get("href")
						_Type = tr.find("td",{"class": "a1"}).a.find("span",{"class": "r"}).get("class")[2]
						_Subtitle_name = tr.find("td",{"class": "a1"}).a.find_all("span")[-1].text
						_Subtitle_name = self.Strip_newlines(_Subtitle_name)
						_Subtitle = dict({"Name": str(_Subtitle_name), "Type": str(_Type), "Link": str(_link)})
						languages[str(Current_language)].append(_Subtitle)
					elif len(self.filter_lang) > 0:
						for lang_filter in self.filter_lang:
							if Current_language == lang_filter:
								if len(self.filter_sub_type) == 0:
									_link = tr.find("td",{"class": "a1"}).a.get("href")
									_Type = tr.find("td",{"class": "a1"}).a.find("span",{"class": "r"}).get("class")[2]
									_Subtitle_name = tr.find("td",{"class": "a1"}).a.find_all("span")[-1].text
									_Subtitle_name = self.Strip_newlines(_Subtitle_name)
									_Subtitle = dict({"Name": str(_Subtitle_name), "Type": str(_Type), "Link": str(_link)})
									languages[str(Current_language)].append(_Subtitle)
								elif len(self.filter_sub_type) > 0:
									for sub_type in self.filter_sub_type:
										_Type = tr.find("td",{"class": "a1"}).a.find("span",{"class": "r"}).get("class")[2]
										if sub_type == _Type:
											_link = tr.find("td",{"class": "a1"}).a.get("href")											
											_Subtitle_name = tr.find("td",{"class": "a1"}).a.find_all("span")[-1].text
											_Subtitle_name = self.Strip_newlines(_Subtitle_name)
											_Subtitle = dict({"Name": str(_Subtitle_name), "Type": str(_Type), "Link": str(_link)})
											languages[str(Current_language)].append(_Subtitle)
			return languages

		def Get_download_link(self,link,headers):
			"""

			Method that return the download link from the subtitle's page

			"""
			default_subsence_link = "https://subscene.com"
			url = default_subsence_link+str(link)
			request_url = HttpAgent.Request(url=url,headers=headers)
			try:
				content = HttpAgent.urlopen(request_url).read()
				soup = BeautifulSoup(content, 'html.parser')
				return str(default_subsence_link + str(soup.find_all("div",{"class": "download"})[0].a.get("href")))
			except Error_handler.URLError as e:
				print("Page request has failed")
				sys.exit()
