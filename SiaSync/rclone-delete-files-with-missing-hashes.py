from rclone_python import rclone

SIA_FOLDER = "sia:/default/"

if rclone.is_installed():
    hashes = rclone.ls(SIA_FOLDER, 1000000, False, True, ["--hash"])
    print("files without hashes")
    for hash in hashes:
        try:
            md5 = hash['Hashes']['md5']
            # hash was found, skip this file
        except:
            # hash not found, delete the file
            file_to_delete = hash['Path']
            print("deleting " + file_to_delete, flush=True)
            rclone.delete(SIA_FOLDER + file_to_delete)
else:
    print("rclone not installed")
