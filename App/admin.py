from django.contrib import admin
from .models import Product,Order,Design,Feedback
# Register your models here.

admin.site.site_header="Dhanam trades"
admin.site.site_title="Admin"
admin.site.index_title="Dhanam Merchant"

admin.site.register(Design)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name','product_brand','product_description','product_image','trending_product','product_kg','product_cost')
    # list_filter =['trending_product'] 
    search_fields = ['product_name']
admin.site.register(Product,ProductAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer_name','customer_number','products', 'total_number_of_product','total_cost',"time",'status')
    list_display_links = ['status']
    list_editable = ['products']
    list_filter=['status']
    search_fields = ['customer_name','customer_number']
admin.site.register(Order,OrderAdmin)

class FeedbackAdmin(admin.ModelAdmin):
    list_display=('feedbacker_name','feedbacker_number','feedback','feedback_status','show_in_page')
    list_display_links=['feedback_status','show_in_page']
    # list_filter=['feedback_status']
    search_fields = ['feedbacker_name','feedbacker_number']
    def has_add_permission(self, request):
        return False
    
    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        extra_context = {}
        extra_context['show_save_and_continue']=False
        # extra_context['show_save']=False
        return super(FeedbackAdmin,self).changeform_view(request, object_id, form_url, extra_context)

admin.site.register(Feedback,FeedbackAdmin)