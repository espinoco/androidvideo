#!/usr/bin/python

import json
import subprocess
import argparse
from argparse import RawTextHelpFormatter
import tempfile


class AndroidVideo:
    'Create Android videos'
    def __init__(self):
        self.description = 'Create Android compatible videos\n'
        self.description += ('androidvideo [quality] [video input] '
                             '[output filename]\n\n')
        self.description += 'Quality options:\n'
        self.description += 'low -> Low quality\n'
        self.description += 'hq  -> High quality\n'
        self.description += 'hd  -> HD 720p (N/A on all devices)\n'
        parser = argparse.ArgumentParser(description=self.description,
                                         formatter_class=RawTextHelpFormatter)
        parser.add_argument("quality", choices=["low", "hq", "hd"],
                            help="Quality")
        parser.add_argument("videoinput",
                            help="Video input")
        parser.add_argument("output",
                            help="Video output",
                            action="store")
        args = parser.parse_args()
        self.quality = args.quality
        self.input_ = args.videoinput
        self.output_ = args.output

        self.file_ = None

        self.outputWidht = 0
        self.outputHeight = 0
        self.outputVideoProfile = ""
        self.outputVideoFrameRate = 0
        self.outputVideoBitrate = 0
        self.outputVideoBitrateValue = ""
        self.outputAudioChannels = ""
        self.outputAudioBitrate = 0
        self.outputAudioBitrateValue = ""

        self.defaultVideoProfile = "Constrained Baseline"

        self.convertVideo()

    def convertVideo(self):
        self.setQuality()
        self.getVideoData()
        self.executeVideoConversion()

    def setQuality(self):
        if self.quality == "hd":
            self.outputWidht = 1280
            self.outputHeight = 720
            self.outputVideoProfile = self.defaultVideoProfile
            self.outputVideoFrameRate = 30
            self.outputVideoBitrate = 2097152
            self.outputVideoBitrateValue = "2M"
            self.outputAudioChannels = "stereo"
            self.outputAudioBitrate = 196608
            self.outputAudioBitrateValue = "192k"
        elif self.quality == "hq":
            self.outputWidht = 480
            self.outputHeight = 360
            self.outputVideoProfile = self.defaultVideoProfile
            self.outputVideoFrameRate = 30
            self.outputVideoBitrate = 512000
            self.outputVideoBitrateValue = "500k"
            self.outputAudioChannels = "stereo"
            self.outputAudioBitrate = 131072
            self.outputAudioBitrateValue = "128k"
        elif self.quality == "low":
            self.outputWidht = 176
            self.outputHeight = 144
            self.outputVideoProfile = self.defaultVideoProfile
            self.outputVideoFrameRate = 12
            self.outputVideoBitrate = 57344
            self.outputVideoBitrateValue = "56k"
            self.outputAudioChannels = "mono"
            self.outputAudioBitrate = 24576
            self.outputAudioBitrateValue = "24k"
        else:
            exit("Invalid quality")

    def getVideoData(self):
        self.file_ = tempfile.NamedTemporaryFile()

        self.file_.write('')

        self.file_.seek(0)

        command = 'ffprobe -v quiet -print_format json -show_format -show_streams "%s" > "%s"' % (self.input_, self.file_.name)

        output = subprocess.call(command, shell=True)

        if output != 0:
            exit("Can't get video input data")

    def executeVideoConversion(self):
        json_data = open(self.file_.name)

        data = json.load(json_data)

        command = 'ffmpeg '

        command += '-i "%s" ' % self.input_

        command += '-vf scale=%sx%s,setsar=1:1 ' % (self.outputWidht,
                                                    self.outputHeight)

        videoBitRate = data["format"]["bit_rate"]

        videoBitRateInt = int(videoBitRate)

        if videoBitRateInt > self.outputVideoBitrate:
            command += '-b:v %s ' % self.outputVideoBitrateValue

        command += '-c:v libx264 '

        command += '-profile:v baseline -level:v 4.0 '

        videoFrameRate = data["streams"][0]["r_frame_rate"]

        videoFrameRateSplited = videoFrameRate.split("/")

        videoFrameRateShort = videoFrameRateSplited[0]

        videoFrameRate = int(videoFrameRateShort[:2])

        if videoFrameRate > self.outputVideoFrameRate:
            command += '-r %s ' % self.outputVideoFrameRate

        videoAudioBitRate = data["streams"][1]["bit_rate"]

        videoAudioBitRateInt = int(videoAudioBitRate)

        command += '-c:a libvo_aacenc '

        if self.outputAudioChannels == "mono":
            command += '-ac 1 '
        else:
            command += '-ac 2 '

        if videoAudioBitRateInt > self.outputAudioBitrate:
            command += '-ab %s ' % self.outputAudioBitrateValue

        command += '%s.mp4' % self.output_

        print command

        output = subprocess.call(command, shell=True)

        if output != 0:
            exit("Video NOT generated")

        print "All done!"

        json_data.close()

        self.file_.close()
