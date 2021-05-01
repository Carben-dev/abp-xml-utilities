# Abp Language XML Utilities

When developing with ASP. NET Boilerplate, if you use a translatable label in your app, you will most likely need to add that label and its translation to every language you intend to support.
This process is time-consuming and repetitive.
ABP Language XML Utilities (ALXU) can help you get rid of some of that trouble.

ALXU supports the following operations:
 - Compare the missing key (label) of the two language XML files
 - Add the missing key (label) to the XML
 - Copy the missing key (label) and value (translation) to the XML
 - Add the missing key, and the Google translated value (translation) to the XML (Google Api Key and Google Python SDK is required)

## Usage
```
usage: python3 main.py base target action
    base: path to the language base xml file
    target: path to the target language xml file
    action: diff      - compare the key difference between base and target
            keyonly   - add the key to target which is missing, leave the value blank
            keyvalue  - add the key to target which is missing, copy the value to target
            translate - add the key to target which is missing, add google translation to target
```
## Google API
### Install Google Python SDK
```
pip install google-cloud-translate==2.0.1
```
### Get you own Google API Auth json file
From: https://cloud.google.com/translate/docs/setup

You json file will look like this:
```
{
  "type": "",
  "project_id": "",
  "private_key_id": "",
  "private_key": "",
  "client_email": "",
  "client_id": "",
  "auth_uri": "",
  "token_uri": "",
  "auth_provider_x509_cert_url": "",
  "client_x509_cert_url": ""
}
```
rename it to:
```
google-key.json
```
and place it with the main.py

## Example Run
### run - diff
```
> python3 main.py base.xml target.xml diff

Compared <base.xml> and <target.xml>:

Found 2 key(s) in base, but not in target:
<text name="IAmNotInTarget1">I am not in target 1.</text>
<text name="IAmNotInTarget2">I am not in target 2.</text>

Found 1 key(s) in target, but not in base:
<text name="IAmNotInBase">I am not in base.</text>
```
### run - keyonly
```
> python3 main.py base.xml target.xml keyonly
Copying new key from <base.xml> to <target.xml>
Done. 2 keys or values has been written to <target.xml>
```
#### target.xml result:
```
<?xml version='1.0' encoding='UTF-8'?>
<localizationDictionary culture="zh-Hans">
  <texts>
    <text name="HomePage">主页</text>
    <text name="AboutUs">关于我们</text>
    <text name="Administration">管理</text>
    <text name="Roles">角色</text>
    <text name="Users">用户</text>
    <text name="IAmNotInBase">I am not in base.</text>

    <!-- === Begin: Auto generate by Abp Language XML Utilities At 2021-04-30 19:34:39.716519 === -->
    <text name="IAmNotInTarget1"> </text>
    <text name="IAmNotInTarget2"> </text>
    <!-- === End: Auto generate by Abp Language XML Utilities At 2021-04-30 19:34:39.716519 === -->
    </texts>
</localizationDictionary>
```
### run - keyvalue
```
> python3 main.py base.xml target.xml keyonly
Copying new key from <base.xml> to <target.xml>
Done. 2 keys or values has been written to <target.xml>
```
#### target.xml result:
```
<?xml version='1.0' encoding='UTF-8'?>
<localizationDictionary culture="zh-Hans">
  <texts>
    <text name="HomePage">主页</text>
    <text name="AboutUs">关于我们</text>
    <text name="Administration">管理</text>
    <text name="Roles">角色</text>
    <text name="Users">用户</text>
    <text name="IAmNotInBase">I am not in base.</text>

    <!-- === Begin: Auto generate by Abp Language XML Utilities At 2021-04-30 19:38:08.842375 === -->
    <text name="IAmNotInTarget1">I am not in target 1.</text>
    <text name="IAmNotInTarget2">I am not in target 2.</text>
    <!-- === End: Auto generate by Abp Language XML Utilities At 2021-04-30 19:38:08.842375 === -->
    </texts>
</localizationDictionary>
```
### run - Google translate
```
> python3 main.py base.xml target.xml translate
Copying new key and google translated value from <base.xml> to <target.xml>
Google Translate: I am not in target 1. -> 我不在目标1中。
Google Translate: I am not in target 2. -> 我不在目标2中。
Done. 2 keys or values has been written to <target.xml>
```
#### target.xml result:
```
<?xml version='1.0' encoding='UTF-8'?>
<localizationDictionary culture="zh-Hans">
  <texts>
    <text name="HomePage">主页</text>
    <text name="AboutUs">关于我们</text>
    <text name="Administration">管理</text>
    <text name="Roles">角色</text>
    <text name="Users">用户</text>
    <text name="IAmNotInBase">I am not in base.</text>

    <!-- === Begin: Auto generate by Abp Language XML Utilities At 2021-04-30 19:40:15.794672 === -->
    <text name="IAmNotInTarget1">我不在目标1中。</text>
    <text name="IAmNotInTarget2">我不在目标2中。</text>
    <!-- === End: Auto generate by Abp Language XML Utilities At 2021-04-30 19:40:15.794672 === -->
    </texts>
</localizationDictionary>
```
