#coding: utf-8
#!/usr/bin/python3

from xml.etree import ElementTree as etree
from mp3_tagger import MP3File, VERSION_2
from PIL.ExifTags import TAGS, GPSTAGS
from PyPDF2 import PdfFileReader
from datetime import datetime
from mutagen.mp3 import MP3
from PIL import Image
from huepy import *
import platform
import pefile
import time
import sys
import os

def metadata_extractor_CONFIG():
	file = ''

	while True:
		user = input(bold(red('\nAMATERASU ')) + '(' + bold(lightcyan('metadata_extractor')) + ')' + '> ')
		if user.startswith('set'):
			try:
				if user.split(' ')[1] == 'file' or user.split(' ')[1] == 'FILE':
					if user.split(' ')[2].startswith("'") or user.split(' ')[2].startswith('"'):
						file = user.split(' ')[2]
						print(bold(info('File set: ' + file)))
					else:
						print(bold(bad('Option not found.')))
				else:
					print(bold(bad('Error: option do not exist.')))
					print(bold(info('Select what to set.\n')))
					print(bold(info('file\tset file FILE')))
					print(bold(info('Amaterasu only supports .png, .jpg, .jpeg, .pdf, .mp3, .docx, .exe')))
			except IndexError:
				print(bold(info('Select what to set.\n')))
				print(bold(info('file\tset file FILE')))
				print(bold(info('Amaterasu only supports .png, .jpg, .jpeg, .pdf, .mp3, .docx, .exe')))
		elif user.startswith('show'):
			try:
				if user.split(' ')[1] == 'config':
					print()
					sConfig = {'File': file}
					print(bold('CONFIG\t\t\tDESCRIPTION'))
					print(bold('------\t\t\t-----------'))
					for a, b in sConfig.items():
						if len(a) > 15:
							print(bold(a + '\t' + b))
						elif len(a) <= 6:
							print(bold(a + '\t\t\t' + b))
						else:
							print(bold(a + '\t\t' + b))
				elif user.split(' ')[1] == 'options':
					print()
					sOptions = {'File': 'set file FILE'}
					print(bold('OPTIONS\t\t\tDESCRIPTION'))
					print(bold('------\t\t\t-----------'))
					for a, b in sOptions.items():
						if len(a) > 15:
							print(bold(a + '\t' + b))
						elif len(a) <= 6:
							print(bold(a + '\t\t\t' + b))
						else:
							print(bold(a + '\t\t' + b))
				else:
					print(bold(bad('Error: option do not exist.')))
			except IndexError:
				print(bold(info('Select what to show.\n')))
				print(bold(info('Config\t\tshow config')))
				print(bold(info('Options\t\tshow options')))
		elif user.startswith('run'):
			try:
				metadata_extractor(file)
			except Exception as e:
				print(bold(bad('Error: {}'.format(e))))
		elif user == '?' or user == 'help':
			sHelp = {'help | ?':'print this help message.',
			'show (config|options)':'show configuration or options',
			'set file': 'set file [FILE]',
			'run':'execute module'}
			print()
			print(bold('COMMAND\t\t\tDESCRIPTION'))
			print(bold('-------\t\t\t-----------'))
			for a, b in sHelp.items():
				if len(a) > 15:
					print(bold(a + '\t' + b))
				elif len(a) <= 6:
					print(bold(a + '\t\t\t' + b))
				else:
					print(bold(a + '\t\t' + b))

		elif user == 'back':
			break
		elif user == 'exit':
			print(bold(good('Thanks for using Amaterasu.')))
			sys.exit()
		else:
			print(bold(bad('Command not found.')))

def metadata_extractor(file):
	try:		
		if file.endswith('.jpg'):
			print()
			try:
				for (tag, value) in Image.open(file)._getexif().items():
					print('%s = %s' % (TAGS.get(tag), value))
			except Exception as e:
				print('Could not get any information.')

		if file.endswith('.jpeg'):
			print()
			try:
				for (tag, value) in Image.open(file)._getexif().items():
					print('%s = %s' % (TAGS.get(tag), value))
			except Exception as e:
				print('Could not get any information.')

		if file.endswith('.png'):
			print()
			try:
				for (tag, value) in Image.open(file)._getexif().items():
					print('%s = %s' % (TAGS.get(tag), value))
			except Exception as e:
				print('Could not get any information.')

		elif file.endswith('.pdf'):
			print()
			stat = os.stat(file)
			try:
				if 'Linux' in platform.system() or 'darwin' in platform.system():
					print(bold(green('Change time: ')) + stat.st_ctime)
				elif 'Windows' in platform.system():
					print(bold(green('Creation date: ')) + time.ctime(os.path.getctime(file)))
				else:
					print(bad('Cant extract creation date. Platform {} is unsupported.'.format(platform.system())))
				print(bold(green('Access time: ')) + time.ctime(os.path.getatime(file)))
				print(bold(green('Modified time: ')) + time.ctime(os.path.getmtime(file)))
				with open(file, 'rb') as f:
					pdf = PdfFileReader(f)
					info = pdf.getDocumentInfo()
					number = pdf.getNumPages()

					try:
						author = info.author
						print(bold(green('Author: ')) + str(author))
					except Exception:
						pass
					try:
						creator = info.creator
						print(bold(green('Creator: ')) + str(creator))
					except Exception:
						pass
					try:
						producer = info.producer
						print(bold(green('Producer: ')) + str(producer))
					except Exception:
						pass
					try:
						subject = info.subject
						print(bold(green('Subject: ')) + str(subject))
					except Exception:
						pass
					try:
						title = info.title
						print(bold(green('Title: ')) + str(title))
					except Exception:
						pass
					
					print(bold(green('Number of pages: ')) + str(number))
					print(bold(green('File size: ')) + str(stat.st_size))
					print(bold(green('File mode: ')) + str(stat.st_mode))
					print(bold(green('File inode: ')) + str(stat.st_ino))
					print(bold(green('Group ID: ')) + str(stat.st_gid))
					print(bold(green('Owner USER ID: ')) + str(stat.st_uid))
			except Exception as e:
				print(e)

		elif file.endswith('.mp3'):
			print()
			try:
				mp3 = MP3File(file)
				tags = mp3.get_tags()
				
				mp3.set_version(VERSION_2)

				title = mp3.song
				artist = mp3.artist
				alb = mp3.album
				trac = mp3.track
				genr = mp3.genre
				year = mp3.year
				band = mp3.band
				composer = mp3.composer
				copyright = mp3.copyright
				publisher = mp3.publisher
				url = mp3.url
				comment = mp3.comment

				audio = MP3(file)
				length = audio.info.length
				bitrate = audio.info.bitrate
				channels = audio.info.channels

				print(bold(green('Title: ')) + str(title))
				print(bold(green('Artist: ')) + str(artist))
				print(bold(green('Band: ')) + str(band))
				print(bold(green('Composer: ')) + str(composer))
				print(bold(green('Publisher: ')) + str(publisher))
				print(bold(green('URL: ')) + str(url))
				print(bold(green('Copyright: ')) + str(copyright))
				print(bold(green('Album: ')) + str(alb))
				print(bold(green('Track: ')) + str(trac))
				print(bold(green('Genre: ')) + str(genr))
				print(bold(green('Year: ')) + str(year))
				print(bold(green('Comment: ')) + str(comment))
				print(bold(green('Bitrate: ')) + str(bitrate))
				print(bold(green('Length: ')) + str(length))
				print(bold(green('Channels: ')) + str(channels))
			except Exception as e:
				print(e)

		elif file.endswith('.docx'):
			print()
			zipfile.is_zipfile(file)
			zfile = zipfile.ZipFile(file)

			#extract key elements for processing
			core_xml = etree.fromstring(zfile.read('docProps/core.xml'))
			app_xml = etree.fromstring(zfile.read('docProps/app.xml'))

			core_map = {
			'title' : 'Title',
			'subject' : 'Subject',
			'creator' : 'Author(s)',
			'keywords' : 'Keywords',
			'description' : 'Description',
			'lastModifiedBy' : 'Last Modified By',
			'modified' : 'Modified Date',
			'created' : 'Created Date', 
			'category' : 'Category',
			'contentStatus' : 'Status',
			'revision' : 'Revision'
			}

			for element in core_xml.getchildren():
				for key, title in core_map.items():
					if key in element.tag:
						if 'date' in title.lower():
							try:
								text = dt.strptime(element.text, '%Y-%m-%dT%H:%M:%SZ')
							except Exception as e:
								pass
						else:
							text = element.text
						print(bold(green('{}: '.format(title))) + '{}'.format(text))

			app_map = {
			'TotalTime' : 'Edit Time (minutes)',
			'Pages' : 'Page Count',
			'Words' : 'Word Count',
			'Characters' : 'Character Count',
			'Lines' : 'Line Count',
			'Paragraphs' : 'Paragraph Count',
			'Company' : 'Company',
			'HyperlinkBase' : 'Hyperlink Base',
			'Slides' : 'Slide count',
			'Notes' : 'Note count',
			'HiddenSlides' : 'Hidden Slide Count'
			}

			for element in app_xml.getchildren():
				for key, title in app_map.items():
					if 'date' in title.lower():
						try:
							text = dt.strptime(element.text, '%Y-%m-%dT%H:%M:%SZ')
						except Exception as e:
							pass
					else:
						text = element.text
					print(bold(green('{}: '.format(title))) + '{}'.format(text))

		elif file.endswith('.exe'):
			stat = os.stat(file)

			link = pefile.PE(file)
			stat = os.stat(file)
			#print(print_info(encoding='utf-8'))
			imp = link.get_imphash()
			errors = link.get_warnings()
			relocs = link.has_relocs()
			checksum = link.verify_checksum()
			strings = link.get_resources_strings()
			print()
			print(bold(green('Hash of Import Address Table (IAT): ')) + imp)
			print(bold(green('Errors: ')) + str(errors))
			print(bold(green('Has relocation directory: ')) + str(relocs))
			print(bold(green('Checksum: ')) + str(checksum))
			print(bold(green('File size: ')) + str(stat.st_size))
			print()
			print(bold(red('Strings')))
			for string in strings:
				print(bold(green('String: ')) + string)
			print()
			print(bold(red('Directory Entry Import')))
			for entry in link.DIRECTORY_ENTRY_IMPORT:
				print('\t' + entry.dll.decode('utf-8'))

	except KeyboardInterrupt:
		print()
		#print('Soon.')
		#file = input(que('Enter file: '))
