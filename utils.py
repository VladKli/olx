import time
from io import BytesIO
from PIL import Image
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import jinja2
import pdfkit
import glob
from PyPDF2 import PdfReader, PdfWriter
import os


headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
}
# proxies = {
#    'http': '46.219.8.201:41890',
#    'https': '46.219.8.201:41890',
# }

# def get_browser():
#     options = webdriver.ChromeOptions()
#     options.add_argument("headless")
#     browser = webdriver.Chrome(options=options)
#     return browser

def get_browser():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = '/olx/chrome/opt/google/chrome'  # Path to Chromium executable
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    return driver


def get_soup(url):
    browser = get_browser()
    browser.get(url)
    time.sleep(2)
    html = browser.page_source
    soup = BeautifulSoup(html, "lxml")
    return soup


def get_all_images(url):
    images = []
    soup = get_soup(url)
    pics = soup.find_all("div", {"data-cy": "adPhotos-swiperSlide"})
    for pic in pics:
        img = pic.find_next("img")
        href = img.get("srcset") or img.get("data-srcset")
        img = href.split()[-2]
        images.append(img)
    return images


def get_pngs(url):
    pngs = get_all_images(url)
    count = 1
    for el in pngs:
        img = Image.open(BytesIO(requests.get(el, headers=headers).content)).convert("RGB")
        img.save(f"pics/file{count}.png")
        count += 1
    return pngs


def scrape(url):
    extra_info = ""
    detailed_info = ""
    soup = get_soup(url)
    title = soup.find("h1", {"data-cy": "ad_title"}).text.strip()
    price = soup.find("div", {"data-testid": "ad-price-container"}).text.strip()
    description = soup.find("div", {"class": "css-bgzo2k er34gjf0"}).text.strip()
    details = soup.find("ul", {"class": "css-sfcl1s"}).find_all("li")
    for data in details:
        if len(data.text) < 80:
            detailed_info += data.text
            detailed_info += "\n"
        else:
            extra_info += data.text

    data = detailed_info[:-1].split("\n")
    context = {
        "title": title,
        "price": price,
        "description": description,
        "imgs": get_pngs(url),
        "data": data,
        "extra_info": extra_info,
    }
    template_loader = jinja2.FileSystemLoader("./")
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template("check.html")
    output_text = template.render(context)
    config = pdfkit.configuration(wkhtmltopdf="/usr/bin/wkhtmltopdf")
    pdfkit.from_string(output_text, "test_it.pdf", configuration=config)


def create_pdf():
    images = []
    for png in glob.glob("/home/andersen/Documents/projects/shar/pics/*.png"):
        im = Image.open(png)
        images.append(im)
    pdf_path = "/home/andersen/Documents/projects/shar/pdfs/test.pdf"
    images[0].save(
        pdf_path, "PDF", resolution=100.0, save_all=True, append_images=images[1:]
    )
    output = PdfWriter()
    pdfOne = PdfReader(
        open("/home/andersen/Documents/projects/shar/pdfs/test.pdf", "rb")
    )
    pdfTwo = PdfReader(open("/home/andersen/Documents/projects/shar/test_it.pdf", "rb"))
    output.add_page(pdfTwo.pages[0])
    count = 0
    for page in pdfOne.pages:
        page.scale_by(1)
        output.add_page(pdfOne.pages[count])
        count += 1
    outputStream = open(r"announcement.pdf", "wb")
    output.write(outputStream)
    outputStream.close()


def remove_trash():
    pics_files = glob.glob("/home/andersen/Documents/projects/shar/pics/*")
    for f in pics_files:
        os.remove(f)
    test_file = "/home/andersen/Documents/projects/shar/test_it.pdf"
    test_file1 = "/home/andersen/Documents/projects/shar/pdfs/test.pdf"
    test_file2 = "/home/andersen/Documents/projects/shar/announcement.pdf"
    os.remove(test_file)
    os.remove(test_file1)
    os.remove(test_file2)


def main(
    url="https://www.olx.ua/d/obyavlenie/prodazha-4k-kvartiry-po-ul-ivana-mazepy-zhk-diamond-hill-pechersk-IDR2vsU.html",
):
    scrape(url)
    create_pdf()


if __name__ == "__main__":
    main()
