import csv
from efficientnet_pytorch import EfficientNet
import os
import torchvision.transforms as transforms
import torchvision.datasets as datasets
import torch.nn as nn
import torch.distributed as dist
import torch.multiprocessing as mp
from collections import OrderedDict
from PIL import Image
import torch
import argparse

# app.py에서 identifier 입력 받은 후 (완)
# 받은 identifier로 500DB에서 표시앞 또는 표시뒤로 추출 (comp)
# 추출 내용을 모델로 전달

f = open("pillTableDB500.csv", "rt", encoding="UTF-8")
rdr = csv.reader(f)
identList = []


def extract500(identifier):
    for line in rdr:
        if identifier == line[1] or identifier == line[2]:
            identList.append(line[0])

<<<<<<< HEAD
    print(identList)
    # for ident in identList :
    #     print(ident)
=======
    for idents in identList:
        print(idents)
    return identList


def setup_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-j",
        "--workers",
        default=16,
        type=int,
        metavar="N",
        help="number of data loading workers (default: 4)",
    )

    parser.add_argument("--gpu", default=0, type=int, help="GPU id to use.")

    return parser


def validate(class_list, model_path, data_path):
    parser = setup_parser()
    args, unknown = parser.parse_known_args()

    args.num_classes = len(class_list)
    args.model_path = model_path
    args.data_path = data_path

    if args.gpu is not None:
        print("Use GPU: {} for training".format(args.gpu))

    print("=> creating model efficientnet-b6")
    model = EfficientNet.from_name("efficientnet-b6", num_classes=4990)
    if os.path.isfile(args.model_path):
        print("=> loading checkpoint '{}'".format(args.model_path))
        state_dict = torch.load(args.model_path)["state_dict"]
        keys = state_dict.keys()
        values = state_dict.values()

        new_keys = []
        for key in keys:
            new_key = key[7:]  # remove the 'module.'
            new_keys.append(new_key)

        new_dict = OrderedDict(list(zip(new_keys, values)))
        model.load_state_dict(new_dict)
        print("=> loaded checkpoint '{}'".format(args.model_path))

    model.cuda(args.gpu)

    image_size = EfficientNet.get_image_size("efficientnet-b6")
    normalize = transforms.Normalize(
        mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
    )
    val_transforms = transforms.Compose(
        [
            transforms.Resize(image_size, interpolation=Image.BICUBIC),
            transforms.CenterCrop(image_size),
            transforms.ToTensor(),
            normalize,
        ]
    )

    """load image, returns cuda tensor"""
    images = Image.open(args.data_path)
    images = val_transforms(images).float()
    images = images.unsqueeze(0)

    # switch to evaluate mode
    model.eval()

    labels = os.listdir("../data/good_image/reference_image/")
    with torch.no_grad():
        images = images.cuda(non_blocking=True)

        # compute output
        output = model(images)
        output_label = torch.topk(output, 1)
        pred_class = labels[int(output_label.indices)]  # final result
        print(pred_class)
    return pred_class
>>>>>>> 98e608e9fa8db1d25f929571b507345505ca5103
