from .api import task_upload,preserve_task
from MangaTranslator.utils.fileutil import guess_mime,read_bytes
from .task import TranslateTask

class Translator:

    def __init__(
        self,
        target_language,
        detector,
        direction,
        translator,
        size
    ) -> None:
        self.target_language = target_language
        self.detector = detector
        self.direction = direction
        self.translator  = translator
        self.size = size
    
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