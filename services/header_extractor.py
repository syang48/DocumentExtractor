import boto3
import cv2
import numpy as np

def get_dynamic_header(img_full):

    height, width, _ = img_full.shape
    # """
    # Analyzes an image using AWS Textract and returns a cropped header strip.
    # """
    # textract = boto3.client('textract')
    # height_full, width_full = img_full.shape[:2]
    
    # # Pre-process: Crop to top 50% to save on Textract processing
    # mid_y = height_full // 2
    # img_top_half = img_full[0:mid_y, 0:width_full]

    # # Encode to bytes for AWS
    # _, buffer = cv2.imencode(".png", img_top_half)
    # image_bytes = buffer.tobytes()

    # try:
    #     response = textract.analyze_document(
    #         Document={'Bytes': image_bytes},
    #         FeatureTypes=["LAYOUT"]
    #     )

    #     max_bottom_pixel = 0
    #     found_content = False

    #     for block in response["Blocks"]:
    #         # Focus on Headers and Titles
    #         if block["BlockType"] in ["LAYOUT_HEADER"]:
    #             found_content = True
    #             box = block['Geometry']['BoundingBox']
    #             # Calculate Y coordinate relative to the top half
    #             current_bottom = int((box['Top'] + box['Height']) * mid_y)
                
    #             if current_bottom > max_bottom_pixel:
    #                 max_bottom_pixel = current_bottom

    #     if found_content and max_bottom_pixel > 0:
    #         padding = 25
    #         final_y = min(mid_y, max_bottom_pixel + padding)
    #         return img_top_half[0:final_y, 0:width_full]
            
    # except Exception as e:
    #     print(f"AWS Error: {e}")
    
    # Return None if no signature is found
    return img_full[0:int(height * 0.15), 0:width]
