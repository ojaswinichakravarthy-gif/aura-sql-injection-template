import pandas as pd
import re

df = pd.read_csv("false_negatives.csv")

def classify(payload):
    p = str(payload).lower()

    if re.search(r"char\s*\(|chr\s*\(", p):
        return "CE"

    if re.search(r"0x[0-9a-f]+", p):
        return "HX"

    if any(x in p for x in [
        "sleep(",
        "benchmark(",
        "waitfor delay",
        "dbms_pipe.receive_message"
    ]):
        return "TB"

    if "%" in p:
        return "URL"

    if "--" in p or "#" in p:
        return "CT"

    if any(x in p for x in [
        "xmltype",
        "regexp_substr",
        "utl_inaddr",
        "xp_cmdshell"
    ]):
        return "DB"

    return "OTHER"

df["category"] = df["payload"].apply(classify)

print(df["category"].value_counts())

df.to_csv("false_negatives_classified.csv", index=False)