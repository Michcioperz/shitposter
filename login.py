#!/usr/bin/env nix-shell
#!nix-shell -i python3 -p "python3.withPackages (ps: [ps.mastodon-py])"
import os

from mastodon import Mastodon

mastodon = Mastodon(
    api_base_url="https://raru.re", client_id="mastodon.app.credentials"
)
scopes = ["write"]
print(mastodon.auth_request_url(scopes=scopes))
mastodon.log_in(
    to_file="mastodon.client.credentials", code=input("code: "), scopes=scopes
)
