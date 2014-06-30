# SJTU Score Fetcher
A tool to fetch scores from the SJTU electsys

## Example
```python
from sjtuscorefetcher import ScoreFetcher


sf = ScoreFetcher('5110312345', '12345678')
sf.login()
scores = sf.get_scores()
for score in scores:
    print score[0], score[1], score[2]
```
