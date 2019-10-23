import discord
from discord.ext import commands
from random import randint
from discord.utils import get

import asyncio
import json
import os
import random
import re
import yaml


token = os.environ.get("api_key")
bot = commands.Bot(command_prefix = '!')
bot.remove_command("help")
client = discord.Client()

minesweeper_emojis = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

#Variables messages reactions
messages_reactions = json.load(open("src/messages_reactions.json", "r", encoding = "utf-8"))
messages_taverne = json.load(open("src/messages_taverne.json", "r", encoding = "utf-8"))


#Variables pour le morpion
grille = [ ["◻", "◻", "◻"],
           ["◻", "◻", "◻"],
           ["◻", "◻", "◻"]
         ]
_grille =  ""

_grille += "{}{}{}\n".format(grille[0][0], grille[0][1], grille[0][2])

_grille += "{}{}{}\n".format(grille[1][0], grille[1][1], grille[1][2])

_grille += "{}{}{}\n".format(grille[2][0], grille[2][1], grille[2][2])
mcour = 0
jrond =""
jcroix = ""
msgtour =""
tour = 0
pnulle = 0
pfp = ""
nj = ""


#--------------------------------------------------Lanceur---------------------------------------------------------------

@bot.event
async def on_ready():
    print("Bot is ready")
    jeu = random.choice([line.strip() for line in open("src/games.txt", "r", encoding = "utf-8").readlines()])
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(jeu))
    await asyncio.sleep(10800)

client.loop.create_task(on_ready())


#--------------------------------------------------AUTRES---------------------------------------------------------------

#Commande HELP
@bot.command()
async def help(ctx):
 spr = ctx.message
 await spr.delete()
 if ctx.message.channel.id == 562394254811463707:

    embed = discord.Embed(
            title = 'René',
            colour = discord.Colour.red()
        )

    embed.add_field(name=':keyboard: Commandes par salon : ', value="\u200b", inline=False)
    embed.add_field(name='🤔-gold-hawk  : ', value="``!utip`` : vous débloque le rôle utip + un channel dédié\n``!ghpts`` : donne le nombre de points que a GH \n``!addpt nbrpts raison`` : ajoute un nombre de point à GH avec la raison\u200b", inline=False)
    embed.add_field(name='#📳-partages : ', value="``!apub`` : permet de vous débloquer le channel pour faire votre pub\n``!rpub`` : permet de vous retirer le rôle/accés au channel une fois votre pub validée ou non.\n\u200b", inline=False)
    embed.add_field(name='#🎲-mini-Jeux : ', value="Si c'est votre première partie de morpion faite ``!reglemorpion`` pour savoir comment y jouer et connaitre l'utilisation de ``!place``.\n``!demineur nombreHauteur nombreLargeur nombreBombes``\n``!duel @pseudo``\n``!morpion @pseudo``(``!reglemorpion`` / ``!place`` / ``!annuler``)\n\u200b", inline=False)
    embed.add_field(name='#🤖-bot  : ', value="``!help``\n``!bug +msg`` : pour reporter un bug\n\u200b", inline=False)
    embed.add_field(name='#🍺-taverne : ', value="Besoin de vous détendre après une longue journée et de discuter de tout et de rien, c'est par ici ! Vous pouvez aussi lui commander des boissons avec la carte.\n\u200b", inline=False)
    embed.add_field(name='#😄-yes : ', value="Il réagira à votre bonne humeur 😄\n``!mariage``\n``!blague``\n\u200b", inline=False)
    embed.add_field(name='#😡-grr : ', value="Il réagira à votre mécontentement 😡\n\u200b", inline=False)
    embed.add_field(name='#💻-programmation  : ', value="``!code``\n\u200b", inline=False)
    embed.set_footer(text = 'Bot by Eowalim v2.2')
    embed.set_thumbnail(url= 'https://cdn.discordapp.com/attachments/586591903085101069/586930271870517278/def8d03172251e7.png')
    await ctx.send(embed=embed)
 else:
     spr2 = await ctx.send(f"{ctx.message.author.mention} la commande ``!help`` n'est autorisée que dans le channel #🤖-bot")
     await asyncio.sleep(30)
     await spr2.delete()



#Commande CODE
@bot.command()
async def code(ctx):
    spr = ctx.message
    await spr.delete()
    if ctx.message.channel.id == 562396361236938781:
        await ctx.send("Voici le code du BOT : https://github.com/Eowalim/BOTRene et merci à QUATRE de m'avoir aidé 🎇 !")
    else:
        spr2 = await ctx.send(f"{ctx.message.author.mention} la commande ``!code`` n'est autorisée que dans le channel #💻-programmation")
        await asyncio.sleep(30)
        await spr2.delete()



#Commande BLAGUE
@bot.command()
async def blague(ctx):
    spr = ctx.message
    await spr.delete()
    if ctx.message.channel.id == 562392613932630076:
        jokes = open("src/jokes.txt", "r", encoding = "utf-8").read().split("\n---\n")
        bl = await ctx.send(random.choice(jokes))
        await asyncio.sleep(20)
        await bl.delete()
    else:
        spr2 = await ctx.send(f"{ctx.message.author.mention} la commande ``!blague`` n'est autorisée que dans le channel #😄-yes")
        await asyncio.sleep(30)
        await spr2.delete()


async def bug(ctx, *, txt):
    if ctx.message.channel.id == 562394254811463707:
        spr = ctx.message
        spr2 = await ctx.send(f"{ctx.message.author.mention} ton message a bien été envoyé.")
        user = await bot.fetch_user(178910891897520128)
        await user.send(f"**{ctx.message.author.display_name}** : {txt}")
        await asyncio.sleep(10)
        await spr.delete()
        await spr2.delete()
    else:
        spr2 = await ctx.send(f"{ctx.message.author.mention} la commande ``!bug`` n'est autorisée que dans le channel #🤖-bot")
        await asyncio.sleep(30)
        await spr2.delete()



#Commande MARIAGE
@bot.command(pass_context = True)
async def mariage(ctx):
    spr = ctx.message
    await spr.delete()
    if ctx.message.channel.id == 562392613932630076:
        role = [role for role in ctx.message.guild.roles if role.name == "Random"][0]
        eligibleMembers = [member for member in ctx.message.guild.members if role in member.roles]
        random.shuffle(eligibleMembers)
        await ctx.send(f"💍 René a décidé d'unir à vie **{eligibleMembers[0].mention}** et **{eligibleMembers[1].mention}**")
    else:
       spr2 = await ctx.send(f"{ctx.message.author.mention} la commande ``!mariage`` n'est autorisée que dans le channel #😄-yes")
       await asyncio.sleep(30)
       await spr2.delete()


@bot.command()
@commands.cooldown(3, 300, commands.BucketType.channel)
async def addpts(ctx,pts,*,txt):
    spr = ctx.message
    await spr.delete()
    if ctx.message.channel.id == 562393748575879178:
        if int(pts)>100:
             spr2 = await ctx.send(f"{ctx.message.author.mention} le nombre maximum de points que tu peux donner est de 100 !")
             await asyncio.sleep(30)
             await spr2.delete()
        else :
            with open('src/GH.yaml') as f:
                point = yaml.safe_load(f)
                point['points'] = point['points'] + int(pts)
            with open('src/GH.yaml', 'w') as f:
              yaml.dump(point, f)
            if int(pts) == 1:
             await ctx.send(f"{ctx.message.author.mention} a donné **{int(pts)}** point à GoldHawk. Raison : **{txt}** \nGoldHawk a actuellement **{point['points']}** points.")
            else :
             await ctx.send(f"{ctx.message.author.mention} a donné **{int(pts)}** points à GoldHawk. Raison : **{txt}** \nGoldHawk a actuellement **{point['points']}** points.")

    else:
        spr2 = await ctx.send(f"{ctx.message.author.mention} la commande ``!addpt nbrpts raison`` n'est autorisée que dans le channel 🤔-gold-hawk")
        await asyncio.sleep(30)
        await spr2.delete()

@bot.command()
@commands.cooldown(3, 300, commands.BucketType.channel)
async def ghpts(ctx):
    spr = ctx.message
    await spr.delete()
    if ctx.message.channel.id == 562393748575879178:
        with open('src/GH.yaml') as f:
            nbpts= yaml.safe_load(f)
        await ctx.send(f"GoldHawk a actuellement **{nbpts['points']}** points")

    else:
        spr2 = await ctx.send(f"{ctx.message.author.mention} la commande ``!ghpts`` n'est autorisée que dans le channel 🤔-gold-hawk")
        await asyncio.sleep(30)
        await spr2.delete()


#Commande Utip
@bot.command()
async def utip(ctx):
    spr = ctx.message
    await spr.delete()
    if ctx.message.channel.id == 562393748575879178:
        channel = bot.get_channel(594123913844490260)
        await ctx.message.author.add_roles([role for role in ctx.message.guild.roles if role.name == "UTIP"][0])
        await channel.send(f"{ctx.message.author.mention} merci de contribuer !")
    else:
       spr2 = await ctx.send(f"{ctx.message.author.mention} la commande ``!utip`` n'est autorisée que dans le channel 🤔-gold-hawk")
       await asyncio.sleep(30)
       await spr2.delete()


#Commande RPUB
@bot.command(pass_context=True)
async def rpub(ctx):
    spr = ctx.message
    await spr.delete()
    if ctx.message.channel.id == 562394093402062868:
        await ctx.message.author.remove_roles([role for role in ctx.message.guild.roles if role.name == "PUB"][0])
    else:
       spr2 = await ctx.send(f"{ctx.message.author.mention} pour te retirer le rôle il te faut déja le rôle.")
       await asyncio.sleep(30)
       await spr2.delete()


#Commande DEMINEUR
@bot.command(pass_context = True)
async def demineur(ctx, height : int = 12, width : int = 12, bombs : int = 30):
    spr = ctx.message
    await spr.delete()
    if ctx.message.channel.id == 587368912090431560:
        if mcour == 1:
                    m = await ctx.send(f"{ctx.message.author.mention} un morpion est en cours. Pour éviter de flooder et réduire la visibilité de la partie, cette commande est désactivée pour la durée du jeu. Merci 🙂.")
                    await asyncio.sleep(5)
                    await m.delete()
        else:
            if any(not 1 < a < 41 for a in (width, height)) or bombs < 1:
                await ctx.send("Erreur : les dimensions de la grille doivent être comprises entre 2 et 40 inclus, et elle doit contenir au moins 1 bombe.")
                return
            if width * height > 175:
                await ctx.send(f"Erreur : à cause de la limite de 2000 caractères, une grille ne peut contenir que maximum 175 cases ! ({width} * {height} = {width * height})")
                return
            if bombs > width * height - 1:
                await ctx.send("Erreur : la grille doit contenir au moins un espace libre !")
                return

            board = [True] * bombs + [False] * (width * height - bombs)
            random.shuffle(board)
            board = [board[x:x + width] for x in range(0, len(board), width)]

            output = ""
            for i, line in enumerate(board):
                for j, square in enumerate(line):
                    if square:
                        output += "||:bomb:||"
                    else:
                        sum = 0
                        for k in range(max(i - 1, 0), min(i + 2, len(board))):
                            for l in range(max(j - 1, 0), min(j + 2, len(line))):
                                sum += 1 if board[k][l] else 0
                        output += f"||:{minesweeper_emojis[sum]}:||"
                    output += " " if j < len(line) - 1 else ""
                output += "\n"

            await ctx.send(f"Dimensions : {width}x{height} ; Bombes : {bombs}")
            await ctx.send(output)
    else:
           spr2 = await ctx.send(f"{ctx.message.author.mention} la commande ``demineur`` n'est autorisée que dans le channel #🎲-minis-jeux")
           await asyncio.sleep(30)
           await spr2.delete()


#Commande REGLEMORPION
@bot.command()
async def reglemorpion(ctx):
    spr = ctx.message
    await spr.delete()
    if ctx.message.channel.id == 587368912090431560:
        spr2 = await ctx.send(f"{ctx.message.author.mention} Le but est d'aligner ton symbole, soit la ❌ ou le ⭕ sur toute une ligne, colonne ou diagonale.\nPour placer un pion il te suffit de faire :  ``!place ligne colonne``  avec pour ligne et colonne un chiffre compris entre 0 et 2.\nDe plus, même si vous voyez que la partie est nulle, veuillez remplir toute la grille.")
        await spr.delete()
    else:
       spr2 = await ctx.send(f"{ctx.message.author.mention} la commande ``!reglemorpion`` n'est autorisée que dans le channel #🎲-minis-jeux")
       await asyncio.sleep(30)
       await spr2.delete()


#Commande MORPION
@bot.command()
async def morpion(ctx, pseudo):
        spr = ctx.message
        await spr.delete()
        if ctx.message.channel.id == 587368912090431560:
            global grille, _grille,msg,jrond,jcroix,msgtour,mcour,tour

            us = pseudo
            us = us.replace("<","")
            us = us.replace(">","")
            us = us.replace("@","")
            us = us.replace("!","")
            user = await bot.fetch_user(us)
            if mcour == 0:
                if user == ctx.message.author:
                    await ctx.send(f"{ctx.message.author.mention} Tu ne peux pas jouer avec toi-même.")
                elif user == bot.user:
                    await ctx.send(f"{ctx.message.author.mention} Tu ne peux pas jouer contre René car il est imbattable à ce jeu.")
                else:
                    await ctx.send(f"Une partie de morpion commence entre {ctx.message.author.mention} (❌) et {user.mention} (⭕). Je vous rappelle que si vous voyez que la partie est nulle veuillez quand même remplir toute la grille :)")
                    msg = await ctx.send(_grille)
                    mcour = 1
                    jcroix = ctx.message.author
                    jrond = user
                    msgtour = await ctx.send(f"Au tour de {jcroix.mention} de jouer.")
                    tour = 1
            else:
                    await ctx.send(f"{ctx.message.author.mention} Une partie est déjà en cours. Merci de d'attendre que celle-ci se termine pour pouvoir jouer.")
        else:
              spr2 = await ctx.send(f"{ctx.message.author.mention} la commande ``!reglemorpion`` n'est autorisée que dans le channel #🎲-minis-jeux")
              await asyncio.sleep(30)
              await spr2.delete()


#Commande PLACE
@bot.command()
async def place(ctx, ligne, col):
    spr = ctx.message
    await spr.delete()
    if ctx.message.channel.id == 587368912090431560:
               global msg, grille, _grille,msgtour,tour,mcour,jrond,jcroix,pnulle

               if mcour == 1:
                    if tour == 1:
                        if ctx.message.author == jcroix:
                            if (int(ligne) < 0 or int(ligne) > 2) or (int(col) < 0 or int(col) > 2):
                                await msgtour.edit(content=f"{jcroix.mention} entre un emplacement de pion correct.")
                            else:
                                if grille[int(ligne)][int(col)] == "❌" or grille[int(ligne)][int(col)] == "⭕":
                                    await msgtour.edit(content=f"{jcroix.mention} Un pion est deja placé sur cette case. Replaces-en un.")
                                else:
                                    grille[int(ligne)][int(col)] = "❌"
                                    _grille2 =""
                                    _grille2 += "{}{}{}\n".format(grille[0][0], grille[0][1], grille[0][2])
                                    _grille2 += "{}{}{}\n".format(grille[1][0], grille[1][1], grille[1][2])
                                    _grille2 += "{}{}{}\n".format(grille[2][0], grille[2][1], grille[2][2])
                                    tour = 2
                                    pnulle = pnulle + 1
                                    await msg.edit(content=_grille2)
                                    await msgtour.edit(content=f"Au tour de {jrond.mention} de jouer.")
                        else:
                            await ctx.send(f"{ctx.message.author.mention} Ce n'est pas à toi de jouer ou tu n'es pas dans une partie.")
                    elif tour == 2:
                        if ctx.message.author == jrond:
                            if (int(ligne) < 0 or int(ligne) > 2) or (int(col) < 0 or int(col) > 2):
                                await msgtour.edit(content=f"{jrond.mention} entre un emplacement de pion correct.")
                            else:
                                if grille[int(ligne)][int(col)] == "❌" or grille[int(ligne)][int(col)] == "⭕":
                                    await msgtour.edit(content=f"{jrond.mention} Un pion est deja placé sur cette case. Replaces-en un.")

                                else:
                                    grille[int(ligne)][int(col)] = "⭕"
                                    _grille2 =""
                                    _grille2 += "{}{}{}\n".format(grille[0][0], grille[0][1], grille[0][2])
                                    _grille2 += "{}{}{}\n".format(grille[1][0], grille[1][1], grille[1][2])
                                    _grille2 += "{}{}{}\n".format(grille[2][0], grille[2][1], grille[2][2])
                                    tour = 1
                                    pnulle = pnulle + 1
                                    await msg.edit(content=_grille2)
                                    await msgtour.edit(content=f"Au tour de {jcroix.mention} de jouer.")
                        else:
                            await ctx.send(f"{ctx.message.author.mention} Ce n'est pas à toi de jouer ou tu n'es pas dans une partie.")
               else:
                    await ctx.send(f"{ctx.message.author.mention} Tu ne peux pas placer car tu n'es pas dans une partie.")


               #Check horizontale et veticale :
               for i in range(3):
                 if (grille[i][0] == "⭕" and grille[i][1] == "⭕" and grille[i][2] == "⭕") or (grille[i][0] == "❌" and grille[i][1] == "❌" and grille[i][2] == "❌"):
                      if(grille[i][1] == "⭕" ):
                       await msgtour.edit(content=f"Partie terminée.🏆 {jrond.mention} gagne la partie.")
                      else:
                       await msgtour.edit(content=f"Partie terminée.🏆 {jcroix.mention} gagne la partie.")
                      win()

               #Check Verticale
               for i in range(3):
                 if (grille[0][i] == "⭕" and  grille[1][i] == "⭕" and  grille[2][i] == "⭕" ) or (grille[0][i] == "❌" and  grille[1][i] == "❌" and  grille[2][i] == "❌"):
                      if(grille[i][1] == "⭕" ):
                       await msgtour.edit(content=f"Partie terminée.🏆 {jrond.mention} gagne la partie.")
                      else:
                       await msgtour.edit(content=f"Partie terminée.🏆 {jcroix.mention} gagne la partie.")
                      win()



               #Check Diagonale
               if (grille[0][0] == "⭕" and  grille[1][1] == "⭕" and grille[2][2] == "⭕" ) or (grille[2][0] == "⭕" and grille[1][1] == "⭕" and grille[0][2] == "⭕" ):
                    await msgtour.edit(content=f"Partie terminée.🏆 {jrond.mention} gagne la partie.")
                    win()


               if (grille[0][0] == "❌" and  grille[1][1] == "❌" and grille[2][2] == "❌" ) or (grille[2][0] == "❌" and grille[1][1] == "❌" and grille[0][2] == "❌" ):
                    await msgtour.edit(content=f"Partie terminée.🏆 {jcroix.mention} gagne la partie.")
                    win()


               #partie nulle
               if (pnulle == 9):
                   await msgtour.edit(content=f"Partie terminée. Partie nulle, personne ne gagne.")
                   win()


    else:
              spr2 = await ctx.send(f"{ctx.message.author.mention} la commande ``!reglemorpion`` n'est autorisée que dans le channel #🎲-minis-jeux")
              await asyncio.sleep(30)
              await spr2.delete()


@bot.command()
async def annuler(ctx):
    spr = ctx.message
    await spr.delete()
    if ctx.message.channel.id == 587368912090431560:
        if ctx.message.author == jcroix:
            spr = await ctx.send(f"La partie entre {jcroix.mention} et {jrond.mention} a été annulée par {ctx.message.author.mention}")
            win()
            await asyncio.sleep(15)
            await spr.delete()
        elif ctx.message.author == jrond:
            spr = await ctx.send(f"La partie entre {jcroix.mention} et {jrond.mention} a été annulée par {ctx.message.author.mention}")
            win()
            await asyncio.sleep(15)
            await spr.delete()
        else:
            spr2 = await ctx.send(f"{ctx.message.author.mention} tu ne peux pas annuler une partie dont tu ne fais pas partie 😄")
            await asyncio.sleep(20)
            await spr2.delete()

    else:
        spr2 = await ctx.send(f"{ctx.message.author.mention} la commande ``!annuler`` n'est autorisée que dans le channel #🤖-bot")
        await asyncio.sleep(30)
        await spr2.delete()

def win():
    global msg, grille, _grille,msgtour,tour,mcour,jrond,jcroix,pnulle
    grille = [ ["◻", "◻", "◻"],
               ["◻", "◻", "◻"],
               ["◻", "◻", "◻"]
             ]
    _grille =  ""

    _grille += "{}{}{}\n".format(grille[0][0], grille[0][1], grille[0][2])

    _grille += "{}{}{}\n".format(grille[1][0], grille[1][1], grille[1][2])

    _grille += "{}{}{}\n".format(grille[2][0], grille[2][1], grille[2][2])
    mcour = 0
    jrond =""
    jcroix = ""
    msgtour =""
    tour = 0
    pnulle = 0

#Commande DUEL
@bot.command()
async def duel(ctx, pseudo):
        spr = ctx.message
        await spr.delete()
        if ctx.message.channel.id == 587368912090431560:
                if mcour == 1:
                    m = await ctx.send(f"{ctx.message.author.mention} un morpion est en cours. Pour éviter de flooder et réduire la visibilité de la partie, cette commande est désactivée pour la durée du jeu. Merci 🙂.")
                    await asyncio.sleep(8)
                    await m.delete()
                else:
                        us = pseudo
                        us = us.replace("<","")
                        us = us.replace(">","")
                        us = us.replace("@","")
                        us = us.replace("!","")
                        user =  await bot.fetch_user(us)

                        if user == ctx.message.author:
                            await ctx.send(f"{ctx.message.author.mention} Tu ne peux pas te battre avec toi-même.")
                        elif user == bot.user:
                            await ctx.send(f"{ctx.message.author.mention} Personne ne peut me battre.")
                        else:

                            defo = random.choice([line.strip() for line in open("src/def.txt", "r", encoding = "utf-8").readlines()])
                            atk = random.choice([line.strip() for line in open("src/atk.txt", "r", encoding = "utf-8").readlines()])

                            vj = 100
                            vr = 100

                            pfp = ctx.message.author.avatar_url
                            nj = ctx.message.author
                            pfpr = user.avatar_url

                            c1 = random.choice([line.strip() for line in open("src/cry.txt", "r", encoding = "utf-8").readlines()])
                            c2 = random.choice([line.strip() for line in open("src/cry.txt", "r", encoding = "utf-8").readlines()])

                            while c1 == c2:
                                c2 = random.choice([line.strip() for line in open("src/cry.txt", "r", encoding = "utf-8").readlines()])
                                await ctx.send("⚔️ **Duel Fight !** ")
                                await asyncio.sleep(1)
                                await ctx.send(f"**{c1}**")
                                await asyncio.sleep(1)
                                await ctx.send(f"**{c2}**")
                                await asyncio.sleep(1)

                                fight = randint(0,1)

                                if fight== 0:
                                    joueur = discord.Embed(
                                            title = f"{nj.display_name}",
                                            colour = discord.Colour.blue()
                                        )
                                    joueur.set_thumbnail(url= (pfp))
                                    joueur.add_field(name='Vie', value=f"{vj}/100", inline=False)
                                    randomj = discord.Embed(
                                                title = f"{user.display_name}",
                                                colour = discord.Colour.red()
                                            )
                                    randomj.set_thumbnail(url= (pfpr))
                                    randomj.add_field(name='Vie', value=f"{vr}/100", inline=False)
                                    fight = randint(0,1)
                                    vj = 0
                                    joueur.set_field_at(0, name='❤️ Vie :', value=f"```{vj}/100```", inline=False )
                                    joueur.add_field(name='📝 Résultat :', value=f"💀 {ctx.message.author.display_name} {defo} {user.display_name}", inline=False )
                                    joueur.colour = discord.Colour.red()
                                    vr = randint(1,100)
                                    randomj.set_field_at(0, name='❤️ Vie :', value=f"```{vr}/100```", inline=False )
                                    randomj.add_field(name='📝 Résultat :', value=f"🏆 {user.display_name} {atk} {ctx.message.author.display_name} ", inline=False )
                                    randomj.colour = discord.Colour.green()
                                    await ctx.send(embed=joueur)
                                    await ctx.send(embed=randomj)
                                    await ctx.send("\u200b\n\u200b")

                                elif fight== 1:
                                    joueur = discord.Embed(
                                            title = f"{nj.display_name}",
                                            colour = discord.Colour.blue()
                                            )
                                    joueur.set_thumbnail(url= (pfp))
                                    joueur.add_field(name='Vie', value=f"{vj}/100", inline=False)
                                    randomj = discord.Embed(
                                                title = f"{user.display_name}",
                                                colour = discord.Colour.red()
                                            )
                                    randomj.set_thumbnail(url= (pfpr))
                                    randomj.add_field(name='Vie', value=f"{vr}/100", inline=False)
                                    fight = randint(0,1)
                                    vj = randint(1,100)
                                    joueur.set_field_at(0, name='❤️ Vie :', value=f"```{vj}/100```", inline=False )
                                    joueur.add_field(name='📝 Résultat :', value=f"🏆 {ctx.message.author.display_name} {atk} {user.display_name} ", inline=False )
                                    joueur.colour = discord.Colour.green()
                                    vr = 0
                                    randomj.set_field_at(0, name='❤️ Vie :', value=f"```{vr}/100```", inline=False )
                                    randomj.add_field(name='📝 Résultat :', value=f"💀 {user.display_name} {defo} {ctx.message.author.display_name}", inline=False )
                                    randomj.colour = discord.Colour.red()

                                    await ctx.send(embed=joueur)
                                    await ctx.send(embed=randomj)
                                    await ctx.send("\u200b\n\u200b")

        else:
           spr2 = await ctx.send(f"{ctx.message.author.mention} la commande ``!duel`` n'est autorisée que dans le channel #🎲-minis-jeux")
           await asyncio.sleep(30)
           await spr2.delete()



async def react(ctx):
    for mr in messages_reactions:
        if re.compile("(?i)" + mr["trigger"]).search(ctx.content) is not None:
            if mr["possible_answers"]:
                await ctx.channel.send(random.choice(mr["possible_answers"]).format(ctx))
            for reaction in mr["reactions"]:
                await ctx.add_reaction(reaction)
            return True
    return False



async def reacttaverne(ctx):
    for mr in messages_taverne:
        if re.compile("(?i)" + mr["trigger"]).search(ctx.content) is not None:
            if mr["possible_answers"]:
                await ctx.channel.send(random.choice(mr["possible_answers"]).format(ctx))
            for reaction in mr["reactions"]:
                await ctx.add_reaction(reaction)
            return True
    return False


@bot.event
async def on_message(ctx):

    if ctx.author.bot:
        return

    has_reacted = False

    if f"{ctx.channel.id}" in ("632615552367591464", "632612046847868978"):

     has_reacted = await reacttaverne(ctx)
     if "carte" in ctx.content or "CARTE" in ctx.content or "Carte" in ctx.content :
        embed = discord.Embed(
                title = 'Carte',
                colour = 0xdfad44
            )

        embed.add_field(name='🥤 FalCola : ', value="- Original 1942\n- Original 1974\n- Habanero 1975\n- Double Sugar 1991\n- Diabetotron 1995 (95% de sucre en plus !)\n- Orange 2006\n- Orange 2009\n- Outrun'84 2017\n- Midnight 2045\n- Funchy 2052\n- Radiation Lemon 2064 (Gold Hawk's Favorite Taste!)\n\u200b", inline=False)
        embed.add_field(name='🍺 Bière : ', value="Bière\nDemi\nPinte\n\u200b", inline=False)
        embed.add_field(name='☕ Boissons chaudes : ', value="-Café\n-Chocolat chaud\n-Thé\n\u200b", inline=False)
        embed.add_field(name='🥪 Sandwich : ', value="-Kebab\n\u200b", inline=False)

        embed.set_thumbnail(url= 'https://cdn.discordapp.com/attachments/616642254852849681/616649582457389061/test.png')
        await ctx.channel.send(embed=embed)



    #  Les deux channels
    if f"{ctx.channel.id}" in ("562392613932630076", "562395596317524011"):
        has_reacted = await react(ctx)

    #  Juste le channel GRR
    if not has_reacted and ctx.channel.id == 562395596317524011:
        if ctx.author != bot.user:
            await ctx.add_reaction("😡")

    # Juste le channel YES
    if not has_reacted and ctx.channel.id == 562392613932630076:
        if ctx.author != bot.user:
            await ctx.add_reaction("😄")

    await bot.process_commands(ctx)

bot.run(token)
