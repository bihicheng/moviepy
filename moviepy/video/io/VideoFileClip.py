import os

from moviepy.video.VideoClip import VideoClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.Clip import Clip
from moviepy.video.io.ffmpeg_reader import FFMPEG_VideoReader

class VideoFileClip(VideoClip):

    """
    
    A video clip originating from a movie file. For instance: ::
    
        >>> clip = VideofileClip("myHolidays.mp4")
        >>> clip2 = VideofileClip("myMaskVideo.avi",ismask = True)
    
    
    Parameters
    ------------
    
    filename:
      The name of the video file. It can have any extension supported
      by ffmpeg: .ogv, .mp4, .mpeg, .avi, .mov etc.
    
    ismask:
      Set this to `True` if the clip is going to be used as a mask.
      
    has_mask:
      Set this to 'True' if there is a mask included in the videofile.
       Video files rarely contain masks, but some video codecs enable
       that. For istance if you have a MoviePy VideoClip with a mask you
       can save it to a videofile with a mask. (see also 
       ``VideoClip.to_videofile`` for more details).
    
    audio:
      Set to `False` if the clip doesn't have any audio or if you do not
      wish to read the audio.
      
    Attributes
    -----------
    
    filename:
      Name of the original video file.
    
    fps:
      Frames per second in the original file. 
        
    """

    def __init__(self, filename, ismask=False, has_mask=False,
                 audio=True, audio_buffersize = 200000,
                 audio_fps=44100, audio_nbytes=2, verbose=False):
        
        VideoClip.__init__(self, ismask)
        
        # We store the construction parameters in case we need to make
        # a copy (a 'co-reader').
        
        self.parameters = {'filename':filename, 'ismask':ismask,
                           'has_mask':has_mask, 'audio':audio,
                           'audio_buffersize':audio_buffersize}
        
        # Make a reader
        pix_fmt= "rgba" if has_mask else "rgb24"
        self.reader = FFMPEG_VideoReader(filename, pix_fmt=pix_fmt)
        
        # Make some of the reader's attributes accessible from the clip
        self.duration = self.reader.duration
        self.end = self.reader.duration
        
        self.fps = self.reader.fps
        self.size = self.reader.size
        self.get_frame = lambda t: self.reader.get_frame(t)
        
        # Make a reader for the audio, if any.
        if audio:
            self.audio = AudioFileClip(filename,
                                       buffersize= audio_buffersize,
                                       fps = audio_fps,
                                       nbytes = audio_nbytes)
    
    def coreader(self, audio=True):
        """
        Returns a copy of the AudioFileClip with an autonomous reader.
        Maybe REMOVED in the coming versions. Wait and see. ::
        
            >>> clip = VideofileClip("myHolidays.mp4", ismask=True)
            >>> clip2 = VideofileClip("myHolidays.mp4", ismask=True)
        
        is equivalent to ::
        
            >>> clip = VideofileClip("myHolidays.mp4", ismask=True)
            >>> clip2 = clip.coreader()
        """
            
        return VideoFileClip(**self.parameters)
