import threading

import obspython as obs
from time import sleep, time

ZOOM_RUN = False
SOURCE_NAME = "cams.zoom"


def zoom_out():
    global ZOOM_RUN
    if ZOOM_RUN: return
    zoom(linspace(110, 100, 400))


def zoom_in():
    global ZOOM_RUN
    if ZOOM_RUN:
        return
    zoom(linspace(100, 110, 400))


def zoom(spaces):
    global ZOOM_RUN
    ZOOM_RUN = True
    source = obs.obs_get_source_by_name("cams.zoom")
    field_filter = obs.obs_source_get_filter_by_name(source, "zoom")
    field_filter_settings = obs.obs_data_create()
    for i in spaces:
        obs.obs_data_set_double(field_filter_settings, "Filter.Transform.Scale.X", i)
        obs.obs_data_set_double(field_filter_settings, "Filter.Transform.Scale.Y", i)
        obs.obs_source_update(field_filter, field_filter_settings)
        sleep(0.03 / 2)
    obs.obs_data_release(field_filter_settings)
    obs.obs_source_release(field_filter)
    obs.obs_source_release(source)
    ZOOM_RUN = False


def blur(spaces):
    source = obs.obs_get_source_by_name("Image")
    field_filter = obs.obs_source_get_filter_by_name(source, "blur")
    for i in spaces:
        field_filter_settings = obs.obs_data_create()
        obs.obs_data_set_int(field_filter_settings, "Filter.Blur.Size", int(i))
        obs.obs_source_update(field_filter, field_filter_settings)
        obs.obs_data_release(field_filter_settings)
        sleep(0.015)
    obs.obs_source_release(field_filter)
    obs.obs_source_release(source)


def fade(spaces):
    cams = obs.obs_get_source_by_name("cams.zoom")
    blur_filter = obs.obs_source_get_filter_by_name(cams, "blur")

    source = obs.obs_get_source_by_name("projector")
    field_filter = obs.obs_source_get_filter_by_name(source, "transparency")
    for i in spaces:
        field_filter_settings = obs.obs_data_create()
        obs.obs_data_set_int(field_filter_settings, "opacity", int(i))
        obs.obs_source_update(field_filter, field_filter_settings)
        obs.obs_data_release(field_filter_settings)

        blur_filter_settings = obs.obs_data_create()
        obs.obs_data_set_int(blur_filter_settings, "Filter.Blur.Size", int(i*0.75))
        obs.obs_source_update(blur_filter, blur_filter_settings)
        obs.obs_data_release(blur_filter_settings)

        sleep(0.015*2)
    obs.obs_source_release(field_filter)
    obs.obs_source_release(source)


def fade_out():
    fade(linspace(100, 0, 50))


def fade_in():
    fade(linspace(0, 100, 50))


def linspace(lower, upper, length):
    return [lower + x * (upper - lower) / (length - 1) for x in range(length)]


def log(txt):
    with open("C:\\Users\\admin\\PycharmProjects\\streaming-scripts\\obs\\log.txt", "a") as f:
        f.write(str(txt) + "\n")


ends = [0, 0, 0, 0, 0, 0]


def wrap(f, idx):
    def a(pressed):
        if not pressed:
            return
        if time() - ends[idx] < 0.01:
            return
        f()
        ends[idx] = time()

    return a


callbacks = [
    ["zoom-in", wrap(zoom_in, 0), None],
    ["zoom-out", wrap(zoom_out, 1), None],
    ["fade-in", wrap(fade_in, 2), None],
    ["fade-out", wrap(fade_out, 3), None]
]


def script_load(settings):
    for i in callbacks:
        hotkey_id = obs.obs_hotkey_register_frontend(i[0], i[0], i[1])
        hotkey_save_array = obs.obs_data_get_array(settings, i[0])
        obs.obs_hotkey_load(hotkey_id, hotkey_save_array)
        obs.obs_data_array_release(hotkey_save_array)
        i[2] = hotkey_id


def script_save(settings):
    for i in callbacks:
        hotkey_save_array = obs.obs_hotkey_save(i[2])
        obs.obs_data_set_array(settings, i[0], hotkey_save_array)
        obs.obs_data_array_release(hotkey_save_array)
