import os
from backlogic.models import NurseInfo,PatientInfo,NurseToPaientInfo
from HeadNurseBackstage.models import Head2Nurse
import xlrd
import xlwt


# 将excel数据写入mysql
def wrdb_nurseinfo(filename):
    # 打开上传 excel 表格
    excel_dir = os.path.join( os.path.dirname(__file__) , 'upload/excel' )
    # book = xlwt.Workbook()
    # sheet = book.add_sheet('Sheet1')
    # sheet.write(0,0,'name')
    # sheet.write(0,1,'username')
    # sheet.write(0,2,'password')
    # sheet.write(0,3,'workPermitNumber')
    # sheet.write(0,4,'workPermitPassword')
    # sheet.write(1,0,'name')
    # sheet.write(1,1,'username')
    # sheet.write(1,2,'password')
    # sheet.write(1,3,'workPermitNumber')
    # sheet.write(1,4,'workPermitPassword')
    # book.save(excel_dir + "/" + filename)
    readboot = xlrd.open_workbook(excel_dir + "/" + filename)
    sheet = readboot.sheet_by_index(0)
    #获取excel的行和列
    nrows = sheet.nrows
    ncols = sheet.ncols
    print(ncols,nrows)
    # sql = "insert into working_hours (name,username,password,workPermitNumber,workPermitPassword) VALUES"
    for i in range(1,):
        row = sheet.row_values(i)
        name = row[0]
        username = row[1]
        password = row[2]
        workPermitNumber = row[3]
        workPermitPassword = row[4]
        # NurseInfo.objects.create(name=name,username=username,password=password,workPermitNumber=workPermitNumber,workPermitPassword=workPermitPassword,login_jwt='')
        # Head2Nurse.objects.create(nurseWorkPermitNumber=listtext['workPermitNumber'],headNurseWorkPermitNumber=idhead)
        print(row)
# @csrf_exempt
# def upload(request):
#     # 根name取 file 的值
#     file = request.FILES.get('file')
#     print('uplaod:%s'% file)
#     # 创建upload文件夹
#     if not os.path.exists(settings.UPLOAD_ROOT):
#         os.makedirs(settings.UPLOAD_ROOT)
#     try:
#         if file is None:
#             return HttpResponse('请选择要上传的文件')
#         # 循环二进制写入
#         with open(settings.UPLOAD_ROOT + "/" + file.name, 'wb') as f:
#             for i in file.readlines():
#                 f.write(i)

#         # 写入 mysql
#         wrdb(file.name)
#     except Exception as e:
#         return HttpResponse(e)

#     return HttpResponse('导入成功')