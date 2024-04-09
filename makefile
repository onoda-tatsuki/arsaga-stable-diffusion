TARGET_DIR ?= arsaga_stable_diffusion

lint: lint/.pyright lint/.flake8

format: format/.isort format/.black

lint/.pyright:
	poetry run pyright ${TARGET_DIR}

lint/.flake8:
	poetry run flake8 ${TARGET_DIR}

format/.black:
	poetry run black ${TARGET_DIR}

format/.isort:
	poetry run isort ${TARGET_DIR}