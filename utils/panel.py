from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.style import Style
from rich.panel import Panel as RichPanel
import json

def load_config(file_path="./utils/config.json"):
    with open(file_path, "r") as json_file:
        return json.load(json_file)

def create_table(title, columns, data, on_style, off_style):
    table = Table(title=title, show_header=True, header_style="bold")
    for column in columns:
        table.add_column(
            column["header"], 
            style=column.get("style", "white"),
            no_wrap=column.get("no_wrap", False), 
            width=column.get("width", None), 
            justify=column.get("justify", "left")
        )
    
    for setting, status in data.items():
        table.add_row(setting.capitalize(), Text("ON" if status else "OFF", style=on_style if status else off_style))
    
    return table

def create_footer(guild, user):
    footer = Table(show_header=False, header_style="bold", show_lines=False, width=47)
    footer.add_column(justify="center")
    footer.add_row(f"[bold green]Server Cloned: [green]{guild}")
    footer.add_row(f"[bold green]Logged in as: [green]{user}")
    return footer

def create_credit_footer():
    credit_footer = Table(show_header=False, header_style="bold", show_lines=False, width=47)
    credit_footer.add_column(justify="center")
    credit_footer.add_row("[bold green]Made by Senzo")
    credit_footer.add_row("[bold green]https://discord.gg/servercloner")
    return credit_footer

def display_panel(paragraph, version):
    console = Console()
    console.print(RichPanel(paragraph, style="bold green", width=47))
    console.print(RichPanel(f"Version: {version}", style="bold green", width=47))

def Panel():
    data = load_config()
    on_style = Style(color="green", bold=True)
    off_style = Style(color="green", bold=True)

    columns = [
        {"header": "Setting", "style": "green", "no_wrap": True, "width": 30},
        {"header": "Status", "justify": "center", "width": 10}
    ]
    table = create_table("Discord Server Cloner", columns, data["copy_settings"], on_style, off_style)
    credit_footer = create_credit_footer()

    console = Console()
    console.print(table)
    console.print(credit_footer)

def Panel_Run(guild, user):
    data = load_config()
    on_style = Style(color="green", bold=True)
    off_style = Style(color="green", bold=True)

    columns = [
        {"header": "Cloner is Running...", "style": "green", "no_wrap": True, "width": 30},
        {"header": "Status", "justify": "center", "width": 10}
    ]
    table = create_table("Discord Server Cloner", columns, data["copy_settings"], on_style, off_style)
    footer = create_footer(guild, user)
    credit_footer = create_credit_footer()

    console = Console()
    console.print(table)
    console.print(footer)
    console.print(credit_footer)