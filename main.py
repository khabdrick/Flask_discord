from quart import Quart, render_template, request, session, redirect, url_for
from quart_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
from discord.ext import ipc
import os

os.environ[
    "OAUTHLIB_INSECURE_TRANSPORT"
] = "1"  # this is required because OAuth 2 utilizes https.


app = Quart(__name__)
ipc_client = ipc.Client(
    secret_key="this_is_token"
)  # secret_key must be the same as your IPC server
app.config["SECRET_KEY"] = "test123"

app.config["DISCORD_CLIENT_ID"] = 969522874446671953  # Discord client ID.
app.config[
    "DISCORD_CLIENT_SECRET"
] = "8NLE815vvDovCBvry84PqaBCA3jXqr7S"  # Discord client secret.
app.config[
    "DISCORD_REDIRECT_URI"
] = "http://127.0.0.1:5000/callback"  # URL to your callback endpoint.


discord = DiscordOAuth2Session(app)


@app.route("/")
async def home():
    return await render_template("home.html", authorized=await discord.authorized)


@app.route("/login")
async def login():
    return await discord.create_session()


@app.route("/callback")
async def callback():
    try:
        await discord.callback()
    except Exception:
        pass

    return redirect(url_for("dashboard"))


@app.route("/dashboard")
async def dashboard():
    guild_count = await ipc_client.request("get_guild_count")
    guild_ids = await ipc_client.request("get_guild_ids")
    user = await discord.fetch_user()

    try:
        user_guilds = await discord.fetch_guilds()
    except:
        return redirect(url_for("login"))

    same_guilds = []

    for guild in user_guilds:
        if guild.id in guild_ids:
            same_guilds.append(guild)

    return await render_template(
        "dashboard.html", guild_count=guild_count, matching=same_guilds, user=user
    )


if __name__ == "__main__":
    app.run(debug=True)
