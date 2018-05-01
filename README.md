# Final (njw275)

Creating a interactive application to take pictures of people and put them into artwork using [DeepLab: Deep Labelling for Semantic Image Segmentation](https://github.com/tensorflow/models/tree/master/research/deeplab) with [deep-painterly-harmonization](https://github.com/luanfujun/deep-painterly-harmonization). These paintings are currently displayed at the Louvre Abu Dhabi.


### The Subjugated Reader
#### René Magritte

<p align="center">
<img src="https://github.com/artintelclass/final-njw275/blob/master/images/Book%20Images/book_target.jpg" width="290">
<img src="https://github.com/artintelclass/final-njw275/blob/master/images/Book%20Images/0_c_mask_dilated%2010.37.00%20PM.jpg" width="290">
<img src="https://github.com/artintelclass/final-njw275/blob/master/images/Book%20Images/0_naive%2010.37.00%20PM.jpg" width="290">
<img src="https://github.com/artintelclass/final-njw275/blob/master/images/My%20Final%20Outputs/NickBook3.jpg" width="290">
</p>

### Vincent Van Gogh’s Self Portrait, 1887
#### Vincent Van Gogh

<p align="center">
<img src="https://github.com/artintelclass/final-njw275/blob/master/images/Self%20Portrait/gogh_target.jpg" width="290">
<img src="https://github.com/artintelclass/final-njw275/blob/master/images/Self%20Portrait/0_c_mask%2010.13.49%20PM.jpg" width="290">
<img src="https://github.com/artintelclass/final-njw275/blob/master/images/Self%20Portrait/0_naive%2010.13.49%20PM.jpg" width="290">
<img src="https://github.com/artintelclass/final-njw275/blob/master/images/My%20Final%20Outputs/NickGogh.jpg" width="290">
</p>

### Game of Bezique
#### Gustave Caillebotte

<p align="center">
<img src="https://github.com/artintelclass/final-njw275/blob/master/images/Card%20Game/cards_target.jpg" width="290">
<img src="https://github.com/artintelclass/final-njw275/blob/master/images/Card%20Game/0_c_mask%2010.54.43%20PM.jpg" width="290">
<img src="https://github.com/artintelclass/final-njw275/blob/master/images/Card%20Game/nick%20getting%20beat%20at%20cards%2022-30-13-416.jpg" width="290">
<img src="https://github.com/artintelclass/final-njw275/blob/master/images/My%20Final%20Outputs/cards_final_res.jpg" width="290">
</p>

### Portrait of George Washington
#### Gilbert Stuart

<p align="center">
<img src="https://github.com/artintelclass/final-njw275/blob/master/images/GW/gw_target.jpg" width="290">
<img src="https://github.com/artintelclass/final-njw275/blob/master/images/GW/0_c_mask_dilated%2010.26.29%20PM.jpg" width="290">
<img src="https://github.com/artintelclass/final-njw275/blob/master/images/GW/0_naive%2010.26.29%20PM.jpg" width="290">
<img src="https://github.com/artintelclass/final-njw275/blob/master/images/My%20Final%20Outputs/gw_final_res.jpg" width="290">
</p>

### Saint Eustace
#### Albrecht Dürer

<p align="center">
<img src="https://github.com/artintelclass/final-njw275/blob/master/images/St.%20Eustace/0_target.jpg" width="290">
<img src="https://github.com/artintelclass/final-njw275/blob/master/images/St.%20Eustace/0_c_mask.jpg" width="290">
<img src="https://github.com/artintelclass/final-njw275/blob/master/images/St.%20Eustace/0_naive.jpg" width="290">
<img src="https://github.com/artintelclass/final-njw275/blob/master/images/My%20Final%20Outputs/print_final_res.jpg" width="290">
</p>

## Set Up

Use googlecollab.py to make:
*0_c_mask.jpg
*0_c_mask_dilated.jpg
*0_naive.jpg

From there, I ran deep-painterly-harmonization's [gen_all.py](https://github.com/luanfujun/deep-painterly-harmonization/blob/master/gen_all.py) and deep-painterly-harmonization's [filt_cnn_artifact.m](https://github.com/luanfujun/deep-painterly-harmonization/blob/master/filt_cnn_artifact.m) to create the final output image. 

## Issues I Ran Into

*If you run out of memory on the GPU, look to change gen_all.py's image_size and make your images the same size ratio

