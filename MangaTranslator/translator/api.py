from MangaTranslator.utils.request import PUT,WS_WAIT_JSON
from MangaTranslator.translator.feature_enumerations import *

def task_upload(
        file: bytes,
        mime: str,
        target_language:TargetLanguages,
        detector:TextDetectors,
        direction:TextDirections,
        translator:TranslatorBackends,
        size:TextDirections
    ):
    
    """
    file: (bytes)
    mime: image/jpeg (auto)
    target_language: CHS
    detector: default
    direction: default
    translator: gpt3.5
    size: S:1024 M:1536 L:2048 X:2560
    """
    req = PUT(
        url='/task/upload/v1',
        files={
            'file':file
        },
        data={
            'mime':mime,
            'target_language':target_language.value,
            'detector':detector.value,
            'direction':direction.value,
            'translator':translator.value,
            'size':size.value
        }
    )
    return req.json()
    """
    return {
        id: "id_str",
        pos: pos
    }
    """

def preserve_task(task_id):
    return WS_WAIT_JSON(f'task/{task_id}/event/v1')