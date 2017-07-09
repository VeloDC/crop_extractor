from __future__ import print_function
from utility import *
import os
from PIL import Image, ImageDraw

from Annotation import Annotation


def generate_crop_dataset(annotations_folder='',
                          images_folder='',
                          target_folder='',
                          dataset_synsets_file='',
                          done_synsets_dump_file=''):
    full_synsets_list = get_list_from_file(dataset_synsets_file)
    try:
        done_synsets_list = get_list_from_file(done_synsets_dump_file)
    except IOError:
        os.system("touch " + done_synsets_dump_file)
        done_synsets_list = []
    synsets_list = insiemistic_difference(full_synsets_list,done_synsets_list)
    create_dataset_folders(target_folder, synsets_list)
    synsets_done = 0
    total_crops_saved = 0
    total_images_cropped = 0
    total_images_notfound = 0
    f = open(done_synsets_dump_file,"a")
    for synset in synsets_list:
        synset_annotation_folder = annotations_folder + synset + '/'
        synset_crops_saved,synset_images_cropped,synset_images_notfound = generate_crop_synset(synset_annotation_folder,images_folder,target_folder)
        total_crops_saved += synset_crops_saved
        total_images_cropped += synset_images_cropped
        total_images_notfound += synset_images_notfound
        synsets_done += 1
        print(synset, file=f)
        print('done for synset ' + synset)
        print('synsets done: ' + str(synsets_done))
        print('------')
    f.close()
    print_done()
    print(str(synsets_done) + ' synsets done')
    print(str(total_crops_saved) + ' crops saved')
    print(str(total_images_cropped) + ' images cropped')
    print(str(total_images_notfound) + ' images with annotations not found')



def generate_crop_synset(synset_annotation_folder,images_folder,target_folder):
    synset_images_cropped = 0
    synset_crops_saved = 0
    synset_images_notfound = 0
    try:
        annotation_files = os.listdir(synset_annotation_folder)
        for xml_file in annotation_files:
            image_annotation = Annotation(synset_annotation_folder + xml_file)
            try:
                image = Image.open(images_folder + image_annotation.folder + '/' + image_annotation.filename + ".JPEG")
                synset_crops_saved += image_annotation.save_crops(image,target_folder,scale=True,p=0.2)
                synset_images_cropped += 1
            except IOError:
                synset_images_notfound += 1
    except OSError:
        print(synset_annotation_folder + " not found")
    print(str(synset_images_cropped) + ' images cropped')
    print(str(synset_images_notfound) + ' images with annotations not found in this synset')
    print(str(synset_crops_saved) + ' synset crops saved')
    return [synset_crops_saved,synset_images_cropped,synset_images_notfound]


def main():
    generate_crop_dataset()

if __name__ == '__main__':
    main()
