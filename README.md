# shitposter

a very simplified twitter-to-fedi crossposter

it doesn't support images. it just takes your top (as in not replying to anything) tweets and your replies to tweets it has seen (so this should mean by recursive definition including self-replies, thus threads) and pushes the text to fedi

## requirements (txt)

nixos. haha yeah okay you don't need it but if you're not gonna use the nix-shell shebang provided you need python (3 obviously) with mastodon.py and tweepy packages installed

## how to use (please don't unless you're desperate (i was))

1. have a twitter dev account with an API v1 app from when you were in high school, put its keys and secrets in `twitter.credentials` file as a json object with keys as seen in `main.py`
2. change up some constants like my user id in `main.py` and my fedi instance in i guess all the python files
3. use `create.py` and `login.py` scripts to generate files with mastodon credentials
4. put `main.py` in a cron job
5. delete 200 toots this thing created based on 200 tweets it saw that were actually pretty old oh well guess you should've commented shit out but that was difficult to explain
