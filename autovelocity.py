import sys
import os
import midi
from pyechonest import config
from pyechonest import song
from pyechonest import artist
from pyechonest import track

midifilename = sys.argv[1]
audiofilename = sys.argv[2]

try:
    config.ECHO_NEST_API_KEY = sys.argv[3]
except:
    config.ECHO_NEST_API_KEY = raw_input('Enter your Echo Nest API key: ')

midifile=midi.read_midifile(midifilename)
audiofile=file(audiofilename)
 

echoTrack = track.track_from_file(audiofile,audiofilename[-3:])
audioSegments = echoTrack.segments
audioSegments = sorted(audioSegments,key=lambda x:x['start'])

events = reduce(lambda x,y :x+y,midifile)
events = sorted(events,key=lambda x: x.msdelay)



t = 0
audioSegments_ix = 0
events_ix=0


while True:
    try:
        current_time = audioSegments[audioSegments_ix]['start']
        if events[events_ix].msdelay/1000. <= current_time:
            if events[events_ix].type == 'NoteOnEvent':
                if events[events_ix].velocity == 0:
                    events[events_ix].type = 'NoteOffEvent'
                else:
                    events[events_ix].velocity = int(128+2*audioSegments[audioSegments_ix]['loudness_max'])
            events_ix += 1
        else:
            audioSegments_ix+=1
    except:
        break

X=midi.EventStream()
X.resolution=480

for track in range(len(midifile)):
    X.add_track()
    for e in events:
        try:
            if e.channel == track:
                X.add_event(e)
        except:
            pass

print len(X)
print len(X[0])


midi.write_midifile(X,midifilename[:-3]+'-velocity.mid')




    



    



                
