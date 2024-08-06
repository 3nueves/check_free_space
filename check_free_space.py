import yaml
import shutil

from yaml.loader import SafeLoader
from subprocess import run

free = {}

def load_config():
    """ load config from yaml file """
    with open('config.yaml', "r", encoding="utf-8") as f:
        try:
            data = yaml.load(f, Loader=SafeLoader)
        except yaml.YAMLError as exc:
            print(exc)
    return data


def check_partition(partition):
    """ check used storage """
    total, _, available = shutil.disk_usage(partition)
    # we calculate the size in percentage
    value = available * 100 / total
    return value


def show_files(path, file):
    """ show files  """
    return run([f"stat -c '%n %s' -- {path}/{file}"], shell=True, text=True, capture_output=True, timeout=30)


def truncate_files(path, file):
    """ truncate files """
    file = open(path+"/"+file, 'a')
    file.truncate(0)
    file.close()


def check_storage():
    """ starting checking to partitions """
    config = load_config()
    for data in config:
        print("\nPartition")
        print("---------")
        size = check_partition(data['partitions'])

        print(f'Part: {data['partitions']}')
        print(f'Free: {int(size)}%')
        print(f'Threshold: {data['threshold']}%')

        if size <= data['threshold']:
            print(f"\nFree storage of partition '{data['partitions']}: {int(size)}%' it's more down that threshold: {data['threshold']}%, action required.\n")
            print("Files to trucate")
            print("---------------")

            for file in data['files']:
                f = show_files(file['path'], file['name'])
                print(f.stdout.strip())
            print("\nFiles Truncated")
            print("---------------")

            for file in data['files']:
                truncate_files(file['path'], file['name'])
                f = show_files(file['path'], file['name'])
                print(f.stdout.strip())

            print("\nCurrent Size")
            print("------------")
            size = check_partition(data['partitions'])
            print(f'Part: {data['partitions']}')
            print(f'Free: {int(size)}%')
        else:
            print(f"\nFree storage of partition '{data['partitions']}: {int(size)}%' it's over threshold: {data['threshold']}%, not action required.\n")

if __name__ == '__main__':
    check_storage()
