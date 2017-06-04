import os
import argparse
from PIL import Image


def main():
    max_width, max_height, paths = parse_args()

    for path in paths:
        file = open(path, 'rb')
        img = Image.open(file)

        width, height = img.size
        ratio = min(float(max_width)/width, float(max_height)/height)
        new_width = int(ratio * width)
        new_height = int(ratio * height)

        img = img.resize((new_width, new_height))

        filename, extension = os.path.splitext(path)
        new_path = filename + '_resized' + extension
        img.save(new_path)

        file.close()


def parse_args():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('width')
    arg_parser.add_argument('height')
    arg_parser.add_argument('image_path', nargs='+')
    args = arg_parser.parse_args()

    return args.width, args.height, args.image_path


if __name__ == '__main__':
    main()
