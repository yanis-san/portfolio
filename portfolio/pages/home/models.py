from django.db import models
from wagtail.models import Page, Orderable
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.admin.panels import InlinePanel
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel


class HomePage(Page):
    template = "pages/home/home.html"
    job_title = models.CharField(
        verbose_name="Job or profession", max_length=255, blank=False, null=False)
    header_image = models.ForeignKey("wagtailimages.Image", verbose_name="Header image",
                                     on_delete=models.SET_NULL, related_name="+", null=True, blank=True)
    text_about = RichTextField(
        verbose_name="About me", blank=False, null=False)

    content_panels = Page.content_panels + [
        FieldPanel("job_title"),
        FieldPanel("header_image"),
        FieldPanel("text_about"),
        InlinePanel("detail_containers", label="Detail Containers"),

    ]


class About(Orderable):
    about_container = ParentalKey('AboutContainer', on_delete=models.CASCADE, related_name='about')
    line = models.CharField(max_length=255, blank=False, null=False)

    panel = [
        FieldPanel('line')
    ]


class AboutContainer(ClusterableModel, Orderable):
    page = ParentalKey(HomePage, on_delete=models.CASCADE,related_name='about_containers')
    title = models.CharField(max_length=255)

    panels = [
        FieldPanel('title'),
        InlinePanel('about', label="About")
        
        ]



class Skill(Orderable):
    detail_container = ParentalKey(
        'DetailContainer', on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=255, blank=False, null=False)
    level = models.CharField(max_length=255, blank=False, null=False)
    icon = models.ForeignKey("wagtailimages.Image", verbose_name="Skill image",
                             on_delete=models.SET_NULL, related_name="+", null=True, blank=True)

    panels = [
        FieldPanel("name"),
        FieldPanel("level"),
        FieldPanel("icon")
    ]


class DetailContainer(ClusterableModel, Orderable):
    page = ParentalKey(HomePage, on_delete=models.CASCADE,
                       related_name='detail_containers')
    title = models.CharField(max_length=255)

    panels = [
        FieldPanel('title'),
        InlinePanel('skills', label="Skills"),
    ]
