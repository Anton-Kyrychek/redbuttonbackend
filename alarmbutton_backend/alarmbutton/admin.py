from django import forms
from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.contrib.admin.views.autocomplete import AutocompleteJsonView
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import Users, Caretaker, Customer, ButtonsEvents, StatusChoices


class MyAutocompleteJsonView(AutocompleteJsonView):
    def get_queryset(self):
        """Return queryset based on ModelAdmin.get_search_results()."""
        return super(MyAutocompleteJsonView, self).get_queryset().filter(active=True)


class SuperAdminSite(AdminSite):
    site_title = 'Червона Кнопка'
    site_header = 'Червона Кнопка'
    index_title = 'Червона Кнопка'

    def has_permission(self, request):
        return request.user.is_superuser and request.user.is_active

    def autocomplete_view(self, request):
        return MyAutocompleteJsonView.as_view(admin_site=self)(request)


admin_super = SuperAdminSite(name='admin_super')


class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email',)}),
        (_('Permissions'), {
            # 'fields': ('is_active', 'is_superuser', 'user_permissions'),
            'fields': ('is_active', 'is_superuser',),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active')
    list_filter = ('is_superuser', 'is_active',)
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-is_active', 'username',)
    filter_horizontal = ('user_permissions',)
    readonly_fields = ('last_login', 'date_joined')
    actions = None

    def has_delete_permission(self, request, obj=None):
        return False


class UserChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return (super().label_from_instance(obj) + " " + str(obj.birth_year)
                if obj.birth_year
                else super().label_from_instance(obj))


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'fathers_name', 'birth_year','phone_number', 'caretaker', 'address', 'number_buttons_event', 'registration_code', 'active', 'comment')
    list_display_links = ()
    search_fields = ('last_name', 'first_name', 'birth_year')
    readonly_fields = ('number_buttons_event', 'registration_code', )
    ordering = ('-active', )
    actions = None

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == 'caretaker':
            kwargs['form_class'] = forms.ModelChoiceField
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def has_delete_permission(self, request, obj=None):
        return False


class CaretakerAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'fathers_name', 'phone_number', 'number_buttons_received', 'number_buttons_responded', 'active', 'comment',)
    search_fields = ('last_name', 'first_name')
    readonly_fields = ('number_buttons_responded', 'number_buttons_received')
    ordering = ('-active', )
    actions = None

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == 'user':
            kwargs['form_class'] = forms.ModelChoiceField
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def has_delete_permission(self, request, obj=None):
        return False


# class StatusChoicesAdmin(admin.ModelAdmin):
#     list_display = ('id', 'status')
#     search_fields = ('status', )
#     save_as = False
#     save_as_continue = False
#     save_on_top = False
#     list_display_links = None
#     actions = None
#     view_on_site = False
#
#     def has_add_permission(self, request):
#         return False
#
#     def has_delete_permission(self, request, obj=None):
#         return False


class ButtonsEventsAdmin(admin.ModelAdmin):
    list_display = ('customer', 'birth_year', 'created_at', 'caretaker', 'caretaker_phone', 'customer_phone', 'status', 'address', 'responded_at', 'resolved_at', 'comment',)
    list_filter = ('status', 'customer', 'caretaker')
    autocomplete_fields = ('caretaker',)
    readonly_fields = ('created_at', 'comment', 'responded_at', 'resolved_at', 'customer')
    list_editable = ('status', 'caretaker', 'comment')
    ordering = ('status', '-created_at', )
    list_display_links = None
    actions = None
    sortable_by = ('customer', 'status', 'caretaker', 'created_at', 'responded_at', 'resolved_at')
    list_per_page = 10

    class Media:
        js = ("sound.js", "events.js", )

    def has_add_permission(self, request):
        return False

    @admin.display(description='Тел. Доглядача')
    def caretaker_phone(self, obj):
        return str(obj.caretaker.phone_number)

    @admin.display(description='Тел. Підопічного')
    def customer_phone(self, obj):
        return str(obj.customer.phone_number)

    @admin.display(description='Адреса')
    def address(self, obj):
        return str(obj.customer.address)

    @admin.display(description='Рік народження')
    def birth_year(self, obj):
        return str(obj.customer.birth_year)

    def has_delete_permission(self, request, obj=None):
        return False


admin_super.register(Users, MyUserAdmin)
admin_super.register(Customer, CustomerAdmin)
admin_super.register(Caretaker, CaretakerAdmin)
# admin_super.register(StatusChoices, StatusChoicesAdmin)
admin_super.register(ButtonsEvents, ButtonsEventsAdmin)
