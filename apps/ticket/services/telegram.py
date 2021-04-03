import re
import requests

from django.template.loader import render_to_string
from django.conf import settings

proxies = {
    'http': f'{settings.PROXY_PROTOCOL}h://{settings.PROXY_HOST}:'
            f'{settings.PROXY_PORT}',
    'https': f'{settings.PROXY_PROTOCOL}h://{settings.PROXY_HOST}:'
             f'{settings.PROXY_PORT}'
}


class TelegramInterface:

    def __init__(self, ticket, reply):
        self.bot_token = settings.BOT_TOKEN
        self.channel_id = settings.CHANNEL_ID
        self.ticket = ticket
        self.reply = reply

    def send(self):

        html = self._get_html_message(
            context=self._create_context()
        )

        self._send_message_bot(
            channel_id=self.channel_id,
            message=html
        )

        return True

    def _create_context(self):
        context = {}
        if self.ticket:
            context = {
                'type': 'Ticket',
                'ticket_id': self.ticket.id,
                'author': self.ticket.author.username,
                'tag': self.ticket.tag.title,
                'title': self.ticket.title,
                'status': self.ticket.status,
                'url': f'https://aichallenge.ir/dashboard/admin/ticket/'
                       f'{self.ticket.id}',
                'ticket_created': self.ticket.created,
                'reply_id': '',
                'user': '',
                'reply_created': ''
            }

        if self.reply:
            context.update(
                {
                    'type': 'Reply',
                    'reply_id': self.reply.id,
                    'user': self.reply.user.username,
                    'reply_created': self.reply.created
                }
            )
        return context

    def _send_message_bot(self, channel_id, message):
        with requests.Session() as session:
            # session.proxies.update(proxies)
            response = session.get(
                f'{settings.TELEGRAM_HOST}/telegram/bot{self.bot_token}/'
                f'sendMessage',
                params={
                    'chat_id': int(f'-100{channel_id}'),
                    'text': message,
                    'parse_mode': 'MarkdownV2'
                },
                headers={
                    'Authorization': 'JhbGciOiJIUzsiYW5hbHl0aWNzX3NhdXJvbiJdLCJzY29wZSI6WyJyZWFkIiwiXJ2'}
            )
            print(response.text, response.status_code)

    def _get_html_message(self, context):
        html = render_to_string('ticket/telegram.html', context=context)
        html = '\n'.join(re.split('\n{2,}', html))

        return html
