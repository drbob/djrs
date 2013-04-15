
##
# Simple Solution for Django + Bootstrap Forms.
# Taken from: http://duganchen.ca/rendering-django-forms-for-the-twitter-bootstrap/
# 

from django import forms

from django.forms import CharField, Form
from django.forms.forms import BoundField
from django.forms.util import ErrorList
from django.template import Context, Template
 
from functools import partial
 
class BootstrapForm(Form):
    template = \
u'''
{%for field in form%}
<div class="control-group {%if field.errors%}error{%endif%}">
{{field.label_tag}}
<div class="controls">
{{field}}<span class="help-inline">{{field.errors}}</span>
</div>
</div>
{% endfor %}
'''
 
    def __unicode__(self):
        c = Context({'form': self})
        t = Template(self.template)
        return t.render(c)
 
 
def decorate_label_tag(f):
 
    def bootstrap_label_tag(self, contents=None, attrs=None):
        attrs = attrs or {}
        add_class(attrs, 'control-label')
        return f(self, contents, attrs)
 
    return bootstrap_label_tag
 
 
BoundField.label_tag = decorate_label_tag(
         BoundField.label_tag)
 
 
def add_class(attrs, html_class):
    assert type(attrs) is dict
 
    if 'class' in attrs:
        classes = attrs['class'].split()
        if not html_class in classes:
            classes.append(html_class)
            attrs['class'] = ' '.join(classes)
    else:
        attrs['class'] = html_class
 
 
class BootstrapErrorList(ErrorList):
 
    def __unicode__(self):
        if not self:
            return u''
        return u' '.join(unicode(e) for e in self)
 
 
####### Real Forms are here #########

class LoginForm(BootstrapForm):
    user = forms.CharField(max_length=20, initial='user')
    password = forms.CharField(max_length=20, widget=forms.PasswordInput)
    host = forms.IPAddressField(initial='127.0.0.1')  # could be ipv4 for the moment.
    port = forms.IntegerField(min_value=1001, max_value=65535, initial=7022)

LoginForm=partial(LoginForm, error_class=BootstrapErrorList)

class SearchForm(BootstrapForm):
    terms = forms.CharField(max_length=256, initial='terms')
#    file_type = forms.CharField(max_length=20, initial='media')
#    max_results = forms.IntegerField(min_value=10, max_value=10000, initial=500)
#    min_filesize = forms.IntegerField(min_value=0, max_value=10000, initial=0)
#    max_filesize = forms.IntegerField(min_value=1, max_value=10000, initial=10000)

SearchForm=partial(SearchForm, error_class=BootstrapErrorList)


# Keep Chat boring for inline stuff.
class ChatForm(forms.Form):
    message = forms.CharField(max_length=1000)

ChatForm=partial(ChatForm, error_class=BootstrapErrorList)

