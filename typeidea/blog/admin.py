import requests
from django.contrib import admin

# Register your models here.
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.auth import get_permission_codename

from typeidea.custom_site import custom_site
from .models import Post,Category,Tag
from .adminforms import PostAdminForm

PERMISSION_API = 'http:xx.sso.com/has_perm?user={}&perm_code={}'


class PostInline(admin.TabularInline):
    fields = ('title','desc')
    extra = 1
    model = Post


class CategoryOwnerFilter(admin.SimpleListFilter):
    '''自定义过滤器只展示当前用户分类'''
    title = '分类过滤器'
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id','name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


@admin.register(Category,site=custom_site)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','status','is_nav','created_time','post_count')
    fields = ('name','status','is_nav')
    list_filter = [CategoryOwnerFilter]
    inlines = [PostInline]

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(CategoryAdmin,self).save_model(request,obj,form,change)

    def post_count(self,obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'


@admin.register(Tag,site=custom_site)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name','status','created_time')
    fields = ('name','status')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(TagAdmin,self).save_model(request,obj,form,change)


@admin.register(Post,site=custom_site)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = [
        'title','category','status','owner',
        'created_time','operator'
    ]
    list_display_links = []

    list_filter = []

    search_fields = ['title','category__name']

    actions_on_top = True
    actions_on_bottom = True

    save_on_top = True

    exclude = ('owner',)

    # fields = (
    #     ('category','title'),
    #     'desc',
    #     'status',
    #     'content',
    #     'tag',
    # )

    fieldsets = (
        ('基础配置',{
            'description':'基础配置描述',
            'fields':(
                ('title','category'),
                'status',
            ),
        }),
        ('内容',{
            'fields':(
                'desc',
                'content',
            )
        }),
        ('额外信息',{
            'classes':('collapse',),
            'fields':('tag',),
        })
    )

    #filter_horizontal = ('tags',)

    def operator(self,obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('cus_admin:blog_post_change',args=(obj.id,))
        )

    operator.short_description = '操作'

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(PostAdmin,self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super(PostAdmin,self).get_queryset(request)
        return qs.filter(owner=request.user)

    #class Media:
        # css = {
        #     'all':('https://cdn.bootcss.com/bootstrap/4.0.0/css/bootstrap.min.css',),
        # }
        #js = ('https://cdn.bootcss.com/bootstrap/4.0.0/js/bootstrap.min.js',)

    def has_add_permission(self, request):
        opts = self.opts
        codename = get_permission_codename('add',opts)
        perm_code = "%s.%s" % (opts.add_label,codename)
        resp = requests.get(PERMISSION_API.format(request.user.username,perm_code))
        if resp.status_code == 200:
            return True
        else:
            return False

