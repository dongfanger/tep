def test(login_xdist):
    ro = login_xdist()
    print(ro.data)
