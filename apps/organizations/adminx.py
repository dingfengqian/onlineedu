from .models import CityDict, CourseOrg, Teacher

import xadmin


class CityDictAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']


class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'click_nums', 'fav_nums', 'address', 'city', 'add_time']
    search_fields = ['name', 'desc', 'click_nums', 'fav_nums', 'address', 'city']
    list_filter = ['name', 'desc', 'click_nums', 'fav_nums', 'address', 'city', 'add_time']


class TeacherAdmin(object):
    list_display = ['organization', 'name', 'work_years', 'work_company', 'work_position']
    search_fields = ['organization', 'name','work_years', 'work_company', 'work_position']
    list_filter = ['organization', 'name', 'work_years', 'work_company', 'work_position']

xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)