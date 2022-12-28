import discord
import aiosqlite
import stripe
import yaml
import paypalrestsdk
from discord import app_commands
from discord.ext import commands
from paypalrestsdk import Invoice

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

guild_id = data["General"]["GUILD_ID"]

paypal_client_id = data["PayPal"]["PAYPAL_CLIENT_ID"]
paypal_client_secret = data["PayPal"]["PAYPAL_CLIENT_SECRET"]
stripe_api_key = data["Stripe"]["STRIPE_API_KEY"]
fees_percent = data["General"]["FEES"]
x = fees_percent.replace("%", "")
y = int(x)
fee_amount = y * 0.01

my_api = paypalrestsdk.Api({
  'mode': 'live',
  'client_id': paypal_client_id,
  'client_secret': paypal_client_secret})

stripe.api_key = stripe_api_key

class RefreshButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(emoji='🔃', label='Refresh', style=discord.ButtonStyle.grey, custom_id='refresh:1', row=1)
    async def refresh(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(thinking=False, ephemeral=True)
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * from invoices WHERE message_id=?', (interaction.message.id, ))
        a = await cursor.fetchone()
        if a[0] == "PayPal":
            payment = paypalrestsdk.Invoice.find(f"{a[3]}", api=my_api)
            x = payment['status']
            if x == "UNPAID":
                await interaction.followup.send("The current invoice is marked as unpaid.", ephemeral=True)
            if x == "PAID":
                payment_message = interaction.channel.get_partial_message(a[2])
                await db.execute('DELETE FROM invoices WHERE message_id=?', (interaction.message.id, ))
                embed = discord.Embed(
                    title="Checkout",
                    description=
                    f"```STATUS: PAID \nSubtotal: ${a[4]:.2f} \nFees: ${a[5]:.2f} \nTotal: ${a[6]:.2f}```",
                    color=discord.Color.orange())
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1032078238706577458/1034883707875639317/1.png")
                await payment_message.edit(embed=embed)
                await interaction.delete_original_response()
        if a[0] == "Stripe":
            invoice = stripe.Invoice.retrieve(
                f'{a[3]}',
            )
            status = invoice['paid']
            if status == False:
                await interaction.followup.send("The current invoice is marked as unpaid.", ephemeral=True)
            if status == True:
                await db.execute('DELETE FROM invoices WHERE message_id=?', (interaction.message.id, ))
                payment_message = interaction.channel.get_partial_message(a[2])
                embed = discord.Embed(
                    title="Checkout",
                    description=
                    f"```STATUS: PAID \nSubtotal: ${a[4]:.2f} \nFees: ${a[5]:.2f} \nTotal: ${a[6]:.2f}```",
                    color=discord.Color.orange())
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1032078238706577458/1044708521498918942/stripe.png")
                await payment_message.edit(embed=embed)
                await interaction.delete_original_response()
        await db.commit()
        await db.close()

class Link(discord.ui.View):
    def __init__(self, method, id):
        super().__init__()
        id = id
        method = method
        if method == "PayPal":
            url = f'https://www.paypal.com/invoice/s/pay/{id}'
            self.add_item(discord.ui.Button(emoji='<:PayPal:1030697270229880862>', label='Pay', url=url))
        if method == "Stripe":
            url = id
            self.add_item(discord.ui.Button(emoji='<:Stripe:1044708783751970866>', label='Pay', url=url))

class PaySlashCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.bot.add_view(RefreshButton())
    
    @app_commands.command(name="pay", description="Make an invoice!")
    @app_commands.describe(amount="How much would you like to create an invoice for?")
    @app_commands.guilds(discord.Object(id=guild_id))
    async def pay(self, interaction: discord.Interaction, amount: float) -> None:
        if "order" in interaction.channel.name:
            await interaction.response.defer(thinking=True)
            db = await aiosqlite.connect('database.db')
            cursor = await db.execute('SELECT * from commissions WHERE channel_id=?', (interaction.channel.id, ))
            a = await cursor.fetchone()
            fees = amount * fee_amount
            total = amount + fees
            invoice = Invoice({
                "merchant_info": {
                    "business_name": "Cookie Services",
                },
                "items": [
                    {
                        "name": "Commission",
                        "quantity": 1,
                        "unit_price": {
                            "currency": "USD",
                            "value": total
                        }
                    }
                ],
                "note": f"An order processed in the Cookie Services Discord server. ({interaction.channel.id})",
                "payment_term": {
                    "term_type": "NET_45"
                }
            }, api=my_api)

            if invoice.create():
                invoice = Invoice.find(invoice['id'], api=my_api)
                if invoice.send():
                    if a[2] != 'null':
                        if a[3] == 'null':
                            await db.execute('UPDATE commissions SET amount=?', (total, ))
                            embed = discord.Embed(
                                title="Checkout",
                                description=
                                f"```STATUS: UNPAID \nSubtotal: ${amount:.2f} \nFees {fees_percent}: ${fees:.2f} \nTotal: ${total:.2f}```",
                                color=discord.Color.orange())
                            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1032078238706577458/1034883707875639317/1.png")
                            id = invoice.id
                            method = "PayPal"
                            a = await interaction.followup.send(embed=embed, view=Link(method, id))
                            embed = discord.Embed(
                                description=
                                f"Click the button below to check the status of the payment!",
                                color=discord.Color.orange())
                            b = await interaction.channel.send(embed=embed, view=RefreshButton())
                            await db.execute('INSERT INTO invoices VALUES (?,?,?,?,?,?,?);', (method, b.id, a.id, id, amount, fees, total))
                        else:
                            embed = discord.Embed(
                                title="ERROR",
                                description=
                                f"This commission already has an invoice number set!",
                                color=discord.Color.red())
                            await interaction.followup.send(embed=embed)
                    else:
                        embed = discord.Embed(
                            title="ERROR",
                            description=
                            f"This commission does not have a freelancer set!",
                            color=discord.Color.red())
                        await interaction.followup.send(embed=embed)
                else:
                    embed = discord.Embed(
                        title="ERROR",
                        description=
                        f"An error occured. Please contact <@503641822141349888> with steps on how to reproduce it!",
                        color=discord.Color.red())
                    await interaction.followup.send(embed=embed)
                    print(invoice.error)
            else:
                embed = discord.Embed(
                    title="ERROR",
                    description=
                    f"An error occured. Please contact <@503641822141349888> with steps on how to reproduce it!",
                    color=discord.Color.red())
                await interaction.followup.send(embed=embed, ephemeral=True)
                print(invoice.error)
            await db.commit()
            await db.close()
        else:
            embed = discord.Embed(
                title="ERROR",
                description=
                f"This is not a ticket channel!",
                color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="stripe", description="Make a Stripe invoice!")
    @app_commands.describe(email="What is the email of the customer?")
    @app_commands.describe(amount="How much would you like to create an invoice for?")
    @app_commands.guilds(discord.Object(id=guild_id))
    async def stripe(self, interaction: discord.Interaction, email: str, amount: int) -> None:
        if "order" in interaction.channel.name:
            await interaction.response.defer(thinking=True)
            invoice_amount = amount * 100
            fee = fee_amount * 100
            fee = amount * fee
            total_invoice_amount = invoice_amount + fee
            total_invoice_amount = int(total_invoice_amount)
            db = await aiosqlite.connect('database.db')
            cursor = await db.execute('SELECT * from commissions WHERE channel_id=?', (interaction.channel.id, ))
            a = await cursor.fetchone()
            if a[2] != 'null':
                if a[3] == 'null':
                    fees = amount * fee_amount
                    total = amount + fees
                    customer = stripe.Customer.create(
                        description="Invoicing Customer",
                        email=email
                    )

                    invoice = stripe.Invoice.create(
                        customer=customer.id,
                        pending_invoice_items_behavior='exclude',
                        collection_method='send_invoice',
                        days_until_due=1
                    )

                    product = stripe.Product.create(name=f"PrismStudios Commission ({interaction.channel.id})")

                    stripe.InvoiceItem.create(
                        customer=customer.id,
                        invoice=invoice.id,
                        price_data={
                            'currency': 'usd',
                            'unit_amount': total_invoice_amount,
                            'tax_behavior': 'exclusive',
                            'product': product.id
                        }
                    )

                    invoice2 = stripe.Invoice.finalize_invoice(invoice.id)

                    await db.execute('UPDATE commissions SET amount=?', (total, ))

                    embed = discord.Embed(
                        title="Checkout",
                        description=
                        f"```STATUS: UNPAID \nSubtotal: ${amount:.2f} \nFees ({fees_percent}): ${fees:.2f} \nTotal: ${total:.2f}```",
                        color=discord.Color.orange())
                    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1032078238706577458/1044708521498918942/stripe.png")
                    id = invoice2.hosted_invoice_url
                    method = "Stripe"
                    a = await interaction.followup.send(embed=embed, view=Link(method, id))
                    embed = discord.Embed(
                        description=
                        f"Click the button below to check the status of the payment!",
                        color=discord.Color.orange())
                    b = await interaction.channel.send(embed=embed, view=RefreshButton())
                    id = invoice.id
                    await db.execute('INSERT INTO invoices VALUES (?,?,?,?,?,?,?);', (method, b.id, a.id, id, amount, fees, total))
                else:
                    embed = discord.Embed(
                        title="ERROR",
                        description=
                        f"This commission already has an invoice number set!",
                        color=discord.Color.red())
                    await interaction.followup.send(embed=embed)
            else:
                embed = discord.Embed(
                    title="ERROR",
                    description=
                    f"This commission does not have a freelancer set!",
                    color=discord.Color.red())
                await interaction.followup.send(embed=embed)
            await db.commit()
            await db.close()
        else:
            embed = discord.Embed(
                title="ERROR",
                description=
                f"This is not a ticket channel!",
                color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(PaySlashCog(bot), guilds=[discord.Object(id=guild_id)])