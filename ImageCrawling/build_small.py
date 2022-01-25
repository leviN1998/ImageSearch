from . import toolbox
from . import database_tools


def __cifar_10_process_batch(file):
    # class, database_name, website, data
    dict = toolbox.unpickle(file)
    keys = [*dict]
    labels = dict.get(keys[1])
    data = dict.get(keys[2])
    output = []
    for l,d in zip(labels, data):
        output.append((l, toolbox.cifar_convert_image(d)))
    return output


def build_cifar_10():
    '''
    '''
    database_tools.create_db("test.db")

    label_names_dict = toolbox.unpickle('original_cifar10/batches.meta')
    label_names = label_names_dict.get([*label_names_dict][1])
    images = __cifar_10_process_batch('original_cifar10/data_batch_1')
    images += __cifar_10_process_batch('original_cifar10/data_batch_2')
    images += __cifar_10_process_batch('original_cifar10/data_batch_3')
    images += __cifar_10_process_batch('original_cifar10/data_batch_4')
    images += __cifar_10_process_batch('original_cifar10/data_batch_5')
    test_images = __cifar_10_process_batch('original_cifar10/data_batch_5')
    images_for_db = []
    for n in label_names:
        images_for_db.append([])
    
    for i in images:
        images_for_db[i[0]].append(i[1])

    conn = database_tools.connect("test.db")
    for i in range(0, len(images_for_db)):
        database_tools.add_images(conn, images_for_db[i], str(label_names[i])[2:-1], "cifar10", "CIFAR-10")

    images_for_db = []
    for n in label_names:
        images_for_db.append([])
    
    for i in test_images:
        images_for_db[i[0]].append(i[1])

    for i in range(0, len(images_for_db)):
        database_tools.add_images(conn, images_for_db[i], str(label_names[i])[2:-1], "cifar10_test", "CIFAR-10")

    database_tools.print_info_images(conn)
    conn.close()


def build_cifar_100():
    '''
    '''
    pass


def build_own_cifar_10():
    '''
    '''
    pass