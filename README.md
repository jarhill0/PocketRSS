# Pocket RSS

*A simple Python project to automatically save links from RSS feeds to Pocket*

## Installation

First, [register an app with Pocket](https://getpocket.com/developer/apps/new).
Make sure it has the **Add** permission. Take note of the resulting "consumer
key."

```
git clone https://github.com/jarhill0/PocketRSS
cd PocketRSS
cp example_config.py config.py
```

Now use your favorite text editor to edit `config.py` to contain your consumer
key. For instance, with `nano`:

```
nano config.py
```

## Configuration

Fill out the file `data/feeds.txt` with links to RSS/Atom feeds, one link per
line.

## Usage

Change the current directory to the directory into which this repository was
cloned. For example:

```
cd ~/PocketRSS
```

Running `ls` should show something that includes the `pocketrss` (lowercase)
directory like the following:

```
README.md       pocketrss
```

Then run with `python3 -m pocketrss`.

The first run will require that you authenticate your Pocket account on the web.
After that, your token will be saved.

The first run will store up to 20 posts from the last week of your feeds to your
Pocket account. Subsequent runs will save all the posts with publish times after
the most recent run.

This project is only intended to work with one Pocket account at a time. If you
wish to switch to a new account, just delete the file `access_token.txt` within
the directory `data`.
