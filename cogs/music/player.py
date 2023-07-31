import asyncio
import random
import time

from discord.errors import ClientException

from cogs.music.player_view import PlayerView
from cogs.music.source import YTDLSource


class MusicPlayer:
    """A class which is assigned to each guild using the bot for Music.
    This class implements a queue and loop, which allows for different guilds
    to listen to different playlists simultaneously.
    When the bot disconnects from the Voice, it's instance will be destroyed.
    """

    def __init__(self, interaction, music):
        self.interaction = interaction
        self.music = music

        self.queue = []
        self.next = asyncio.Event()

        self.np_msg = None
        self.volume = 0.1
        self.current_pointer = 0
        self.next_pointer = -1
        self.loop_queue = False
        self.loop_track = False

        self.timestamp = 0

        self.view = None
        self.workaround = 1

        interaction.client.loop.create_task(self.player_loop())

    async def player_loop(self):
        """Our main player loop."""

        await self.interaction.client.wait_until_ready()

        while not self.interaction.client.is_closed():
            self.next.clear()

            try:
                if not self.loop_track:
                    self.next_pointer += 1  # next song
                if self.next_pointer >= len(self.queue):
                    if self.loop_queue:
                        self.next_pointer = 0  # queue loop
                    else:
                        await self.next.wait()
                        self.next.clear()

                self.current_pointer = self.next_pointer
                source = self.queue[self.current_pointer]

            # used to be implemented with destroy, cleanup, it is in main f.
            except (IndexError, asyncio.TimeoutError):
                guild = self.interaction.guild
                try:
                    await guild.voice_client.disconnect()
                except AttributeError:
                    pass
                return

            try:
                while self.workaround:
                    if not isinstance(source, YTDLSource):
                        re_source = await YTDLSource.regather_stream(
                            source,
                            loop=self.interaction.client.loop,
                            timestamp=self.timestamp,
                        )
                        self.timestamp = 0  # Why
                    re_source.volume = self.volume

                    self.workaround = 0     # it simply skips this (one song)
                    self.interaction.guild.voice_client.play(re_source,
                        after=self.play_next_song
                    )
                    time.sleep(1)

            except (ClientException, AttributeError) as err:
                print(f"ClientException: {err}")
                return
            except AttributeError as err:
                print(f"AttributeError: {err}")
                return
            except Exception as err:
                print(f"Exception: {err}")
                msg = f"Error:\n```css\n[{err}]\n```"
                await self.interaction.channel.send(msg)
                return

            self.next.clear()
            self.view = PlayerView(self, re_source)
            await self.update_player_status_message()

            await self.next.wait()

    def play_next_song(self, error=None):
        if error:
            pass
        self.workaround = 1
        self.next.set()

    async def update_player_status_message(self):
        # if no np.msg, create new msg
        if not self.np_msg:
            self.np_msg = await self.interaction.channel.send(
                content=self.view.msg, view=self.view
            )

        # if np.msg is the last one, just update it
        elif self.np_msg.channel.last_message_id == self.np_msg.id:
            self.np_msg = await self.np_msg.edit(
                content=self.view.msg, view=self.view
            )

        # if np.msg is not the last one, remove old and create new one
        else:  
            await self.np_msg.delete()
            self.np_msg = await self.interaction.channel.send(
                content=self.view.msg, view=self.view
            )


    def shuffle(self):
        """Randomizes the position of tracks in queue."""

        if not self.queue:
            return

        shuffled_remains = self.queue[self.current_pointer + 1 :]
        random.shuffle(shuffled_remains)

        self.queue = (
            self.queue[: self.current_pointer + 1] + shuffled_remains
        )

    def toggle_loop_queue(self):
        """Loops the queue of tracks."""

        self.loop_queue = not self.loop_queue

    def toggle_loop_track(self):
        """Loops the currently playing track."""

        self.loop_track = not self.loop_track
