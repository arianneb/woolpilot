def test_imports():
    import woolpilot  # noqa: F401
    from woolpilot.models import Product
    p = Product("Brand", "Name")
    assert p.brand == "Brand" and p.name == "Name"
