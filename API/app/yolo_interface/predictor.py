import subprocess
import sys
import os, glob
from PIL import Image
from pydantic import BaseModel
from app.settings import config

""" 
Class interfacing with Yolov7 object detection model 
"""    

class Predictor():


    def init(weight_file_path :str, input_folder : str, output_folder : str):
        """ 
        init : Initialize class variables
        
        :param conf_threshold: confidence threshold to be used for prediction
        :param conf_threshold: IoU threshold to be used for prediction
        """

        Predictor.process_path = os.getcwd()

        # A subfolder named output will be automatically used  to store the annotated image
        # YOLO expects a subfolder so output path is derived from PROJ_PATH
        
        os.makedirs(output_folder, exist_ok = True)
        Predictor.output_path = os.path.join(Predictor.process_path, output_folder)   

        # Let's use input subfolder as the same level for original images to be predicted   

        Predictor.input_path = os.path.join(Predictor.process_path, input_folder)         
        os.makedirs(input_folder, exist_ok = True)


        # Path to the weights of our best YOLO model so far
        yolo_conf = config.get("yolo")
        Predictor.weight_file_path = os.path.join(Predictor.process_path, "app/model_params",  yolo_conf.get("weight_file"))
        Predictor.confidence_threshold = yolo_conf.get("confidence_threshold")
        Predictor.iou_threshold = yolo_conf.get("iou_threshold")


    def __init__(self):
        """ 
        __init__ : Constructor for class Predictor 
        """
        return 
      

    def predict(self, input_file_name : str):
        """ 
        predict : use Yolo V7 model to performa object detection 
        
        :input_file_name: file name in the input folder of the image to be used for prediction
        :return: filename of the image where detection/classification has been indicated
        """        
      
        # Get the image dropped by the end-user 

        uploaded_img = Image.open(os.path.join(Predictor.input_path, input_file_name))

        # Save the image in a folder that will be accessed by the inference process

        sourcefile = os.path.join(Predictor.input_path, input_file_name)
        uploaded_img.save(sourcefile)

        # Pending question : no need to resize ?  Apparently not !
        # img= image.load_img(img_data.name, target_size= (256,256))

        # Call the YOLOV7 inference process 

        subprocess.run([f"{sys.executable}", 
                        "./app/yolov7/detect.py",
                        "--weights", Predictor.weight_file_path,
                        "--img", "256",                                         # inference size h,w
                        "--conf-thres", str(Predictor.confidence_threshold),    # confidence threshold set from the slider
                        "--iou-thres", str(Predictor.iou_threshold),            # NMS IoU threshold set from the slider
                        # "--max-det", "36",                                    # maximum detections per image
                        "--source", Predictor.input_path,                       # full path to input folder
                        "--project", Predictor.process_path,                    # full path to results folder (without "output")
                        "--name", Predictor.output_path,                        # this will add "output" to the above
                        # "--line-thickness", "2",                              # bounding box thickness (pixels) 
                        "--exist-ok",                                           # existing project/name ok, do not increment
                        ], shell=False)

        # For the record, the following command does not work under a streamlit process :
        #!python detect.py --weights best.pt --img 256 --conf 0.5 --source mypic.jpg --project /content/yolov5/runs/detect

        # Return file path to the image decorated by red bouding boxes around detected containers
        return os.path.join(Predictor.output_path, input_file_name)

    
    def clean_up_folders(self, clean_input: bool, clean_output: bool):
        """ 
        clean-up : delete input and output folders
        :clean_input: indicates if input folder has to be cleaned-up
        :clean_output: indicates if output folder has to be cleaned-up  
        :return: nothing
        """        
        if clean_input:
            for file in os.scandir(Predictor.input_path):
                os.remove(file.path)
        if clean_output:
            for file in os.scandir(Predictor.output_path):
                os.remove(file.path)