from upload_machine.utils.uploader.piggo_upload import piggo_upload




def auto_upload(siteitem,file,record_path,qbinfo,basic,hashlist):
    return eval(siteitem.sitename+'_upload(siteitem,file,record_path,qbinfo,basic,hashlist)')