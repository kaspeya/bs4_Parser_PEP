from pathlib import Path

DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'

MAIN_DOC_URL = 'https://docs.python.org/3/'
PEP_URL = 'https://peps.python.org/'
BASE_DIR = Path(__file__).parent

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


DOWNLOAD_LOG_INFO = 'Архив был загружен и сохранён: {archive_path}'
START_LOG_INFO = 'Парсер запущен!'
FINISH_LOG_INFO = 'Работа парсера завершена'

ARGS_LOG_INFO = 'Аргументы командной строки: {args}'
FILE_OUTPUT_LOG_INFO = 'Файл с результатами был сохранён: {file_path}'
GET_RESPONSE_LOG_ERROR = 'Возникла ошибка при загрузке страницы {url}'
TAG_NOT_FOUND_LOG_ERROR = 'Не найден тег {tag} {attrs}'
