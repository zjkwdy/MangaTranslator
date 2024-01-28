import os
from os.path import exists
from MangaTranslator import TranslateTask,Translator
from MangaTranslator.translator.feature_enumerations import *
from MangaTranslator.utils.encoding import md5enc
from threading import Lock

#记录上传过的本地id
class Session:

    task_map:dict[str,str] #{b64path:id}
    write_lock:Lock
    session_file:str

    def __init__(
            self,
            translator:Translator
        ) -> None:
        self.session_file = f'.translate-{translator.generate_inner_id()}.session'
        mode = 'r+' if exists(self.session_file) else 'w+'
        self.__session_fp__=open(self.session_file,mode=mode)
        self.task_map={(x:=self.__decode_line__(line))[0]:x[1] for line in self.__session_fp__.readlines()}
        self.write_lock=Lock()

    def __decode_line__(self,line:str):
        "md5enc(ofile_path)@task_id@finished?"
        ofile_path_enc,client_id,finished=line.split('@')
        return (ofile_path_enc,f'{client_id}@{finished}')
    
    def __encode_line__(self,task:TranslateTask) -> str:
        "md5enc(ofile_path)@task_id@finished?"
        return f"{md5enc(task.original_file_path)}@{task.id}@{int(task.server_finished)}"
    
    #可多次调用,后盖前
    def add_task(self,task:TranslateTask):
        self.task_map[md5enc(task.original_file_path)]=f'{task.id}@{int(task.server_finished)}'
        line_to_add = self.__encode_line__(task=task)
        with self.write_lock:
            self.__session_fp__.write(line_to_add+'\n')
            self.__session_fp__.flush()
    
    def get_task(self,task_opath):
        "返回 taskid@status"
        k=md5enc(task_opath)
        return self.task_map.get(k,False)
    
    def delete(self):
        self.__session_fp__.close()
        os.remove(self.session_file)