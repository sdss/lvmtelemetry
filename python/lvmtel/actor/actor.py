# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel(briegel@mpia.de)
# @Date: 2022-04-06
# @Filename: actor.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

import asyncio

from clu import AMQPActor

from lvmtel import __version__


class LVMTelemetryActor(AMQPActor):
    """LVM Telemetry actor."""

    def __init__(
        self,
        config,
        *args,
        simulate: bool = False,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self.schema = {
            "type": "object",
            "properties": {
                "temperature": {"type": "number"},
                "dewpoint_enclosure": {"type": "number"},
                "humidity": {"type": "number"},
                "temperature_enclosure": {"type": "number"},
                "humidity_enclosure": {"type": "number"},
            },
            "additionalProperties": False,
        }

        self.sensor = None

    async def start(self):
        """Start actor"""

        await super().start()
        self.load_schema(self.schema, is_file=False)
        self.log.debug("Start done")

    async def stop(self):
        """Stop actor."""

        await super().stop()

    @classmethod
    def from_config(cls, config, *args, **kwargs):
        """Creates an actor from hierachical configuration file(s)."""

        instance = super(LvmtelActor, cls).from_config(
            config, version=__version__, loader=Loader, *args, **kwargs
        )

        if kwargs["verbose"]:
            instance.log.fh.setLevel(DEBUG)
            instance.log.sh.setLevel(DEBUG)

        return instance
