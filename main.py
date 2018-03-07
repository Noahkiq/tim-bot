import discord


TIMS_ROLE = 303295839026020352
TIMS_GUILD = 223217962184736768
TIMS_CHANNEL = 332995131386888195


class TimChecks(discord.AutoShardedClient):
    def __init__(self):
        discord.AutoShardedClient.__init__(self)
        
        self.ready = False
                
    async def on_shard_ready(self, shard_id):
        print('Shard {} started up'.format(shard_id))
    
    async def on_ready(self):
        self.tims_guild = self.get_guild(TIMS_GUILD)
        self.tims_channel = self.tims_guild.get_channel(TIMS_CHANNEL)
        self.tims_role = discord.utils.get(self.tims_guild.roles, id=TIMS_ROLE)
    
        print('Oh HI there. *See what I did there?*')
        print('Logged in as {}'.format(self.user.name))
        self.ready = True
        
    async def on_member_update(self, before, after):
        if not self.ready:
            return
        if after.guild != self.tims_guild:
            return
        
        if self.tims_role in after.roles:            
            if before.status == discord.Status.online and after.status == discord.Status.offline:
                blacklist = [140564059417346049, 191365244948316160, 127373929600778240, 207788560953114625, 191365244948316160, 188477859420045312] # no. 1,4 are temp, listened already
                tims = []
                for m in self.tims_guild.members:
                    if m.id != after.id and m.id not in blacklist:
                        if self.tims_role in m.roles:
                            tims.append(m)
                
                onlines = [m.status != discord.Status.offline for m in tims]
                if all(onlines):
                    await self.tims_channel.send('someone\'s o**ff**line now')
            elif before.status == discord.Status.offline and after.status == discord.Status.online:
                if self.tims_guild.large:
                    await self.request_offline_members(self.tims_guild)
                
                blacklist = [140564059417346049, 191365244948316160, 127373929600778240, 207788560953114625, 191365244948316160, 188477859420045312] # no. 1,4 are temp, listened already
                tims = []
                for m in self.tims_guild.members:
                    if self.tims_role in m.roles and m.id not in blacklist:
                        tims.append(m)
                
                onlines = [m.status != discord.Status.offline for m in tims]
                if all(onlines):
                    await self.tims_channel.send('all the tims are online')
                
            print('Woah!')
        pass
        

if __name__ == '__main__':
    bot = TimChecks()
    bot.run(open('token.txt').read().split('\n')[0])
