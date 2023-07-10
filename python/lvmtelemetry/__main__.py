#!/usr/bin/env python
# encoding: utf-8
#
# @Author: José Sánchez-Gallego
# @Date: Dec 1, 2017
# @Filename: cli.py
# @License: BSD 3-Clause
# @Copyright: José Sánchez-Gallego

import os

import click
from click_default_group import DefaultGroup

from clu.tools import cli_coro as cli_coro_lvm
from sdsstools.daemonizer import DaemonGroup

from lvmtelemetry.actor import LVMTelemetryActor


@click.group(cls=DefaultGroup, default="actor")
@click.option(
    "-c",
    "--config",
    "config_file",
    type=str,
    help="Path to the user configuration file.",
)
@click.option(
    "-r",
    "--rmq_url",
    "rmq_url",
    default=None,
    type=str,
    help="rabbitmq url, eg: amqp://guest:guest@localhost:5672/",
)
@click.option(
    "-v",
    "--verbose",
    count=True,
    help="Debug mode. Use additional v for more details.",
)
@click.option(
    "-s",
    "--simulate",
    count=True,
    help="Simulation mode.",
)
@click.pass_context
def lvmtelemetry(ctx, config_file, rmq_url, verbose, simulate):
    """lvm controller"""

    ctx.obj = {
        "verbose": verbose,
        "config_file": config_file,
        "rmq_url": rmq_url,
        "simulate": simulate,
    }


@lvmtelemetry.group(cls=DaemonGroup, prog="lvmtelemetry_actor", workdir=os.getcwd())
@click.pass_context
@cli_coro_lvm
async def actor(ctx):
    """Runs the actor."""

    config_file = ctx.obj["config_file"]
    lvmtelemetry_obj = LVMTelemetryActor.from_config(
        config_file,
        url=ctx.obj["rmq_url"],
        verbose=ctx.obj["verbose"],
        simulate=ctx.obj["simulate"],
    )

    await lvmtelemetry_obj.start()
    await lvmtelemetry_obj.run_forever()


if __name__ == "__main__":
    lvmtelemetry()
