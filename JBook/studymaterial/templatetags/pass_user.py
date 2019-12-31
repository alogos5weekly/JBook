from django import template

register = template.Library()

@register.simple_tag
def pass_user(doc,user):
    return doc.is_liked(user)
