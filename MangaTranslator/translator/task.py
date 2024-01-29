from MangaTranslator.utils.request import GET
from MangaTranslator.utils.imageutil import image_from_bytes,image_from_file,mix_images
from MangaTranslator.utils.fileutil import link_path,mkdirs

from MangaTranslator.translator.feature_enumerations import *

class TranslateTask:
    
    server_finished:bool = False
    client_finished:bool = False
    
    error_retries = 0

    __status_str__: str
    result_mask_url:str 
    original_file_path:str

    def __init__(self,id:str,ofile:str) -> None:
        print(f'New Task {id} initialized. ofile={ofile}')
        self.id = id
        self.original_file_path=ofile
    
    @property
    def status_str(self):
        return self.__status_str__

    @status_str.setter
    def status_str(self,val):
        self.__status_str__ = val
        print(f'Task {self.id} for {self.original_file_path} new Status: {val}')

    def success(self,result_mask_url):
        self.server_finished = True
        self.result_mask_url=result_mask_url
        self.status_str='Server finished'
        self.client_finished = True
    
    def error(self):
        #在无法拉取任务信息时调用
        self.error_retries+=1
        self.status_str = f'{self.error_retries} error(s)'
    
    def save(self,dir):
        self.status_str = 'Downloading'
        mask_img_bytes = GET(self.result_mask_url).content
        self.status_str = 'Image combining'
        
        mask_img=image_from_bytes(mask_img_bytes)
        orig_img=image_from_file(self.original_file_path)
        
        self.result_image=mix_images(orig_img,mask_img)
        fin_path=link_path(dir,self.original_file_path)+'.png'
        mkdirs(fin_path)
        self.status_str = 'Saving'
        self.result_image.save(fin_path)
        self.status_str = 'Save success!'
