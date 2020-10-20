from django.forms import ModelForm


class BloggerForm(ModelForm):
    class Meta:
        fields = ('image', 'blog_name', 'email', 'phone')
