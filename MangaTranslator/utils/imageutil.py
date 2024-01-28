from io import BytesIO
from PIL import Image 

def image_from_bytes(ib:bytes) -> Image:
    return Image.open(BytesIO(ib)).convert('RGBA')

def image_from_file(file_path:str) -> Image:
    return Image.open(fp=file_path).convert('RGBA')

def mix_images(img:Image,mask:Image):
    try:
        final_img = Image.new("RGBA",img.size)
        final_img.paste(img,(0,0),img)
        final_img.paste(mask,(0,0),mask)
        return final_img
    except:
        print('Warning: img mix faild,returning base img...')
        return img