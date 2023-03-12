import logging

from bs4 import BeautifulSoup
from requests import RequestException

from exceptions import ParserFindTagException

GET_RESPONSE_LOG_ERROR = 'Возникла ошибка при загрузке страницы {url}'
TAG_NOT_FOUND_LOG_ERROR = 'Не найден тег {tag} {attrs}'


def get_response(session, url):
    """Перехват ошибки RequestException."""
    try:
        response = session.get(url)
        response.encoding = 'utf-8'
        return response
    except RequestException:
        logging.exception(
            GET_RESPONSE_LOG_ERROR.format(url=url),
            stack_info=True
        )


def find_tag(soup, tag, attrs=None):
    """Перехват ошибки поиска тегов."""
    searched_tag = soup.find(tag, attrs=(attrs or {}))
    if searched_tag is None:
        error_msg = TAG_NOT_FOUND_LOG_ERROR.format(
            tag=tag, attrs=attrs
        )
        logging.error(error_msg, stack_info=True)
        raise ParserFindTagException(error_msg)
    return searched_tag


def get_soup(session, url):
    """Создание "супа"."""
    response = get_response(session, url)
    return BeautifulSoup(response.text, features='lxml')
