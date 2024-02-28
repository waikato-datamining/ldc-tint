# de-macronize

* domain(s): pairs, pretrain, translation, classification
* accepts: ldc.api.supervised.pairs.PairData, ldc.api.pretrain.PretrainData, ldc.api.translation.TranslationData, ldc.api.supervised.classification.ClassificationData
* generates: ldc.api.supervised.pairs.PairData, ldc.api.pretrain.PretrainData, ldc.api.translation.TranslationData, ldc.api.supervised.classification.ClassificationData

Removes macrons from text, e.g., Ā -> Aa and ā -> aa

```
usage: de-macronize [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                    [-N LOGGER_NAME] [-d {strip,double,triple}]
                    [-L [{any,instruction,input,output,content,text} [{any,instruction,input,output,content,text} ...]]]
                    [-g [LANGUAGE [LANGUAGE ...]]]

Removes macrons from text, e.g., Ā -> Aa and ā -> aa

optional arguments:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  -d {strip,double,triple}, --demacronization {strip,double,triple}
                        How to process the macrons (default: double)
  -L [{any,instruction,input,output,content,text} [{any,instruction,input,output,content,text} ...]], --location [{any,instruction,input,output,content,text} [{any,instruction,input,output,content,text} ...]]
                        Where to look for the macrons; classification:
                        any|text, pairs: any|instruction|input|output,
                        pretrain: any|content, translation: any|content
                        (default: any)
  -g [LANGUAGE [LANGUAGE ...]], --language [LANGUAGE [LANGUAGE ...]]
                        The languages to inspect; inspects all if not
                        specified (default: None)
```
