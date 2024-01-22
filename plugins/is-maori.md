# is-maori

* domain(s): pretrain, pairs
* accepts: ldc.pretrain.PretrainData, ldc.supervised.pairs.PairData
* generates: ldc.pretrain.PretrainData, ldc.supervised.pairs.PairData

Determines whether text is Māori or not (weak or strict mode), using the supplied threshold. The filter action then determines what to do with the record.

```
usage: is-maori [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}] [-N LOGGER_NAME]
                [-m MIN_MAORI] [-s]
                [-L [{any,instruction,input,output,content} [{any,instruction,input,output,content} ...]]]
                [-a {keep,discard}]

Determines whether text is Māori or not (weak or strict mode), using the
supplied threshold. The filter action then determines what to do with the
record.

optional arguments:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  -m MIN_MAORI, --min_maori MIN_MAORI
                        The minimum required ratio (0-1) of Māori words in the
                        text. (default: 0.0)
  -s, --strict          Whether to use strict mode rather than weak one.
                        (default: False)
  -L [{any,instruction,input,output,content} [{any,instruction,input,output,content} ...]], --location [{any,instruction,input,output,content} [{any,instruction,input,output,content} ...]]
                        Which data use for counting tokens; pairs:
                        any,instruction,input,output, pretrain: any,content
                        (default: any)
  -a {keep,discard}, --action {keep,discard}
                        How to react when the thresholds are met (default:
                        keep)
```
