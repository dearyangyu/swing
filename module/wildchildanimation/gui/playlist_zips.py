import zipfile

PLAYBLAST_FILE = "Z:/productions/wotw/wotw_build/101_alickofpaint/shots/sc010/sh000/layout/sc010_sh000_layout/playblasts.zip"

zip_file = zipfile.ZipFile(PLAYBLAST_FILE, 'r')
for item in zip_file.filelist:
    print(item)

