Create Android Compatible Videos
================================

Create Android compatible videos that play in ANY Android device without
third party software. Based on `Android Supported Media
Formats <https://developer.android.com/intl/es/guide/appendix/media-formats.html#recommendations>`__.

*Playability depends in device resolution only, i.e. HD 720p video won't
play correctly on 240x320 resolution device*

**DEPENDS ON `FFmpeg <https://www.ffmpeg.org/>`__**

Video quality
=============

Choose a video quality between following options:

-  low -> Low quality
-  hq -> High quality
-  hd -> HD 720p (N/A on all devices)

Usage
=====

``androidvideo [quality] [video input] [output filename without extension]``

**Example**

``androidvideo hq input.mov output``

Will output an ``output.mp4`` file.

Installation
============

Please make sure you have `FFmpeg <https://www.ffmpeg.org/>`__
installed. Run ``ffmpeg -version`` to check installation.

``pip install androidvideo``

Help
====

Run ``androidvideo -h`` for help.
