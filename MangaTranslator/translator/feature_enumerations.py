from enum import StrEnum,unique

@unique
class TargetLanguages(StrEnum):
    Chinese_Simplified='CHS'  
    Chinese_Traditional='CHT'
    Czech='CSY'
    Dutch='NLD'
    English='ENG'
    French='FRA'
    German='DEU'
    Hungarian='HUN'
    Italian='ITA'
    Japanese='JPN'
    Korean='KOR'
    Polish='PLK'
    Portuguese_Brazil='PTB'
    Romanian='ROM'
    Russian='RUS'
    Spanish='ESP'
    Turkish='TRK'
    Ukrainian='UKR'
    Vietnamese='VIN'
    Arabic='ARA'

@unique
class TextDetectors(StrEnum):
    Default="default"
    ComicTextDetector="ctd"

@unique
class DetectionSizes(StrEnum):
    px1024="S"
    px1536="M"
    px2048="L"
    px2560="X"

@unique
class TextDirections(StrEnum):
    Default="default"
    Auto="auto"
    Horizontal="h"
    Vertical="v"

@unique
class TranslatorBackends(StrEnum):
    GPT35="gpt3.5"
    Youdao="youdao"
    Baidu="baidu"
    Google="google"
    Deepl="deepl"
    Papago="papago"
    Offline="offline"
