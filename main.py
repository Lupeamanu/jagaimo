'''Main bot organization and other shenanigans'''

import os
import logging

# Discord module
import discord
from discord import app_commands
# Read in Environment variables
from dotenv import load_dotenv

from translate import JagaimoClient

load_dotenv('c:\\Users\\lupea\\Documents\\Lupeamanu\\Env\\.env')

from deck import Deck


logger = logging.getLogger(__name__)
logging.basicConfig(filename="jagaimo.log", level=logging.INFO)

jagaimo = JagaimoClient()

intents = discord.Intents.default()
intents.message_content = True

# Initialize bot with our above intents
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# Global variable to control the listening state
listening: bool = False


@tree.command(name="start_reading", description="Start listening")
async def start_reading_manga(interaction) -> None:
    """Starts listening to the chat.
    
    This function sets the global variable 'listening' to True and sends a message to the chat indicating that it is now reading the chat.
    
    Args:
        interaction (object): The interaction object that triggered the bot to start listening.
    
    Raises:
        Exception: An error occurred while sending the message.
    
    Returns:
        None
    """
    
    global listening
    listening = True
    await interaction.response.send_message("I am now reading the chat.")


@tree.command(name="stop_reading", description="Stop listening")
async def stop_reading_manga(interaction) -> None:
    """This function is used to stop reading the manga. It sets the global variable 'listening' to False and sends a message 'I am no longer reading the chat.'.
    
    Args:
        interaction (object): An object that represents the interaction.
    
    Returns:
        None
    """
    
    global listening
    listening = False
    await interaction.response.send_message('I am no longer reading the chat.')


@tree.command(name="testembed", description="Test embed")
async def testembed(interaction):
    embed = discord.Embed(
        title="Sample Embed",
        description="This is an example of an embed.",
        color=discord.Color.blue()  # You can set a custom color
    )
    await interaction.response.send_message(embed=embed)


@tree.command(name="correct", description="Correct a sentence")
async def correct(interaction, sentence: str, verbosity: int):
    """This function corrects a given sentence based on the interaction and verbosity level.
    
    Args:
        interaction (Interaction): The interaction object that is used to defer the response and send the followup.
        sentence (str): The sentence that needs to be corrected.
        verbosity (int): The verbosity level that determines the amount of information to be included in the suggestion.
    
    Coroutine function:
        This function is a coroutine, i.e., it is designed to be used with Python's asyncio library. The function should be called using the 'await' keyword in an asyncio environment.
    
    Raises:
        TypeError: If the input types of the parameters are not as expected.
        ValueError: If the input values of the parameters are not as expected.
    
    Returns:
        None: This function does not return a value. It sends a suggestion as a followup to the interaction.
    """

    logger.info(f"\tCorrecting sentence: {sentence}")

    await interaction.response.defer()
    suggestion = jagaimo.suggest(text=sentence, v=verbosity)
    await interaction.followup.send(suggestion)


def _correct(sentence: str):
    """This function corrects a given sentence using the jagaimo suggest method.
    
    Args:
        sentence (str): The sentence that needs to be corrected.
    
    Returns:
        suggestion: The corrected sentence suggested by the jagaimo method.
    """
    
    suggestion = jagaimo.suggest(text=sentence, v=2)
    return suggestion


@client.event
async def on_message(message) -> None:
    """This function handles the messages received by the bot. It checks if the message is from the bot itself and ignores it. 
    It also handles the toggling of the bot's listening state with the "-start" and "-stop" commands. 
    The "-sync" command is used to sync the bot's commands for the guild. 
    If the bot is in listening mode, it processes the messages received.
    
    Args:
        message (discord.Message): The message received by the bot.
    
    Raises:
        discord.DiscordException: If there is an error while sending a message.
    
    Returns:
        None
    """
    
    global listening

    # Prevent the bot from responding to it's own messages
    if message.author == client.user:
        return

    guild_id = message.guild.id

    match message.content:
        case "-start":
            listening = True
            await message.channel.send('I am reading the chat.')
        case "-stop":
            listening = False
            await message.channel.send('I am no longer reading the chat.')
        case "-sync":
            await message.channel.send(f"Syncing commands for guild: {guild_id}")
            cmds = await tree.sync(guild=client.get_guild(guild_id))
            await message.channel.send(f"Synced {len(cmds)} commands for guild: {client.get_guild(guild_id)}")
            commands = [command.name for command in tree.get_commands()]
            await message.channel.send(f"Current bot commands: {', '.join(commands)}")

    # Handle toggling of listening
    # if message.content == "-start":
    #     listening = True
    #     await message.channel.send('I am reading the chat.')

    # if message.content == "-stop":
    #     listening = False
    #     await message.channel.send('I am no longer reading the chat.')

    # if message.content == "-sync":
    #     await message.channel.send(f"Syncing commands for guild: {guild_id}")
    #     cmds = await tree.sync(guild=client.get_guild(guild_id))
    #     await message.channel.send(f"Synced {len(cmds)} commands for guild: {client.get_guild(guild_id)}")
    #     commands = [command.name for command in tree.get_commands()]
    #     await message.channel.send(f"Current bot commands: {', '.join(commands)}")

    # If listening is enabled, process the messages
    valid_channel: bool = listening and guild_id == 1297990572883312740 and message.content not in ["-start", "-stop"]
    if valid_channel:
        await message.channel.send(_correct(sentence=message.content))


token: str = os.getenv('JAGAIMO_DISCORD_TOKEN')
client.run(token=token)
