from django.utils.translation import ugettext_lazy as _

from wagtail.contrib.table_block.blocks import TableBlock
from wagtail import blocks
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock


class HeadingBlock(blocks.StructBlock):
    text = blocks.CharBlock(classname='title')
    size = blocks.ChoiceBlock(choices=[
        ('h2', 'H2'),
        ('h3', 'H3'),
        ('h4', 'H4'),
    ], default='h2')

    class Meta:
        icon = 'title'
        template = 'core/blocks/heading_block.html'


class ImageWithCaptionBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    alt_text = blocks.CharBlock(required=False, help_text=_('Describe the image for screen readers'))
    caption = blocks.CharBlock(required=False)

    class Meta:
        icon = 'image'
        template = 'core/blocks/image_block.html'


class QuoteBlock(blocks.StructBlock):
    text = blocks.TextBlock()
    attribution = blocks.CharBlock(required=False)

    class Meta:
        icon = 'openquote'
        template = 'core/blocks/quote_block.html'


class CallToActionBlock(blocks.StructBlock):
    heading = blocks.CharBlock()
    text = blocks.TextBlock(required=False)
    page = blocks.PageChooserBlock()
    button_label = blocks.CharBlock(default='Find out more')

    class Meta:
        icon = 'pick'
        template = 'core/blocks/call_to_action_block.html'


class DocumentLinkBlock(blocks.StructBlock):
    document = DocumentChooserBlock()
    label = blocks.CharBlock(required=False, help_text=_('Defaults to the document title'))

    class Meta:
        icon = 'doc-full'
        template = 'core/blocks/document_block.html'


class BaseStreamBlock(blocks.StreamBlock):
    heading = HeadingBlock()
    paragraph = blocks.RichTextBlock(icon='pilcrow')
    image = ImageWithCaptionBlock()
    quote = QuoteBlock()
    call_to_action = CallToActionBlock()
    embed = EmbedBlock(help_text=_('Paste a YouTube or Vimeo URL'))
    document = DocumentLinkBlock()
    table = TableBlock()
