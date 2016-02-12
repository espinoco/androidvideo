#!/usr/bin/python

import json
import subprocess
import sys

if len(sys.argv) == 1:
    print "Can't get args"
    exit()
else:
    if len(sys.argv) < 4:
        print "Can't get video file name args"
        exit()
    else:
        inputFileName = sys.argv[1]
        outputFileName = sys.argv[2]
        quality = sys.argv[3]

if quality == "hd":
    outputWidht = 1280
    outputHeight = 720
    outputVideoProfile = "Constrained Baseline"
    outputVideoFrameRate = 30
    outputVideoBitrate = 2197152
    outputVideoBitrateValue = "1.9M"
    outputAudioChannels = "stereo"
    outputAudioBitrate = 193000
    outputAudioBitrateValue = "192k"
elif quality == "hq":
    outputWidht = 480
    outputHeight = 360
    outputVideoProfile = "Constrained Baseline"
    outputVideoFrameRate = 30
    outputVideoBitrate = 500900
    outputVideoBitrateValue = "480k"
    outputAudioChannels = "stereo"
    outputAudioBitrate = 129000
    outputAudioBitrateValue = "128k"
elif quality == "low":
    outputWidht = 176
    outputHeight = 144
    outputVideoProfile = "Constrained Baseline"
    outputVideoFrameRate = 12
    outputVideoBitrate = 57000
    outputVideoBitrateValue = "55k"
    outputAudioChannels = "mono"
    outputAudioBitrate = 25000
    outputAudioBitrateValue = "24k"
else:
    print "Invalid quality"
    exit()

command = 'ffprobe -v quiet -print_format json -show_format -show_streams "%s" > "meta.json"' % inputFileName

output = subprocess.call(command, shell=True)

if output == 0:
    print 'Input video data was generated'
else:
    print "Can't get input video data"
    exit()

json_data = open('meta.json')

data = json.load(json_data)

command = 'ffmpeg -i %s ' % inputFileName

videoWidth = data["streams"][0]["width"]
videoHeight = data["streams"][0]["height"]

if videoWidth > outputWidht:
    command += '-s %sx%s ' % (outputWidht, outputHeight)

videoBitRate = data["streams"][0]["bit_rate"]
videoBitRateInt = int(videoBitRate)

if videoBitRateInt > outputVideoBitrate:
    command += '-b:v %s ' % outputVideoBitrateValue

videoCodec = data["streams"][0]["codec_name"]

command += '-c:v libx264 '

command += '-profile:v baseline '

videoFrameRate = data["streams"][0]["r_frame_rate"]
videoFrameRateSplited = videoFrameRate.split("/")
videoFrameRateShort = videoFrameRateSplited[0]
videoFrameRate = int(videoFrameRateShort[:2])

if videoFrameRate > outputVideoFrameRate:
    command += '-r %s ' % outputVideoFrameRate

videoAudioCodec = data["streams"][1]["codec_name"]
videoAudioChannel = data["streams"][1]["channel_layout"]
videoAudioBitRate = data["streams"][1]["bit_rate"]
videoAudioBitRateInt = int(videoAudioBitRate)

command += '-c:a libvo_aacenc '
if outputAudioChannels == "mono":
    command += '-ac 1 '
else:
    command += '-ac 2 '
if videoAudioBitRateInt > outputAudioBitrate:
    command += '-ab %s ' % outputAudioBitrateValue
else:
    videoAudioBitRateInt = int(videoAudioBitRateInt / 1000)
    command += '-ab %sk ' % videoAudioBitRateInt

command += '%s' % outputFileName

if quality == "hd":
    command += '-hd.mp4'
elif quality == "hq":
    command += '-hq.mp4'
else:
    command += '.mp4'

output = subprocess.call(command, shell=True)

if output == 0:
    print 'Video generated'
else:
    print "Can't generate video"
    print command
    exit()

json_data.close()
