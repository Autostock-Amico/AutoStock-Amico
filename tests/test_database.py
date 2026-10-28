def test_mongo_uri_parsing():
    uri = "mongodb://santi:santi123@localhost:27017/autostock"
    assert "autostock" in uri
    assert uri.startswith("mongodb://")
