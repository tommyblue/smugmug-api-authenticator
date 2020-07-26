from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode


def fix_auth_url(auth_url):
    parts = urlsplit(auth_url)
    query = parse_qsl(parts.query, True)
    query.append(("Access", "Full"))
    query.append(("Permissions", "Modify"))
    return urlunsplit(
        (parts.scheme, parts.netloc, parts.path, urlencode(query, True), parts.fragment)
    )
