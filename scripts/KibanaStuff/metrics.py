#!/usr/bin/env python3

import aggs
import params

# ########################################################################### #
# ############################ Metrics ###################################### #
# ########################################################################### #


class BaseMetric:

    def __init__(self, id):
        self.agg = None
        self.param = None

    def json_agg(self):
        pass

    def json_series_params(self):
        pass

    def dict_agg(self):
        pass

    def dict_series_params(self):
        pass

# ########################################################################### #
# ############################ Area ######################################### #
# ########################################################################### #


class AreaMetric(BaseMetric):

    def __init__(self, id, field, enabled=None, type=None, label=None,
                 valueAxis=None, interpolate=None, mode=None,
                 showCircles=None):
        self.agg = aggs.AverageAgg(id=id, field=field, enabled=enabled)
        self.param = params.AverageParamSeries(
            id=id, enabled=enabled, field=field, type=type, label=label,
            valueAxis=valueAxis, interpolate=interpolate, mode=mode,
            showCircles=showCircles
        )

    def agg(self):
        return self.agg()

    def param(self):
        return self.param()
