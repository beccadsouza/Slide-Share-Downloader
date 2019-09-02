from bs4 import BeautifulSoup
from requests import get
from pandas import DataFrame
from os import getcwd, mkdir
from os.path import isdir
from presentation import make_presentation

# presentation_url = 'https://www.slideshare.net/ellepiu/cure-clustering-algorithm'
presentation_url = 'https://www.slideshare.net/ramaseshanr/nlp-and-deep-learning/'


def download_slide_urls(url):
	try:
		resp = get(url)
		if resp.status_code == 200:
			soup = BeautifulSoup(resp.content, 'html.parser')
			title = soup.title.text
			slide_images = soup.find_all(class_='slide_image')
			slide_image_urls = [img.attrs for img in slide_images]
			return list(DataFrame(slide_image_urls)['data-normal']), title
		else:
			return [], ''
	except:
		return [], ''


def download_slides(slide_image_urls, presentation_title):
	output_dir = getcwd() + '/{0}'.format(presentation_title)
	try:
		mkdir(output_dir)
	except FileExistsError:
		copy_count = 1
		while isdir(output_dir + ' ({0})'.format(copy_count)): copy_count += 1
		output_dir += ' ({0})'.format(copy_count)
		mkdir(output_dir)

	padding = len(str(len(slide_image_urls)))
	for i, image_url in enumerate(slide_image_urls):
		slide_name = 'slide {0}'.format(str(i + 1).zfill(padding))
		resp = get(image_url, allow_redirects=True)
		if resp.status_code == 200: open('{0}/'.format(output_dir) + slide_name, 'wb').write(resp.content)
		print('Downloading {0}'.format(slide_name))

	return output_dir + '/'


slides_details = download_slide_urls(presentation_url)
if len(slides_details[0]) == 0: print('SlideShare URL entered does not exist or is incorrect')
else:
	slides_dir_path = download_slides(slides_details[0], slides_details[1])
	make_presentation(slides_dir_path, slides_details[1])
