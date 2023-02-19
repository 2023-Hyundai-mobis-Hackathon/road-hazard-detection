import cv2

image_path = '../dataset/mainroad2_data/imag/V1F_HY_7476_20201209_143452_E_CH1_Seoul_Cloud_Mainroad_Day_41878.png'
label_path ='../dataset/mainroad2_data/labels/V1F_HY_7476_20201209_143452_E_CH1_Seoul_Cloud_Mainroad_Day_41878.txt'

image = cv2.imread(image_path)

class_list = ['Animals(Dolls)', 'Person', 'Garbage bag & sacks', 'Construction signs & Parking prohibited board', 'Traffic cone', 'Box', 'Stones on road', 'Pothole on road', 'Filled pothole', 'Manhole', 'overloaded', 'not overloaded']
colors = [(0, 255, 0), (0, 0, 255), (255, 0, 0), (0, 255, 255), (255,0, 255), (255, 255, 0), (255, 127, 0), (127, 255, 0), (0, 255, 127), (0, 127, 255),(255, 0, 127), (127, 0, 255)]

height, width, _ = image.shape
print(image.shape)

T=[]
with open(label_path, "r") as file1:
    for line in file1.readlines():
        split = line.split(" ")

        # getting the class id
        class_id = int(split[0])
        color = colors[class_id]
        clazz = class_list[class_id]

        # getting the xywh bounding box coordinates
        x, y, w, h = float(split[1]), float(split[2]), float(split[3]), float(split[4])

        # re-scaling xywh to the image size
        box = [int((x - 0.5*w)* width), int((y - 0.5*h) * height), int(w*width), int(h*height)]
        cv2.rectangle(image, box, color, 2)
        cv2.rectangle(image, (box[0], box[1] - 20), (box[0] + box[2], box[1]), color, -1)
        cv2.putText(image, class_list[class_id], (box[0], box[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, .5, (0,0,0))

cv2.imwrite("./output.jpg", image)
