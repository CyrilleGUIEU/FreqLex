pyinstaller --onefile ^
    --add-data="DATA;." ^
    --add-data="bases_sql;." ^
    --icon=Data/icon.ico ^
	--name=FreqLex ^
    FreqLex.py
.\make.py