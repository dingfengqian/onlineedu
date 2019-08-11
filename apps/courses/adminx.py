from .models import Course, CourseResource, Lesson, Video

import xadmin


class CourseAdmin(object):
    list_display = ['name', 'desc', 'learn_time', 'learn_nums', 'fav_nums', 'click_nums', 'add_time']
    search_fields = ['name', 'desc', 'learn_time', 'learn_nums', 'fav_nums', 'click_nums']
    list_filter = ['name', 'desc', 'learn_time', 'learn_nums', 'fav_nums', 'click_nums', 'add_time']

class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name', 'add_time']
    list_filter = ['course__name', 'name', 'add_time']

class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name', 'add_time']
    list_filter = ['lesson', 'name', 'add_time']

class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name', 'add_time']
    list_filter = ['course', 'name', 'add_time']

xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
