#!/usr/bin/env nix-shell
#!nix-shell -i python3 -p "python3.withPackages (ps: [ps.mastodon-py])"
import os

from mastodon import Mastodon

Mastodon.create_app(
    "shitposter", api_base_url="https://raru.re", to_file="mastodon.app.credentials"
)
