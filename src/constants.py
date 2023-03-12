from pathlib import Path

DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
MAIN_DOC_URL = 'https://docs.python.org/3/'
PEP_URL = 'https://peps.python.org/'
BASE_DIR = Path(__file__).parent

DT_FORMAT = '%d.%m.%Y %H:%M:%S'
LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'

ARGS_LOG_INFO = 'Аргументы командной строки: {args}'
DOWNLOAD_LOG_INFO = 'Архив был загружен и сохранён: {archive_path}'
START_LOG_INFO = 'Парсер запущен!'
FINISH_LOG_INFO = 'Работа парсера завершена'
FILE_OUTPUT_LOG_INFO = 'Файл с результатами был сохранён: {file_path}'
GET_RESPONSE_LOG_ERROR = 'Возникла ошибка при загрузке страницы {url}'
TAG_NOT_FOUND_LOG_ERROR = 'Не найден тег {tag} {attrs}'

EXPECTED_STATUS = {
    'A': ('Active', 'Accepted'),
    'D': ('Deferred',),
    'F': ('Final',),
    'P': ('Provisional',),
    'R': ('Rejected',),
    'S': ('Superseded',),
    'W': ('Withdrawn',),
    '': ('Draft', 'Active'),
}
