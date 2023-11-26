"""
Description 
Auteur : Felix Lamarche
Inspiré de : https://builtin.com/software-engineering-perspectives/discord-bot-python

Date :2023-09-08
"""

# importe discord.py
import discord
import random
from discord.ext import commands
# IMPORT THE OS MODULE.
import os
import asyncio

# IMPORT LOAD_DOTENV FUNCTION FROM DOTENV MODULE.
from dotenv import load_dotenv

# Permet de lire le fichier .env
load_dotenv()

# Recupere le token du bot
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.members = True  # Enable the GUILD_MEMBERS intent
intents.message_content = True
# Crée une instance de la classe Client qui représente le bot
bot = commands.Bot(command_prefix='!', intents=intents)


# Permet de savoir quand le bot est a on et affiche le nombre de serveur auquel il est connecté
@bot.event
async def on_ready():
	# Variable pour compter le nombre de serveur 
	guild_count = 0
	for guild in bot.guilds:
		# PRINT THE SERVER'S ID AND NAME.
		print(f"- {guild.id} (name: {guild.name})")

		# INCREMENTS THE GUILD COUNTER.
		guild_count = guild_count + 1
	# Permet de créer les channels de bienvenue et de role
	await creation_role(guild)
	await creation_channel(guild)
	
	print("AmishBot is in " + str(guild_count) + " guilds.")
    
# Messge de bienvenue quand un nouveau membre arrive sur le serveur
@bot.event
async def on_member_join(member):
    # Get the guild (server) where the member joined
	guild = member.guild
	message_explicatif = """
	Nous avons ajouté quelques fonctionnalités pratiques à notre bot pour faciliter la gestion des rôles dans notre serveur Discord. Voici comment les utiliser : \n
	1. **Création de rôle :
	**Pour créer un nouveau rôle, 
	utilisez la commande suivante : !creationRole [nom du rôle]
	Exemple : !creationRole MonRole\n
	2. **Ajout de rôle :
	**Pour s'ajouter un rôle,
	utilisez la commande suivante : !ajoutRole [nom du rôle]
	Exemple : !ajoutRole MonRole\n
	3. **Retrait de rôle :
	**Pour retirer un rôle,
	utilisez la commande suivante : !retirerRole [nom du rôle]
	Exemple : !retirerRole MonRole\n
	4. **Suppression de rôle :
	**Pour supprimer un rôle,
	utilisez la commande suivante : !suppressionRole [nom du rôle]
	Exemple : !suppressionRole MonRole \n
	5. **Liste des rôles :
	**Pour afficher la liste des rôles,
	utilisez la commande suivante : !listeRole
	Exemple : !listeRole \n
	Vous pouvez aussi faire !aide si vous avez des questions
	"""
    # Pour trouver le channel de bienvenue
	channel_bienvenue = discord.utils.get(guild.text_channels, name='bienvenue')  
	if channel_bienvenue:
        # Send the welcome message in the specified channel
		welcome_message = f'Salut {member.mention}! Bienvenue sur le serveur discord!'+ message_explicatif
		await channel_bienvenue.send(welcome_message)
	await member.add_roles(discord.utils.get(guild.roles, name="Peuple"))
# EVENT LISTENER FOR WHEN A NEW MESSAGE IS SENT TO A CHANNEL.
@bot.event
async def on_reaction_add(reaction,member):
    ## Get info pour le channel de role
	
	roleCsGo = discord.utils.get(member.guild.roles, name="Counter-Strike")
	roletLeagueOfLegend = discord.utils.get(member.guild.roles, name="League of Legend")
	roleRocketleague = discord.utils.get(member.guild.roles, name="Rocket League")
	roleWow = discord.utils.get(member.guild.roles, name="World of Warcraft")
	roleTwitch = discord.utils.get(member.guild.roles, name="Twitch")
    
	if reaction.emoji == "🔫":
		await member.add_roles(roleCsGo)
	if reaction.emoji == "🧙‍♂️":
		await member.add_roles(roletLeagueOfLegend)
	if reaction.emoji == "⚽":
		await member.add_roles(roleRocketleague)
	if reaction.emoji == "🫣":
		await member.add_roles(roleWow)
	if reaction.emoji == "⚜️":
		await member.add_roles(roleTwitch)

@bot.event
async def on_reaction_remove(reaction,member):
	## Get info pour le channel de role

	
	roleCsGo = discord.utils.get(member.guild.roles, name="Counter-Strike")
	roletLeagueOfLegend = discord.utils.get(member.guild.roles, name="League of Legend")
	roleRocketleague = discord.utils.get(member.guild.roles, name="Rocket League")
	roleWow = discord.utils.get(member.guild.roles, name="World of Warcraft")
	roleTwitch = discord.utils.get(member.guild.roles, name="Twitch")

	if reaction.emoji == "🔫":
		await member.remove_roles(roleCsGo)
	if reaction.emoji == "🧙‍♂️":
		await member.remove_roles(roletLeagueOfLegend)
	if reaction.emoji == "⚽":
		await member.remove_roles(roleRocketleague)
	if reaction.emoji == "🫣":
		await member.remove_roles(roleWow)
	if reaction.emoji == "⚜️":
	   await member.remove_roles(roleTwitch)
# Permet de créer les channels de bienvenue et de role
async def creation_channel(guild : discord.Guild):

	await asyncio.sleep(1)
	## Trouvé dans la doc officiel https://discordpy.readthedocs.io/en/stable/api.html#discord.TextChannel.set_permissions
	overwrite = discord.PermissionOverwrite()
	## Permet de trouvé le role peuple qui est attribué a tout le monde qui entre dans le serveur
	rolePeuple = discord.utils.get(guild.roles, name="Peuple")
	overwrite = {
		rolePeuple: discord.PermissionOverwrite(read_messages=False, send_messages=False),
		guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False)
	}
	roleLol = discord.utils.get(guild.roles, name="League of Legend")
	roleCsGo = discord.utils.get(guild.roles, name="Counter-Strike")
	roleRocketLeague = discord.utils.get(guild.roles, name="Rocket League")
	roleWow = discord.utils.get(guild.roles, name="World of Warcraft")
	roleTwitch = discord.utils.get(guild.roles, name="Twitch")

	droitLol = permission_role(guild,roleLol)
	

	channel_bienvenue = discord.utils.get(guild.text_channels, name='bienvenue')
	
	if channel_bienvenue == None:
		channel_bienvenue =await guild.create_text_channel('bienvenue')
		# Bloque le fais de pouvoir écrire pour tout le monde
		await channel_bienvenue.set_permissions(rolePeuple, read_messages=True,send_messages=False)

	channelRole = discord.utils.get(guild.text_channels, name='assosiation-role')
	if channelRole == None:
		channelRole == await guild.create_text_channel('assosiation-role')
	else:
		channelRole = discord.utils.get(guild.text_channels, name='assosiation-role')
		await channelRole.purge(limit=100)
	
	channelAjoutRole = discord.utils.get(guild.text_channels, name='ajout-role')
	if channelAjoutRole == None:
		channelAjoutRole == await guild.create_text_channel('ajout-role')

	
	channelLol = discord.utils.get(guild.text_channels, name='league-of-legend')
	if channelLol == None:
		channelLol = await guild.create_text_channel('league-of-legend')
		await channelLol.set_permissions(rolePeuple, read_messages=False,send_messages=False)
		await channelLol.set_permissions(roleLol, read_messages=True,send_messages=True)


	channelCsGo = discord.utils.get(guild.text_channels, name='counter-strike')
	if channelCsGo == None:
		channelCsGo = await guild.create_text_channel('counter-strike')
		await channelCsGo.set_permissions(rolePeuple, read_messages=False,send_messages=False)
		await channelCsGo.set_permissions(roleCsGo, read_messages=True,send_messages=True)


	channelRocketLeague = discord.utils.get(guild.text_channels, name='rocket-league')
	if channelRocketLeague == None:
		channelRocketLeague = await guild.create_text_channel('rocket-league')
		await channelRocketLeague.set_permissions(rolePeuple, read_messages=False,send_messages=False)
		await channelRocketLeague.set_permissions(roleRocketLeague, read_messages=True,send_messages=True)


	channelWow = discord.utils.get(guild.text_channels, name='world-of-warcraft')
	if channelWow == None:
		channelWow = await guild.create_text_channel('world-of-warcraft')
		await channelWow.set_permissions(rolePeuple, read_messages=False,send_messages=False)
		await channelWow.set_permissions(roleWow, read_messages=True,send_messages=True)


	channelTwitch = discord.utils.get(guild.text_channels, name='twitch')
	if channelTwitch == None:
		channelTwitch = await guild.create_text_channel('twitch')
		await channelTwitch.set_permissions(rolePeuple, read_messages=False,send_messages=False)
		await channelTwitch.set_permissions(roleTwitch, read_messages=True,send_messages=True)

	
	## Permet de créer le message de role
	channelRole = discord.utils.get(guild.text_channels, name='assosiation-role')
	Text = "Réagissez avec l'emoji correspondant à votre jeu préféré pour avoir accès au channel de ce jeu \n Counter-Strike : 🔫 \n League of Legend : :man_mage: \n Rocket League : :soccer: \n World of Warcarft : :face_with_peeking_eye: \n Twitch : :fleur_de_lis:"
	ajoutRole = await channelRole.send(Text)
    # J'ai trouver les emoji sur le site https://emojipedia.org 
    # Permet de rajouter un réaction au message
	await ajoutRole.add_reaction("🔫")
	await ajoutRole.add_reaction("🧙‍♂️")
	await ajoutRole.add_reaction("⚽")
	await ajoutRole.add_reaction("🫣")
	await ajoutRole.add_reaction("⚜️")
	## Permet d'enlever le droit d'écrire au role peuple apres avor envoyer le message
	await channelRole.set_permissions(rolePeuple, read_messages=True,send_messages=False)
# Inspiré de https://stackoverflow.com/questions/48216914/how-to-add-and-create-roles-in-discord-py
async def creation_role(guild):
	await asyncio.sleep(1)

	premCsGo = discord.utils.get(guild.channels, name="counter-strike")
	if discord.utils.get(guild.roles, name="Counter-Strike") == None:
		await guild.create_role(name="Counter-Strike", color=discord.Color(0xffff00))
	if discord.utils.get(guild.roles, name="Peuple") == None:
		await guild.create_role(name="Peuple", color=discord.Color(0xa52a2a))
	if discord.utils.get(guild.roles, name="League of Legend") == None:
		await guild.create_role(name="League of Legend", color=discord.Color(0x1e90ff))

	if discord.utils.get(guild.roles, name="Rocket League") == None:
		await guild.create_role(name="Rocket League", color=discord.Color(0xff4500))

	if discord.utils.get(guild.roles, name="World of Warcraft") == None:
		await guild.create_role(name="World of Warcraft", color=discord.Color(0x7cfc00))

	if discord.utils.get(guild.roles, name="Twitch") == None:
		await guild.create_role(name="Twitch", color=discord.Color(0x9370db))

async def creation_role_channel_custom(member,guild,nomVoulu):
	## Permet de trouvé le role peuple qui est attribué a tout le monde qui entre dans le serveur
	rolePeuple = discord.utils.get(guild.roles, name="Peuple")
	roleVoulu = discord.utils.get(guild.roles, name=nomVoulu)
	if nomVoulu == "Peuple":
		return "Vous ne créer pas avoir le role peuple"
	if roleVoulu != None:
		return "Le role existe deja"
	
	tabCouleurs = [0xFFE4E1, 0x00FF7F, 0xD8BFD8, 0xDC143C, 0xFF4500, 0xDEB887, 0xADFF2F, 0x800000, 0x4682B4, 0x006400, 0x808080, 0xA0522D, 0xF08080, 0xC71585, 0xFFB6C1, 0x00CED1]
	nombreRandom = random.randint(0,15)
	couleur = tabCouleurs[nombreRandom]
	if discord.utils.get(guild.roles, name=nomVoulu) == None:
		roleVoulu = await guild.create_role(name=nomVoulu, color=discord.Color(couleur))
		await member.add_roles(roleVoulu)
	if discord.utils.get(guild.channels, name=nomVoulu) == None:
		channelVoulu = await guild.create_text_channel(nomVoulu)
		await channelVoulu.set_permissions(rolePeuple, read_messages=False,send_messages=False)
		await channelVoulu.set_permissions(roleVoulu, read_messages=True,send_messages=True)
 
async def supression_role_channel_custom(guild,nomVoulu):
	if nomVoulu == "Peuple":
		return "Vous ne pouvez pas supprimer le role peuple"
	if nomVoulu == "MonBoatCool":
		return "Vous ne pouvez pas supprimer le role MonBoatCool"
	roleVoulu = discord.utils.get(guild.roles, name=nomVoulu)
	nomVouluLower = nomVoulu.lower()
	channelVoulu = discord.utils.get(guild.channels, name=nomVouluLower)
	messageRetour = ""
	if roleVoulu != None:
		await roleVoulu.delete()
		messageRetour += "Le role " + nomVoulu + " a été supprimé"
	else:
		messageRetour += "Le role n'existe pas, alors il n'a pas été supprimé"

	if channelVoulu != None:
		await channelVoulu.delete()
		messageRetour += " Le channel pour le role " + nomVoulu + " a été supprimé"

	return messageRetour
async def ajout_role_channel_custom(member,guild,nomVoulu):
	if nomVoulu == "Peuple":
		return "Vous ne pouvez pas avoir le role peuple"
	if nomVoulu == "MonBoatCool":
		return "Vous ne pouvez pas avoir le role MonBoatCool"
	roleVoulu = discord.utils.get(guild.roles, name=nomVoulu)
	messageRetourAjout = ""
	if roleVoulu != None:
		await member.add_roles(roleVoulu)
		messageRetourAjout += "Vous avez été ajouté au role " + nomVoulu
	else:
		messageRetourAjout += "Le role n'existe pas, alors vous n'avez pas été ajouté"
	return messageRetourAjout	
async def retirer_role_channel_custom(member,guild,nomVoulu):
	if nomVoulu == "Peuple":
		return "Vous ne pouvez pas retirer le role peuple"
	if nomVoulu == "MonBoatCool":
		return "Vous ne pouvez pas retirer le role MonBoatCool"
	roleVoulu = discord.utils.get(guild.roles, name=nomVoulu)
	messageRetourAjout = ""
	if roleVoulu != None:
		await member.remove_roles(roleVoulu)
		messageRetourAjout += "Vous avez retiré du role " + nomVoulu
	else:
		messageRetourAjout += "Le role n'existe pas, alors vous n'avez pas été retiré"
	return messageRetourAjout
	



@bot.command()
async def creationRole(ctx,arg):
	member = ctx.message.author
	messageRetour = await creation_role_channel_custom(member,ctx.guild,arg)
	await ctx.send(messageRetour)

@bot.command()
async def ajoutRole(ctx,arg):
	member = ctx.message.author
	messageRetour = await ajout_role_channel_custom(member,ctx.guild,arg)
	await ctx.send(messageRetour)
@bot.command()
async def retirerRole(ctx,arg):
	member = ctx.message.author
	messageRetour = await retirer_role_channel_custom(member,ctx.guild,arg)
	await ctx.send(messageRetour)

@bot.command()
async def suppressionRole(ctx,arg):
	message = await supression_role_channel_custom(ctx.guild,arg)
	await ctx.send(message)
	
@bot.command()
async def aide(ctx):
	message_explicatif = """
	Nous avons ajouté quelques fonctionnalités pratiques à notre bot pour faciliter la gestion des rôles dans notre serveur Discord. Voici comment les utiliser : \n
	1. **Création de rôle :
	**Pour créer un nouveau rôle, 
	utilisez la commande suivante : !creationRole [nom du rôle]
	Exemple : !creationRole MonRole\n
	2. **Ajout de rôle :
	**Pour s'ajouter un rôle,
	utilisez la commande suivante : !ajoutRole [nom du rôle]
	Exemple : !ajoutRole MonRole\n
	3. **Retrait de rôle :
	**Pour retirer un rôle,
	utilisez la commande suivante : !retirerRole [nom du rôle]
	Exemple : !retirerRole MonRole\n
	4. **Suppression de rôle :
	**Pour supprimer un rôle,
	utilisez la commande suivante : !suppressionRole [nom du rôle]
	Exemple : !suppressionRole MonRole \n
	5. **Liste des rôles :
	**Pour afficher la liste des rôles,
	utilisez la commande suivante : !listeRole
	Exemple : !listeRole
	"""
	await ctx.send(message_explicatif)





@bot.command()
async def listeRole(ctx):
    roles = ctx.guild.roles[1:] # Exclu le @everyone role
    await ctx.send('\n'.join(r.name for r in roles))



@bot.command()
async def Test(ctx):
	roles = ctx.guild.roles
	print('\n'.join(r.name for r in roles))
	
@bot.command()
async def ping(ctx):
	await ctx.send('pong')

@bot.command()
async def foo(arg):
    await discord.utils.send(arg)

async def regarde_message(guild,arg):
	await guild.send(arg)
async def permission_role(guild,roleVoulu):
	rolePeuple = discord.utils.get(guild.roles, name="Peuple")
	overwrite = {
	rolePeuple: discord.PermissionOverwrite(read_messages=False, send_messages=False),
	guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False),
	roleVoulu: discord.PermissionOverwrite(read_messages=True, send_messages=True)
	}
# EXECUTES THE BOT WITH THE SPECIFIED TOKEN. TOKEN HAS BEEN REMOVED AND USED JUST AS AN EXAMPLE.


bot.run(DISCORD_TOKEN)