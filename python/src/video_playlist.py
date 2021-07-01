"""A video playlist class."""


class Playlist:
    """A class used to represent a Playlist."""
    def __init__(self, playlist_name: str):
        self._name = playlist_name
        self._videos = []
    
    @property
    def name(self):
        return self._name

    @property
    def videos(self):
        return self._videos

    def add_video(self,video):
        self._videos.append(video)
    
    def clear_videos(self):
        self._videos = []