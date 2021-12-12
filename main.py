#!/usr/bin/env nix-shell
#!nix-shell -i python3 -p "python3.withPackages (ps: [ps.tweepy ps.mastodon-py])"
import html
import json
import os
import sqlite3

from mastodon import Mastodon
import tweepy

conn = sqlite3.connect("database.sqlite3")
conn.execute("CREATE TABLE IF NOT EXISTS kv (key TEXT PRIMARY KEY, value TEXT)")


def get_crossposted_url(ident):
    for row in conn.execute("SELECT value FROM kv WHERE key = ? LIMIT 1", (ident,)):
        return row[0]


mastodon = Mastodon(
    access_token="mastodon.client.credentials",
    api_base_url="https://raru.re",
)

with open("twitter.credentials") as f:
    twitter_auth_info = json.load(f)

twitter_auth = tweepy.OAuthHandler(
    twitter_auth_info["app_key"], twitter_auth_info["app_secret"]
)
twitter_auth.set_access_token(
    twitter_auth_info["user_key"], twitter_auth_info["user_secret"]
)
twitter = tweepy.API(twitter_auth)

last_used_id = get_crossposted_url("last_handled_id")

new_tweets = sorted(
    twitter.user_timeline(
        user_id="772111562127601665",
        since_id=last_used_id,
        trim_user=True,
        include_rts=False,
        tweet_mode="extended",
    ),
    key=lambda x: x.id,
)
for tweet in new_tweets:
    print(tweet.id)
    parent_tweet_id = tweet.in_reply_to_status_id
    try:
        parent_toot_id = (
            int(get_crossposted_url(parent_tweet_id))
            if parent_tweet_id is not None
            else None
        )
        toot = mastodon.status_post(
            html.unescape(tweet.full_text), in_reply_to_id=parent_toot_id
        )
        conn.execute(
            "INSERT INTO kv(key, value) VALUES (?, ?)", (tweet.id_str, str(toot.id))
        )
    except TypeError:
        pass
    conn.execute(
        "INSERT INTO kv(key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
        ("last_handled_id", tweet.id_str),
    )
    conn.commit()
