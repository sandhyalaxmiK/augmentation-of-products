# Creating a dataset with grocery store products and augmentation-of-grocery-products
short way to create a large dataset of products  (grocery store) in a rack by using less images.
Taken 11 products and annotated using labelImg tool,created xml files. based on this annotations along with images, generated more number of images (can create lackss of images) along with jsons.

### all_temp_comb.py
This file is used to place augmented products on the rack randomly

### comb_place_order_original.py
This file is used to place 11 products in a rack with different permutations

### json2xml.py
This file is used to create xml for the given json file.

### remove_node_xml.py
This file is used to remove a node and appending its childs to its parent node in xml file.

### augmentation.py
This file is used for augmentations for products (flip, rotate,resize,crop,Ltranslation)
