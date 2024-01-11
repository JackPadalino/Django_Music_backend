from django.db import models
from colorfield.fields import ColorField

# Create your models here.
class BaseStyle(models.Model):
    title = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        abstract = True

# all pages - page body
class MainStyle(BaseStyle):
    page_body_color = ColorField(format="hexa", default="#000000")

# nav model  
class NavStyle(BaseStyle):
    background_color = ColorField(format="hexa",default="#000000")
    height = models.IntegerField(default=10)
    link_font_family = models.CharField(max_length=100,default="Times New Roman")
    link_font_size = models.IntegerField(default=10)
    link_font_color = ColorField(format="hexa",default="#000000")
    logo_size = models.IntegerField(default=10)
    profile_cart_icon_size = models.IntegerField(default=10)
    is_sticky = models.BooleanField(default=False)

# model for home page footer
class FooterStyle(BaseStyle):
    background_color = ColorField(format="hexa",default="#000000")
    waveform_height = models.IntegerField(default=10)
    waveform_color = ColorField(format="hexa",default="#000000")
    footer_font_family = models.CharField(max_length=100,default="Times New Roman")
    footer_font_color = ColorField(format="hexa",default="#000000")
    footer_font_size = models.IntegerField(default=10)
    play_pause_button_color = ColorField(format="hexa",default="#000000")
    download_button_color = ColorField(format="hexa",default="#000000")

# model for catalog page artist form
class CatalogStyle(BaseStyle):
    regular_forms = models.BooleanField(default=False)
    popup_forms = models.BooleanField(default=False)