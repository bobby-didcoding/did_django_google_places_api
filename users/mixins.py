from django.conf import settings
from django.shortcuts import render, redirect, reverse
from users.models import UserToken
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail, EmailMessage, get_connection
from urllib.parse import urlencode
import six




'''
Handles form error that are passed back to AJAX calls
'''
def FormErrors(*args):
	message = ""
	for f in args:
		if f.errors:
			message = f.errors.as_text()
	return message




'''
Used to append url parameters when redirecting users
'''
def RedirectParams(**kwargs):
	url = kwargs.get("url")
	params = kwargs.get("params")
	response = redirect(url)
	if params:
		query_string = urlencode(params)
		response['Location'] += '?' + query_string
	return response




'''
Creates a token that is used for email and password verification emails
'''
# DOCS - https://docs.djangoproject.com/en/3.1/topics/auth/default/
class TokenGenerator(PasswordResetTokenGenerator):
	
	def _make_hash_value(self, user, timestamp):
		
		return (
			six.text_type(user.pk) + 
			six.text_type(timestamp) + 	
			six.text_type(user.is_active)
			)




'''
Used to send emails from a Gmail account with an app password (see README.md file)
'''
# DOCS - https://docs.djangoproject.com/en/3.1/topics/email/
class CreateEmail:

	def __init__(self, request, *args, **kwargs):

		self.email_account = kwargs.get("email_account")
		self.subject = kwargs.get("subject", "")
		self.email = kwargs.get("email")
		self.template = kwargs.get("template")
		self.context = kwargs.get("context")
		self.cc_email = kwargs.get("cc_email")
		self.token = kwargs.get("token")
		self.url_safe = kwargs.get("url_safe")

		domain = settings.CURRENT_SITE

		context = {
			"user": request.user,
			"domain": domain,
		}

		if self.token:
			context["token"] = self.token
		
		if self.url_safe:
			context["url_safe"] = self.url_safe

		email_accounts = {
			"donotreply": {
				'name': settings.EMAIL_HOST_USER,
				'password':settings.DONOT_REPLY_EMAIL_PASSWORD,
				'from':settings.EMAIL_HOST_USER,
				'display_name': settings.DISPLAY_NAME},
		}


		html_content = render_to_string(self.template, context ) # render with dynamic value
		text_content = strip_tags(html_content) # Strip the html tag. So people can see the pure text at least.

		with get_connection(
			    host= settings.EMAIL_HOST, 
			    port= settings.EMAIL_PORT, 
			    username=email_accounts[self.email_account]["name"], 
			    password=email_accounts[self.email_account]["password"], 
			    use_tls=settings.EMAIL_USE_TLS,
			) as connection:
				msg = EmailMultiAlternatives(
					self.subject,
				 	text_content,
				 	f'{email_accounts[self.email_account]["display_name"]} <{email_accounts[self.email_account]["from"]}>',
				 	[self.email],
				 	cc=[self.cc_email],
				 	connection=connection)
				msg.attach_alternative(html_content, "text/html")
				msg.send()