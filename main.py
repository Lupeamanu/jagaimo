'''Main bot organization and other shenanigans'''

import os

# 3rd Party
from translate import JagaimoClient
jagaimo = JagaimoClient()

# Discord module
import discord
from discord import app_commands

# Read in Environment variables
from dotenv import load_dotenv
load_dotenv('c:\\Users\\lupea\\Documents\\Lupeamanu\\Env\\.env')


intents = discord.Intents.default()
intents.message_content = True

# Initialize bot with our above intents
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@client.event
async def on_ready():
    cmds = await tree.sync()
    print(f'Synced {len(cmds)} commands')
    print('Ready!')


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
    
    await interaction.response.defer()
    suggestion = jagaimo.suggest(text=sentence, v=verbosity)
    await interaction.followup.send(suggestion)


token: str = os.getenv('JAGAIMO_DISCORD_TOKEN')
client.run(token=token)
