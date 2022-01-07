import os
import datetime
import json
import decimal

import yattag

from vkr_modules.scenario import Scenario
from vkr_modules.exceptions import NoStatFoundException

class Playlist:
	tracking = 'tracking'
	clicking = 'clicking'
	switching = 'switching'

	color_style = {
					tracking: Scenario.style_tracking, 
					clicking: Scenario.style_clicking,
					switching: Scenario.style_switching
					}

	# folders
	path_files = None
	path_imgs = None
	path_pages = None
	path_resources = None

	# files
	path_css = None

	path_index = None
	path_iron = None
	path_bronze = None
	path_silver = None
	path_gold = None
	path_platinum = None
	path_diamond = None
	path_jade = None
	path_master = None
	path_grandmaster = None

	path_playlists_json = None

	# playlists
	playlist_json = None

	# ranks
	rank_iron = 'iron'
	rank_bronze = 'bronze'
	rank_silver = 'silver'
	rank_gold = 'gold'
	rank_platinum = 'platinum'
	rank_diamond = 'diamond'
	rank_jade = 'jade'
	rank_master = 'master'
	rank_grandmaster = 'grandmaster'

	def __init__(self, stats_folder, root_folder):
		self.stats_folder = stats_folder
		self.root_folder = root_folder

		if Playlist.path_files is None:
			Playlist.path_files = os.path.join(self.root_folder, 'report_files')
			Playlist.path_imgs = os.path.join(Playlist.path_files, 'imgs')
			Playlist.path_pages = os.path.join(Playlist.path_files, 'pages')
			Playlist.path_resources = os.path.join(self.root_folder, 'resources')

			Playlist.path_index = os.path.join(self.root_folder, 'report.html')
			Playlist.path_iron = os.path.join(Playlist.path_pages, 'report_iron.html')
			Playlist.path_bronze = os.path.join(Playlist.path_pages, 'report_bronze.html')
			Playlist.path_silver = os.path.join(Playlist.path_pages, 'report_silver.html')
			Playlist.path_gold = os.path.join(Playlist.path_pages, 'report_gold.html')
			Playlist.path_platinum = os.path.join(Playlist.path_pages, 'report_platinum.html')
			Playlist.path_diamond = os.path.join(Playlist.path_pages, 'report_diamond.html')
			Playlist.path_jade = os.path.join(Playlist.path_pages, 'report_jade.html')
			Playlist.path_master = os.path.join(Playlist.path_pages, 'report_master.html')
			Playlist.path_grandmaster = os.path.join(Playlist.path_pages, 'report_grandmaster.html')

			Playlist.path_css = os.path.join(Playlist.path_resources, 'voltaic_style.css')
			Playlist.path_playlists_json = os.path.join(Playlist.path_resources, "playlists.json")

	def generate_scenarios(self, scenarios_template):
		scenarios = {Playlist.tracking: dict(), Playlist.clicking: dict(), Playlist.switching: dict()}

		for scenario_type in scenarios_template:
			for scenario_name in scenarios_template[scenario_type]:
				scenario = Scenario(scenario_name, self.stats_folder)
				scenarios[scenario_type][scenario_name] = scenario

		return scenarios

	def generate_scenario_data(self, scenarios):
		scenarios_data = {Playlist.tracking: dict(), Playlist.clicking: dict(), Playlist.switching: dict()}
		
		for scenario_type in scenarios:
			for scenario_name in scenarios[scenario_type]:
				scenario = scenarios[scenario_type][scenario_name]

				try:
					scenario_data = scenario.process()
					scenarios_data[scenario_type][scenario_name] = scenario_data
				except NoStatFoundException:
					scenarios_data[scenario_type][scenario_name] = None

		return scenarios_data

	def generate_graphs(self, scenarios, scenario_data):
		for scenario_type in scenario_data:
			for scenario_name in scenario_data[scenario_type]:
				sc_data = scenario_data[scenario_type][scenario_name]

				if sc_data is not None:
					scenario = scenarios[scenario_type][scenario_name]
					graph_path = os.path.join(Playlist.path_imgs, f'{scenario_name}.png')
					scenario.generate_graph(sc_data['all'], 20, Playlist.color_style[scenario_type], graph_path)

	def generate_reports(self):
		reports_to_make = [
							'index', 
							Playlist.rank_iron, 
							Playlist.rank_bronze, 
							Playlist.rank_silver, 
							Playlist.rank_gold, 
							Playlist.rank_platinum, 
							Playlist.rank_diamond, 
							Playlist.rank_jade, 
							Playlist.rank_master, 
							Playlist.rank_grandmaster
							]

		for report in reports_to_make:
			doc, tag, text = yattag.Doc().tagtext()

			doc.asis('<!DOCTYPE html>')

			with tag('html'):
				with tag('head'):
					# doc.stag('link', rel='stylesheet', href=Playlist.path_css)
					doc.stag('link', rel='stylesheet', href='https://fonts.googleapis.com/css?family=PT+Sans')

					with tag('title'):
						text('Voltaic Fundamentals Report')

					with tag('style'):
						with open(Playlist.path_css, 'r') as fp:
							text(fp.read())

				with tag('body'):
					with tag('div', klass='header'):
						with tag('h1'):
							text('Voltaic Fundamentals Report')
						with tag('p'):
							date_str = datetime.datetime.now().strftime('%Y-%M-%d')
							text(f'Made for Fundamental KvKs Routines 2.0 | Last update: {date_str}')

					with tag('div', klass='navbar'):
						with tag('a', klass=Playlist.rank_iron, href=Playlist.path_iron):
							text('Iron')
						with tag('a', klass=Playlist.rank_bronze, href=Playlist.path_bronze):
							text('Bronze')
						with tag('a', klass=Playlist.rank_silver, href=Playlist.path_silver):
							text('Silver')
						with tag('a', klass=Playlist.rank_gold, href=Playlist.path_gold):
							text('Gold')
						with tag('a', klass=Playlist.rank_platinum, href=Playlist.path_platinum):
							text('Platinum')
						with tag('a', klass=Playlist.rank_diamond, href=Playlist.path_diamond):
							text('Diamond')
						with tag('a', klass=Playlist.rank_jade, href=Playlist.path_jade):
							text('Jade')
						with tag('a', klass=Playlist.rank_master, href=Playlist.path_master):
							text('Master')
						with tag('a', klass=Playlist.rank_grandmaster, href=Playlist.path_grandmaster):
							text('Grandmaster')

					with tag('div', klass='main'):
						doc.stag('hr', klass='horizontal_separator')

					if report == 'index':
						with tag('div', klass='index_report'):
							with tag('h2'):
								text('How to read the report')
							text('Each dot represents the average of a training session (taking into account the closest 2 hours since the start of the training), the continuous line its just a visual feedback to connect these dots.')
							doc.stag('br')
							text('The dashed line represents the average of the last 20 training sessions for each scenario.')
							doc.stag('br')
							text('The numbers on the X axis represents how many days ago that session was played.')
							doc.stag('br')
							doc.stag('br')
							text('Click on a rank button to get started.')

				if report == 'index':
					with open(Playlist.path_index, 'w') as fp:
						fp.write(doc.getvalue())

					continue

				scenarios_template = self.get_rank_template(report)
				scenarios = self.generate_scenarios(scenarios_template)
				scenarios_data = self.generate_scenario_data(scenarios)
				self.generate_graphs(scenarios, scenarios_data)

				for sc_type in [Playlist.tracking, Playlist.clicking, Playlist.switching]:
					with tag('div', klass=f'scenario_type {sc_type}'):
						with tag('h2'):
							text(sc_type.capitalize())

						for sc_name in scenarios_data[sc_type]:
							sc_data = scenarios_data[sc_type][sc_name]

							with tag('div', klass='scenario'):
								with tag('div', klass='name'):
									with tag('h3'):
										text(sc_name)

								with tag('div', klass='contents'):
									if sc_data is None:
										text('Data not found.')
									else:
										with tag('div', klass='graph'):
											# doc.stag('img', src=os.path.join(imgs, f'{sc_name}.png'))
											doc.stag('img', src=f'../imgs/{sc_name}.png')

										doc.stag('hr', klass='vertical_separator')

										with tag('div', klass='data'):
											with tag('div', klass='alltime'):
												with tag('h4'):
													text('All-time')

												with tag('table', klass='data_table'):
													with tag('tr'):
														with tag('th'):
															text('Max')
														with tag('td'):
															n = round(max([run['score'] for run in sc_data['all']]), 2)
															n = int(n) if (10*n)%10==0 else n
															text(n)
													with tag('tr'):
														with tag('th'):
															text('Min')
														with tag('td'):
															n = round(min([run['score'] for run in sc_data['all']]), 2)
															n = int(n) if (10*n)%10==0 else n
															text(n)
													with tag('tr'):
														with tag('th'):
															text('Average')
														with tag('td'):
															n = round(sc_data['total_trends']['average']['score'], 2)
															n = int(n) if (10*n)%10==0 else n
															text(n)
													with tag('tr'):
														with tag('th'):
															text('StDev')
														with tag('td'):
															n = round(sc_data['total_trends']['stdev']['score'], 2)
															n = int(n) if (10*n)%10==0 else n
															text(n)

											with tag('div', klass='last20'):
												with tag('h4'):
													text('Last 20')

												with tag('table', klass='data_table'):
													with tag('tr'):
														with tag('th'):
															text('Max')
														with tag('td'):
															n = round(max([run['score'] for run in sc_data['last20']]), 2)
															n = int(n) if (10*n)%10==0 else n
															text(n)
													with tag('tr'):
														with tag('th'):
															text('Min')
														with tag('td'):
															n = round(min([run['score'] for run in sc_data['last20']]), 2)
															n = int(n) if (10*n)%10==0 else n
															text(n)
													with tag('tr'):
														with tag('th'):
															text('Average')
														with tag('td'):
															n = round(sc_data['last20_trends']['average']['score'], 2)
															n = int(n) if (10*n)%10==0 else n
															text(n)
													with tag('tr'):
														with tag('th'):
															text('StDev')
														with tag('td'):
															n = round(sc_data['last20_trends']['stdev']['score'], 2)
															n = int(n) if (10*n)%10==0 else n
															text(n)

					doc.stag('hr', klass='horizontal_separator')

			if report == Playlist.rank_iron:
				save_path = Playlist.path_iron
			elif report == Playlist.rank_bronze:
				save_path = Playlist.path_bronze
			elif report == Playlist.rank_silver:
				save_path = Playlist.path_silver
			elif report == Playlist.rank_gold:
				save_path = Playlist.path_gold
			elif report == Playlist.rank_platinum:
				save_path = Playlist.path_platinum
			elif report == Playlist.rank_diamond:
				save_path = Playlist.path_diamond
			elif report == Playlist.rank_jade:
				save_path = Playlist.path_jade
			elif report == Playlist.rank_master:
				save_path = Playlist.path_master
			elif report == Playlist.rank_grandmaster:
				save_path = Playlist.path_grandmaster

			with open(save_path, 'w') as fp:
				fp.write(doc.getvalue())

	def generate_folders(self):
		for path_ in [Playlist.path_files, Playlist.path_imgs, Playlist.path_pages]:
			if not os.path.isdir(path_):
				os.mkdir(path_)

	def get_rank_template(self, rank):
		if Playlist.playlist_json is None:
			with open(Playlist.path_playlists_json, 'r') as fp:
				Playlist.playlist_json = json.load(fp)

		return Playlist.playlist_json[rank]
