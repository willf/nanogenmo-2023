import json
import sys


def find_misspellings(obj):
    """
    Given a structure like this:

    {
    "src": "     * Verify that JVM has support for the Collator for the datbase's locale.",
    "tgt": "     * Verify that JVM has support for the Collator for the database's locale.",
    "lang": "eng"
    }

    Return a list of misspellings, like this:

    [
    {
    "src": "datbase",
    "tgt": "database",
    "lang": "eng"
    }
    ]
    """
    src_tokens = obj["src"].split()
    tgt_tokens = obj["tgt"].split()
    if len(src_tokens) != len(tgt_tokens):
        return []
    misspellings = []
    for src_token, tgt_token in zip(src_tokens, tgt_tokens):
        if src_token != tgt_token:
            misspellings.append(
                {"src": wordlike(src_token), "tgt": wordlike(tgt_token)}
            )
    return misspellings


def wordlike(token):
    """
    remove non-wordlike characters from token
    """
    return "".join([c for c in token if c.isalpha()])


def dump(obj):
    """
    print obj to stdout
    """

    print(json.dumps(obj, ensure_ascii=False))


def main():
    """
    Reading from stdin, write to stdout.

    """
    # read dictionary of words from /tmp/1

    dictionary = set()
    with open("/tmp/1") as f:
        for line in f:
            dictionary.add(line.strip())

    print("dictionary has {} words".format(len(dictionary)), file=sys.stderr)

    for line in sys.stdin:
        obj = json.loads(line)
        for misspelling in find_misspellings(obj):
            if len(misspelling["src"]) < 3:
                continue
            src = misspelling["src"]
            tgt = misspelling["tgt"]
            lc_src = misspelling["src"].lower()
            lc_tgt = misspelling["tgt"].lower()
            if lc_src != lc_tgt:
                if tgt in dictionary:
                    if lc_src != src:
                        new = {"src": lc_src, "tgt": tgt}
                        dump(new)
                    else:
                        dump(misspelling)
                elif lc_tgt in dictionary:
                    new = {"src": lc_src, "tgt": lc_tgt}
                    dump(new)


if __name__ == "__main__":
    main()
