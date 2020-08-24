"""Client for the Wikipedia REST API, version 1."""

from dataclasses import dataclass

import click
import desert
import marshmallow
import requests

API_URL: str = "https://{language}.wikipedia.org/api/rest_v1/page/random/summary"


@dataclass
class Page:
    """Page resource.

    Attributes:
        titl: The title of the Wikipedia page.
        extract: A plain text summary.
    """

    title: str
    extract: str


schema = desert.schema(Page, meta={"unknown": marshmallow.EXCLUDE})


def random_page(language: str = "en") -> Page:
    """Returen a random page.

    Args:
        language (str): The Wikipedia language edition. Defaults to "en".

    Raises:
        click.ClickException: The HTTP request failed or the HTTP response
            contained an invalid body.

    Returns:
        Page: A page resource.

    Example:
        >>> from hypermodern_python_cli99 import wikipedia
        >>> page = wikipedia.random_page(language="en")
        >>> bool(page.title)
        True
    """
    url = API_URL.format(language=language)
    try:
        with requests.get(url) as response:
            response.raise_for_status()
            data = response.json()
            return schema.load(data)
    except (requests.RequestException, marshmallow.ValidationError) as error:
        message = str(error)
        raise click.ClickException(message)
