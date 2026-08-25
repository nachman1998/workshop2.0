"""
Save a random sample of 2D histogram images as individual PNGs, then
stitch them together into a single mosaic image for quick visual
review.
"""
import os
import numpy as np
from matplotlib import pyplot as plt

path=data = r"C:\Users\nachm\PycharmProjects\workshop\python_for_handin\sts\_unified_pics\sc_ok_sts.npy"
output_dir=r"C:\Users\nachm\PycharmProjects\workshop\python_for_handin\sts\_unified_pics\output"
num_cols = 4
size=8

def carate_pics(data,output_dir,size=60,num_cols = 4):
  from PIL import Image
  import math
  x = np.zeros(len(data), dtype=int)
  x[:size] = 1
  np.random.shuffle(x)
  data=data[x==1,:,:]
  print(data.shape)
  os.makedirs(output_dir, exist_ok=True)
  for i, histogram in enumerate(data):
      print(histogram.shape,i)
      fig, ax = plt.subplots(figsize=(8, 6))
      im = ax.imshow(histogram, cmap="grey_r",vmax=1,extent=[0, 1500, 0, 1500])
      #fig.colorbar(im, ax=ax, label="Value")
      fig.tight_layout()
      fig.savefig(
          os.path.join(output_dir, f"image_{i:05d}.png"),
          dpi=150
      )
      plt.close(fig)

  # Create mosaic
  image_files = sorted([
      os.path.join(output_dir, f)
      for f in os.listdir(output_dir)
      if f.endswith(".png") and f.startswith("image_")
  ])
  images = [Image.open(f) for f in image_files]
  n_cols = num_cols
  n_rows = math.ceil(len(images) / n_cols)
  img_width, img_height = images[0].size
  mosaic = Image.new(
      "RGB",
      (n_cols * img_width, n_rows * img_height),
      "white"
  )
  for i, img in enumerate(images):
      row = i // n_cols
      col = i % n_cols
      x = col * img_width
      y = row * img_height
      mosaic.paste(img, (x, y))
  mosaic_path = os.path.join(output_dir, "mosaic.png")
  mosaic.save(mosaic_path)
  print("Mosaic saved to:", mosaic_path)



data = np.load(path)
carate_pics(data,output_dir,size,num_cols)