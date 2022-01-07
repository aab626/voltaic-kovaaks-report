import os
import datetime
import statistics

from vkr_modules.exceptions import NoStatFoundException, LastNError

import numpy as np
import matplotlib.dates
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline

class Scenario:
	csv_files = None

	style_tracking = {'dots': '#E0FFFF', 'continuous': '#00FFFF', 'average': '#87CEFA'}
	style_clicking = {'dots': '#FBCEB1', 'continuous': '#E62020', 'average': '#A52A2A'}
	style_switching = {'dots': '#dcbaff', 'continuous': '#7f00ff', 'average': '#a055ed'}

	def __init__(self, scenario_name, stats_folder):
		self.scenario_name = scenario_name
		self.stats_folder = stats_folder

		if Scenario.csv_files is None:
			Scenario.csv_files = [f for f in os.listdir(self.stats_folder) if os.path.splitext(f)[1].lower() == '.csv']

	def process(self):
		scenario_files = self.get_files()
		scenario_data_list = [self.parse_file(sf) for sf in scenario_files]
		scenario_data_list = self.join_sessions(scenario_data_list)

		last20_data = scenario_data_list[len(scenario_data_list)-20: len(scenario_data_list)]

		total_trends = self.calculate_trends(scenario_data_list)
		last20_trends = self.calculate_trends(scenario_data_list, 20)

		data = {'all': scenario_data_list,
				'last20': last20_data,
				'total_trends': total_trends,
				'last20_trends': last20_trends}

		return data

	def get_files(self):
		scenario_files = [f for f in Scenario.csv_files if f.split(' - ')[0] == self.scenario_name]

		if len(scenario_files) == 0:
			raise NoStatFoundException(f'No files found for scenario: {self.scenario_name}.')

		return scenario_files

	def parse_file(self, scenario_file):
		date_str = os.path.splitext(scenario_file)[0].split(' - ')[2].strip(' Stats')
		date = datetime.datetime.strptime(date_str, '%Y.%m.%d-%H.%M.%S')

		with open(os.path.join(self.stats_folder, scenario_file), 'r') as fp:
			block = 1
			for line in fp:
				if line == '\n':
					block += 1
				else:
					if block == 1:
						pass

					elif block == 2:
						if 'Weapon,Shots,Hits,Damage Done,Damage Possible' in line:
							pass
						else:
							split = line.strip('n').split(',')

							weapon = split[0]
							shots = int(split[1])
							hits = int(split[2])
							accuracy = hits/shots if shots > 0 else 1
							dmg_done = float(split[3])
							dmg_possible = float(split[4])

					elif block == 3:
						if 'Kills:,' in line:
							kills = int(line.strip('\n').split(',')[1])
						elif 'Avg TTK:,' in line:
							avg_ttk = float(line.strip('\n').split(',')[1])
						elif 'Score:,' in line:
							score = float(line.strip('\n').split(',')[1])

					elif block == 4:
						pass
		
		scenario_data = {
							'date': date,
							'shots': shots,
							'hits': hits,
							'accuracy': accuracy,
							'dmg_done': dmg_done,
							'dmg_possible': dmg_possible,
							'kills': kills,
							'avg_ttk': avg_ttk,
							'score': score
		}

		return scenario_data

	def join_sessions(self, scenario_data_list, time_threshold=datetime.timedelta(hours=2)):
		scenario_data_cleaned = []

		while len(scenario_data_list) > 0:
			data0 = scenario_data_list.pop(0)

			to_be_joined = [data0]
			i = 0
			while i < len(scenario_data_list):
				if abs(scenario_data_list[i]['date'] - data0['date']) <= time_threshold:
					to_be_joined.append(scenario_data_list[i])
					scenario_data_list.pop(i)
				else:
					i += 1

			session_average = self.calculate_trends(to_be_joined, None)['average']
			session_average['date'] = datetime.datetime.fromtimestamp(statistics.mean([sd['date'].timestamp() for sd in to_be_joined]))

			scenario_data_cleaned.append(session_average)

		return scenario_data_cleaned

	def calculate_trends(self, scenario_data_list, last_n=None):
		n = len(scenario_data_list)

		if last_n is None:
			last_n = n
		else:
			if last_n <= 0:
				raise LastNError(f'last_n should be set to a positive integer || Current value: {last_n}')

			last_n = min(n, last_n)
			scenario_data_list = scenario_data_list[n-last_n: n]

		averages = dict()
		stdevs = dict()

		if len(scenario_data_list) == 1:
			averages = scenario_data_list[0].copy()
			stdevs = {key: 0 for key in scenario_data_list[0]}
			
			del averages['date']
			del stdevs['date']

		else:
			for key in scenario_data_list[0]:
				if key == 'date':
					continue

				key_list = [scenario_data[key] for scenario_data in scenario_data_list]
				averages[key] = statistics.mean(key_list)
				stdevs[key] = statistics.stdev(key_list)

		return {'average': averages, "stdev": stdevs}

	def generate_graph(self, scenario_data_list, average_threshold, color_style, save_path):
		# raw data
		dates = [sd['date'] for sd in scenario_data_list]
		dates_n = matplotlib.dates.date2num(dates)
		scores = [sd['score'] for sd in scenario_data_list]

		# calculate last k averages for each score
		scores_average = []
		for i in range(len(scores)):
			i_min = max(0, i - average_threshold)
			i_max = i + 1
			i_neighbours = scores[i_min: i_max]
			scores_average.append(statistics.mean(i_neighbours))

		# spline interpolation
		if len(dates) >= 3:
			dates_continuous = np.linspace(dates_n.min(), dates_n.max(), 500)

			spl_scores = make_interp_spline(dates_n, scores, k=2)
			scores_continuous = spl_scores(dates_continuous)

			spl_averages = make_interp_spline(dates_n, scores_average, k=2)
			averages_continuous = spl_averages(dates_continuous)

		# prepare figure
		fig, ax = plt.subplots(figsize=(10, 2))

		# set colors and graph style
		fig.set_facecolor('#7F00FF')
		ax.set_facecolor('#7F00FF')

		ax.spines['bottom'].set_color('white')
		ax.spines['top'].set_color('white')
		ax.tick_params(colors='white')

		ax.spines['left'].set_visible(False)
		ax.spines['right'].set_visible(False)

		# y/x ticks
		yticks = [(max(scores)-min(scores))/4*i + min(scores) for i in range(0, 4+1)]
		plt.yticks(yticks)

		xtick0 = min(dates_n)
		xtick1 = 0.5*(max(dates_n) - min(dates_n)) + xtick0
		xtick2 = 0.5*(max(dates_n) - xtick1) + xtick1
		xtick3 = 0.5*(max(dates_n) - xtick2) + xtick2
		xtick4 = max(dates_n)
		xticks = [xtick0, xtick1, xtick2, xtick3, xtick4]

		xtickdates = [matplotlib.dates.num2date(d) for d in xticks]
		xticklabels = [(d.replace(tzinfo=None)-datetime.datetime.now()).days for d in matplotlib.dates.num2date(xticks)]
		plt.xticks(xticks, rotation=0, fontsize=8, labels=xticklabels)

		for y in yticks[1:4]:
			plt.axhline(y=y, color='gray', linestyle='-', alpha=0.2, linewidth=1)

		for x in xticks[1:4]:
			plt.axvline(x=x, color='gray', linestyle='--', alpha=0.2, linewidth=1)
	
		# plotting
		if len(dates) >= 3:
			plt.plot(dates_continuous, averages_continuous, '--', color=color_style['average'], alpha=0.5)
			plt.plot(dates_continuous, scores_continuous, '-', color=color_style['continuous'], linewidth=1.75)
			plt.plot(dates, scores, 'o', markersize=5, color=color_style['dots'])
		else:
			plt.plot(dates, scores, '-', color=color_style['continuous'])
			plt.plot(dates, scores, 'o', markersize=5, color=color_style['dots'])

		plt.tight_layout()
		plt.savefig(save_path, transparent=True)
