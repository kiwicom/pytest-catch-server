def test_catch_server__get(testdir):
    testdir.makepyfile(
        """
        import urllib.request

        def test_get(catch_server):
            url = "http://{cs.host}:{cs.port}/get_it".format(cs=catch_server)
            request = urllib.request.Request(url, method="GET")

            with urllib.request.urlopen(request) as response:
                assert response.status == 200
                assert response.read() == b"OK"

            assert catch_server.requests == [
                {"method": "GET", "path": "/get_it", "data": b""},
            ]
        """
    )

    result = testdir.runpytest("-v")

    result.stdout.fnmatch_lines(["*::test_get PASSED*"])
    assert result.ret == 0


def test_catch_server__post(testdir):
    testdir.makepyfile(
        """
        import urllib.request

        def test_post(catch_server):
            url = "http://{cs.host}:{cs.port}/post_it".format(cs=catch_server)
            request = urllib.request.Request(url, method="POST", data=b"something")

            with urllib.request.urlopen(request) as response:
                assert response.status == 200
                assert response.read() == b"OK"

            assert catch_server.requests == [
                {"method": "POST", "path": "/post_it", "data": b"something"},
            ]
        """
    )

    result = testdir.runpytest("-v")

    result.stdout.fnmatch_lines(["*::test_post PASSED*"])
    assert result.ret == 0


def test_catch_server__put(testdir):
    testdir.makepyfile(
        """
        import urllib.request

        def test_put(catch_server):
            url = "http://{cs.host}:{cs.port}/put_it".format(cs=catch_server)
            request = urllib.request.Request(url, method="PUT", data=b"other data")

            with urllib.request.urlopen(request) as response:
                assert response.status == 200
                assert response.read() == b"OK"

            assert catch_server.requests == [
                {"method": "PUT", "path": "/put_it", "data": b"other data"},
            ]
        """
    )

    result = testdir.runpytest("-v")

    result.stdout.fnmatch_lines(["*::test_put PASSED*"])
    assert result.ret == 0


def test_catch_server__patch(testdir):
    testdir.makepyfile(
        """
        import urllib.request

        def test_patch(catch_server):
            url = "http://{cs.host}:{cs.port}/patch_it".format(cs=catch_server)
            request = urllib.request.Request(url, method="PATCH", data=b'{"x": 42}')

            with urllib.request.urlopen(request) as response:
                assert response.status == 200
                assert response.read() == b"OK"

            assert catch_server.requests == [
                {"method": "PATCH", "path": "/patch_it", "data": b'{"x": 42}'},
            ]
        """
    )

    result = testdir.runpytest("-v")

    result.stdout.fnmatch_lines(["*::test_patch PASSED*"])
    assert result.ret == 0


def test_catch_server__delete(testdir):
    testdir.makepyfile(
        """
        import urllib.request

        def test_delete(catch_server):
            url = "http://{cs.host}:{cs.port}/delete_it".format(cs=catch_server)
            request = urllib.request.Request(url, method="DELETE")

            with urllib.request.urlopen(request) as response:
                assert response.status == 200
                assert response.read() == b"OK"

            assert catch_server.requests == [
                {"method": "DELETE", "path": "/delete_it", "data": b""},
            ]
        """
    )

    result = testdir.runpytest("-v")

    result.stdout.fnmatch_lines(["*::test_delete PASSED*"])
    assert result.ret == 0


def test_catch_server__multiple_requests(testdir):
    testdir.makepyfile(
        """
        import urllib.request

        def test_multiple_requests(catch_server):
            for n, method in enumerate(["PUT", "POST", "PATCH"]):
                url = "http://{cs.host}:{cs.port}/req_{n}".format(cs=catch_server, n=n)
                data = "{} {}".format(n, method).encode("utf-8")
                request = urllib.request.Request(url, method=method, data=data)

                with urllib.request.urlopen(request) as response:
                    assert response.status == 200
                    assert response.read() == b"OK"

            assert catch_server.requests == [
                {"method": "PUT", "path": "/req_0", "data": b"0 PUT"},
                {"method": "POST", "path": "/req_1", "data": b"1 POST"},
                {"method": "PATCH", "path": "/req_2", "data": b"2 PATCH"},
            ]
        """
    )

    result = testdir.runpytest("-v")

    result.stdout.fnmatch_lines(["*::test_multiple_requests PASSED*"])
    assert result.ret == 0
