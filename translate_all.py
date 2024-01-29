from multiprocessing.pool import Pool

from MangaTranslator import Translator,TranslateTask
from MangaTranslator import (
    TargetLanguages,
    TextDetectors,
    DetectionSizes,
    TextDirections,
    TranslatorBackends
)

from session import Session

from glob import glob

import asyncio

# --------------------- CONFIG ---------------------
INPUT_DIR = 'input' #输入文件夹
RESULT_DIR = 'result'  #输出文件夹(自动创建)

#翻译器设定
TARGET_LANGUAGE=TargetLanguages.Chinese_Simplified
TRANS_DETECTOR=TextDetectors.Default
TRANS_DIRECTION=TextDirections.Default
TRANS_TRANSLATOR=TranslatorBackends.GPT35
TRANS_SIZE=DetectionSizes.px2560

#上传下载线程数量
WORKERS_UPLOAD=10
WORKERS_DOWNLOAD=10

# --------------------- ENDCONFIG ---------------------

file_list = sorted(
    glob(
        pathname=f'{INPUT_DIR}/**/*[jpg,png]',
        recursive=True
    )
)

file_count = len(file_list)

translator=Translator(
    target_language=TARGET_LANGUAGE,
    detector=TRANS_DETECTOR,
    direction=TRANS_DIRECTION,
    translator=TRANS_TRANSLATOR,
    size=TRANS_SIZE
)

session = Session(translator=translator)

class jumpOut(Exception):
    ...

def push_task(file_path) -> TranslateTask:
    try:
        if id_status:=session.get_task(file_path):
            id,status = id_status.split('@')
            if id == 'None':
                raise jumpOut("not a valid id")
            t = TranslateTask(id,file_path)
            if status.strip()=='1':
                t.success(f'https://r2.cotrans.touhou.ai/mask/{t.id}.png')
            return t
    except Exception:
        ...
    t=translator.new_task(file_path)
    session.add_task(t)
    return t

def save_img(task:TranslateTask):
    task.save(RESULT_DIR)

async def main():
    # print('Start Translate...')
    print('Start to upload Images')
    task_list:list[TranslateTask]=[]

    with Pool(processes=WORKERS_UPLOAD) as tp:
        task_list=tp.map(
            push_task,
            file_list
        )
        tp.close()
        tp.join()

    print('All upload Success!')
    unfinished_tasks=[t for t in task_list if not t.client_finished]
    
    while len(unfinished_tasks:=[t for t in unfinished_tasks if not t.client_finished]) > 0:
        print(f'find {len(unfinished_tasks)} unfinished task(s),wait them...')
        for ut in unfinished_tasks:
            print(f'waiting for task {ut.id} o={ut.original_file_path}')
            await translator.preserve_task(ut)
            if ut.client_finished:
                session.add_task(ut)
            elif ut.error_retries >= 3:
                #失败过多直接跳过!,用1x1图片盖住()
                ut.success('https://i0.hdslb.com/bfs/bangumi/94466dbf154b7da5fa0f1f20dae476efe8892368.jpg@1w_1h.png')
    print('Saving Images...')
    with Pool(processes=WORKERS_DOWNLOAD) as tp:
        tp.map(
            save_img,
            task_list
        )

    print('All Done')
    # print('delete session file...')
    # session.delete()
    input('press any key to quit')
        

asyncio.run(main())