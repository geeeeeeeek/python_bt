from django.db import models

# Create your models here.
from django.db.models import Q


class LinkQuerySet(models.query.QuerySet):

    def get_search_list(self, q):
        if q:
            return self.filter(status=True).filter(Q(title__contains=q)).order_by('-timestamp')
        else:
            return self.filter(status=True).order_by('-timestamp')

    def get_recommend_list(self):
        return self.filter(status=True).order_by('-hot')[:4]

    def get_fake_list(self):
        return self.filter(status=True).order_by('-hot')[:]


class Link(models.Model):
    list_display = ("url", "desc", "contact")
    url = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    cover = models.ImageField(upload_to='cover/', null=True)
    size = models.CharField(max_length=100, blank=True, null=True)
    hot = models.IntegerField(default=0)
    desc = models.CharField(max_length=200, blank=True, null=True)
    contact = models.CharField(max_length=100, blank=True, null=True)
    status = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    objects = LinkQuerySet.as_manager()

    def __str__(self):
        return self.title

    class Meta:
        db_table = "bt_link"

    def increase_hot_count(self):
        self.hot += 1
        self.save(update_fields=['hot'])
