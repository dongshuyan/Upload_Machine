from upload_machine.utils.uploader.piggo_upload import piggo_upload
from upload_machine.utils.uploader.hdsky_upload import hdsky_upload





def auto_upload(siteitem,file,record_path,qbinfo,basic,hashlist):
    return eval(siteitem.sitename+'_upload(siteitem,file,record_path,qbinfo,basic,hashlist)')