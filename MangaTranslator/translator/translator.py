from .api import task_upload,preserve_task
from MangaTranslator.utils.fileutil import guess_mime,read_bytes
from MangaTranslator.utils.encoding import sb64enc
from .task import TranslateTask
from .feature_enumerations import *

class Translator:

    def __init__(
        self,
        target_language:TargetLanguages,
        detector:TextDetectors,
        direction:TextDirections,
        translator:TranslatorBackends,
        size:TextDirections
    ) -> None:
        self.target_language = target_language
        self.detector = detector
        self.direction = direction
        self.translator  = translator
        self.size = size
    
    def generate_inner_id(self):
        #区别一次会话
        return sb64enc("{lang}@{det}@{dir}@{tran}@{size}".format_map(
            {
                'lang':self.target_language.value,
                'det':self.detector.value,
                'dir':self.direction.value,
                'tran':self.translator.value,
                'size':self.size.value
            }
        ))

    def new_task(self,file_path):
        print(f'Uploading {file_path}...')
        j = task_upload(
            file=read_bytes(file_path),
            mime=guess_mime(file_path),
            target_language=self.target_language,
            detector=self.detector,
            direction=self.direction,
            translator=self.translator,
            size=self.size
        )
        task = TranslateTask(
            id=j['id'],
            ofile=file_path
        )
        if 'result' in j:
            task.success(j['result']['translation_mask'])
        
        return task
    async def preserve_task(self,task:TranslateTask):
        if task.server_finished:
            return
        c = preserve_task(task_id=task.id)
        async for msg in c:
            if msg['type'] == 'status':
                task.status_str = msg['status']
            if msg['type'] == 'result':
                task.success(msg['result']['translation_mask'])
                break