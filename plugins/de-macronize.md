# de-macronize

* domain(s): pairs, pretrain, translation
* accepts: PairData, PretrainData, TranslationData
* generates: PairData, PretrainData, TranslationData

Removes macrons from text, e.g., Ā -> Aa and ā -> aa

```
usage: de-macronize [-h] [-l {DEBUG,INFO,WARN,ERROR,CRITICAL}]
                    [-N LOGGER_NAME] [-d {strip,double-up}]
                    [-L {any,instruction,input,output,content}]
                    [-g [LANGUAGE [LANGUAGE ...]]]

Removes macrons from text, e.g., Ā -> Aa and ā -> aa

optional arguments:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARN,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARN,ERROR,CRITICAL}
                        The logging level to use (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  -d {strip,double-up}, --demacronization {strip,double-up}
                        How to process the macrons (default: double-up)
  -L {any,instruction,input,output,content}, --location {any,instruction,input,output,content}
                        Where to look for the macons; pairs:
                        any,instruction,input,output, pretrain: any,content,
                        translation: any,content (default: any)
  -g [LANGUAGE [LANGUAGE ...]], --language [LANGUAGE [LANGUAGE ...]]
                        The languages to inspect; inspects all if not
                        specified (default: None)
```
