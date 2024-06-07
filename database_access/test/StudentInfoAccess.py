from ...common_object.RowDataStatusEnum import RowDataStatusEnum
from ...database_access.BaseAccess import BaseAccess
from odoo.http import request


class StudentInfoAccess(BaseAccess):
    def __init__(self, postgresql_operate, base_management):
        super().__init__(postgresql_operate, base_management)

        self._table_name = 'student_info'

        self._primary_key_list = []

        self._primary_key_list.append('id')

        self._add_initial_data = {}

    def query_all_student_info(self, query_condition, page_index, page_size,
                               query_name_list, show_name_list, order_by, group_by):

        where_sql, paras = self._convert_query_condition_2_sql_condition(query_condition, need_data_permission=True)
        exist_sql = ''

        select_sql = """SELECT *
                          FROM student_info AS a
                          JOIN student_class_info  AS b  ON a.student_id = b.student_id 
                          JOIN student_private_info AS c ON a.student_id = c.student_id
                   """

        query_sql = super()._generate_specify_query_name_sql(select_sql, query_name_list=query_name_list)

        if exist_sql:
            query_sql += exist_sql

        if where_sql:
            query_sql += where_sql

        if order_by:
            query_sql += " Order By " + order_by

        return self._query_pagination(query_sql, paras=paras, page_index=page_index, page_size=page_size)
#
#

#
    # def modify_student_info(self, page_index, page_size, order_by, group_by, modify_name_list=None):
    #     where_sql, paras = self._convert_query_condition_2_sql_condition(query_condition, need_data_permission=True)
    #     exist_sql = ''
    #
    #     modify_sql = """
    #                     insert into student_info('id','age','class','student_name','student_id')
    #                     values (15,16,2,'十一','20231111')
    #
    #             """
    #
    #     modify_sql = super()._generate_specify_modify_name_sql(modify_sql, modify_name_list=modify_name_list)
    #     if exist_sql:
    #         modify_sql += exist_sql
    #
    #     if where_sql:
    #         modify_sql += where_sql
    #
    #     if order_by:
    #         modify_sql += " Order By " + order_by
    #
    #     return self._query_pagination(modify_sql, paras=paras, page_index=page_index, page_size=page_size)

    # def query_all_student_info(self, query_condition,query_name_list, show_name_list, page_index, page_size,
    #                              order_by, group_by):
    #     where_sql, paras = self._convert_query_condition_2_sql_condition(query_condition, need_data_permission=True)
    #     exist_sql = ''
    #
    #     select_sql = """
    #                     select *
    #                       from student_info
    #                       left join student_class_info
    #                       on student_info.student_id=student_class_info.student_id
    #                     """
    #     query_sql = super()._generate_specify_query_name_sql(select_sql, query_name_list=query_name_list)
    #
    #     if exist_sql:
    #         query_sql += exist_sql
    #
    #     if where_sql:
    #         query_sql += where_sql
    #
    #     if order_by:
    #         query_sql += " Order By " + order_by
    #
    #     return self._query_pagination(query_sql, paras=paras, page_index=page_index, page_size=page_size)

    def query_student_info(self,id_list):
        select_sql="""
                select student_name
                from student_info
        """
        return self.query(select_sql,(tuple(id_list),))


    # def __init__(self, postgresql_operate, base_management):
    #     super().__init__(postgresql_operate, base_management)
    #
    #     self._table_name = 'system_menu_list'
    #
    #     self._primary_key_list = []
    #     self._primary_key_list.append('menu_code')
    #
    #     self._add_initial_data = {}
    #
    #     self._add_initial_data.update({"status": RowDataStatusEnum.Complete.value[0]})
    #     self._add_initial_data.update({"sort_order": 10})
    #     self._add_initial_data.update({"navigate_menu": True})
    #     self._add_initial_data.update({"lower_code_page": False})

    # def query_all_student_info(self, query_condition, page_index, page_size,
    #                            query_name_list, show_name_list, order_by, group_by):
    #
    #     where_sql, paras = self._convert_query_condition_2_sql_condition(query_condition, need_data_permission=True)
    #     exist_sql = ''
    #
    #     select_sql = """
    #                    SELECT *
    #                    FROM student_info
    #                    JOIN student_class_info    ON student_info.student_id = student_class_info.student_id ;
    #                    JOIN student_private_info  ON student_info.student_id = student_private_info.student_id;
    #                  """
    #
    #     query_sql = super()._generate_specify_query_name_sql(select_sql, query_name_list=query_name_list)
    #
    #     if exist_sql:
    #         query_sql += exist_sql
    #
    #     if where_sql:
    #         query_sql += where_sql
    #
    #     if order_by:
    #         query_sql += " Order By " + order_by
    #
    #     return self._query_pagination(query_sql, paras=paras, page_index=page_index, page_size=page_size)
