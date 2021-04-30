import sys, os
import xml.etree.ElementTree as XML
from datetime import datetime

googe_api_key_json = "./google-key.json"

def translate_text(target, text):
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    import six
    from google.cloud import translate_v2 as translate

    translate_client = translate.Client()

    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, target_language=target)
    print("Google Translate: <{}> -> <{}>".format(result["input"], result["translatedText"]))

    return result['translatedText']

class AbpLanguageXML:
    def __init__(self, file_path):
        self.file_path = file_path
        self.dict = {}

        # create element tree object
        self.tree = XML.parse(self.file_path)
        # get root element
        self.root = self.tree.getroot()
        # set language code
        self.lang_code = self.root.attrib['culture']
        # set
        for text in self.root.findall('./texts/text'):
            self.dict[text.attrib['name']] = text.text

    def diff(self, target):
        no_in_target = {}
        no_in_base = {}
        for key, value in self.dict.items():
            if key not in target.dict:
                no_in_target[key] = value

        for key, value in target.dict.items():
            if key not in self.dict:
                no_in_base[key] = value

        return no_in_target, no_in_base

    def add_key(self, target, copy_value=False, translation=False):
        now = datetime.now()
        target_missing, base_missing = self.diff(target)
        if len(target_missing) == 0:
            print("No difference is found between {} and {}".format(self.file_path, target.file_path))
            exit(0)
        texts = target.root[0]

        texts[-1].tail = "\n\n    "
        comment = XML.Comment(' === Begin: Auto generate by Abp Language XML Utilities At {} === '.format(now))
        comment.tail = "\n    "
        texts.append(comment)

        for key, value in target_missing.items():
            new_text = XML.Element('text')
            new_text.set('name', key)
            if copy_value :
                new_text.text = value
            elif translation :
                new_text.text = translate_text(target.lang_code, value)
            else:
                new_text.text = " "
            new_text.tail = "\n    "
            texts.append(new_text)

        comment = XML.Comment(' === End: Auto generate by Abp Language XML Utilities At {} === '.format(now))
        comment.tail = "\n    "
        texts.append(comment)

        target.tree.write(target.file_path, encoding="UTF-8", xml_declaration=True)

        return

    def add_key_value(self, target):
        return

    def add_translation(self, target):
        return


def print_usage(prog_name):
    print("usage: " + prog_name + " base target action")
    print("  base: path to the language base xml file")
    print("  target: path to the target language xml file")
    print("  action: diff      - compare the key difference between base and target")
    print("          keyonly   - add the key to target which is missing, leave the translation blank")
    print("          keyvalue  - add the key to target which is missing, copy the translation to target")
    print("          translate - add the key to target which is missing, add google translation to target")
    print("See: https://github.com/Carben-dev/abp-xml-utilities")


def main(argv):
    if len(argv) < 4:
        print_usage(argv[0])
        exit(1)

    base_file_path = argv[1]
    target_file_path = argv[2]
    action = argv[3]

    if action == "diff":

        base = AbpLanguageXML(base_file_path)
        target = AbpLanguageXML(target_file_path)
        no_in_target, no_in_base = base.diff(target)

        # Printing the report
        print("\nCompared <{}> and <{}>:\n".format(base_file_path, target_file_path))

        if len(no_in_target) > 0:
            print("Found {} key(s) in base, but not in target:".format(len(no_in_target)))
            for key, value in no_in_target.items():
                print("<text name=\"{}\">{}</text>".format(key, value))

        if len(no_in_base) > 0:
            print("\nFound {} key(s) in target, but not in base:".format(len(no_in_base)))
            for key, value in no_in_base.items():
                print("<text name=\"{}\">{}</text>".format(key, value))

        if len(no_in_target) == 0 and len(no_in_base) == 0:
            print("No difference is found.")

        exit(0)

    elif action == "keyonly":
        base = AbpLanguageXML(base_file_path)
        target = AbpLanguageXML(target_file_path)
        base.add_key(target)
        exit(0)

    elif action == "keyvalue":
        base = AbpLanguageXML(base_file_path)
        target = AbpLanguageXML(target_file_path)
        base.add_key(target, copy_value=True)
        exit(0)

    elif action == "translate":
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = googe_api_key_json
        base = AbpLanguageXML(base_file_path)
        target = AbpLanguageXML(target_file_path)
        base.add_key(target, translation=True)
        exit(0)

    else:
        print("Error: unrecognized action.\n")
        print_usage(argv[0])
        exit(1)


if __name__ == '__main__':
    main(sys.argv)
