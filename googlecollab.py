#@title Imports

import os
from io import BytesIO
import tarfile
import tempfile
from six.moves import urllib

from matplotlib import gridspec
from matplotlib import pyplot as plt
import numpy as np
from PIL import Image, ImageDraw, ImageFont

import cv2

import tensorflow as tf

import subprocess

#@title Helper methods


class DeepLabModel(object):
  """Class to load deeplab model and run inference."""

  INPUT_TENSOR_NAME = 'ImageTensor:0'
  OUTPUT_TENSOR_NAME = 'SemanticPredictions:0'
  INPUT_SIZE = 513
  FROZEN_GRAPH_NAME = 'frozen_inference_graph'

  def __init__(self, tarball_path):
    """Creates and loads pretrained deeplab model."""
    self.graph = tf.Graph()

    graph_def = None
    # Extract frozen graph from tar archive.
    tar_file = tarfile.open(tarball_path)
    for tar_info in tar_file.getmembers():
      if self.FROZEN_GRAPH_NAME in os.path.basename(tar_info.name):
        file_handle = tar_file.extractfile(tar_info)
        graph_def = tf.GraphDef.FromString(file_handle.read())
        break

    tar_file.close()

    if graph_def is None:
      raise RuntimeError('Cannot find inference graph in tar archive.')

    with self.graph.as_default():
      tf.import_graph_def(graph_def, name='')

    self.sess = tf.Session(graph=self.graph)

  def run(self, image):
    """Runs inference on a single image.

    Args:
      image: A PIL.Image object, raw input image.

    Returns:
      resized_image: RGB image resized from original input image.
      seg_map: Segmentation map of `resized_image`.
    """
    width, height = image.size
    resize_ratio = 1.0 * self.INPUT_SIZE / max(width, height)
    target_size = (int(resize_ratio * width), int(resize_ratio * height))
    resized_image = image.convert('RGB').resize(target_size, Image.ANTIALIAS)
    batch_seg_map = self.sess.run(
        self.OUTPUT_TENSOR_NAME,
        feed_dict={self.INPUT_TENSOR_NAME: [np.asarray(resized_image)]})
    seg_map = batch_seg_map[0]
    return resized_image, seg_map


def create_pascal_label_colormap():
  """Creates a label colormap used in PASCAL VOC segmentation benchmark.

  Returns:
    A Colormap for visualizing segmentation results.
  """
  colormap = np.zeros((256, 3), dtype=int)
  ind = np.arange(256, dtype=int)

  for shift in reversed(range(8)):
    for channel in range(3):
      colormap[:, channel] |= ((ind >> channel) & 1) << shift
    ind >>= 3

  return colormap


def label_to_color_image(label):
  """Adds color defined by the dataset colormap to the label.

  Args:
    label: A 2D array with integer type, storing the segmentation label.

  Returns:
    result: A 2D array with floating type. The element of the array
      is the color indexed by the corresponding element in the input label
      to the PASCAL color map.

  Raises:
    ValueError: If label is not of rank 2 or its value is larger than color
      map maximum entry.
  """
  if label.ndim != 2:
    raise ValueError('Expect 2-D input label')

  colormap = create_pascal_label_colormap()

  for x in range(len(colormap)):
    if np.array_equal(colormap[x],[192, 128, 128]):
      colormap[x] = [255,255,255]

  if np.max(label) >= len(colormap):
    raise ValueError('label value too large.')

  return colormap[label]


def vis_segmentation(image, seg_map):
  """Visualizes input image, segmentation map and overlay view."""
  plt.figure(figsize=(15, 5))
  grid_spec = gridspec.GridSpec(1, 4, width_ratios=[6, 6, 6, 1])

  plt.subplot(grid_spec[0])
  plt.imshow(image)
  plt.axis('off')
  plt.title('input image')

  plt.subplot(grid_spec[1])
  seg_image = label_to_color_image(seg_map).astype(np.uint8)
  plt.imshow(seg_image)
  plt.axis('off')
  plt.title('segmentation map')

  plt.subplot(grid_spec[2])
  plt.imshow(image)
  plt.imshow(seg_image, alpha=0.7)
  plt.axis('off')
  plt.title('segmentation overlay')

  unique_labels = np.unique(seg_map)
  ax = plt.subplot(grid_spec[3])
  plt.imshow(
      FULL_COLOR_MAP[unique_labels].astype(np.uint8), interpolation='nearest')
  ax.yaxis.tick_right()
  plt.yticks(range(len(unique_labels)), LABEL_NAMES[unique_labels])
  plt.xticks([], [])
  ax.tick_params(width=0.0)
  plt.grid('off')
  #plt.show()


LABEL_NAMES = np.asarray([
    'background', 'aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus',
    'car', 'cat', 'chair', 'cow', 'diningtable', 'dog', 'horse', 'motorbike',
    'person', 'pottedplant', 'sheep', 'sofa', 'train', 'tv'
])

FULL_LABEL_MAP = np.arange(len(LABEL_NAMES)).reshape(len(LABEL_NAMES), 1)
FULL_COLOR_MAP = label_to_color_image(FULL_LABEL_MAP)

#@title Select and download models {display-mode: "form"}

MODEL_NAME = 'mobilenetv2_coco_voctrainaug'  # @param ['mobilenetv2_coco_voctrainaug', 'mobilenetv2_coco_voctrainval', 'xception_coco_voctrainaug', 'xception_coco_voctrainval']

_DOWNLOAD_URL_PREFIX = 'http://download.tensorflow.org/models/'
_MODEL_URLS = {
    'mobilenetv2_coco_voctrainaug':
        'deeplabv3_mnv2_pascal_train_aug_2018_01_29.tar.gz',
    'mobilenetv2_coco_voctrainval':
        'deeplabv3_mnv2_pascal_trainval_2018_01_29.tar.gz',
    'xception_coco_voctrainaug':
        'deeplabv3_pascal_train_aug_2018_01_04.tar.gz',
    'xception_coco_voctrainval':
        'deeplabv3_pascal_trainval_2018_01_04.tar.gz',
}
_TARBALL_NAME = 'deeplab_model.tar.gz'

model_dir = tempfile.mkdtemp()
tf.gfile.MakeDirs(model_dir)

download_path = os.path.join(model_dir, _TARBALL_NAME)
print('downloading model, this might take a while...')
urllib.request.urlretrieve(_DOWNLOAD_URL_PREFIX + _MODEL_URLS[MODEL_NAME],
                   download_path)
print('download completed! loading DeepLab model...')

MODEL = DeepLabModel(download_path)
print('model loaded successfully!')

#@title Run on sample images {display-mode: "form"}

# SAMPLE_IMAGE = 'image1'  # @param ['image1', 'image2', 'image3']
IMAGE_URL = 'leadphoto.jpg'  #@param {type:"string"}

# _SAMPLE_URL = ('https://github.com/tensorflow/models/blob/master/research/'
#                'deeplab/g3doc/img/%s.jpg?raw=true')


def run_visualization(url):
  """Inferences DeepLab model and visualizes result."""
  try:
#     f = urllib.request.urlopen(url)
#     jpeg_str = f.read()
#     orignal_im = Image.open(url) #BytesIO(jpeg_str))
    orignal_im = Image.open(url)
  except IOError:
    print('Cannot retrieve image. Please check url: ' + url)
    return

  print('running deeplab on image %s...' % url)
  resized_im, seg_map = MODEL.run(orignal_im)

  vis_segmentation(resized_im, seg_map)
  return resized_im, seg_map

image_url = IMAGE_URL or _SAMPLE_URL % SAMPLE_IMAGE
subprocess.call(['ffmpeg', '-i', 'me.jpg', '-vf', 'scale=500:500', 'me500.jpg'])
usersImage = raw_input("Enter image name: ");
resized_im, seg_map = run_visualization(usersImage)



orgPixelMap = resized_im.load()
seg_image = seg_map.T


img = Image.new( resized_im.mode, resized_im.size)
img = img.convert('RGBA')
pixelsNew = img.load()
for i in range(img.size[0]):
    for j in range(img.size[1]):
        if np.all(seg_image[i,j]) == 0:
            pixelsNew[i,j] = (255,0,255,0)
        else:
            pixelsNew[i,j] = orgPixelMap[i,j]
seg_image = label_to_color_image(seg_map).astype(np.uint8)

kernel = np.ones((5,5), np.uint8)

dilation = cv2.dilate(seg_image,kernel,iterations = 1)
# seg_image
# plt.imshow(seg_image)
plt.imsave('sticker.png',img);
plt.imsave('0_c_mask.jpg', seg_image)
plt.imsave('0_c_mask_dilated.jpg', dilation)


filename='sticker.png'
ironman = Image.open(filename, 'r')
filename1='0_target.jpg'
bg = Image.open(filename1, 'r')
bg_w, bg_h = bg.size
text_img = Image.new('RGBA', (bg_w,bg_h), (0, 0, 0, 0))
text_img.paste(bg, (0,0))
text_img.paste(ironman, (0,0), mask=ironman)
text_img = text_img.convert('RGB')
text_img.save("0_naive.jpg", format="jpeg")




subprocess.call(['ffmpeg', '-i', '0_c_mask.jpg', '-vf', 'scale=500:500', '0_c_mask500.jpg'])
subprocess.call(['ffmpeg', '-i', '0_c_mask_dilated.jpg', '-vf', 'scale=500:500', '0_c_mask_dilated500.jpg'])
subprocess.call(['ffmpeg', '-i', 'sticker.png', '-vf', 'scale=500:500', 'sticker500.png'])
subprocess.call(['ffmpeg', '-i', '0_naive.jpg', '-vf', 'scale=500:500', '0_naive500.jpg'])



# import pysftp

# srv = pysftp.Connection(host="10.224.18.247", username="nyuad",
# password="A@rt!1ntelll")


# srv.put('data/*')

