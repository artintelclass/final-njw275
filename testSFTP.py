import pysftp
import os

srv = pysftp.Connection(host="10.224.18.247", username="nyuad",
password="A@rt!1ntelll")

srv.chdir('MachineLearning/deep-painterly-harmonization/data')
print(srv.pwd)

try: 

	srv.remove("0_c_mask.jpg")
	srv.remove("0_c_mask_dilated.jpg")
	srv.remove("0_target.jpg")
	srv.remove("0_naive.jpg")
except Exception,e:
	print(e)

os.remove('0_c_mask_dilated.jpg')
os.remove('0_c_mask.jpg')
os.remove('0_naive.jpg')


os.rename('0_c_mask_dilated500.jpg', '0_c_mask_dilated.jpg')
os.rename('0_c_mask500.jpg', '0_c_mask.jpg')
os.rename('0_naive500.jpg', '0_naive.jpg')

srv.put('0_c_mask.jpg')
srv.put('0_c_mask_dilated.jpg')
srv.put('0_naive.jpg')
srv.put('0_target.jpg')
# srv.get('me.jpg')