from upload_machine.utils.uploader.piggo_upload import piggo_upload
from upload_machine.utils.uploader.hdsky_upload import hdsky_upload
from upload_machine.utils.uploader.audience_upload import audience_upload
from upload_machine.utils.uploader.ssd_upload import ssd_upload
from upload_machine.utils.uploader.pter_upload import pter_upload
from upload_machine.utils.uploader.hhclub_upload import hhclub_upload
from upload_machine.utils.uploader.lemonhd_upload import lemonhd_upload





def auto_upload(siteitem,file,record_path,qbinfo,basic,hashlist):
    return eval(siteitem.sitename+'_upload(siteitem,file,record_path,qbinfo,basic,hashlist)')