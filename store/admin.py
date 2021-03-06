from django.contrib import admin
from store.models import *

# Register your models here.


class AdressAdmin(admin.ModelAdmin):
    list_display = ("numero", "rue", "complement", "code_postal", "ville")


class VarietyAdmin(admin.ModelAdmin):
    list_display = ("fk_product", "name", "price", "stock", "available")
    list_filter = (
        "available",
        "fk_product",
    )


class ProductAdmin(admin.ModelAdmin):
    list_filter = ("fk_category",)


class CommandTypeAdmin(admin.ModelAdmin):
    list_display = (
        "type",
        "available",
    )
    readonly_fields = ("type",)

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False


class ClientTypeAdmin(admin.ModelAdmin):
    list_display = (
        "type_client",
        "available",
    )
    readonly_fields = ("type_client",)

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False


class AdminCodeAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "fk_client",
        "fk_direct_withdrawal",
        "fk_locker",
        "fk_delivery"
    )


class CartAdmin(admin.ModelAdmin):
    list_display = ("fk_client", "fk_variety", "quantity")
    list_filter = ("fk_client",)


class ClientAdmin(admin.ModelAdmin):
    list_display = ("user", "phone", "fk_adress", "fk_client_type")
    list_filter = ("fk_client_type",)


class MinimumCommandAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False


class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ("fk_order", "fk_variety", "quantity")
    list_filter = ("fk_order",)


class OrderHistoricAdmin(admin.ModelAdmin):
    list_display = (
        "fk_order",
        "date_creation",
        "date_end",
        "date_cancellation"
    )


class DeliveryAdmin(admin.ModelAdmin):
    list_display = ("ref_client", "instruction", "fk_delivery_slot")

    def ref_client(self, obj):
        name_client = Order.objects.get(
            fk_delivery=obj
        ).fk_client.user.username
        return name_client


admin.site.register(Adress, AdressAdmin)
admin.site.register(Variety, VarietyAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(CommandType, CommandTypeAdmin)
admin.site.register(ClientType, ClientTypeAdmin)
admin.site.register(Category)
admin.site.register(Unity)
admin.site.register(TimeSlot)
admin.site.register(CollectLocation)
admin.site.register(Locker)
admin.site.register(AdminCode, AdminCodeAdmin)
admin.site.register(DirectWithdrawal)
admin.site.register(Order, OrderAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(MinimumCommand, MinimumCommandAdmin)
admin.site.register(MessageToClient)
admin.site.register(ClientReadyToCommand)
admin.site.register(OrderDetail, OrderDetailAdmin)
admin.site.register(OrderHistoric, OrderHistoricAdmin)
admin.site.register(DeliverySlots)
admin.site.register(Delivery, DeliveryAdmin)
