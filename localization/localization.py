#%%

#%%
import time

import cv2
import torch
import random


from localization.models.common import DetectMultiBackend, AutoShape
from localization.utils.general import (LOGGER, Profile, check_file, check_imshow, check_requirements, colorstr, cv2,
                           non_max_suppression, scale_boxes, strip_optimizer, xyxy2xywh, check_img_size)
from localization.utils.plots import Annotator, colors, save_one_box
from localization.utils.dataloaders import transform_img

def detect( image,model,imgsz=(640,640), conf_thres=0.8,
            iou_thres=0.15, augment=False, classes=0, agnostic_nms=False):

    # Initialize
    bs = 1
    image = cv2.resize(image,(640*3,352*3))
    img = cv2.resize(image,(640,352))
    stride, names, pt = model.stride, model.names, model.pt
    #imgsz = check_img_size(imgsz, s=stride)
    im0 = image
    img, im0 = transform_img(image)
    # Run inference
    t0 = time.time()
    #model.warmup(imgsz=(1 if pt or model.triton else bs, 3, *imgsz))  # warmup
    img = torch.from_numpy(img).to(model.device)
    img = img.half() if model.fp16 else img.float()  # uint8 to fp16/32
    img /= 255  # 0 - 255 to 0.0 - 1.0
    if len(img.shape) == 3:
        img = img[None]
    #img = img.permute(0, 3, 1, 2)
    t1 = time.time()
    pred = model(img,augment=augment)
    t2 = time.time()
    # Apply NMS
    pred = non_max_suppression(pred, conf_thres, iou_thres, classes, agnostic_nms)
    final_pred = []
    t3 = time.time()
    for i, det in enumerate(pred):  # detections per image
        annotator = Annotator(im0, line_width=2, example=str(names))
        if len(det):
            # Rescale boxes from img_size to im0 size
            det[:, :4] = scale_boxes(img.shape[2:], det[:, :4], im0.shape).round()
            final_pred.append(det)
            # Write results
            for *xyxy, conf, cls in reversed(det):
                c = int(cls)  # integer class
                label = f'{names[c]} {conf:.2f}'
                annotator.box_label(xyxy, label, color=colors(c, True))
        # Print time (inference + NMS)
        print('Number of License Plate:', len(det))
        #cv2.imshow('Detected license plates', cv2.resize(im0, dsize=None, fx=0.5, fy=0.5))
    print(t2-t1)
    print(f'Done. ({(1E3 * (t2 - t0)):.1f}ms) Inference, ({(1E3 * (t3 - t2)):.1f}ms) NMS')
    return final_pred[0].to(device='cpu').detach().numpy(), im0
def load_model_local():
    weight = "/Users/tranminh/Desktop/Hoc online/Проект к ВКР/Renew Project/localization/v9-50epochs.pt"
    if torch.backends.mps.is_available():
        device = torch.device("mps")
        print('mps')
    else:
        device = torch.device("cpu")
        print('cpu')
    model_LP = DetectMultiBackend(weight, device, fuse=True)
    return model_LP

def main():
    weight = "/Users/tranminh/Desktop/Hoc online/Проект к ВКР/Renew Project/localization/v9-50epochs.pt"
    if torch.backends.mps.is_available():
        device = "mps"
    else:
        device = "cpu"
    print(device)
    model = DetectMultiBackend(weight, device, fuse=True)
    image_path = '/Users/tranminh/Desktop/Hoc online/Проект к ВКР/Renew Project/img_28.png'
    source_img = cv2.imread(image_path)
    #source_img = cv2.resize(source_img,(1920,1088))
    results = detect(source_img, model, device)
    cv2.imshow("dd",results[1])
    cv2.waitKey(0)


if __name__ == '__main__':
    main()

#%%
