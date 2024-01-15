import auditok

sr = 44100
sw = 2
ch = 1
eth = 55 # alias for energy_threshold, default value is 50

try:
    for region in auditok.split(input=None, sr=sr, sw=sw, ch=ch, eth=eth):
        print(region)
        region.play(progress_bar=True) # progress bar requires `tqdm`
except KeyboardInterrupt:
     pass