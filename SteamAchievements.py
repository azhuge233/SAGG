import platform, os, multiprocessing
from MyClass.GETSOUP import *
from MyClass.LOG import *

URL = "https://steamcommunity.com/stats/{0}/achievements"
HEAD["Accept-Language"] = "zh-CN,zh;q=0.5,en-US;"
HEAD["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0"
PATH = "."


GAME_NAME = ""
logger.name = "SA"


def get_achieve_info():
	try:
		global GAME_NAME
		soup = get_url_single(url=URL, headers=HEAD)
		GAME_NAME = soup.select(".profile_small_header_texture h1")[0].string.replace(":", "").replace("*", "")
		picture_soup = soup.select(".achieveRow img")
		title_soup = soup.select(".achieveTxt h3")
		description_soup = soup.select(".achieveTxt h5")
		logger.warning(GAME_NAME + ": Found " + str(len(picture_soup)) + " Achievements")

		pictures_q = list([])
		titles = list([])
		descriptions = list([])

		for i in range(len(picture_soup)):
			pictures_q.append((picture_soup[i].get("src"), str(i) + "_" + title_soup[i].string + ".jpg", os.path.join(PATH, GAME_NAME, title_soup[i].string + ".jpg")))
			titles.append(title_soup[i].string)
			descriptions.append(description_soup[i].string)

		return pictures_q, titles, descriptions
	except IndexError as ex:
		logger.error("Index out of range, this game may have no achievements!")
		logger.error("Error message: " + str(ex))
	except Exception as ex:
		logger.error("Get soup error!")
		logger.error("Error message: " + str(ex))


def create_folder():
	if not os.path.exists(os.path.join(PATH, GAME_NAME)):
		os.mkdir(os.path.join(PATH, GAME_NAME))


def download(url, name, pic_path):
	if os.path.exists(pic_path):
		logger.warning(name + " exists, skipping")
		return
	req = request.Request(url, headers=HEAD)
	resp = request.urlopen(req)
	if resp.getcode() == 200:
		with open(pic_path, "wb") as f:
			f.write(resp.read())
		logger.warning("Downloaded " + name)
	else:
		logger.error("Get " + name + " returned code " + str(resp.getcode()))
		return


def download_pictures(pictures_q):
	try:
		pool = multiprocessing.Pool(processes=multiprocessing.cpu_count() - 1)
		output = pool.starmap(download, pictures_q)
	except Exception as ex:
		logger.error("Download Pictures Failed!")
		logger.error("Error Message: " + str(ex))


def trans_to_cols(title, description):
	result = "  [tr]\n"

	result += "    [td] " + title + " [/td]\n"
	result += "    [td] " + description + " [/td]\n"
	result += "    [td] [/td]\n"

	return result + "  [/tr]\n"


def wrap_steam_format(titles, descriptions):
	result = "[table]\n  [tr]\n    [th]名称[/th]\n    [th]说明[/th]\n    [th]达成条件[/th]\n  [/tr]\n"

	for i in range(len(titles)):
		if descriptions[i] == None:
			result += trans_to_cols(titles[i], "无")
		else:
			result += trans_to_cols(titles[i], descriptions[i])

	result += "[/table]\n"
	return result


def main():
	global URL
	logger.warning(" ----- Start Job -----")

	app_id = input("Please input the game's App ID: ")

	if not app_id.isnumeric():
		logger.error("App ID should only be numbers.")
		logger.error("App ID Invalid, quiting")
		logger.info("\n\n")
		return

	URL = URL.format(app_id)
	logger.warning("The achievements page will be: " + URL)

	logger.warning("Fetching Achievements...")
	pictures_q, titles, descriptions = get_achieve_info()
	logger.warning("Done.")

	logger.warning("Creating Folder...")
	create_folder()
	logger.warning("Done.")

	logger.warning("Downloading Pictures...")
	download_pictures(pictures_q)
	logger.warning("Done.")

	logger.warning("Formatting to Steam Guide...")
	result = wrap_steam_format(titles, descriptions)
	logger.warning("Done.")

	logger.warning("Writing result to file...")
	with open(os.path.join(PATH, GAME_NAME, GAME_NAME+".txt"), "w+", encoding='utf-8') as f:
		f.write(result)
	logger.warning("Done.")

	logger.warning("Job Done.")
	logger.info("\n\n")



if __name__ == "__main__":
	main()
