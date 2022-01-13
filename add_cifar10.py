from PIL import Image
import numpy as np
import io
from ImageCrawling import database_tools
from ImageCrawling import crawling_base


def unpickle(file):
    import pickle
    with open(file, 'rb') as fo:
        dict = pickle.load(fo, encoding='bytes')
    return dict


def convert_image(array):
    img = np.reshape(array, (3, 32, 32))
    img = np.transpose(img, (1,2,0))
    img =  Image.fromarray(img, "RGB")
    buf = io.BytesIO()
    img.save(buf, format='JPEG')
    return buf.getvalue()


def process_batch(file):
    # class, database_name, website, data
    dict = unpickle(file)
    keys = [*dict]
    labels = dict.get(keys[1])
    data = dict.get(keys[2])
    output = []
    for l,d in zip(labels, data):
        output.append((l, convert_image(d)))
    return output



def process_all():
    label_names_dict = unpickle('original_cifar10/batches.meta')
    label_names = label_names_dict.get([*label_names_dict][1])
    images = process_batch('original_cifar10/data_batch_1')
    images += process_batch('original_cifar10/data_batch_2')
    images += process_batch('original_cifar10/data_batch_3')
    images += process_batch('original_cifar10/data_batch_4')
    images += process_batch('original_cifar10/data_batch_5')
    test_images = process_batch('original_cifar10/data_batch_5')
    images_for_db = []
    for n in label_names:
        images_for_db.append([])
    
    for i in images:
        images_for_db[i[0]].append(i[1])

    for i in range(0, len(images_for_db)):
        database_tools.load_images_to_db("light_database.db", "images", images_for_db[i], str(label_names[i])[2:-1], "cifar10", "CIFAR-10")

    images_for_db = []
    for n in label_names:
        images_for_db.append([])
    
    for i in test_images:
        images_for_db[i[0]].append(i[1])

    for i in range(0, len(images_for_db)):
        database_tools.load_images_to_db("light_database.db", "images", images_for_db[i], str(label_names[i])[2:-1], "cifar10_test", "CIFAR-10")

    database_tools.print_info_images_connect("light_database.db", "images")

    
def create_db():
    conn = database_tools._connect_to_db("light_database.db")
    database_tools._create_images_table(conn)
    conn.commit()
    conn.close()
    
# def load_images_to_db(database: str, table: str, images, img_class: str, database_name: str, website: str):

# So muss ein Bild angezeigt werden können
# image = Image.open(io.BytesIO(image_data)).convert("RGBA")

if __name__ == '__main__':
    crawling_base._change_folder("ImageDatabases", verbose=True)
    create_db()
    process_all()
    database_tools.print_info_images_connect("light_database.db", "images")