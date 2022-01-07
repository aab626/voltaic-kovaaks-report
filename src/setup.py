import sys
from cx_Freeze import setup, Executable

if sys.platform == 'win32':
	base = 'Win32GUI'

build_exe_options = {
						'include_files': ['resources'],
						'packages': 	[
											'os',
											'datetime',
											'json',
											'tkinter',
											'statistics',
											'PIL',
											'yattag',
											'numpy',
											'matplotlib',
											'scipy',
											'vkr_modules'
										]
					}

executables = [Executable(
							script='main.py',
							base=base,
							icon='resources/vkr_icon.ico',
							target_name='VoltaicKovaaKsReport'
							)
]

setup(
		name= 'Voltaic KovaaK\'s Report',
		version = '1.0',
		description = 'Report viewer for Voltaic\'s Fundamental Aim Training with KovaaK\'s',
		options = {'build_exe': build_exe_options},
		executables = executables
		)
