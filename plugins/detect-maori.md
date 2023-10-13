# detect-maori

* domain(s): pretrain
* accepts: ldc.pretrain.PretrainData
* generates: ldc.pretrain.PretrainData

Detects whether text is Māori or not, by calculating scores based on encountered characters after lower-casing the text and removing all white spaces/punctuation.

```
usage: detect-maori [-h] [-l {DEBUG,INFO,WARN,ERROR,CRITICAL}]
                    [-N LOGGER_NAME] [-M MAX_NON_MAORI] [-m MIN_MAORI]
                    [-a {keep,discard}]

Detects whether text is Māori or not, by calculating scores based on
encountered characters after lower-casing the text and removing all white
spaces/punctuation.

optional arguments:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARN,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARN,ERROR,CRITICAL}
                        The logging level to use (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  -M MAX_NON_MAORI, --max_non_maori MAX_NON_MAORI
                        The maximum allowed ratio (0-1) of non-Māori
                        characters in the text. (default: 1.0)
  -m MIN_MAORI, --min_maori MIN_MAORI
                        The minimum required ratio (0-1) of Māori characters
                        (ie long vowels) in the text. (default: 0.0)
  -a {keep,discard}, --action {keep,discard}
                        How to react when the thresholds are met (default:
                        keep)
```
