import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage

from selenium import webdriver
from PIL import Image

print("""

  ÛÛÛÛÛÛÛÛÛ                                         ÛÛÛÛÛÛÛÛÛÛÛ                                    
 ÛÛÛ°°°°°ÛÛÛ                                       °°ÛÛÛ°°°°°ÛÛÛ                                   
°ÛÛÛ    °°°  ÛÛÛÛÛÛÛÛ    ÛÛÛÛÛÛ   ÛÛÛÛÛÛÛÛ   ÛÛÛÛÛ  °ÛÛÛ    °ÛÛÛ ÛÛÛÛÛÛÛÛ   ÛÛÛÛÛÛ   ÛÛÛÛÛ   ÛÛÛÛÛ 
°°ÛÛÛÛÛÛÛÛÛ °°ÛÛÛ°°ÛÛÛ  °°°°°ÛÛÛ °°ÛÛÛ°°ÛÛÛ ÛÛÛ°°   °ÛÛÛÛÛÛÛÛÛÛ °°ÛÛÛ°°ÛÛÛ ÛÛÛ°°ÛÛÛ ÛÛÛ°°   ÛÛÛ°°  
 °°°°°°°°ÛÛÛ °ÛÛÛ °ÛÛÛ   ÛÛÛÛÛÛÛ  °ÛÛÛ °ÛÛÛ°°ÛÛÛÛÛ  °ÛÛÛ°°°°°°   °ÛÛÛ °°° °ÛÛÛÛÛÛÛ °°ÛÛÛÛÛ °°ÛÛÛÛÛ 
 ÛÛÛ    °ÛÛÛ °ÛÛÛ °ÛÛÛ  ÛÛÛ°°ÛÛÛ  °ÛÛÛ °ÛÛÛ °°°°ÛÛÛ °ÛÛÛ         °ÛÛÛ     °ÛÛÛ°°°   °°°°ÛÛÛ °°°°ÛÛÛ
°°ÛÛÛÛÛÛÛÛÛ  ÛÛÛÛ ÛÛÛÛÛ°°ÛÛÛÛÛÛÛÛ °ÛÛÛÛÛÛÛ  ÛÛÛÛÛÛ  ÛÛÛÛÛ        ÛÛÛÛÛ    °°ÛÛÛÛÛÛ  ÛÛÛÛÛÛ  ÛÛÛÛÛÛ 
 °°°°°°°°°  °°°° °°°°°  °°°°°°°°  °ÛÛÛ°°°  °°°°°°  °°°°°        °°°°°      °°°°°°  °°°°°°  °°°°°°  
                                  °ÛÛÛ                                                             
                                  ÛÛÛÛÛ                                                            
                                 °°°°°                                                             
""")

print("SnapsPress 2019 - Snaps Maker Tool")

# Chrome webdriver options

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--remote-debugging-port=9223")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--hide-scrollbars")
chrome_options.add_argument("--enable-logging")
chrome_options.add_argument("--log-level=0")
chrome_options.add_argument("--v=99")
chrome_options.add_argument("--single-process")
chrome_options.add_argument("--ignore-certificate-errors")

# SnapsPress parameters

default_width = 1100
default_height = 1320
work_path = "tmp"
today = datetime.date.today().strftime("%Y%m%d")

print("Initializing Webdriver ...")

browser = webdriver.Chrome(options=chrome_options)
browser.set_window_size(default_width, default_height)

print("Connecting to Firebase ...")

# Use a firebase service account

cred = credentials.Certificate("serviceAccount.json")
options = {"storageBucket": "snapspress-a5592.appspot.com"}
firebase_admin.initialize_app(cred, options=options)

db = firestore.client()

sources_ref = db.collection("sources")
sources = sources_ref.get()

bucket = storage.bucket()

for source in sources:
    source_dict = source.to_dict()
    print("{} => {}".format(source.id, source_dict["link"]))
    browser.get(source_dict["link"])
    print("{} => loaded!".format(source.id))
    img_path = "{}/{}.png".format(work_path, source.id)
    browser.save_screenshot(img_path)
    image = Image.open(img_path)
    image.thumbnail((500, 610))
    rgb_image = Image.new("RGB", image.size, (255,255,255))
    rgb_image.paste(image, (0,0), image)
    web_img_path = "{}/{}_500x610.jpg".format(work_path, source.id)
    rgb_image.save(web_img_path,optimize=True,quality=95)
    blob = bucket.blob("{}/{}_500x610.jpg".format(today,source.id))
    blob.upload_from_string(
        rgb_image.tobytes(),
        content_type="image/jpg"
    )
    print('Blob: {}'.format(blob.name))
    print('Bucket: {}'.format(blob.bucket.name))
    print('Storage class: {}'.format(blob.storage_class))
    print('ID: {}'.format(blob.id))
    print('Size: {} bytes'.format(blob.size))
    print('Updated: {}'.format(blob.updated))
    print('Generation: {}'.format(blob.generation))
    print('Metageneration: {}'.format(blob.metageneration))
    print('Etag: {}'.format(blob.etag))
    print('Owner: {}'.format(blob.owner))
    print('Component count: {}'.format(blob.component_count))
    print('Crc32c: {}'.format(blob.crc32c))
    print('md5_hash: {}'.format(blob.md5_hash))
    print('Cache-control: {}'.format(blob.cache_control))
    print('Content-type: {}'.format(blob.content_type))
    print('Content-disposition: {}'.format(blob.content_disposition))
    print('Content-encoding: {}'.format(blob.content_encoding))
    print('Content-language: {}'.format(blob.content_language))
    print('Metadata: {}'.format(blob.metadata))  
    print(blob.public_url)
    break

browser.quit()

