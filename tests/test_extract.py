from pipeline.extract import fetch_weather

class FakeResponse:
    def raise_for_status(self): pass
    def json(self): return {"hourly": {"time": []}}

class FakeSession:
    def get(self, url, params, timeout):
        assert params["latitude"] == 50.6
        assert timeout == 20
        return FakeResponse()

def test_fetch_weather_adds_city():
    result = fetch_weather(
        {"city": "Lille", "latitude": 50.6, "longitude": 3.0},
        session=FakeSession(),
    )
    assert result["city"] == "Lille"
