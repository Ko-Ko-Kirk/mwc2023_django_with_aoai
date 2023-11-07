from django import forms


class StoryForm(forms.Form):
    ANIMAL_CHOICES = [
        ('熊熊', '熊熊'),
        ('兔兔', '兔兔'),
        ('貓貓', '貓貓'),
        ('狗狗', '狗狗'),
    ]

    SCENE_RADIO = [
        ('都市', '都市'),
        ('森林', '森林'),
        ('學校', '學校'),
        ('海邊', '海邊'),
    ]

    animals = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-control'}), choices=ANIMAL_CHOICES,
        label='選擇動物',
    )

    scene = forms.ChoiceField(
        widget=forms.RadioSelect(attrs={'class': 'form-control'}),
        choices=SCENE_RADIO,
        label='選擇場景',
    )
