from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Tag, Scope


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        forms = {'count_mains': 0}
        for form_num, form in enumerate(self.forms):
            data = form.cleaned_data
            if not data or not data.get('tag'):
                continue

            print(data)

            if not forms.get(data['tag']):
                forms[data['tag']] = data
            else:
                raise ValidationError('Уберите дубликаты')

            if data['is_main']:
                forms['count_mains'] += 1

        print(forms)

        if len(forms) < 2:
            raise ValidationError('Выберите хотя бы один тэг')

        if forms['count_mains'] < 1 or forms['count_mains'] > 1:
            raise ValidationError('Должен быть один и только один главный'
                                  ' тэг')

        return super().clean()


class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass
