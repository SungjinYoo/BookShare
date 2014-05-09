# -*- coding:utf-8 -*-
from .models import User

from django import forms
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect

from django.contrib import messages
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import (
    ReadOnlyPasswordHashField, AdminPasswordChangeForm)

from django.utils.html import escape
from django.shortcuts import get_object_or_404

from django.utils.translation import ugettext, ugettext_lazy as _
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters

def admin_register(model, user_admin):
    try:
        admin.site.register(model, user_admin)
    except AlreadyRegistered:
        admin.site.unregister(model)
        admin.site.register(model, user_admin)


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'user_id', 'sex') 

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):

    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField(label=_("Password"),
                                         help_text=_(u"비밀번호는 문자 그대로 저장되지 않습니다."
                                                     u" 다음 링크를 통해 변경 가능합니다."
                                                     u" <a href=\"password/\">비밀번호 변경</a>."))

    class Meta:
        model = User

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

class MyUserAdmin(UserAdmin):
    # The forms to add and change user instances
    change_user_password_template = None
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    actions = []

    filter_horizontal = ()
    list_display = (
        'user_id', 'name' ,'email', 'age', 'sex', 'date_joined', 'is_active' )
    list_filter = ('sex',)

    fieldsets = (
        (None, {'fields': ('email', 'user_id', 'password', 'phone_number',)}),
        ('Personal info',
         {'fields': ('sex', )}),
        ('Permissions', {'fields': ('is_active',)}),
        ('Important dates', {'fields': ('last_login', 'date_joined',)}),
    )
    add_fieldsets = (
        (_(u'새로운 유저 만들기'), {
            'classes': ('wide',),
            'fields': ('email', 'user_id', 'phone_number', 'sex',
                       'is_active', 'password1', 'password2')}
         ),
    )
    search_fields = ('email', 'name', 'user_id')
    ordering = ('-date_joined', 'id', 'email',)

    def lookup_allowed(self, lookup, value):
        # See #20078: we don't want to allow any lookups involving passwords.
        if lookup.startswith('password'):
            return False
        return super(UserAdmin, self).lookup_allowed(lookup, value)

    def get_urls(self):
        from django.conf.urls import patterns
        return patterns('',
                       (r'^(\d+)/password/$',
                        self.admin_site.admin_view(self.user_change_password))
                        ) + super(UserAdmin, self).get_urls()

    @method_decorator(sensitive_post_parameters())
    def user_change_password(self, request, id, form_url=''):
        if not self.has_change_permission(request):
            raise PermissionDenied
        user = get_object_or_404(self.queryset(request), pk=id)
        if request.method == 'POST':
            form = self.change_password_form(user, request.POST)
            if form.is_valid():
                form.save()
                msg = ugettext('Password changed successfully.')
                messages.success(request, msg)
                return HttpResponseRedirect('..')
        else:
            form = self.change_password_form(user)

        fieldsets = [(None, {'fields': list(form.base_fields)})]
        adminForm = admin.helpers.AdminForm(form, fieldsets, {})

        context = {
            'title': _('Change password: %s') % escape(user.get_username()),
            'adminForm': adminForm,
            'form_url': form_url,
            'form': form,
            'is_popup': '_popup' in request.REQUEST,
            'add': True,
            'change': False,
            'has_delete_permission': False,
            'has_change_permission': True,
            'has_absolute_url': False,
            'opts': self.model._meta,
            'original': user,
            'save_as': False,
            'show_save': True,
        }
        return TemplateResponse(request,
                                self.change_user_password_template or
                                'admin/auth/user/change_password.html',
                                context, current_app=self.admin_site.name)

# Now register the new UserAdmin...
admin_register(User, MyUserAdmin)
