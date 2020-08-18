# https://bitbucket.org/bendodds/obs-source-transition/src/master/

import obspython as obs
import re
import datetime

COLOR_FILTER_NAME = "Source Transition Transparency"

FIELDS = []
FIELD_COUNT = 0

class Field(object):
    name = None
    fadeInDelayTime = None
    fadeInTransitionTime = None
    fadeOutDelayTime = None
    fadeOutTransitionTime = None

    inTransition = False
    transitionStartTime = None
    __opacity = None

    def __init__(self, name, fadeInDelayTime, fadeInTransitionTime,
                 fadeOutDelayTime, fadeOutTransitionTime):
        self.name = name
        self.fadeInDelayTime = fadeInDelayTime
        self.fadeInTransitionTime = fadeInTransitionTime
        self.fadeOutDelayTime = fadeOutDelayTime
        self.fadeOutTransitionTime = fadeOutTransitionTime

        CreateCorrectionFilter(self.name)

    def __repr__(self):
        return "<Field name=%r, fadeIn times=%r/%r, fadeOut times=%r/%s, inTransition=%r>" % (
            self.name, self.fadeInDelayTime, self.fadeInTransitionTime,
            self.fadeOutDelayTime, self.fadeOutTransitionTime, self.inTransition)

    @property
    def doFadeOut(self):
        return bool(self.fadeOutDelayTime or self.fadeOutTransitionTime)

    def Activate(self):
        self.inTransition = True
        self.transitionStartTime = datetime.datetime.now()

        self.SetOpacity(0)

    def Deactivate(self):
        # On Deactivate, always reset the opacity to 100 so that it can
        # be seen in the preview.
        self.SetOpacity(100)
        self.inTransition = False

    def SetOpacity(self, opacity):
        opacity = int(opacity)
        if opacity == self.__opacity:
            return

        self.__opacity = opacity

        source = obs.obs_get_source_by_name(self.name)
        if source is None:
            # This shouldn't ever happen actually because the whole
            # event chain is triggered by detecting the activation
            # of a source by name.
            print("Error! Could not find source for %r" % self)
            return

        fieldFilter = obs.obs_source_get_filter_by_name(source,
                                                        COLOR_FILTER_NAME)
        fieldFilterSettings = obs.obs_data_create()

        obs.obs_data_set_int(fieldFilterSettings, "opacity", self.__opacity)
        obs.obs_source_update(fieldFilter, fieldFilterSettings)

        obs.obs_data_release(fieldFilterSettings)
        obs.obs_source_release(fieldFilter)
        obs.obs_source_release(source)

    def StopTransition(self):
        self.inTransition = False

        # If a fade-out is configured, the end state should be
        # totally faded out, otherwise it should end totally
        # faded in.
        if self.doFadeOut:
            self.SetOpacity(0)
        else:
            self.SetOpacity(100)


def Initialize():
    global FIELDS

    for field in FIELDS:
        field.SetOpacity(100)

    obs.timer_add(RunFrame, 25)

    signalHandler = obs.obs_get_signal_handler()
    obs.signal_handler_connect(signalHandler, "source_activate", SourceActivated)
    obs.signal_handler_connect(signalHandler, "source_deactivate", SourceDeactivated)


def RunFrame():
    global FIELDS

    for field in FIELDS:
        if not field.inTransition:
            continue

        currentTime = datetime.datetime.now()
        timeSinceTransitionStart = currentTime - field.transitionStartTime
        msSinceStart = timeSinceTransitionStart.total_seconds() * 1000

        if msSinceStart < field.fadeInDelayTime:
            # The field is within the fade in delay
            field.SetOpacity(0)

        elif msSinceStart < field.fadeInDelayTime + field.fadeInTransitionTime:
            # The field is within the fade in
            msSinceFadeStart = msSinceStart - field.fadeInDelayTime
            field.SetOpacity((100.0 * msSinceFadeStart) / field.fadeInTransitionTime)

        elif field.doFadeOut and msSinceStart < field.fadeInDelayTime \
                + field.fadeInTransitionTime + field.fadeOutDelayTime:
            # The field is within the fade out delay
            field.SetOpacity(100)

        elif field.doFadeOut and msSinceStart < field.fadeInDelayTime \
                + field.fadeInTransitionTime + field.fadeOutDelayTime \
                + field.fadeOutTransitionTime:
            # The field is within the fade out
            msSinceFadeStart = msSinceStart - (field.fadeInDelayTime
                                               + field.fadeInTransitionTime + field.fadeOutDelayTime)
            field.SetOpacity(100 - ((100.0 * msSinceFadeStart) / field.fadeOutTransitionTime))

        else:
            # The fade out is complete
            field.StopTransition()


def script_description():
    return "Fades source in and out when they're activated.\n\n" \
           "You can apply this affect to as many sources as you " \
           "want, simply enter details for one and click the reload " \
           "script button.\n\nIf no fade out is desired, leave the " \
           "fade out delay and transition at 0.\n\nNote: This plugin " \
           "is not compatible with the \"Duplicate Sources\" transition " \
           "feature."


def script_properties():
    """Creates the properties the user may set"""
    global FIELD_COUNT

    properties = obs.obs_properties_create()

    # Get list of possible text fields for selection
    possibleSources = []
    sources = obs.obs_enum_sources()
    if sources is not None:
        for source in sources:
            output_flags = obs.obs_source_get_output_flags(source)
            if output_flags & obs.OBS_SOURCE_VIDEO:
                name = obs.obs_source_get_name(source)
                possibleSources.append(name)

    # Create properties. Add 2, one since we're 1-indexing the list
    # and one to allow another field to be added.
    for index in range(1, FIELD_COUNT + 2):
        sourceProp = obs.obs_properties_add_list(
            properties,
            "source_%s" % index,
            "Source %s" % index,
            obs.OBS_COMBO_TYPE_LIST,
            obs.OBS_COMBO_FORMAT_STRING,
        )

        obs.obs_property_list_add_string(sourceProp, "None", "")
        for sourceName in possibleSources:
            obs.obs_property_list_add_string(sourceProp, sourceName, sourceName)

        obs.obs_properties_add_int(
            properties,
            "fade_in_delay_time_%s" % index,
            "Fade In Delay time %s (ms)" % index,
            0,
            999999999,
            1,
        )
        obs.obs_properties_add_int(
            properties,
            "fade_in_transition_time_%s" % index,
            "Fade In Transition time %s (ms)" % index,
            0,
            999999999,
            1,
        )
        obs.obs_properties_add_int(
            properties,
            "fade_out_delay_time_%s" % index,
            "Fade Out Delay time %s (ms)" % index,
            0,
            999999999,
            1,
        )
        obs.obs_properties_add_int(
            properties,
            "fade_out_transition_time_%s" % index,
            "Fade Out Transition time %s (ms)" % index,
            0,
            999999999,
            1,
        )

    obs.source_list_release(sources)

    return properties


def script_load(settings):
    """called at startup"""
    # Make the text sources show nothing at startup
    Initialize()


def SourceActivated(callData):
    global FIELDS

    source = obs.calldata_source(callData, "source")
    sourceName = obs.obs_source_get_name(source)
    for field in FIELDS:
        if sourceName == field.name:
            field.Activate()


def SourceDeactivated(callData):
    global FIELDS

    source = obs.calldata_source(callData, "source")
    sourceName = obs.obs_source_get_name(source)
    for field in FIELDS:
        if sourceName == field.name:
            field.Deactivate()


def script_unload():
    obs.timer_remove(RunFrame)


def script_update(settings):
    """called when user updates settings"""
    global FIELDS
    global FIELD_COUNT

    FIELDS = []
    for index in range(1, 1000):
        name = obs.obs_data_get_string(settings,
                                       "source_%s" % index)

        if not name:
            continue

        fadeInDelayTime = obs.obs_data_get_int(settings,
                                               "fade_in_delay_time_%s" % index)
        fadeInTransitionTime = obs.obs_data_get_int(settings,
                                                    "fade_in_transition_time_%s" % index)
        fadeOutDelayTime = obs.obs_data_get_int(settings,
                                                "fade_out_delay_time_%s" % index)
        fadeOutTransitionTime = obs.obs_data_get_int(settings,
                                                     "fade_out_transition_time_%s" % index)

        # Keep track of the highest index reached with values.
        FIELD_COUNT = index

        field = Field(name, fadeInDelayTime, fadeInTransitionTime,
                      fadeOutDelayTime, fadeOutTransitionTime)
        FIELDS.append(field)


def CreateCorrectionFilter(source_name):
    global COLOR_FILTER_NAME

    source = obs.obs_get_source_by_name(source_name)
    if source is None:
        return

    filter_ = obs.obs_source_get_filter_by_name(source, COLOR_FILTER_NAME)
    if filter_ is None:
        new_filter = obs.obs_source_create("color_filter",
                                           COLOR_FILTER_NAME, None, None)
        obs.obs_source_filter_add(source, new_filter)
        obs.obs_source_release(new_filter)

    obs.obs_source_release(filter_)
    obs.obs_source_release(source)
