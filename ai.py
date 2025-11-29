import discord
from discord.ext import commands

class aicog(commands.Cog):
    def __init__(self, client, gemmy, MODEL):
        self.client = client
        self.gemmy = gemmy
        self.model_name = MODEL

    @commands.command()
    async def ask(self, ctx, *, prompt: str):
        modified_prompt = (
                f"Repond concisely, using a maximum of 500 tokens. User question: {prompt}"
                )

        async with ctx.typing():
            try:
                response = self.gemmy.models.generate_content(
                        model=self.model_name,
                        contents=modified_prompt,
                )

                await ctx.reply(response.text)

            except Exception as e:
                print(f"Error iwth Gemini API: {e}")
                await ctx.reply("i no not")


