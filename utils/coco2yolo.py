import cv2
import json
import os

labels = {0:0, 1:0, 2:0, 3:0,4:0,5:0,6:0,7:0}
count = 0

class ConvertCOCOToYOLO:

    """
    Takes in the path to COCO annotations and outputs YOLO annotations in multiple .txt files.
    COCO annotation are to be JSON formart as follows:

        "annotations":{
            "area":2304645,
            "id":1,
            "image_id":10,
            "category_id":4,
            "bbox":[
                0::704
                1:620
                2:1401
                3:1645
            ]
        }
        
    """

    def __init__(self, json_path):
        self.json_path = json_path
        

    def get_img_shape(self, img_path):
        img = cv2.imread(img_path)
        try:
            return img.shape
        except AttributeError:
            print('error!', img_path)
            return (None, None, None)

    def convert_labels(self, size, x,y,w,h):
        """
        Definition: Parses label files to extract label and bounding box
        coordinates. Converts (x1, y1, x1, y2) KITTI format to
        (x, y, width, height) normalized YOLO format.
        """

        x_centre = (x + (x+w))/2
        y_centre = (y + (y+h))/2

        # Normalization
        try:
            x_centre = x_centre / size[0]
        except:
            x_centre = x_centre / 1280
        try:
            y_centre = y_centre / size[1]
        except:
            y_centre = y_centre / 720

        try:
            w = w / size[0]
        except:
            w = w / 1280
        try:
            h = h / size[1]
        except:
            h = h / 720
        
        # Limiting upto fix number of decimal places
        x_centre = format(x_centre, '.6f')
        y_centre = format(y_centre, '.6f')
        w = format(w, '.6f')
        h = format(h, '.6f')

        return (x_centre,y_centre,w,h)

    def convert(self,annotation_key='annotations',img_id='image_id',cat_id='category_id',bbox='bbox'):
        global count
        count = 0
        # Enter directory to read JSON file
        data = json.load(open(self.json_path))
        
        check_set = set()

        size =(data['images']['width'],data['images']['height'],3)

        # Retrieve data
        for i in range(len(data[annotation_key])):

            # Get required data
            image_id = data['images']['file_name'].replace('.png', '')
            category_id = f'{data[annotation_key][i][cat_id]}'
            if int(category_id) > 8:
                continue
            
            count += 1

            bbox = data[annotation_key][i]['bbox']

            # Convert the data
            #kitti_bbox = [bbox[0], bbox[1], bbox[2] + bbox[0], bbox[3] + bbox[1]]
            yolo_bbox = self.convert_labels(size, bbox[0], bbox[1], bbox[2], bbox[3])
            
            # Prepare for export
            
            filename = f"../dataset/mainroad_data/labels/{data['images']['file_name'].replace('.png', '')}.txt"
            content =f"{int(category_id) - 1} {yolo_bbox[0]} {yolo_bbox[1]} {yolo_bbox[2]} {yolo_bbox[3]}"

            labels[int(category_id) - 1] += 1

            # Export 
            if image_id in check_set:
                # Append to existing file as there can be more than one label in each image
                file = open(filename, "a")
                file.write("\n")
                file.write(content)
                file.close()

            elif image_id not in check_set:
                check_set.add(image_id)
                # Write files
                file = open(filename, "w")
                file.write(content)
                file.close()

        if count == 0:
            try:
                #print("removing", data['images']['file_name'])
                os.remove('../dataset/mainroad_data/images/' + data['images']['file_name'])
            except:
                print("remove error", data['images']['file_name'])
                pass



# To run in as a class
if __name__ == "__main__":
    # directory = '../dataset/notcity/Validation/Annotations/1.TOA'
    # for dir in os.listdir(directory):
    #     if not dir.startswith('.'):
    #         f = os.path.join(directory, dir)
    #         for file in os.listdir(f):
    #             if not file.startswith('.'):
    #                 annot = os.path.join(f, file)
    #                 try:
    #                     ConvertCOCOToYOLO(json_path=annot).convert()
    #                 except:
    #                     print("error", annot)
    directory = '../dataset/mainroad/annotation/5.Mainroad_G04'
    for file in os.listdir(directory):
        if not file.startswith('.'):
            f = os.path.join(directory, file)
            ConvertCOCOToYOLO(json_path=f).convert()

print(labels)