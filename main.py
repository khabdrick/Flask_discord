from flask import Flask, render_template, request, session, redirect, url_for
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
from discord.ext import ipc


app = Flask(__name__)
app.config["SECRET_KEY"] = "test123"

app.config["DISCORD_CLIENT_ID"] = 969522874446671953  # Discord client ID.
app.config[
    "DISCORD_CLIENT_SECRET"
] = "8NLE815vvDovCBvry84PqaBCA3jXqr7S"  # Discord client secret.
app.config[
    "DISCORD_REDIRECT_URI"
] = "http://127.0.0.1:5000/callback"  # URL to your callback endpoint.
app.config["DISCORD_BOT_TOKEN"] = ""  # Required to access BOT resources.

discord = DiscordOAuth2Session(app)

ipc_client = ipc.Client(secret_key="Swas")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login")
def login():
    return discord.create_session()


@app.route("/dashboard")
def dashboard():
    guild_count = ipc_client.request("get_guild_count")
    guild_ids = ipc_client.request("get_guild_ids")

    try:
        user_guilds = discord.fetch_guilds()
    except:
        return redirect(url_for("login"))

    same_guilds = []

    for guild in user_guilds:
        if guild.id in guild_ids:
            same_guilds.append(guild)

    return render_template(
        "dashboard.html", guild_count=guild_count, matching=same_guilds
    )


if __name__ == "__main__":
    app.run(debug=True)
