from back.libs.token_required import token_required


@token_required
def test(p):
    print("ok")
    return "ok"
