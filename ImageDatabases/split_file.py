import os

CHUNK_SIZE = 50000000 # 50 mb File sizes

def split_file(filename: str, new_name: str):
    file_number = 1
    os.mkdir(new_name)
    with open(filename, "rb") as f:
        chunk = f.read(CHUNK_SIZE)
        while chunk:
            with open(new_name + '/' + new_name + str(file_number), "wb") as chunk_file:
                chunk_file.write(chunk)
            file_number += 1
            chunk = f.read(CHUNK_SIZE)


def restore_file(folder_name: str, file_name: str):
    file_number = 1
    with open(file_name, "wb") as file:
        while True:
            try: 
                with open(folder_name + '/' + folder_name + str(file_number), "rb") as f:
                    chunk = f.read()
                    file.write(chunk)
                    print(file_number)
                    file_number += 1

            except:
                break


if __name__ == '__main__':
    # split_file('light_database.db', 'light_database')
    # restore_file('light_database', 'light_database1.db')
    # split_file('test.db', 'test')
    restore_file("test","test.db")
    pass
