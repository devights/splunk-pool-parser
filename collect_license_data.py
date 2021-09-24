import configparser
import sys


def get_pools_from_file(path):
    config = configparser.ConfigParser()
    config.read(path)
    sections = config.sections()
    pool_data = []
    for section in sections:
        if "lmpool" in section:
            quota_bytes = config[section]['quota']
            if quota_bytes != "MAX":
                quota_gb = int(quota_bytes)/1024/1024/1024
                pool_id = config[section].name.replace("lmpool:", "")
                pool_data.append({"pool": pool_id,
                                  "quota": quota_gb})
    return pool_data


def run():
    data = None
    try:
        data = get_pools_from_file(sys.argv[1])
    except configparser.MissingSectionHeaderError as ex:
        print("Bad/missing server.conf file", sys.argv[1], ex)
    if len(data) > 0:
        print_data(data)
    else:
        print("No pool data in file")


def print_data(data):
    total = 0
    for row in data:
        print("%s %s" % (row['pool'], row['quota']))
        total += row['quota']
    print("total %s" % total)


run()
