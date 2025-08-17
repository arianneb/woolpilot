import pytest
from woolpilot.models import Product
from woolpilot.parsers.wollplatz import WollplatzParser
from woolpilot.parsers.utils import convert_price_to_float
from bs4 import BeautifulSoup

@pytest.fixture
def parser():
    return WollplatzParser()

@pytest.fixture
def mock_html():
    return """
    <span class="product-price" itemprop="price" content="8.46">
    <span class="product-price-currency">€ </span>
    <span class="product-price-amount">8,46</span>
    </span>
    <meta itemprop="availability" content="http://schema.org/InStock">
    <tr><td>Nadelstärke</td><td>4 mm</td></tr>
    <tr><td>Zusammenstellung</td><td>100% Acryl</td></tr>
    """

@pytest.fixture
def mock_bad_html():
    return """
    <span class="bad-price" itemprop="price" content="">
    <span class="bad-price">€ </span>
    <span class="bad-pricet"></span>
    </span>
    <meta trash="rubbish" content="http://schema.org/InStock">
    <tr><td>blasphemy</td><td>4 mm</td></tr>
    <tr><td>hogwash</td><td>100% Acryl</td></tr>
    """

@pytest.fixture
def soup(mock_html):
    return BeautifulSoup(mock_html, "html.parser")

@pytest.fixture
def invalid_soup(mock_bad_html):
    return BeautifulSoup(mock_bad_html, "html.parser")

# sanity check - test imports
def test_imports():
    import woolpilot  # noqa: F401
    from woolpilot.models import Product
    p = Product("Brand", "Name")
    assert p.brand == "Brand" and p.name == "Name"

# test model structure
def test_product_model():
    p = Product(
        brand="Brand",
        name="Name",
        price="9,99",
        availability=True,
        needle_size="4 mm",
        composition="100% Cotton",
        source_url="https://example.com/product"
    )
    assert p.brand == "Brand"
    assert p.name == "Name"
    assert p.price == "9,99"
    assert p.availability is True
    assert p.needle_size == "4 mm"
    assert p.composition == "100% Cotton"
    assert "example.com" in p.source_url

# price parsing tests
def test_parse_price(parser, soup):
    price = parser.parse_price(soup)
    assert price == 8.46

def test_convert_price_to_float():
    price_string = "8,46"
    price = convert_price_to_float(price_string)
    assert price == 8.46

def test_parse_price_invalid(parser, invalid_soup):
    price = parser.parse_price(invalid_soup)
    assert price == 0

# parse remaining fields tests
def test_parse_availability(parser, soup):
    availability = parser.parse_availability(soup)
    assert availability == "Available"

def test_parse_availability(parser, invalid_soup):
    availability = parser.parse_availability(invalid_soup)
    assert availability == "Availability not found"

def test_parse_needle_size(parser, soup):
    needle_size = parser.parse_needle_size(soup)
    assert needle_size == "4 mm"

def test_parse_composition(parser, soup):
    composition = parser.parse_composition(soup)
    assert composition == "100% Acryl"

# detail page parsing tests
def test_parse_product_detail_full_fields(parser, mock_html):
    result = parser.parse_product_detail(mock_html)
    assert result["price"] == 8.46
    assert result["availability"] == "Available"
    assert result["needle_size"] == "4 mm"
    assert result["composition"] == "100% Acryl"

def test_parse_product_detail_invalid_data(parser, mock_bad_html):
    result = parser.parse_product_detail(mock_bad_html)
    assert result["price"] == 0
    assert result["availability"] == "Availability not found"
    assert result["needle_size"] == "Needle size not found"
    assert result["composition"] == "Composition not found"
