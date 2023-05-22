from import_export.admin import ImportExportModelAdmin, ExportMixin
from django.contrib import admin
from .models import Cart, Order, Review, Cart_Items
from import_export import resources


class OrderResource(resources.ModelResource):
    class Meta:
        model = Order
        fields = [
            "id",
            "vendor__email",
            "customer__email",
            "item_order__item_title",
            "total_order",
            "address",
            "order_place",
            "date_time_order",
        ]
        export_order = [
            "id",
            "vendor__email",
            "customer__email",
            "item_order__item_title",
            "total_order",
            "address",
            "order_place",
            "date_time_order",
        ]


class OrderAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = OrderResource


admin.site.register(Cart)
admin.site.register(Order, OrderAdmin)
admin.site.register(Review)
admin.site.register(Cart_Items)
