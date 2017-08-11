import caffe
import numpy as np 

caffe.set_mode_gpu()

# make sure the train data for the 2 different nets are different (e.g. train for trained_VGG and val for new_VGG
# because caffe will bug out otherwise

trained_VGG = caffe.Net("Teacher-Student-Training/imagenet/alexnet-VGG/vgg16_original.prototxt", "VGG_ILSVRC_16_layers.caffemodel", caffe.TRAIN)

new_VGG = caffe.Net("Teacher-Student-Training/imagenet/alexnet-VGG/vgg16_dummy.prototxt", caffe.TRAIN)

# we load the first 4 convolutions
mapping = {"conv1_1" : "conv_st_1_1",
		   "conv1_2" : "conv_st_1_2",
		   "conv2_1" : "conv_st_2_1",
		   "conv2_2" : "conv_st_2_2"}

for i in range(0, len(mapping)):
	trained = mapping.keys()[i]
	new = mapping.values()[i]
	new_VGG.params[new][0].data[...] = trained_VGG.params[trained][0].data[...]
	new_VGG.params[new][1].data[...] = trained_VGG.params[trained][1].data[...]
	print "mapped %s to %s" % (trained, new)

# remove layers that were not copied over
for key in new_VGG.params.keys():
	if key not in mapping.keys():
		new_VGG.params.pop(key)
		new_VGG.blobs.pop(key)

new_VGG.save("preloaded_VGG.caffemodel")
