# encoding=utf8
import os,sys


def create_dataset_folders(target_folder, synsets_list):
    for synset in synsets_list:
        cmd = 'mkdir -p ' + target_folder + synset
        os.system(cmd)

def insiemistic_difference(list_a, list_b):
        list_b = set(list_b)
        return[el for el in list_a if el not in list_b]

def get_list_from_file(f_name):
        content = open(f_name).readlines()
        content = [x.strip('\n') for x in content]
        return content

def dump_list_to_file(lines, f_name):
    out_file = open(f_name, "w")
    lines = map(lambda x: x+"\n", lines)
    out_file.writelines(lines)
    out_file.close()

def print_progress (iteration, total, prefix = 'Progress:', suffix = 'Complete', decimals = 1, barLength = 50):
    formatStr = "{0:." + str(decimals) + "f}"
    percent = formatStr.format(100 * (iteration / float(total)))
    filledLength = int(round(barLength * iteration / float(total)))
    bar = '█' * filledLength + '-' * (barLength - filledLength)
    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percent, '%', suffix)),
    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()

def print_done():
    print('------')
    print('DONE!!!')
    print('------')
