import subscene_api as api
import sys
import os

"""

Simple interface for the subsence API

"""

Movie_name = input("Movie name: ").replace(" ", "+") #Remove spaces form the input and replace it with +
os.system('cls' if os.name == 'nt' else 'clear')

headers = {"user-agent": "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"} #Setting the header for the URLs
#initlizing the class and get the Movies dict
Movies_class = api.subscene.Movies(url="https://subscene.com/subtitles/title?q={}".format(Movie_name),headers=headers)
movies_dict = Movies_class.Movies()

# Take the keys from movies dict (the type of the result)
movie_type_list = []
for key, movie_type in movies_dict.items():
	print(key)
	if key == "No results found":
		sys.exit()
	movie_type_list.append(str(key))

#Getting the desired search result's type
while True:
	_movie_type = input("Choose movie type (from the list above) : ")
	Is_there_movie_type = movie_type_list.count(str(_movie_type).lower())
	if Is_there_movie_type == 0:
		print("No movie type was found")
	elif Is_there_movie_type > 0:
		break
os.system('cls' if os.name == 'nt' else 'clear')

# Getting the movies in the that specific search result's type, and put it in list
movies_name = []
Counter = 0
for key, movie_type in movies_dict.items():
	if key == _movie_type.lower():
		for movie in movie_type:
			print("{:s}: {:s}".format(str(Counter),movie["title"]))
			movies_name.append(movie['link'])
			Counter +=1

#Getting the desired Movie
while True:
	Select_movie_number = input("Please select a movie by it's number: ")
	if len(movies_name) < int(Select_movie_number):
		print("No movie by number '{:d}' was found".format(int(Select_movie_number)))
	else:
		Select_movie_link = movies_name[int(Select_movie_number)]
		break

os.system('cls' if os.name == 'nt' else 'clear')

#initlizing the class and get the available languages
Subtitles_class = api.subscene.Subtitles(url="https://subscene.com"+Select_movie_link,headers=headers)
Available_lang = enumerate(Subtitles_class.languages)

#Print all languages, and let the user select the language
for key,lang in Available_lang:
	print("{:d}: {:s}".format(key,lang))

select_lang = ""
while True:
	select_lang_number = input("Please select a language by number from the above list: ")
	Available_lang = enumerate(Subtitles_class.languages)
	for key,lang in Available_lang:
		if int(select_lang_number) == int(key):
			select_lang = lang
	if len(select_lang) == 0:
		print("No language by number '{:d}' was found".format(int(select_lang_number)))
	else:
		break

os.system('cls' if os.name == 'nt' else 'clear')

#Setting the language filter
Subtitles_class.Add_filter("lang",str(select_lang).lower())

#Printing Subtitles type
print("0: positve")
print("1: Not rated")
print("2: bad")

#Getting the desired subtitle type
while True:
	select_sub_type_number = input("Please select subtitle type number from the list above: ")
	print(repr(select_sub_type_number))
	print(int(select_sub_type_number))
	if int(select_sub_type_number) != 0: 
		if int(select_sub_type_number) != 1: 
			if int(select_sub_type_number) != 2:
				print("No subtitle type by number {:d} was found".format(int(select_sub_type_number))) 
			else:
				#Setting subtitle type filter
				Subtitles_class.Add_filter("sub",str(int(select_sub_type_number) + 1))	
				break	
		else:
			Subtitles_class.Add_filter("sub",str(int(select_sub_type_number) + 1))	
			break
	else:
		Subtitles_class.Add_filter("sub",str(int(select_sub_type_number) + 1))
		break

os.system('cls' if os.name == 'nt' else 'clear')

#Get subtitles dict which is filtterd using the given filters
sub_dict = Subtitles_class.Subtitles()

#Printing all subtitles that are in the sub_dict
for key, value in sub_dict.items():
	for sub in value:
		print("Subtitle name: " + sub["Name"])
		#Calling the method Get_download_link using the link of the subtitle
		print("link: " + Subtitles_class.Get_download_link(sub["Link"],headers))

		
