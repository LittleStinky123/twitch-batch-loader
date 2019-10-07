# Twitch Clip Batch Downloader  
![example-gif](https://github.com/amiechen/twitch-batch-loader/blob/master/example.gif)

### Pre-Install:

1) Get a twitch `Client ID` by registering a twitch app [here](https://dev.twitch.tv/dashboard/apps/create).
Once finished, copy the `Client ID`. You will need it to run the script.

2) Install python 3 on your machine if you haven't.

### Usage:

1) Install python packages
```
pip install requests
```

2) Delete the example clips in `clips.txt` and the ones your want. Put each URL on it's own line. No commas or anything like that.

3) Then run the batchloader script with your new Client Id using the provided clip list or create your list automatically with a provided broadcaster id, filtering by time is possible by provding two RFC3339 timestamps
```
cd twitch-batch-loader
python batchloader.py <YOUR AWESOME CLIENT ID> [<THE AWESOME BROADCASTER ID> [<Start date of time frame> <End date of time frame>]]
```
The clip list creator does not include every clip for the provided broadcaster_id though, not using first=100 in the requests that use pagination returns 993 clips, with first=100 1012 in my testing but never all clips as sometimes running the script returns clips that are missing in other runs, strange...

Voilà! once you see the finished message in your terminal, check the `downloads` folder in this repo and you should see the videos there.
