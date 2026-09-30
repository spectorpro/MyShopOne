from django import forms
from django.core.exceptions import ValidationError
from PIL import Image, UnidentifiedImageError

from .models import Product

FORBIDDEN_WORDS = (
    'казино',
    'криптовалюта',
    'крипта',
    'биржа',
    'дешево',
    'бесплатно',
    'обман',
    'полиция',
    'радар',
)

ALLOWED_IMAGE_FORMATS = ('JPEG', 'PNG')
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5 МБ


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'image', 'category', 'price')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            if isinstance(widget, forms.CheckboxInput):
                widget.attrs.update({'class': 'form-check-input'})
            elif isinstance(widget, forms.ClearableFileInput):
                widget.attrs.update({'class': 'form-control-file'})
            else:
                widget.attrs.setdefault('class', 'form-control')
            widget.attrs.setdefault('placeholder', field.label or '')

    def _check_forbidden_words(self, value, label):
        if not value:
            return value
        normalized = value.lower().replace('ё', 'е')
        found = sorted({word for word in FORBIDDEN_WORDS if word in normalized})
        if found:
            raise ValidationError(
                f'В поле «{label}» нельзя использовать слова: {", ".join(found)}.'
            )
        return value

    def clean_name(self):
        return self._check_forbidden_words(self.cleaned_data.get('name'), 'Название')

    def clean_description(self):
        return self._check_forbidden_words(self.cleaned_data.get('description'), 'Описание')

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise ValidationError('Цена не может быть отрицательной. Укажите сумму от 0 и выше.')
        return price

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if not image:
            return image

        if image.size > MAX_IMAGE_SIZE:
            raise ValidationError(f'Файл весит {image.size / 1024 / 1024:.2f} МБ, а можно не больше 5 МБ.')

        try:
            image.seek(0)
            with Image.open(image) as img:
                fmt = img.format
        except UnidentifiedImageError:
            raise ValidationError('Файл повреждён или это не изображение.')

        if fmt not in ALLOWED_IMAGE_FORMATS:
            raise ValidationError(f'Поддерживаются только форматы JPEG и PNG, а у файла — {fmt or "неизвестный"}.')
        return image
