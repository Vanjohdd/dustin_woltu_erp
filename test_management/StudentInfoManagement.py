from ..business_api import request
from ..common_object import Global
from ..common_object.WhichDatabaseEnum import WhichDatabaseEnum
from ..common_util.ResponseMessageHelper import ResponseMessageHelper, ResponseHelper
from ..database_access.BaseAccess import BaseAccess
from ..database_access.test.StudentInfoAccess import StudentInfoAccess
from ..database_util.PSQLOperate import PSQLOperate
from ..database_util.PostgresqlOperate import PostgresqlOperate
from ..common_util.BaseManagement import BaseManagement




class StudentInfoManagement(BaseManagement):
# #查
#     def query_all_student_info(self, query_condition, page_index=1, page_size=80, query_name_list=[],
#                                  show_name_list=[], order_by=None, group_by=None):
#
#         with PostgresqlOperate(WhichDatabaseEnum.Odoo10Database) as op:
#             access = StudentInfoAccess(op, self)
#             row_count, result, page_index = access.query_all_student_info(query_condition, page_index, page_size,
#                                                                             query_name_list, show_name_list, order_by,
#                                                                             group_by)
#             if access.error_code == Global.response_error_code:
#                 return ResponseHelper.error("查询学生信息失败[%s]" % access.error_message)
#
#             return ResponseHelper.success_pagination(row_count, result, page_index)

    #分页查询
    def query_all_student_info(self, query_condition, page_index=1, page_size=80, query_name_list=[],
                                  show_name_list=[], order_by=None, group_by=None):
        #定义函数并接收了查询条件：.........
        with PostgresqlOperate(WhichDatabaseEnum.Odoo10Database, False) as op:
            #执行对postgresqloperate数据库的操作
            access = StudentInfoAccess(op, self)
            #对系统子系统进行操作
            row_count, result, next_page_index = access.query_all_student_info(query_condition,
                                                                                    query_name_list=query_name_list,
                                                                                    show_name_list=show_name_list,
                                                                                    page_index=page_index,
                                                                                    page_size=page_size,
                                                                                    order_by=order_by,
                                                                                    group_by=group_by)
            #调用方法传入查询条件并返回row_count, result, next_page_index
            if access.error_code == Global.response_error_code:
                error_info = "query sub system failure[%s]" % access.error_message
                return ResponseMessageHelper.get_error_response_dict(error_info)
            #错误响应字典，有错误就返回


            return ResponseMessageHelper.get_pagination_response_dict(row_count, result, next_page_index)
        #若没有发生错误，就返回row_count, result, next_page_index

#查询
    def query_student_info(self, query_json_data, query_name_list=[],
          show_name_list=[]):
        with PostgresqlOperate(WhichDatabaseEnum.Odoo10Database, False) as op:
            access = StudentInfoAccess(op, self)
            row_count, result, next_page_index = access.query_all_student_info(query_json_data,
                                                                               query_name_list=query_name_list,
                                                                               show_name_list=show_name_list)
            if access.error_code == Global.response_error_code:
                error_info = "query sub system failure[%s]" % access.error_message
                return ResponseMessageHelper.get_error_response_dict(error_info)
            return ResponseMessageHelper.get_pagination_response_dict(row_count, result, next_page_index)




#增
    # def modify_student_info(self, json_data):

    #   def modify_student_info(self, json_data):
    #     request_data = request.jsonrequest
    #
    #     validator = ModifyStudentInfo(request_data)
    #
    #     is_pass = validator.is_valid()
    #     if not is_pass:
    #        return ResponseMessageHelper.get_error_response_dict(validator.errors)
    #
    #     account = StudentInfoManagement(request)
    #
    #     return account.modify_student_info(request_data)
    # def modify_student_info(self, page_index, page_size,order_by,group_by):
    #     with PSQLOperate(WhichDatabaseEnum.Odoo10Database, False) as op:
    #         access = StudentInfoAccess(op, self)
    #         row_count, result, page_index = access.modify_student_info(page_index, page_size,order_by,group_by)
    #         if access.error_code == Global.response_error_code:
    #             return ResponseHelper.error("添加学生信息失败[%s]" % access.error_message)
    #         return ResponseHelper.success_pagination(row_count, result, page_index)
    def modify_student_info(self,json_data):
        with PostgresqlOperate(WhichDatabaseEnum.Odoo10Database, False) as op:
            access = StudentInfoAccess(op, self)
            save_data = json_data.get("update_save_json")
            update_dict = {
                "id": save_data.get("id"),
                "age": save_data.get("age")
            }

            access.write_no_log(update_dict)
            if access.error_code == Global.response_error_code:
                op.rollback()
                return ResponseHelper.error("修改学生信息失败[%s]" % (access.error_message))

            op.commit()

            return ResponseHelper.success_message('hello')

    def modify_student_info(self,  json_data):
        with PostgresqlOperate(WhichDatabaseEnum.Odoo10Database, False) as op:
            access = StudentInfoAccess(op, self)
            save_data = json_data.get("delete_save_json")
            delete_dict = {
                "id": save_data.get("id"),
                "age": save_data.get("age")
            }
            access.delete(delete_dict)
            if access.error_code == Global.response_error_code:
                op.rollback()
                return ResponseHelper.error("删除学生信息失败[%s]" % (access.error_message))
            op.commit()
            return ResponseHelper.success_message('hello')


    def modify_student_info(self, json_data):
        with PostgresqlOperate(WhichDatabaseEnum.Odoo10Database, False) as op:
            access = StudentInfoAccess(op, self)
            save_data = json_data.get("create_save_json")
            create_dict = {
                "age": save_data.get("age"),
                "class": save_data.get("class"),
                "student_name": save_data.get("student_name"),
                "student_id": save_data.get("student_id")
            }
            access.create_odoo_no_log(create_dict)
            if access.error_code == Global.response_error_code:
                op.rollback()
                return ResponseHelper.error("添加学生信息失败[%s]" % (access.error_message))
            op.commit()
            return ResponseHelper.success_message('hello')

    def query_student_info(self, json_data):
        with PostgresqlOperate(WhichDatabaseEnum.Odoo10Database, False) as op:
            access = StudentInfoAccess(op, self)
            save_data = json_data.get("query_save_json")
            query_dict={
                "id": save_data.get("id"),
                "age": save_data.get("age"),
                "class": save_data.get("class"),
                "student_name": save_data.get("student_name"),
                "student_id": save_data.get("student_id")

            }
            access.query(query_dict)
            if access.error_code == Global.response_error_code:
                op.rollback()
                return ResponseHelper.error("查询学生信息失败[%s]" % (access.error_message))
            op.commit()
            return ResponseHelper.success_message('hello')


    def query_student_info(self, query_json_data, query_name_list=[],
          show_name_list=[]):
        with PostgresqlOperate(WhichDatabaseEnum.Odoo10Database, False) as op:
            access = StudentInfoAccess(op, self)
            row_count, result, next_page_index = access.query_all_student_info(query_json_data,
                                                                               query_name_list=query_name_list,
                                                                               show_name_list=show_name_list)
            access.query(query_dict)
            if access.error_code == Global.response_error_code:
                op.rollback()
                return ResponseHelper.error("查询学生信息失败[%s]" % (access.error_message))
            op.commit()
            return ResponseHelper.success_message('hello')


