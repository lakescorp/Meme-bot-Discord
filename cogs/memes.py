import discord,os,requests,random,string
from bs4 import BeautifulSoup
from discord.ext import commands

class Memes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Diccionario con todas las urls de donde se toman los memes
        self.urls = {
        "topdia":"https://es.memedroid.com/memes/top/day",
        "topsemanal":'https://es.memedroid.com/memes/top/week',
        'topmensual':'https://es.memedroid.com/memes/top/month',
        'topsiempre':'https://es.memedroid.com/memes/top/ever',
        'aleatorio':'https://es.memedroid.com/memes/random',
        'ultimos':'https://es.memedroid.com/memes/latest'
        }
        print('Memes Cog Funcionando')

    ##### Funciones de apoyo ####
    
    ##
    #   filename_generator: Crea un nombre unico para el archivo
    #       que va a quedar descargado temporalmente
    #
    async def filename_generator(self):
        """
        Generate a unique file name for the song file to be named as
        """
        chars=list(string.ascii_letters+string.digits)
        name=''
        for i in range(random.randint(9,25)):
            name+=random.choice(chars)
        
        return name

    ##
    #   callSoup: Toma la web especificada 
    #
    def callSoup(self, link):
        r = requests.get(link)        
        return BeautifulSoup(r.content, 'html.parser')   

    ##
    #   getLastImageMeme: Toma la primera imagen que sea un meme
    #       de lña web especificada
    #
    async def getLastImageMeme(self,ctx,link):           
        soup = self.callSoup(link)
        rows = soup.select('img')
        for x in rows:
            conSRC = x.find_all(attrs={"src"})
            if not conSRC is None:
                if 'https:' in x['src']:
                    await self.downloadFile(ctx,x['src'],'.jpeg')
                    return

    ##
    #   getLastVideoMeme: Toma el primer video que sea un meme
    #       de la web especificada
    #
    async def getLastVideoMeme(self,ctx,link):
        soup = self.callSoup(link)
        rows = soup.select('source')
        for x in rows:
            conSRC = x.find_all(attrs={"src"})
            if not conSRC is None:
                if 'https:' in x['src'] and 'webm' in x['src']:
                    await self.downloadFile(ctx,x['src'],'.webm')
                    return

    ##
    #   downloadFile: descarga el video pedido y lo envia
    #       al servidor
    #
    async def downloadFile(self, ctx, file, type):
        fileresult = requests.get(file, stream = True)
        print('Url descargada')
        filename =  await self.filename_generator()
        filename+=type
        print('Nombre del archivo generado -> '+filename)
        with open(filename,"wb") as f:
            for chunk in fileresult.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    print('Archivo escrito')
        embed = discord.Embed(title="Aqui lo tienes")
        mesage = await ctx.send(embed=embed,file=discord.File(filename))
        await mesage.add_reaction('✅')
        await mesage.add_reaction('❌')
        os.remove(filename)  

    ##
    #   meme: comando que se llama cuando se quiere un  
    #       meme de una imagen al servidor
    #
    @commands.command(name='meme', brief='Envia un meme', description='Envia una imagen de un meme')
    async def meme(self, ctx, *, tipo = None):
        if tipo is None:  
            em = discord.Embed(title='Selecciona que categoría de meme quieres',description='1 - Dia\n2 - Semana\n3 - Mes\n4 - Siempre\n5 - Ultimos\n6 - aleatorio')
            await ctx.send(embed=em)
        elif tipo == 1 or tipo.lower() == 'dia':
            await self.getLastImageMeme(ctx,self.urls['topdia'])
        elif tipo == 2 or tipo.lower() == 'semana':
            await self.getLastImageMeme(ctx,self.urls['topsemanal'])
        elif tipo == 3 or tipo.lower() == 'mes':
            await self.getLastImageMeme(ctx,self.urls['topmensual'])
        elif tipo == 4 or tipo.lower() == 'siempre':
            await self.getLastImageMeme(ctx,self.urls['topsiempre'])
        elif tipo == 5 or tipo.lower() == 'ultimos':
            await self.getLastImageMeme(ctx,self.urls['ultimos'])
        elif tipo == 6 or tipo.lower() == 'aleatorio':
            await self.getLastImageMeme(ctx,self.urls['aleatorio'])
        else:
            em = discord.Embed(title='Entrada no válida')
            await ctx.send(embed=em)

    ##
    #   memeVideo: comando que se llama cuando se quiere un  
    #       meme de un video al servidor
    #
    @commands.command(name='memeVideo', brief='Envia un meme', description='Envia un video de un meme')
    async def memeVideo(self, ctx, *, tipo = None):
        if tipo is None:    
            em = discord.Embed(title='Selecciona que categoría de meme quieres',description='1 - Dia\n2 - Semana\n3 - Mes\n4 - Siempre\n5 - Ultimos\n6 - aleatorio')
            await ctx.send(embed=em)
        elif tipo == 1 or tipo.lower() == 'dia':
            await self.getLastVideoMeme(ctx,self.urls['topdia'])
        elif tipo == 2 or tipo.lower() == 'semana':
            await self.getLastVideoMeme(ctx,self.urls['topsemanal'])
        elif tipo == 3 or tipo.lower() == 'mes':
            await self.getLastVideoMeme(ctx,self.urls['topmensual'])
        elif tipo == 4 or tipo.lower() == 'siempre':
            await self.getLastVideoMeme(ctx,self.urls['topsiempre'])
        elif tipo == 5 or tipo.lower() == 'ultimos':
            await self.getLastVideoMeme(ctx,self.urls['ultimos'])
        elif tipo == 6 or tipo.lower() == 'aleatorio':
            await self.getLastVideoMeme(ctx,self.urls['aleatorio'])
        else:
            em = discord.Embed(title='Entrada no válida')
            await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Memes(bot))