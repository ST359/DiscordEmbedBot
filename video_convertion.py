import ffmpeg
from converter import Converter
import platform


def convert_video(path_to_file: str):
    c = Converter()
    info = c.probe(path_to_file)
    if platform.system() == 'Windows':
        conv = c.convert(path_to_file, 'converted_vids/output.mp4', {
            'format': 'mp4',
            'audio': {
                'codec': 'aac',
                'samplerate': 11025,
                'channels': 2
            },
            'video': {
                'codec': 'h264'
            }}, timeout=None)
    else:
        conv = c.convert(path_to_file, 'converted_vids/output.mp4', {
            'format': 'mp4',
            'audio': {
                'codec': 'aac',
                'samplerate': 11025,
                'channels': 2
            },
            'video': {
                'codec': 'h264'
            }})
    for timecode in conv:
        print
        "Converting (%f) ...\r" % timecode
