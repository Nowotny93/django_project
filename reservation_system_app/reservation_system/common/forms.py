from django import forms

from reservation_system.common.models import MakeOrder


# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = ('text',)
from reservation_system.menu.models import Menu


# def get_my_choices():
#     choices_list = []
#     for obj in Menu.objects.all():
#         choices_list.append(obj.name)
#     return choices_list

class MakeOrderForm(forms.ModelForm):
    # def __init__(self, name, *args, **kwargs):
    #     super(MakeOrderForm, self).__init__(*args, **kwargs)
    #     self.fields["name"] = forms.ChoiceField(choices=name)

    # def __init__(self, *args, **kwargs):
    #     super(MakeOrderForm, self).__init__(*args, **kwargs)
    #     self.fields['name'].choices = forms.ChoiceField(choices=get_my_choices())

    class Meta:
        model = MakeOrder
        fields = ('product',)



