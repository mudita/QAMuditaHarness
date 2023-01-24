# Copyright (c) 2017-2020, Mudita Sp. z.o.o. All rights reserved.
# For licensing, see https://github.com/mudita/MuditaOS/LICENSE.md
import logging

logging.basicConfig(
    format="%(asctime)s %(levelname)-6s %(module)-8s:%(filename)s:%(lineno)s %(message)s",
    level=logging.DEBUG,
    datefmt="%Y/%m/%d %H:%M:%S",
)
log = logging.getLogger(__name__)
