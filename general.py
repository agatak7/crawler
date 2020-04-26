import os


# each website is a separate folder
def create_dir(direct):
    if not os.path.exists(direct):
        print('creating directory: ' + direct)
        os.makedirs(direct)


def create_data_files(project, base_url):
    queue = os.path.join(project, 'queue.txt')
    crawled = os.path.join(project, "crawled.txt")
    if not os.path.isfile(queue):
        write_file(queue, base_url)
    if not os.path.isfile(crawled):
        write_file(crawled, '')


def write_file(path, data):
    with open(path, 'w') as f:
        f.write(data)


def append_file(path, data):
    with open(path, 'a') as file:
        file.write(data + '\n')


def clear_file(path):
    f = open(path, 'w').close()


def links_set(path):
    results = set()
    with open(path, 'rt') as f:
        for line in f:
            results.add(line.replace('\n', ''))
    return results


def set_file(path, links):
    with open(path, "w") as f:
        for l in sorted(links):
            f.write(l + "\n")
