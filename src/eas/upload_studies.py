#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from geojson import Feature, Point, LineString, FeatureCollection
from zepben.eas import Study, EasClient

from utils.style_creator import CircleStyle, LineStyle, InterpolateColor, LinePaint, CirclePaint


def upload_study(config):
    print('Uploading study to EAS Server...')
    eas_client = EasClient(host=config['eas_server']['host'], port=config['eas_server']['port'],
                           client_id=config['auth0']['client_id'],
                           username=config['auth0']['username'],
                           password=config['auth0']['password'])

    feature1 = Feature(id='id1', geometry=Point((144.408936254, -37.6999353628)))
    feature2 = Feature(id='id2', geometry=Point((144.408936254, -37.99353628)))
    feature3 = Feature(id='id3', geometry=LineString([(144.408936254, -37.99353628), (144.408936254, -37.6999353628)]),
                       properties={"number": "100"})
    fc1 = FeatureCollection([feature1, feature2, feature3])
    fc2 = FeatureCollection([feature3])

    styles = [CircleStyle(style_id='circle').style,
              LineStyle(style_id='line').style,
              LineStyle(style_id='line_loading', paint=LinePaint(
                  line_color=InterpolateColor(to_number_name="number", limits=[0, 50, 100]).color()).paint).style,
              CircleStyle(style_id='circle2', paint=CirclePaint(color="red").paint).style]

    result1 = Study.Result(name='2 x Circle &  1 x Line',
                           geo_json_overlay=Study.Result.GeoJsonOverlay(data=fc1, styles=['circle', 'line']))
    result2 = Study.Result(name='1 x Line',
                           geo_json_overlay=Study.Result.GeoJsonOverlay(data=fc2, styles=['line_loading']))

    results = [result1, result2]

    study = Study(
        name='Basic Study',
        description='',
        tags=['basic_study'],
        results=results,
        styles=styles
    )

    eas_client.upload_study(study)

    print(f'https://{config["eas_server"]["host"]}')
