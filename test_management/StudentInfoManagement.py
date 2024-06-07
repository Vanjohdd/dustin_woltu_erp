import json
from datetime import datetime
from odoo.http import request
import pandas as pd
from ..common_util.ResponseMessageHelper import ResponseMessageHelper
from ..common_object import Global
from ..common_object.WhichDatabaseEnum import WhichDatabaseEnum
from ..common_util.ResponseMessageHelper import ResponseHelper
from ..database_access.common.BusinessTableChangedLogAccess import BusinessTableChangeLogAccess
from ..database_access.test.StudentInfoAccess import StudentInfoAccess
from ..database_util.PostgresqlOperate import PostgresqlOperate
from ..common_util.BaseManagement import BaseManagement
from ..common_util.FileUploadHelper import FileUploadHelper
import xlrd
import xlwt
from ..common_util.ExcelHelper import ExcelHelper
from io import BytesIO
from ..common_util.HttpHelper import HttpHelper
class StudentInfoManagement(BaseManagement):

    def import_student_info(self, file_list, upload_json_data):
        file = file_list[0]
        file_type = file.filename.split(".")[-1]
        file_data = file.stream._file

        if file_type not in ["xlsx", "xls"]:
            return ResponseHelper.error("上传的文件类型必须是*.xls or *.xlsx")

        success, content_list = self._deal_student_info(file_data)
        if not success:
            return ResponseHelper.error(content_list)

        with PostgresqlOperate(WhichDatabaseEnum.Odoo10Database, False) as op:
            log_access = BusinessTableChangeLogAccess(op, self)
            access = StudentInfoAccess(op, self)
            category_list = [item.get('cn_sub_category') for item in content_list]
            if not category_list:
                return ResponseHelper.error('品类不能为空')
            category_list = [item.get('cn_sub_category') for item in content_list]
            if not category_list:
                return ResponseHelper.error('品类不能为空')

            result = access.search([('cn_sub_category', 'in', list(set(category_list))), ('status', '=', 20)],
                                   ['id', 'cn_sub_category'])
            if access.error_code == Global.response_error_code:
                op.rollback()
                return ResponseHelper.error('查询品类失败%s' % access.error_message)

            if not result:
                op.rollback()
                return ResponseHelper.error('品类不存在')

            category_dict = {item.get('cn_sub_category'): item.get('id') for item in result}
            error_list = []

            for item in content_list:
                cn_sub_category = item.get("cn_sub_category")
                ref_yoy_growth = item.get("ref_yoy_growth")
                plan_ads_fee_ratio = item.get("plan_ads_fee_ratio")
                category_id = category_dict.get(cn_sub_category)

                if not category_id:
                    op.rollback()
                    error_list.append('当前三级分类不存在%s' % cn_sub_category)
                    continue

                write_data = {}
                log_content = "更新"
                if ref_yoy_growth:
                    write_data.update({"ref_yoy_growth": ref_yoy_growth})
                    log_content += '参考同比增长%s;' % ref_yoy_growth

                if plan_ads_fee_ratio:
                    write_data.update({"plan_ads_fee_ratio": plan_ads_fee_ratio})
                    log_content += '参考CPC预算比例%s;' % plan_ads_fee_ratio

                if not write_data:
                    continue

                write_data.update({"id": category_id})
                access.write(write_data)
                if access.error_code == Global.response_error_code:
                    op.rollback()
                    error_list.append('修改品类增长比例失败%s' % access.error_message)
                    continue

                log_access.add_business_table_log(access._table_name, category_id, "更新", log_content)
                if access.error_code == Global.response_error_code:
                    op.rollback()
                    error_list.append('添加日志失败%s' % log_access.error_message)
                    continue

            if error_list:
                op.rollback()
                return ResponseHelper.error(str(error_list))

            op.commit()

            return ResponseHelper.success()

    def export_student_info(self, json_data):
        with PostgresqlOperate(WhichDatabaseEnum.Odoo10Database) as op:
            student_access = StudentInfoAccess(op, self)

            query_name_list = [
                'id', 'age', 'class', 'student_name', 'student_id'
            ]

            id_list = json_data.get("id_list")
            id_list = json.loads(id_list)
            student_result = student_access.search([("id","in",id_list)], query_name_list)
            if student_access.error_code == Global.response_error_code:
                return ResponseHelper.error("查询失败[%s]" % student_access.error_code)

            wbk = xlwt.Workbook(encoding='utf-8')

            sheet = wbk.add_sheet("说明书", cell_overwrite_ok=True)

            excel_helper = ExcelHelper()

            title_style = excel_helper.set_excel_style(height=220, bold=False, nalign=1, border=1, wrap=True)
            content_style = excel_helper.set_excel_style(height=220, bold=False, nalign=1, border=1,
                                                         fontname='Times New Roman', wrap=True)
            header_list = [ "ID", "年龄", "班级", "学生姓名", "学号"]

            header_width_list = [2000, 2000, 2000, 2000, 2000]

            for col in range(len(header_list)):
                sheet.write(0, col, header_list[col], title_style)
                sheet.col(col).set_width(header_width_list[col])

            rows = 1
            for student in student_result:
                sheet.write(rows, 0, student.get("id"), content_style)
                sheet.write(rows, 1, student.get("age"), content_style)
                sheet.write(rows, 2, student.get("class"), content_style)
                sheet.write(rows, 3, student.get("student_name"), content_style)
                sheet.write(rows, 4, student.get("student_id"), content_style)

                rows += 1

            excel_obj = BytesIO()

            wbk.save(excel_obj)

            a=excel_obj.getvalue()

            file_name = "student_%s.xls" % (datetime.now().strftime("%Y%m%d%H%M%S"))

            http_helper = HttpHelper()
            return http_helper.get_response(request, excel_obj.getvalue(), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", file_name)
