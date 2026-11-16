import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))



from src.feature_extractor import SQLiFeatureExtractor

extractor = SQLiFeatureExtractor()

samples = [
    "char(49)=char(49)",
    "0x41424344",
    "1 OR SLEEP(5)",
    "admin'--",
]

for payload in samples:
    print(payload)
    print(extractor.extract(payload))
    print()