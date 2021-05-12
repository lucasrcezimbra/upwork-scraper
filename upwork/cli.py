import click

from upwork.upwork import Upwork


@click.command()
@click.argument('username')
@click.argument('password')
@click.argument('secret_answer')
def cli(username, password, secret_answer):
    # TODO: adds headless option
    upwork = Upwork(username, password, secret_answer)
    upwork.login()
    upwork.dump_userdata()
    upwork.dump_profile()
