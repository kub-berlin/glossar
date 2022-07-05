import csv
import html
import locale
import datetime
from pathlib import Path

LABELS = {
	'de': 'Deutsch',
	'ar': 'Arabisch',
	'en': 'Englisch',
	'fr': 'Französisch',
	'ru': 'Russisch',
	'sq': 'Albanisch',
	'fa': 'Persisch',
	'tr': 'Türkisch',
	'ku': 'Kurdisch',
	'es': 'Spanisch',
	'ps': 'Paschto',
	'pt': 'Portugiesisch',
}
DIR = {
	'ar': 'rtl',
	'fa': 'rtl',
}


locale.setlocale(locale.LC_ALL, '')


def sort_key(item):
	lang = item[0]
	# sort by custom order
	order = ['de', 'en', 'fr', 'ar', 'fa', 'ru', 'es', 'tr', 'ku', 'sq', 'ps', 'pt']
	return order.index(lang)


def get_data(root):
	data = {}
	for path in root.iterdir():
		if path.suffix == '.csv':
			with path.open() as fh:
				rows = csv.reader(fh)
				data[path.stem] = dict(rows)

	# remove languages without any translations
	for lang, translation in list(data.items()):
		if not any(translation.values()):
			del data[lang]

	return data


def get_header(data):
	header = []
	for lang, _ in sorted(data.items(), key=sort_key):
		header.append((lang, LABELS[lang]))
	return header


def get_rows(data):
	for word in sorted(data['de'], key=locale.strxfrm):
		row = []
		for lang, translation in sorted(data.items(), key=sort_key):
			row.append((lang, translation[word]))
		# include only words with translations
		if any(data[lang][word] and lang != 'de' for lang in data):
			yield row


if __name__ == '__main__':
	root = Path('data')
	data = get_data(root)

	with open('template.html') as fh:
		template = fh.read()

	thead = ''
	for lang, label in get_header(data):
		_lang = html.escape(lang)
		_label = html.escape(label)
		thead += f'<th data-lang="{_lang}">{_label}</th>\n'

	tbody = ''
	for row in get_rows(data):
		tbody += '<tr>\n'
		for lang, label in row:
			_lang = html.escape(lang)
			_label = html.escape(label)
			_dir = html.escape(DIR.get(lang, 'ltr'))
			tbody += f'<td lang="{_lang}" dir="{_dir}">{_label}</td>\n'
		tbody += '</tr>\n'

	print(
		template
		.replace('{{{ thead }}}', thead)
		.replace('{{{ tbody }}}', tbody)
		.replace('{{{ date }}}', datetime.date.today().strftime('%d.%m.%Y'))
	)
