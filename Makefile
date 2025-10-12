install:
	poetry install 

project:
	poetry run project

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	python -m pip install C:\Users\KK\Documents\MIFI\project_1_Lebedinsky_M25-555\dist\project_1_lebedinsky_m25_555-0.1.0-py3-none-any.whl
	
lint:
	poetry run ruff check .