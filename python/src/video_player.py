"""A video player class."""

from .video_library import VideoLibrary
from .video_playlist import Playlist
import random


class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self.currentlyPlaying = None
        self.videoPaused = False
        self.playlists = []

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        print("Here's a list of all available videos:")
        # print(self._video_library.get_all_videos()[0].tags)
        videoProperties = []
        for video in self._video_library.get_all_videos():
            if video.flag != None:
                videoProperties.append("  "+video.title + " (" + video.video_id +") ["+ " ".join(video.tags) + "] - FLAGGED (reason: " + video.flag + ")")
                continue
            videoProperties.append("  "+video.title + " (" + video.video_id +") ["+ " ".join(video.tags) + "]")
        videoProperties.sort()
        for i in videoProperties:
            print(i)


    def play_video(self, video_id):
        """Plays the respective video.
        Args:
            video_id: The video_id to be played.
        """
        video = self._video_library.get_video(video_id)
        if video == None:
            print("Cannot play video: Video does not exist")
            return
        if video.flag != None:
            print("Cannot play video: Video is currently flagged (reason: " + video.flag + ")")
            return
        if self.currentlyPlaying != None:
            print("Stopping video: " + self.currentlyPlaying.title)
        self.videoPaused = False
        self.currentlyPlaying = self._video_library.get_video(video_id)
        print("Playing video: " + self.currentlyPlaying.title)


    def stop_video(self):
        """Stops the current video."""
        if self.currentlyPlaying == None:
            print("Cannot stop video: No video is currently playing")     
        else:
            print("Stopping video: " + self.currentlyPlaying.title)
            self.currentlyPlaying = None



    def play_random_video(self):
        """Plays a random video from the video library."""
        videoLibrary = self._video_library.get_all_videos()
        unflagged_videos = []
        for video in videoLibrary:
            if video.flag == None:
                unflagged_videos.append(video)
        if len(unflagged_videos) == 0:
            print("No videos available")
            return
        
        randomVid = random.choice(unflagged_videos) 
        self.play_video(randomVid.video_id)

    def pause_video(self):
        """Pauses the current video."""
        if self.currentlyPlaying == None:
            print("Cannot pause video: No video is currently playing")
        elif self.videoPaused == True:
            print("Video already paused: "+self.currentlyPlaying.title)
        else:
            self.videoPaused = True
            print("Pausing video: " + self.currentlyPlaying.title)



    def continue_video(self):
        """Resumes playing the current video."""
        if self.currentlyPlaying == None:
            print("Cannot continue video: No video is currently playing")
        elif self.videoPaused == False:
            print("Cannot continue video: Video is not paused")
        else:
            self.videoPaused = False
            print("Continuing video: "+ self.currentlyPlaying.title)

    def show_playing(self):
        """Displays video currently playing."""
        if self.currentlyPlaying == None:
            print("No video is currently playing")
            return
        message = "Currently playing: " + self.currentlyPlaying.title + " (" + self.currentlyPlaying.video_id +") ["+ " ".join(self.currentlyPlaying.tags) + "]"
        if self.videoPaused:
            message += " - PAUSED"
        print(message)

    def playlist_exists(self,playlist_name):
        for i in self.playlists:
            if i.name.lower() == playlist_name.lower():
                return True
        return False

    def search_playlists(self,playlist_name):
        for i in self.playlists:
            if i.name.lower() == playlist_name.lower():
                return i
        return None

        
    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        # print(self.playlist_exists(playlist_name))
        if not self.playlist_exists(playlist_name):
            playlist = Playlist(playlist_name)
            self.playlists.append(playlist)
            print("Successfully created new playlist: "+playlist_name)
        else:
            print("Cannot create playlist: A playlist with the same name already exists")
        # print(self.playlists)
        
    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        video = self._video_library.get_video(video_id)
        if not self.playlist_exists(playlist_name):
            print("Cannot add video to " + playlist_name + ": Playlist does not exist")
            return
        
        if video == None:
            print("Cannot add video to " + playlist_name + ": Video does not exist")
            return
        if video.flag != None:
            print("Cannot add video to " + playlist_name + ": Video is currently flagged (reason: " + video.flag + ")")
            return


        playlist = self.search_playlists(playlist_name)
        if video in playlist.videos:
            print("Cannot add video to " + playlist_name + ": Video already added")
            return
        playlist.add_video(video)
        print("Added video to " + playlist_name +": "+video.title)

    def show_all_playlists(self):
        """Display all playlists."""
        if len(self.playlists) == 0:
            print("No playlists exist yet")
        else:
            print("Showing all playlists:")
            playlists = [i.name for i in self.playlists]
            playlists.sort()

            for x in playlists:
                print("  "+x)

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist = self.search_playlists(playlist_name)
        if playlist == None:
            print("Cannot show playlist " + playlist_name + ": Playlist does not exist")
            return
        print("Showing playlist: "+playlist_name)

        if len(playlist.videos) == 0:
            print("  No videos here yet")
            return
        for video in playlist.videos:
            if video.flag != None:
                print("  "+video.title + " (" + video.video_id +") ["+ " ".join(video.tags) + "] - FLAGGED (reason: " + video.flag + ")")
                continue

            print("  " + video.title + " (" + video.video_id +") ["+ " ".join(video.tags) + "]")



    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        playlist = self.search_playlists(playlist_name)
        video = self._video_library.get_video(video_id)
        if video == None:
            print("Cannot remove video from " + playlist_name + ": Video does not exist")
            return
        if playlist == None:
            print("Cannot remove video from " + playlist_name + ": Playlist does not exist")
            return
        if video not in playlist.videos:
            print("Cannot remove video from " + playlist_name + ": Video is not in playlist")
            return
        print("Removed video from " + playlist_name + ": "+video.title)
        playlist.videos.remove(video)

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist = self.search_playlists(playlist_name)
        if playlist == None:
            print("Cannot clear playlist " + playlist_name + ": Playlist does not exist")
            return
        playlist.clear_videos()
        print("Successfully removed all videos from "+playlist_name)

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist = self.search_playlists(playlist_name)
        if playlist == None:
            print("Cannot delete playlist " + playlist_name + ": Playlist does not exist")
            return
        self.playlists.remove(playlist)
        print("Deleted playlist: "+playlist_name)

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        videos = self._video_library.get_all_videos()
        matching_videos = []
        for i in range(len(videos)):
            video = videos[i]
            if video.title.lower().find(search_term.lower()) != -1 and video.flag == None:
                matching_videos.append(video)
        
        if len(matching_videos) == 0:
            print("No search results for " + search_term)
            return

        results = []
        for x in range(len(matching_videos)):
            video = matching_videos[x]
            results.append(video.title + " (" + video.video_id +") ["+ " ".join(video.tags) + "]")

        print("Here are the results for " + search_term +":")

        results.sort()
        for y in range(len(results)):
            print("  " + str(y+1) + ") " + results[y] )
        print("Would you like to play any of the above? If yes, specify the number of the video.")
        print("If your answer is not a valid number, we will assume it's a no.")
        command = input()
        if command.isnumeric():
            if int(command) in range(1, len(matching_videos)+1):
                self.play_video(matching_videos[int(command)-1].video_id)
     
    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        videos = self._video_library.get_all_videos()
        matching_videos = []
        for i in range(len(videos)):
            video = videos[i]
            if video_tag.lower() in [tag.lower() for tag in video.tags] and video.flag == None:
                matching_videos.append(video)
        
        if len(matching_videos) == 0:
            print("No search results for " + video_tag)
            return

        results = []
        for x in range(len(matching_videos)):
            video = matching_videos[x]
            results.append(video.title + " (" + video.video_id +") ["+ " ".join(video.tags) + "]")

        print("Here are the results for " + video_tag +":")

        results.sort()
        for y in range(len(results)):
            print("  " + str(y+1) + ") " + results[y] )
        print("Would you like to play any of the above? If yes, specify the number of the video.")
        print("If your answer is not a valid number, we will assume it's a no.")
        command = input()
        if command.isnumeric():
            if int(command) in range(1, len(matching_videos)+1):
                self.play_video(matching_videos[int(command)-1].video_id)

    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        video = self._video_library.get_video(video_id)
        if video == None:
            print("Cannot flag video: Video does not exist")
            return
        if video.flag != None:
            print("Cannot flag video: Video is already flagged")
            return
        if self.currentlyPlaying != None and self.currentlyPlaying == video:
            self.stop_video()

        if len(flag_reason) == 0:
            flag_reason = "Not supplied"
        video.set_flag(flag_reason)
        print("Successfully flagged video: " +  video.title + " (reason: " + flag_reason + ")")



    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        video = self._video_library.get_video(video_id)
        if video == None:
            print("Cannot remove flag from video: Video does not exist")
            return
        if video.flag == None:
            print("Cannot remove flag from video: Video is not flagged")
            return
        video.set_flag(None)
        print("Successfully removed flag from video: "+video.title)