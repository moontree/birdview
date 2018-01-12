# birdview flow

### calibrate cameras 
run `calibration.py` and get results,
results include mtx, dist, and newcameramtx

### get transport matrix
run `corners.py` and get results.
- find corners in undisorted image
- calculate target coordianates
- get transport matrix

### get birdview
run `birdview.py`
