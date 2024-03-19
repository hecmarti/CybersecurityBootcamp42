import argparse
import requests
import glob
import os, re
from lxml import etree

agent = {"User-Agent":"Mozilla/5.0"}

def download_image(n, img, format_img, directory):
	response = requests.get(img, headers=agent, timeout=10)
	file = open(directory + "/img_" + str(n) + "." + format_img, "wb")
	file.write(response.content)
	file.close()

def pathm(directory):
	try:
		if os.path.exists(directory):
			py_files = glob.glob(directory + "/img_*.*")
			for py_file in py_files:
				try:
					os.remove(py_file)
				except OSError as e:
					print(f"Error:{ e.strerror}")
		else:
			os.mkdir(directory + "/")
	except OSError as error:
		print(error)

def program(url, r_num, directory):
	r = requests.get(url, headers=agent)
	content = r.text
	html = etree.HTML(content)
	recursiva = html.xpath("// a / @href ")
	niveles = ""
	busqueda = [{url}]
	for x in range(r_num):
		niveles += ".*?/"
		enlaces_bus = re.compile('(%s/'%url + '%s).*?'%niveles)
		for i in recursiva:
			busqueda.append(enlaces_bus.findall(str(i)))
	filt = []
	for j in busqueda:
		if j not in filt and j != []:
			filt.append(j)
	n = 1
	for i in filt:
		print("Downloading images from: ",*i)
		try:
			r = requests.get(*i, headers=agent)
			content = r.text
			html = etree.HTML(content)
			result = html.xpath("// img / @src ")
			for i in result:
				try:
					if not ("https:" or "http:") in i:
						i = "https:" + i
					x = requests.get(i, headers=agent, timeout=5)
					ref = x.headers['Content-Type']
					if ref[6:] == "jpeg":
						download_image(n, i, "jpeg", directory)
					if ref[6:] == "jpg":
						download_image(n, i, "jpg", directory)
					if ref[6:] == "png":
						download_image(n, i, "png", directory)
					if ref[6:] == "gif":
						download_image(n, i, "gif", directory)
					if ref[6:] == "bmp":
						download_image(n, i, "bmp", directory)
					n += 1
				except requests.exceptions.RequestException:
					if requests.exceptions.InvalidURL:
						#print("Invalid URL: ", i)
						continue
				except OSError as error:
					print(error)
					continue
				except KeyError as error:
					print(error)
					continue
		except AttributeError:
			print("Format error in URL: ", *i)
			continue
		except ValueError as err:
			print("Format error in URL: ", *i)
			continue

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-r', action='store', dest='url')
	parser.add_argument('-l', action='store', dest='level', default='5')
	parser.add_argument('-p', action='store', dest='path', default='data')
	args = parser.parse_args()

	if not "https://" in args.url:
		args.url = "https://" + args.url
	print("Scraping web: ", args.url)
	path = str(args.path)
	pathm(path)
	level = int(args.level)
	program(args.url, level, path)
	print("Successfully!")

if __name__ == '__main__':
	main()
