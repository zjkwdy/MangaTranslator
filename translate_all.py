from multiprocessing.pool import Pool

from MangaTranslator import Translator,TranslateTask
from MangaTranslator import (
    TargetLanguages,
    TextDetectors,
    DetectionSizes,
    TextDirections,
    TranslatorBackends
)

from time import sleep
from glob import glob

import asyncio

# --------------------- CONFIG ---------------------
INPUT_DIR = 'input' #输入文件夹
RESULT_DIR = 'result'  #输出文件夹(自动创建)

#翻译器设定
TARGET_LANGUAGE=TargetLanguages.Chinese_Simplified.value
TRANS_DETECTOR=TextDetectors.Default.value
TRANS_DIRECTION=TextDirections.Default.value
TRANS_TRANSLATOR=TranslatorBackends.GPT35.value
TRANS_SIZE=DetectionSizes.px2560.value

#上传下载线程数量
WORKERS_UPLOAD=10
WORKERS_DOWNLOAD=10

# --------------------- ENDCONFIG ---------------------

translator=Translator(
    target_language=TARGET_LANGUAGE,
    detector=TRANS_DETECTOR,
    direction=TRANS_DIRECTION,
    translator=TRANS_TRANSLATOR,
    size=TRANS_SIZE
)

def push_task(file_path) -> TranslateTask:
    return translator.new_task(file_path)

def save_img(task:TranslateTask):
    task.save(RESULT_DIR)

async def main():
    print('Start Translate...')
    print('Start to upload Images')
    
    task_list:list[TranslateTask]=[]

    with Pool(processes=WORKERS_UPLOAD) as tp:
        task_list=tp.map(
            push_task,
            sorted(
        glob(
                pathname=f'{INPUT_DIR}/**/*[jpg,png]',
                recursive=True
            ))
        )
        tp.close()
        tp.join()

    print('All upload Success!')
    for t in task_list:
        await translator.preserve_task(t)

    while not all([t.client_finished for t in task_list]):
        sleep(1)
    
    print('Saving Images...')
    with Pool(processes=WORKERS_DOWNLOAD) as tp:
        tp.map(
            save_img,
            task_list
        )

    print('All Done')
        

asyncio.run(main())