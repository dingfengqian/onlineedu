from datetime import datetime

from django.db import models

# Create your models here.
from apps.users.models import UserProfile
from apps.courses.models import Course

# Create your models here.


class UserAsk(models.Model):
    """
    用户我要学习表单
    """
    name = models.CharField(max_length=20, verbose_name="姓名")
    mobile = models.CharField(max_length=11, verbose_name="手机")
    course_name = models.CharField(max_length=50, verbose_name="课程名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户咨询"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '用户: {0} 手机号: {1}'.format(self.name, self.mobile)


class CourseComments(models.Model):
    """
    用户对于课程评论
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程")
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户")
    comments = models.CharField(max_length=250, verbose_name="评论")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="评论时间")

    class Meta:
        verbose_name = "课程评论"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '用户({0})对于《{1}》 评论 :'.format(self.user, self.course)


class UserFavorite(models.Model):
    """
    用户对于课程,机构，讲师的收藏
    """
    # 会涉及四个外键。用户，课程，机构，讲师
    TYPE_CHOICES = (
        (1, u"课程"),
        (2, u"课程机构"),
        (3, u"讲师")
    )

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户")
    fav_id = models.IntegerField(default=0, verbose_name="数据id")
    fav_type = models.IntegerField(choices=TYPE_CHOICES, default=1, verbose_name="收藏类型")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户收藏"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '用户({0})收藏了{1} '.format(self.user, self.fav_type)


class UserMessage(models.Model):
    """
    用户消息表
    """
    # 因为我们的消息有两种:发给全员和发给某一个用户。
    # 所以如果使用外键，每个消息会对应要有用户。很难实现全员消息。

    # 机智版 为0发给所有用户，不为0就是发给用户的id
    user = models.IntegerField(default=0, verbose_name="接收用户")
    message = models.CharField(max_length=500, verbose_name="消息内容")

    # 是否已读: 布尔类型 BooleanField False未读,True表示已读
    has_read = models.BooleanField(default=False, verbose_name="是否已读")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户消息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '用户({0})接收了{1} '.format(self.user, self.message)


class UserCourse(models.Model):
    """
    用户课程表
    """
    # 会涉及两个外键: 1. 用户， 2. 课程
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程")
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户课程"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '用户({0})学习了{1} '.format(self.user, self.course)