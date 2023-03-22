#!/usr/bin/python3
"""

"""

import os
import sys
import glob
import subprocess

import tqdm

def make_count_resolution():
    resolution2count = {}
    def count_resolution(stdout:str):
        resolution = stdout.split(" ")[0]
        if resolution not in resolution2count:
            resolution2count[resolution] = 1
        else:
            resolution2count[resolution] += 1
        return resolution2count
    return count_resolution

if __name__ == "__main__":

    if len(sys.argv)<=1 or 3<=len(sys.argv): # no argument
        print("get_images_shape <anydir>")
        sys.exit(1)

    target_dir = sys.argv[1]
    target_dir = os.path.abspath(target_dir)
    assert os.path.exists(target_dir)
    assert os.path.isdir(target_dir)

    # load img paths 
    image_paths = []
    image_suffixes = ['.JPG', '.jpg', '.png', '.PNG']
    for suffix in image_suffixes:
        image_paths += glob.glob(f"{target_dir}/*{suffix}")
    image_paths.sort()

    # 
    template = "{:<30}: {}"
    print(template.format("Target Dir Name", target_dir))
    print(template.format('Number of Images', len(image_paths)))

    # count resoulution 
    print("# Resolution counts")
    stdouts = []
    count_resolution = make_count_resolution()
    for path in tqdm.tqdm(image_paths):
        result = subprocess.run(["identify", "-format", "%G %M", f"{path}"], 
                                stdout=subprocess.PIPE)
        stdouts += [result.stdout.decode("UTF-8")]
        resolution2count = count_resolution(stdouts[-1])
    
    for resolution, count in resolution2count.items():
        print(template.format(resolution, count))
    
