from pytube import YouTube
yt=YouTube('https://www.youtube.com/watch?v=fTVwGNqbBYg&list=RDMMfTVwGNqbBYg&start_radio=1')
t=yt.streams.filter(only_audio=True).first().download()
