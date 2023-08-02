import json

def loadKeysTelega():
    with open("../data/keys.json", "r") as file:
        keys_data = file.read()
    return json.loads(keys_data)

def saveKeysTelega(keys):

    keys_data = json.dumps(keys)
    with open("../data/keys.json", "w") as file:
        file.write(keys_data)

def onlySaveKeys(keys):

    keys_data = json.dumps(keys)
    with open("../data/keys.json", "w") as file:
        file.write(keys_data)


def reset():
    keys_data = json.dumps(dct)
    with open("data/keys.json", "w") as file:
        file.write(keys_data)


def saveKeys(keys):

    keys_data = json.dumps(keys)
    with open("data/keys.json", "w") as file:
        file.write(keys_data)


def loadKeys():
    with open("data/keys.json", "r") as file:
        keys_data = file.read()

    return json.loads(keys_data)


def loadKeysGui():
    with open("data/keys.json", "r") as file:
        keys_data = file.read()

    return json.loads(keys_data)


dct = {
       "base": {
                        "activate_key": "",
                        "key1": {"name": "", "value": ""},
                        "key2": {"name": "", "value": ""},
                        "key3": {"name": "", "value": ""},
                        "key4": {"name": "", "value": ""},
                        "key5": {"name": "", "value": ""},
                        "key6": {"name": "", "value": ""},
                    },

       "fluxing": {
                        "activate_key": "f1",
                        "key1": {"name": "yPos", "value": "40"},
                        "key2": {"name": "depth", "value": "169"},
                        "key3": {"name": "----", "value": "w"},
                        "key4": {"name": "----", "value": "a"},
                        "key5": {"name": "----", "value": "d"},
                        "key6": {"name": "----", "value": "2"},
                        "key7": {"name": "----", "value": "3"},
                        "key8": {"name": "----", "value": "4"},
                        "key9": {"name": "----", "value": "5"},
                        "key10": {"name": "----", "value": "7"},
                        "key11": {"name": "----", "value": "0.993"},
                        "key12": {"name": "----", "value": "1.85"},
                        "key13": {"name": "----", "value": "4"},
                        "key14": {"name": "----", "value": "30"},
                        "key15": {"name": "----", "value": "spirit1.png"},
                        "key16": {"name": "----", "value": "1.3"},
                        "key17": {"name": "USER 1 ID", "value": "5068259579"},
                        "key18": {"name": "USER 2 ID", "value": "521725785"},
                        "key19": {"name": "TOKEN", "value": "5228926798:AAFeB3JRJsNxted88ljIgqPTmaXxxKYxJdU"},
                    }
       }


if __name__ == "__main__":
    onlySaveKeys(dct)
    # print(loadKeys())

