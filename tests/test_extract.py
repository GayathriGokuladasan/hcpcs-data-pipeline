from src import extract


class FakeSession:
    pass


def test_get_hcpcs_groups(monkeypatch):
    html = """
    <html>
        <body>
            <table>
                <tr>
                    <td>1</td>
                    <td>
                        <a href="/Codes/A">A</a>
                    </td>
                    <td>Transportation Services</td>
                </tr>
            </table>
        </body>
    </html>
    """

    def fake_get_page(session, url):
        from bs4 import BeautifulSoup
        return BeautifulSoup(html, "html.parser")

    monkeypatch.setattr(
        extract,
        "get_page",
        fake_get_page
    )

    result = extract.get_hcpcs_groups(FakeSession())

    assert len(result) == 1
    assert result[0]["group_code"] == "A"
    assert result[0]["category_name"] == "Transportation Services"
    assert result[0]["url"] == "https://www.hcpcsdata.com/Codes/A"


def test_extract_group(monkeypatch):
    html = """
    <html>
        <body>
            <table>
                <tbody>
                    <tr class="clickable-row">
                        <td>A0021</td>
                        <td>Ambulance service</td>
                    </tr>
                    <tr class="clickable-row">
                        <td>A0023</td>
                        <td>Transportation service</td>
                    </tr>
                </tbody>
            </table>
        </body>
    </html>
    """

    def fake_get_page(session, url):
        from bs4 import BeautifulSoup
        return BeautifulSoup(html, "html.parser")

    monkeypatch.setattr(
        extract,
        "get_page",
        fake_get_page
    )

    group = {
        "group_code": "A",
        "category_name": "Transportation Services",
        "url": "https://www.hcpcsdata.com/Codes/A",
    }

    result = extract.extract_group(
        FakeSession(),
        group
    )

    assert len(result) == 2

    assert result[0]["hcpcs_code"] == "A0021"
    assert result[0]["group_code"] == "A"
    assert result[0]["category_name"] == "Transportation Services"
    assert result[0]["long_description"] == "Ambulance service"

    assert result[1]["hcpcs_code"] == "A0023"
    assert result[1]["long_description"] == "Transportation service"
