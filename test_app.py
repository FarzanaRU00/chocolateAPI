import json

class TestAPICase():
    def test_welcome(self, api):
        res = api.get('/')
        assert res.status == '200 OK'
        # assert res.json['message'] == 'Welcome to the chocolate API!'

    def test_get_chocolate(self, api):
        res = api.get('/chocolates')
        assert res.status == '200 OK'
        assert len(res.json) == 2