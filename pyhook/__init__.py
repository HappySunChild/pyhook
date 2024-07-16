# PyHook __init__.py

from __future__ import annotations

from dateutil.parser import parse
from requests import request, HTTPError

class Message:
	def __init__(self, message_data: dict) -> None:
		self.channel_id = message_data.get('channel_id', -1)
		self.id = message_data.get('id', -1)
		self.type = message_data.get('type', -1)
		
		self.content = message_data.get('content', '')
		self.embeds = message_data.get('embeds', [])
		
		self.post_timestamp = parse(message_data.get('timestamp', 0))
		
		self.raw = message_data
		
		#self.EditTimestamp = parse(message_data.get('edited_timestamp'))
	
	def get_http_object(self):
		data = {
			'content': self.content,
			'embeds': self.embeds
		}
		
		return data

class Embed:
	def __init__(self, title: str = None, desc: str = None, **kwargs) -> None:
		self.title = title
		self.description = desc
		self.color = kwargs.get('color')
		
		self.url = kwargs.get('url')
		self.footer = kwargs.get('footer')
		self.author = kwargs.get('author')
		
		self.fields = []
	
	def add_field(self, name: str, value: str, inline: bool = True):
		self.fields.append({'name': name, 'value': str(value), 'inline': inline})
	
	def set_title(self, title: str):
		self.title = title
	
	def add_image(self, url: str):
		self.image = {'url': url}
	
	def set_description(self, desc: str):
		self.description = desc
	
	def set_color(self, color: int):
		self.color = color
	
	def set_footer(self, text: str):
		self.footer = {'text': text}
	
	def set_author(self, name: str):
		self.author = {'name': name}
	
	def set_url(self, url: str):
		self.url = url
	
	def get_http_object(self):
		data = {
			'title': self.title,
			'description': self.description,
			'color': self.color,
			
			'url': self.url,
			
			'image': self.image,
			'fields': self.fields,
			'footer': self.footer,
			'author': self.author,
		}
		
		return data

class Webhook:
	'''
	Instance responsible for sending requests to discord.
	'''
	
	def __init__(self, id: int, token: str) -> None:
		self.id = id
		self.token = token
		
		self.name = None
		self.avatar_url = None
		
		self.last_message = None
	
	def delete(self, message: Message):
		if not isinstance(message, Message):
			return
		
		_request(f'{self.url}/messages/{message.id}', method='DELETE')
	
	def edit(self, message: Message = None, text: str = '', *embeds: Embed):
		'''
		Edits a given message.
		'''
		
		if not isinstance(message, Message):
			if not self.last_message or not message:
				return self.send(text, *embeds)
			else:
				message = self.last_message
		
		data = message.get_http_object()
		data['content'] = text or data['content']
		
		if len(embeds) > 0:
			data['embeds'] = embeds
		
		_request(f'{self.url}/messages/{message.id}', data, 'PATCH')
		
		return message
	
	def send(self, text: str = '', *embeds: Embed):
		'''
		Sends a message with the webhook.
		'''
		
		embedData = []
		
		for embed in embeds:
			embedData.append(embed.get_http_object() if isinstance(embed, Embed) else embed)
		
		data = self.get_http_object()
		data['content'] = text
		data['embeds'] = embedData
		
		self.last_message = _send_message(self.url, data)
		
		return self.last_message
	
	def get_http_object(self):
		data = {
			'username': self.name,
			'avatar_url': self.avatar_url,
			'content': ''
		}
		
		return data
	
	@property
	def url(self):
		return f'https://discord.com/api/webhooks/{self.id}/{self.token}'

def _request(url: str, json: dict = None, method: str = 'POST'):
	try:
		response = request(method, url, json=json, headers={'content-type': 'application/json'})
		response.raise_for_status()
		
		return response
	except HTTPError as e:
		print(e)
	
	return None

def _send_message(url: str, data: dict):
	response = _request(f'{url}?wait=true', data, 'POST')
	
	return Message(response.json())